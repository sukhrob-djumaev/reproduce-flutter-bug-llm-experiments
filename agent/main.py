"""Run the Phase 3 local LM Studio Agents SDK tool-call proof."""

import asyncio

from agents import Agent, ModelSettings, Runner

from capabilities import CapabilityMode
from models import (
    create_local_client,
    create_local_model,
    get_local_model_config,
    verify_configured_model,
)
from tools import add_numbers, get_tool_call_log, reset_tool_call_log

EXPECTED_A = 17
EXPECTED_B = 25
EXPECTED_RESULT = 42

INSTRUCTIONS = """You are validating a local tool integration.
You must call add_numbers exactly once with a=17 and b=25.
Do not calculate the answer yourself. After receiving the tool result, reply with
the result and state that it came from add_numbers.
"""

PROMPT = "Use the available tool to calculate 17 + 25 and return the result."


async def run_proof() -> str:
    """Run and verify the full model -> tool -> model loop once."""
    config = get_local_model_config()
    client = create_local_client(config)
    await verify_configured_model(config, client)

    reset_tool_call_log()
    agent = Agent(
        name="LM Studio tool-call proof",
        instructions=INSTRUCTIONS,
        model=create_local_model(config, client),
        model_settings=ModelSettings(
            temperature=0.0,
            tool_choice="required",
            parallel_tool_calls=False,
        ),
        tools=[add_numbers],
    )
    result = await Runner.run(agent, PROMPT, max_turns=3)
    final_output = str(result.final_output).strip()
    tool_calls = get_tool_call_log()

    expected_call = (EXPECTED_A, EXPECTED_B, EXPECTED_RESULT)
    actual_calls = tuple((call.a, call.b, call.result) for call in tool_calls)
    if actual_calls != (expected_call,):
        raise RuntimeError(
            "Expected exactly one add_numbers(17, 25) call returning 42; "
            f"received {actual_calls!r}."
        )
    if str(EXPECTED_RESULT) not in final_output:
        raise RuntimeError(
            "The agent completed the tool call but its final output did not contain 42: "
            f"{final_output!r}"
        )

    print(f"Capability mode: {CapabilityMode.FULL}")
    print(f"LM Studio endpoint: {config.base_url}")
    print(f"LM Studio model: {config.model_name}")
    print("Tool call: add_numbers(a=17, b=25) -> 42")
    print(f"Final result: {final_output}")
    print("Verification: PASS")
    return final_output


def main() -> None:
    """Run the proof and make integration failures actionable."""
    try:
        asyncio.run(run_proof())
    except Exception as error:
        print("Phase 3 local agent proof failed.")
        print(f"{type(error).__name__}: {error}")
        raise SystemExit(1) from error


if __name__ == "__main__":
    main()
