"""Run one issue-driven Flutter bug-reproduction attempt."""

import asyncio
import argparse
import os
from dataclasses import dataclass
from pathlib import Path
from time import monotonic
from typing import Literal

from pydantic import BaseModel
from pydantic_ai import Agent, capture_run_messages
from pydantic_ai.exceptions import UnexpectedModelBehavior, UsageLimitExceeded
from pydantic_ai.usage import UsageLimits
from pydantic_ai.messages import ModelMessagesTypeAdapter

from capabilities import CapabilityMode
from models import (
    create_local_client,
    create_local_model,
    get_local_model_config,
    verify_configured_model,
)
from public_cases import CALIBRATION_CASES, is_public_case, issue_path as public_issue_path, running_case
from results import persist_run
from tools import FlutterRuntimeAdapter, create_flutter_mcp_toolset


# Stage 14 pre-study configuration: identical for every candidate model and public case.
STUDY_TEMPERATURE = 0.2
STUDY_REQUEST_LIMIT = 40
STUDY_DEVICE = "emulator-5556"
# Revision 2 (2026-10-12): thinking disabled uniformly for every candidate.
STUDY_EXTRA_BODY = {"reasoning_effort": "none"}

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ISSUES_DIRECTORY = PROJECT_ROOT / "issues"

REPRODUCTION_INSTRUCTIONS = """You are given a reported Flutter bug.

Use the available runtime tools to inspect and operate the running application. Try to
reproduce the reported behavior. When you have enough evidence, return a structured
self-assessment. Do not invent evidence. Use runtime observations as the basis for
your conclusion. Never guess targets: use only targets returned by inspect_app()."""


class ReproductionResult(BaseModel):
    """Typed self-assessment from the issue-driven reproduction attempt."""

    status: Literal["REPRODUCED", "NOT_REPRODUCED", "INCONCLUSIVE"]
    evidence: str


@dataclass(frozen=True)
class RuntimeAttempt:
    """Typed result, complete PydanticAI history, and private runtime evidence."""

    case: str
    issue_path: Path
    issue_text: str
    instructions: str
    model_name: str
    result: ReproductionResult | None
    termination: str
    failure: str | None
    messages_json: str
    calls: tuple[object, ...]
    normalized_inspection: str | None
    duration_seconds: float
    turns: int


def load_issue(case: str) -> tuple[Path, str]:
    """Load the natural-language issue report supplied to the model."""
    issue_path = public_issue_path(case) if is_public_case(case) else ISSUES_DIRECTORY / f"case_{case}.md"
    return issue_path, issue_path.read_text(encoding="utf-8")


