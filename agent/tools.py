"""Generic Flutter runtime adapter backed by the Dart MCP server."""

from dataclasses import dataclass
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import re
from time import monotonic
from typing import Any, Literal

from fastmcp.exceptions import ToolError
from pydantic_ai.mcp import MCPToolset, StdioTransport

from formal_contracts import (
    RuntimeErrorItem,
    RuntimeErrorObservation,
    RuntimeErrorReason,
    RuntimeErrorScope,
)


PROJECT_ROOT = Path(__file__).resolve().parent.parent
FLUTTER_APP_ROOT = PROJECT_ROOT / "flutter_app"


def create_flutter_mcp_toolset(workspace: Path | None = None) -> MCPToolset:
    """Connect PydanticAI's MCP client to the Dart MCP server for the given workspace."""
    return MCPToolset(
        StdioTransport(
            command="dart",
            args=["mcp-server", "--force-roots-fallback"],
            cwd=str(workspace or FLUTTER_APP_ROOT),
        ),
        tool_error_behavior="error",
    )


@dataclass(frozen=True)
class UnderlyingMCPCall:
    """One Dart MCP call made by the generic model-facing adapter."""

    call_id: str
    started_at_utc: str
    tool_name: str
    arguments: dict[str, Any]
    duration_seconds: float
    outcome: str
    output_characters: int
    output: str
    output_sha256: str

    def audit_record(self) -> dict[str, Any]:
        """Return the private, persisted form of this raw Dart MCP event."""
        return {
            "event_id": self.call_id,
            "tool_name": self.tool_name,
            "started_at_utc": self.started_at_utc,
            "duration_seconds": self.duration_seconds,
            "outcome": self.outcome,
            "arguments": self.arguments,
            "output": self.output,
            "output_sha256": self.output_sha256,
        }


