"""Generic Flutter runtime adapter backed by the Dart MCP server."""

from dataclasses import dataclass
import json
from pathlib import Path
import re
from time import monotonic
from typing import Any

from pydantic_ai.mcp import MCPToolset, StdioTransport


PROJECT_ROOT = Path(__file__).resolve().parent.parent
FLUTTER_APP_ROOT = PROJECT_ROOT / "flutter_app"


def create_flutter_mcp_toolset() -> MCPToolset:
    """Connect PydanticAI's MCP client to the existing Dart MCP server."""
    return MCPToolset(
        StdioTransport(
            command="dart",
            args=["mcp-server", "--force-roots-fallback"],
            cwd=str(FLUTTER_APP_ROOT),
        ),
        tool_error_behavior="error",
    )


@dataclass(frozen=True)
class UnderlyingMCPCall:
    """One Dart MCP call made by the generic model-facing adapter."""

    tool_name: str
    arguments: dict[str, Any]
    duration_seconds: float
    output_characters: int
    output: str


class FlutterRuntimeAdapter:
    """Expose compact inspection and value-key Driver actions over Dart MCP."""

    _APP_URI_PATTERN = re.compile(r"ws://[^\s\"']+/ws")
    _DTD_URI_PATTERN = re.compile(r"ws://[^\s\"']+")
    _STRING_VALUE_KEY_PATTERN = re.compile(r"-\[<'([^']+)'\>")

    def __init__(self, mcp_toolset: MCPToolset) -> None:
        self._mcp_toolset = mcp_toolset
        self._app_uri: str | None = None
        self._calls: list[UnderlyingMCPCall] = []
        self._actionable_targets: set[str] = set()
        self.raw_inspection: str | None = None
        self.normalized_inspection: str | None = None

    @property
    def calls(self) -> tuple[UnderlyingMCPCall, ...]:
        """Return the private Dart MCP trace for the current run."""
        return tuple(self._calls)

    async def inspect_app(self) -> str:
        """Return a compact, normalized catalog of actionable app targets."""
        app_uri = await self._get_app_uri()
        self.raw_inspection = await self._call_text(
            "widget_inspector",
            {"command": "get_widget_tree", "summaryOnly": True, "appUri": app_uri},
        )
        self.normalized_inspection = self._normalize_inspection(self.raw_inspection)
        return self.normalized_inspection

    async def get_text(self, target: str) -> str:
        """Read text from a target previously exposed by ``inspect_app``."""
        return await self._driver_command("get_text", target)

    async def tap(self, target: str) -> str:
        """Tap a target previously exposed by ``inspect_app``."""
        return await self._driver_command("tap", target)

    async def _get_app_uri(self) -> str:
        if self._app_uri is not None:
            return self._app_uri
        dtd_uris = await self._call_text("dtd", {"command": "listDtdUris"})
        dtd_uri = self._first_uri(dtd_uris, self._DTD_URI_PATTERN, "DTD URI")
        await self._call_text("dtd", {"command": "connect", "uri": dtd_uri})
        apps = await self._call_text("dtd", {"command": "listConnectedApps"})
        self._app_uri = self._first_uri(apps, self._APP_URI_PATTERN, "app URI")
        return self._app_uri

    async def _driver_command(self, command: str, target: str) -> str:
        if target not in self._actionable_targets:
            raise ValueError("target must exactly match a target returned by inspect_app")
        return await self._call_text(
            "flutter_driver_command",
            {
                "command": command,
                "finderType": "ByValueKey",
                "keyValueString": target,
                "keyValueType": "String",
                "appUri": await self._get_app_uri(),
                "timeout": "5000",
            },
        )

    async def _call_text(self, tool_name: str, arguments: dict[str, Any]) -> str:
        started_at = monotonic()
        result = await self._mcp_toolset.direct_call_tool(tool_name, arguments)
        text = result if isinstance(result, str) else json.dumps(result, ensure_ascii=False)
        self._calls.append(
            UnderlyingMCPCall(
                tool_name=tool_name,
                arguments=arguments,
                duration_seconds=monotonic() - started_at,
                output_characters=len(text),
                output=text,
            )
        )
        return text

    @staticmethod
    def _first_uri(text: str, pattern: re.Pattern[str], label: str) -> str:
        match = pattern.search(text)
        if match is None:
            raise RuntimeError(f"Dart MCP did not return a {label}: {text!r}")
        return match.group(0)

    def _normalize_inspection(self, raw_tree: str) -> str:
        """Turn compact Inspector JSON into model-facing ValueKey targets."""
        try:
            tree = json.loads(raw_tree)
        except json.JSONDecodeError as error:
            raise RuntimeError("Dart MCP compact widget tree was not valid JSON") from error
        elements: list[dict[str, str]] = []
        self._actionable_targets.clear()
        for node in self._walk_tree(tree):
            target = self._value_key_for(node)
            if target is None:
                continue
            widget_type = str(node.get("widgetRuntimeType", "Widget"))
            element: dict[str, str] = {
                "type": self._element_type(widget_type),
                "widget_type": widget_type,
                "target": target,
            }
            visible_text = self._visible_text(node)
            if visible_text:
                element["text" if element["type"] == "text" else "label"] = visible_text
            elements.append(element)
            self._actionable_targets.add(target)
        return json.dumps({"elements": elements}, ensure_ascii=False, separators=(",", ":"))

    @staticmethod
    def _walk_tree(node: object):
        if not isinstance(node, dict):
            return
        yield node
        for child in node.get("children", []):
            yield from FlutterRuntimeAdapter._walk_tree(child)

    def _value_key_for(self, node: dict[str, Any]) -> str | None:
        match = self._STRING_VALUE_KEY_PATTERN.search(str(node.get("description", "")))
        return match.group(1) if match else None

    @staticmethod
    def _element_type(widget_type: str) -> str:
        if widget_type == "Text":
            return "text"
        if "Button" in widget_type:
            return "button"
        return "widget"

    def _visible_text(self, node: dict[str, Any]) -> str | None:
        preview = node.get("textPreview")
        if isinstance(preview, str) and preview:
            return preview
        for child in node.get("children", []):
            if isinstance(child, dict):
                child_text = self._visible_text(child)
                if child_text:
                    return child_text
        return None