async def run_flutter_runtime_attempt(case: str, workspace: Path | None = None, dtd_uri: str | None = None) -> RuntimeAttempt:
    """Run PydanticAI normally; it owns the tool loop and natural termination."""
    issue_path, issue_text = load_issue(case)
    config = get_local_model_config()
    client = create_local_client(config)
    await verify_configured_model(config, client)

    mcp_toolset = create_flutter_mcp_toolset(workspace)
    async with mcp_toolset:
        discovered_tool_names = {tool.name for tool in await mcp_toolset.list_tools()}
        required_tools = {
            "dtd",
            "get_runtime_errors",
            "widget_inspector",
            "flutter_driver_command",
        }
        missing_tools = required_tools - discovered_tool_names
        if missing_tools:
            raise RuntimeError(
                "Dart MCP did not expose the required runtime tools: "
                f"{sorted(missing_tools)}; available: {sorted(discovered_tool_names)}"
            )

        adapter = FlutterRuntimeAdapter(mcp_toolset, dtd_uri)
        await adapter.begin_runtime_error_window()
        agent = Agent(
            create_local_model(config, client),
            output_type=ReproductionResult,
            instructions=REPRODUCTION_INSTRUCTIONS,
            model_settings=(
                {"temperature": STUDY_TEMPERATURE, "extra_body": STUDY_EXTRA_BODY}
                if (workspace and os.environ.get("STUDY_REVISION") == "2")
                else {"temperature": STUDY_TEMPERATURE if workspace else 0.0}
            ),
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

        @agent.tool_plain
        async def get_runtime_errors() -> str:
            """Read recent runtime errors from the active Flutter application."""
            return await adapter.get_runtime_errors()

        started_at = monotonic()
        result: ReproductionResult | None = None
        termination = "natural"
        failure: str | None = None
        with capture_run_messages() as captured_messages:
            try:
                run = await agent.run(
                    f"Reported issue:\n\n{issue_text}",
                    usage_limits=UsageLimits(request_limit=STUDY_REQUEST_LIMIT) if workspace else None,
                )
                result = run.output
            except UsageLimitExceeded as error:
                termination, failure = "budget_exhausted", str(error)
            except UnexpectedModelBehavior as error:
                termination, failure = "invalid_output", str(error)
        duration_seconds = monotonic() - started_at
        messages = run.all_messages() if result is not None else list(captured_messages)
        return RuntimeAttempt(
            case=case,
            issue_path=issue_path,
            issue_text=issue_text,
            instructions=REPRODUCTION_INSTRUCTIONS,
            model_name=config.model_name,
            result=result,
            termination=termination,
            failure=failure,
            messages_json=ModelMessagesTypeAdapter.dump_json(messages, indent=2).decode(),
            calls=adapter.calls,
            normalized_inspection=adapter.normalized_inspection,
            duration_seconds=duration_seconds,
            turns=len(messages),
        )


def _print_attempt(
    attempt: RuntimeAttempt,
    run_id: str,
    result_path: Path,
    trace_path: Path,
) -> None:
    """Print evidence without evaluating or correcting the model's conclusion."""
    print(f"Capability mode: {CapabilityMode.FULL}")
    print(f"Run ID: {run_id}")
    print(f"Result path: {result_path}")
    print(f"Trace path: {trace_path}")
    print(f"Issue path: {attempt.issue_path}")
    print("Exact issue text supplied to the model:")
    print(attempt.issue_text)
    print("Agent instruction:")
    print(attempt.instructions)
    print(f"Typed result: {attempt.result.model_dump_json() if attempt.result else None}")
    print(f"Termination: {attempt.termination}" + (f" ({attempt.failure})" if attempt.failure else ""))
    print(f"Duration seconds: {attempt.duration_seconds:.2f}")
    print(f"Turns: {attempt.turns}")
    print("Underlying Dart MCP trace:")
    for call in attempt.calls:
        print(
            f"- {call.tool_name}: {call.arguments}; {call.duration_seconds:.2f}s; "
            f"output: {call.output}"
        )
    print(f"Normalized inspection: {attempt.normalized_inspection}")
    print("Complete PydanticAI message history:")
    print(attempt.messages_json)


def _parse_arguments() -> argparse.Namespace:
    """Accept one existing issue case without selecting a model or capability variant."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", required=True, choices=["001", "002", "003", "004", "005", *CALIBRATION_CASES])
    return parser.parse_args()


async def _run_case(case: str) -> RuntimeAttempt:
    """Synthetic cases use the already-running pilot app; public cases get a fresh launch."""
    if not is_public_case(case):
        return await run_flutter_runtime_attempt(case)
    async with running_case(case, STUDY_DEVICE) as (workspace, dtd_uri):
        return await run_flutter_runtime_attempt(case, workspace, dtd_uri)


def main() -> None:
    """Run and persist one issue-driven reproduction attempt."""
    arguments = _parse_arguments()
    try:
        attempt = asyncio.run(_run_case(arguments.case))
        run_id, result_path, trace_path = persist_run(
            case=attempt.case,
            model=attempt.model_name,
            capabilities=str(CapabilityMode.FULL),
            status=attempt.result.status if attempt.result else f"NO_RESULT_{attempt.termination.upper()}",
            evidence=attempt.result.evidence if attempt.result else (attempt.failure or ""),
            duration_seconds=attempt.duration_seconds,
            turns=attempt.turns,
            messages_json=attempt.messages_json,
            tool_events=[call.audit_record() for call in attempt.calls],
        )
        _print_attempt(attempt, run_id, result_path, trace_path)
    except Exception as error:
        print("Stage 7 issue-driven reproduction and persistence failed.")
        print(f"{type(error).__name__}: {error}")
        raise SystemExit(1) from error


if __name__ == "__main__":
    main()