class FlutterRuntimeAdapter:
    """Expose compact inspection and value-key Driver actions over Dart MCP."""

    _APP_URI_PATTERN = re.compile(r"ws://[^\s\"']+/ws")
    _DTD_URI_PATTERN = re.compile(r"ws://[^\s\"']+")
    _RUNTIME_ERROR_COUNT_PATTERN = re.compile(r"Found (\d+) error")
    _RUNTIME_ERROR_SUMMARY_PATTERN = re.compile(
        r"renderedErrorText: .*?The following (?P<type>.+?) was thrown.*?\n"
        r"(?P<summary>.+?)(?:\n|$)",
        re.DOTALL,
    )
    _INTERACTIVE_WIDGET_PATTERN = re.compile(
        r"Button|Menu|^Tab$|TextField|ListTile|InkWell|GestureDetector|Checkbox|Switch|Radio|Chip|Slider"
    )
    _STRING_VALUE_KEY_PATTERN = re.compile(r"-\[<'([^']+)'\>")

    def __init__(self, mcp_toolset: MCPToolset, dtd_uri: str | None = None) -> None:
        self._mcp_toolset = mcp_toolset
        self._dtd_uri = dtd_uri
        self._app_uri: str | None = None
        self._calls: list[UnderlyingMCPCall] = []
        self._actionable_targets: set[str] = set()
        self._has_current_inspection = False
        self._runtime_error_window_started_at: str | None = None
        self._runtime_session_id: str | None = None
        self._runtime_observation_count = 0
        self.raw_inspection: str | None = None
        self.normalized_inspection: str | None = None

    @property
    def calls(self) -> tuple[UnderlyingMCPCall, ...]:
        """Return the private Dart MCP trace for the current run."""
        return tuple(self._calls)

    async def inspect_app(self) -> str:
        """Return actionable targets plus passive visible text observations."""
        app_uri = await self._get_app_uri()
        self.raw_inspection = await self._call_text(
            "widget_inspector",
            {"command": "get_widget_tree", "summaryOnly": True, "appUri": app_uri},
        )
        self.normalized_inspection = self._normalize_inspection(self.raw_inspection)
        return self.normalized_inspection

    async def get_text(self, target: str) -> str:
        """Read text from a target previously exposed by ``inspect_app``."""
        try:
            return await self._driver_command("get_text", target)
        except ToolError as error:
            if not self._is_unsupported_text_read(error):
                raise
            return json.dumps(
                {
                    "ok": False,
                    "target": target,
                    "reason": "text retrieval is not supported for this widget",
                },
                separators=(",", ":"),
            )

    async def tap(self, target: str) -> str:
        """Tap a target previously exposed by ``inspect_app``."""
        return await self._driver_command("tap", target)

    async def get_runtime_errors(self) -> str:
        """Return typed runtime-error evidence without exposing raw MCP output."""
        if self._runtime_error_window_started_at is None:
            try:
                await self.begin_runtime_error_window()
            except Exception:
                return self._failure_runtime_observation(
                    status="unavailable",
                    code="runtime_session_unavailable",
                    message="The active Flutter runtime session is unavailable.",
                ).model_dump_json()

        try:
            raw_errors = await self._call_text(
                "get_runtime_errors",
                {"appUri": await self._get_app_uri()},
            )
        except ToolError:
            return self._failure_runtime_observation(
                status="tool_error",
                code="dart_mcp_tool_error",
                message="The Dart MCP runtime-error tool returned an error.",
            ).model_dump_json()
        except Exception:
            return self._failure_runtime_observation(
                status="tool_error",
                code="dart_mcp_transport_error",
                message="The Dart MCP runtime-error transport failed.",
            ).model_dump_json()

        return self._runtime_observation_from_raw(raw_errors).model_dump_json()

    async def begin_runtime_error_window(self) -> None:
        """Clear inherited errors before a run so later evidence has a known window."""
        app_uri = await self._get_app_uri()
        await self._call_text(
            "get_runtime_errors",
            {"appUri": app_uri, "clearRuntimeErrors": True},
        )
        self._runtime_session_id = sha256(app_uri.encode("utf-8")).hexdigest()[:16]
        self._runtime_error_window_started_at = self._utc_now()

    async def _get_app_uri(self) -> str:
        if self._app_uri is not None:
            return self._app_uri
        if self._dtd_uri is not None:
            dtd_uri = self._dtd_uri
        else:
            dtd_uris = await self._call_text("dtd", {"command": "listDtdUris"})
            dtd_uri = self._first_uri(dtd_uris, self._DTD_URI_PATTERN, "DTD URI")
        await self._call_text("dtd", {"command": "connect", "uri": dtd_uri})
        apps = await self._call_text("dtd", {"command": "listConnectedApps"})
        self._app_uri = self._first_uri(apps, self._APP_URI_PATTERN, "app URI")
        return self._app_uri

    async def _driver_command(self, command: str, target: str) -> str:
        if not self._has_current_inspection:
            return json.dumps(
                {
                    "ok": False,
                    "reason": "app state may have changed; call inspect_app() before using target-based tools",
                },
                separators=(",", ":"),
            )
        if target not in self._actionable_targets:
            return json.dumps(
                {
                    "ok": False,
                    "target": target,
                    "reason": "target is not available in the current inspected state",
                },
                separators=(",", ":"),
            )
        try:
            result = await self._call_text(
                "flutter_driver_command",
                {
                    "command": command,
                    **self._finder_arguments(target),
                    "appUri": await self._get_app_uri(),
                    "timeout": "5000",
                },
            )
        except ToolError as error:
            # A driver action that fails or never settles is an observable app outcome, not a
            # harness crash; report it to the model as an ordinary tool result.
            self._actionable_targets.clear()
            self._has_current_inspection = False
            reason = (
                "the action did not complete within 5 seconds; the app may be unresponsive or in an error state"
                if "Timed out waiting for Flutter Driver" in str(error)
                else "the target could not be found or used; call inspect_app() again"
            )
            return json.dumps(
                {"ok": False, "target": target, "reason": reason},
                separators=(",", ":"),
            )
        if command == "tap":
            self._actionable_targets.clear()
            self._has_current_inspection = False
        return result

    @staticmethod
    def _finder_arguments(target: str) -> dict[str, str]:
        """Map a model-facing target to a Flutter Driver finder (generic, case-independent)."""
        # Driver actions fail on ambiguous finders, so text/type targets resolve to the
        # first match (document order) via an Ancestor finder that matches the root.
        if target.startswith("text:"):
            finder: dict[str, str] = {"finderType": "ByText", "text": target[len("text:") :]}
        elif target.startswith("type:"):
            finder = {"finderType": "ByType", "type": target[len("type:") :]}
        else:
            finder = {}
        if finder:
            return {
                "finderType": "Ancestor",
                "of": finder,
                "matching": finder,
                "matchRoot": "true",
                "firstMatchOnly": "true",
            }
        return {
            "finderType": "ByValueKey",
            "keyValueString": target,
            "keyValueType": "String",
        }

    async def _call_text(self, tool_name: str, arguments: dict[str, Any]) -> str:
        started_at = monotonic()
        started_at_utc = self._utc_now()
        try:
            result = await self._mcp_toolset.direct_call_tool(tool_name, arguments)
        except ToolError as error:
            self._record_call(
                tool_name,
                arguments,
                started_at,
                started_at_utc,
                "tool_error",
                str(error),
            )
            raise
        except Exception as error:
            self._record_call(
                tool_name,
                arguments,
                started_at,
                started_at_utc,
                "transport_error",
                str(error),
            )
            raise
        text = result if isinstance(result, str) else json.dumps(result, ensure_ascii=False)
        self._record_call(tool_name, arguments, started_at, started_at_utc, "success", text)

        return text

    def _record_call(
        self,
        tool_name: str,
        arguments: dict[str, Any],
        started_at: float,
        started_at_utc: str,
        outcome: str,
        output: str,
    ) -> None:
        self._calls.append(
            UnderlyingMCPCall(
                call_id=f"mcp-{len(self._calls) + 1:04d}",
                started_at_utc=started_at_utc,
                tool_name=tool_name,
                arguments=arguments,
                duration_seconds=monotonic() - started_at,
                outcome=outcome,
                output_characters=len(output),
                output=output,
                output_sha256=sha256(output.encode("utf-8")).hexdigest(),
            )
        )

    @staticmethod
    def _is_unsupported_text_read(error: ToolError) -> bool:
        error_text = str(error)
        return "Unsupported operation:" in error_text and "getText" in error_text

    def _runtime_observation_from_raw(self, raw_errors: str) -> RuntimeErrorObservation:
        """Normalize structured MCP content while retaining raw evidence privately."""
        self._runtime_observation_count += 1
        fragments = self._runtime_text_fragments(raw_errors)
        non_error_markers = [
            fragment
            for fragment in fragments
            if fragment.strip() != "No runtime errors found."
            and self._RUNTIME_ERROR_COUNT_PATTERN.search(fragment) is None
        ]
        errors = [
            self._runtime_error_item(fragment, index)
            for index, fragment in enumerate(non_error_markers, start=1)
            if fragment.strip()
        ]
        return RuntimeErrorObservation(
            observation_id=self._runtime_observation_id(),
            scope=self._runtime_scope(),
            status="observed",
            error_count=len(errors),
            errors=errors,
        )

    @staticmethod
    def _runtime_text_fragments(raw_errors: str) -> list[str]:
        """Extract text content from supported Dart MCP response envelopes."""
        try:
            payload = json.loads(raw_errors)
        except json.JSONDecodeError:
            return [raw_errors]

        def text_items(value: object) -> list[str]:
            if isinstance(value, str):
                return [value]
            if isinstance(value, list):
                return [text for item in value for text in text_items(item)]
            if isinstance(value, dict):
                text = value.get("text")
                if isinstance(text, str):
                    return [text]
                content = value.get("content")
                if content is not None:
                    return text_items(content)
            return []

        fragments = text_items(payload)
        return fragments or [raw_errors]

    def _runtime_error_item(self, fragment: str, index: int) -> RuntimeErrorItem:
        summary_match = self._RUNTIME_ERROR_SUMMARY_PATTERN.search(fragment)
        if summary_match:
            category = summary_match.group("type").strip()
            message = summary_match.group("summary").strip()
        else:
            category = "runtime_error"
            message = " ".join(fragment.split())[:300]
        raw_hash = self._calls[-1].output_sha256 if self._calls else sha256(
            fragment.encode("utf-8")
        ).hexdigest()
        return RuntimeErrorItem(
            category=category,
            message=message,
            raw_evidence_ref=(
                f"tool_events.json#sha256:{raw_hash}:fragment:{index}"
            ),
        )

    def _failure_runtime_observation(
        self,
        *,
        status: Literal["unavailable", "tool_error"],
        code: str,
        message: str,
    ) -> RuntimeErrorObservation:
        self._runtime_observation_count += 1
        return RuntimeErrorObservation(
            observation_id=self._runtime_observation_id(),
            scope=self._runtime_scope(),
            status=status,
            reason=RuntimeErrorReason(code=code, message=message),
        )

    def _runtime_scope(self) -> RuntimeErrorScope:
        now = self._utc_now()
        return RuntimeErrorScope(
            app_session_id=self._runtime_session_id or "unavailable",
            since=self._runtime_error_window_started_at or now,
            until=now,
            clear_before_observation=self._runtime_error_window_started_at is not None,
        )

    def _runtime_observation_id(self) -> str:
        session_id = self._runtime_session_id or "unavailable"
        return f"runtime-errors-{session_id}-{self._runtime_observation_count:04d}"

    @staticmethod
    def _utc_now() -> str:
        return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    @staticmethod
    def _first_uri(text: str, pattern: re.Pattern[str], label: str) -> str:
        match = pattern.search(text)
        if match is None:
            raise RuntimeError(f"Dart MCP did not return a {label}: {text!r}")
        return match.group(0)

    def _normalize_inspection(self, raw_tree: str) -> str:
        """Turn compact Inspector JSON into targets and passive text observations."""
        try:
            tree = json.loads(raw_tree)
        except json.JSONDecodeError as error:
            raise RuntimeError("Dart MCP compact widget tree was not valid JSON") from error
        elements: list[dict[str, str]] = []
        observations: list[dict[str, str]] = []
        self._actionable_targets.clear()
        self._has_current_inspection = True
        for node in self._walk_tree(tree):
            target = self._value_key_for(node)
            widget_type = str(node.get("widgetRuntimeType", "Widget"))
            visible_text = self._visible_text(node)
            if target is None and self._INTERACTIVE_WIDGET_PATTERN.search(widget_type):
                target = f"text:{visible_text}" if visible_text else f"type:{widget_type}"
                if target in self._actionable_targets:
                    continue
            if target is not None:
                element: dict[str, str] = {
                    "type": self._element_type(widget_type),
                    "widget_type": widget_type,
                    "target": target,
                }
                if visible_text:
                    element["text" if element["type"] == "text" else "label"] = visible_text
                elements.append(element)
                self._actionable_targets.add(target)
            elif widget_type == "Text" and visible_text:
                observations.append(
                    {
                        "type": "text",
                        "widget_type": widget_type,
                        "text": visible_text,
                    }
                )
        return json.dumps(
            {"elements": elements, "observations": observations},
            ensure_ascii=False,
            separators=(",", ":"),
        )

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
