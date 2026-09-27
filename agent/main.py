"""Run one Stage 5 PydanticAI Flutter-interaction attempt."""

import asyncio
from dataclasses import dataclass

from pydantic import BaseModel
from pydantic_ai import Agent
from pydantic_ai.messages import ModelMessagesTypeAdapter

from capabilities import CapabilityMode
from models import (
    create_local_client,
    create_local_model,
    get_local_model_config,
    verify_configured_model,
)
from tools import FlutterRuntimeAdapter, create_flutter_mcp_toolset


RUNTIME_INSTRUCTIONS = """Use only the provided runtime tools to complete the task.
Never guess targets: use only targets returned by inspect_app(). Return the values
you observed in the required structured result."""

RUNTIME_PROMPT = """Inspect the running application. Read the current counter value.
Press the + button once. Read the counter value again. Return the observed before and
after values."""


class CounterResult(BaseModel):
    """Typed observation returned by the infrastructure-validation run."""

    before_value: str
    after_value: str


@dataclass(frozen=True)
class RuntimeAttempt:
    """Typed result, complete PydanticAI history, and private runtime evidence."""

    result: CounterResult
    messages_json: str
    calls: tuple[object, ...]
    normalized_inspection: str | None


async def run_flutter_runtime_attempt() -> RuntimeAttempt:
    """Run PydanticAI normally; it owns the tool loop and natural termination."""
    config = get_local_model_config()
    client = create_local_client(config)
    await verify_configured_model(config, client)

    mcp_toolset = create_flutter_mcp_toolset()
    async with mcp_toolset:
        discovered_tool_names = {tool.name for tool in await mcp_toolset.list_tools()}
        required_tools = {"dtd", "widget_inspector", "flutter_driver_command"}
        missing_tools = required_tools - discovered_tool_names
        if missing_tools:
            raise RuntimeError(
                "Dart MCP did not expose the required runtime tools: "
                f"{sorted(missing_tools)}; available: {sorted(discovered_tool_names)}"
            )

        adapter = FlutterRuntimeAdapter(mcp_toolset)
        agent = Agent(
            create_local_model(config, client),
            output_type=CounterResult,
            instructions=RUNTIME_INSTRUCTIONS,
            model_settings={"temperature": 0.0},
            end_strategy="graceful",
        )

        @agent.tool_plain
        async def inspect_app() -> str:
            """Inspect the app and return its compact catalog of actionable targets."""
            return await adapter.inspect_app()

        @agent.tool_plain
        async def get_text(target: str) -> str:
            """Read the text associated with a target returned by inspect_app."""
            return await adapter.get_text(target)

        @agent.tool_plain
        async def tap(target: str) -> str:
            """Tap a target returned by inspect_app."""
            return await adapter.tap(target)

        run = await agent.run(RUNTIME_PROMPT)
        messages = run.all_messages()
        return RuntimeAttempt(
            result=run.output,
            messages_json=ModelMessagesTypeAdapter.dump_json(messages, indent=2).decode(),
            calls=adapter.calls,
            normalized_inspection=adapter.normalized_inspection,
        )


def _print_attempt(attempt: RuntimeAttempt) -> None:
    """Print evidence without evaluating or correcting the model's conclusion."""
    print(f"Capability mode: {CapabilityMode.FULL}")
    print(f"Typed result: {attempt.result.model_dump_json()}")
    print("Underlying Dart MCP trace:")
    for call in attempt.calls:
        print(f"- {call.tool_name}: {call.arguments}; {call.duration_seconds:.2f}s")
    print(f"Normalized inspection: {attempt.normalized_inspection}")
    print("Complete PydanticAI message history:")
    print(attempt.messages_json)


def main() -> None:
    """Run the single Stage 5 interaction attempt."""
    try:
        _print_attempt(asyncio.run(run_flutter_runtime_attempt()))
    except Exception as error:
        print("Stage 5 PydanticAI runtime interaction failed.")
        print(f"{type(error).__name__}: {error}")
        raise SystemExit(1) from error


if __name__ == "__main__":
    main()
