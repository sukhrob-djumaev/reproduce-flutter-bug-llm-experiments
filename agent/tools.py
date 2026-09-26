"""The single local tool used to prove Agents SDK execution."""

from dataclasses import dataclass

from agents import function_tool


@dataclass(frozen=True)
class AddNumbersCall:
    """A recorded invocation of the deterministic Phase 3 tool."""

    a: int
    b: int
    result: int


_tool_calls: list[AddNumbersCall] = []


def reset_tool_call_log() -> None:
    """Clear local verification state before an agent run."""
    _tool_calls.clear()


def get_tool_call_log() -> tuple[AddNumbersCall, ...]:
    """Return the calls the SDK made to the local test tool."""
    return tuple(_tool_calls)


@function_tool
def add_numbers(a: int, b: int) -> int:
    """Add two integers and return their sum."""
    result = a + b
    _tool_calls.append(AddNumbersCall(a=a, b=b, result=result))
    return result
