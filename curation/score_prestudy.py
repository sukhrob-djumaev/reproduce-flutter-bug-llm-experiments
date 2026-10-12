"""Curator-side independent scoring of Stage 14 pre-study runs (never given to the agent).

Scores whether the retained tool evidence satisfies each case's recorded predicate. It does not
read the model's self-assessment to decide reproduction. Limit: only evidence the agent's own tool
calls retained can be scored; a bug that fired but was never observed is scored as not evidenced.
"""

import csv
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent


def events(run_id: str) -> list[dict]:
    """Agent-originated tool events only; the harness's own error-window priming call is excluded."""
    path = ROOT / "results" / "runs" / run_id / "tool_events.json"
    loaded = json.loads(path.read_text()) if path.exists() else []
    return [e for e in loaded if not e.get("arguments", {}).get("clearRuntimeErrors")]


def text_of(run_id: str, tool: str | None = None) -> str:
    return "\n".join(e["output"] for e in events(run_id) if tool is None or e["tool_name"] == tool)


def taps(run_id: str) -> list[dict]:
    return [e for e in events(run_id) if e["tool_name"] == "flutter_driver_command" and e["arguments"].get("command") == "tap"]


def counter_sequence(run_id: str) -> list[int]:
    values = []
    for e in events(run_id):
        if e["tool_name"] == "widget_inspector":
            for m in re.finditer(r'"textPreview": "counter: (\d+)"', e["output"]):
                values.append(int(m.group(1)))
    return values


def score(case: str, run_id: str) -> bool:
    errors = text_of(run_id, "get_runtime_errors")
    inspections = text_of(run_id, "widget_inspector")
    if case == "S12-001":
        return "ran out of extent before child could be laid out" in errors
    if case == "S12-003":
        return bool(taps(run_id)) and "sizeAccessAllowed" in errors
    if case == "S12-004":
        return "configuration.isNotEmpty || configuration.isError" in errors
    if case == "S13-002":
        return "Action " in inspections.split("PopupMenuButton")[-1] and any(e["outcome"] == "success" for e in taps(run_id))
    if case == "S13-005":
        return "no longer has a context" in errors or "has been unmounted" in errors
    if case == "S13B-002":
        seq = counter_sequence(run_id)
        return any(a >= 2 and b == 0 for a, b in zip(seq, seq[1:]))
    if case == "S13B-003":
        return "mostRightSpot" in errors or "LateInitializationError" in inspections
    raise ValueError(case)


def main() -> None:
    ledger = []
    for name, revision in (("ledger.jsonl", "1"), ("ledger_r2.jsonl", "2"), ("ledger_r3.jsonl", "3"), ("ledger_r4.jsonl", "4")):
        path = ROOT / "results" / "prestudy" / name
        if path.exists():
            ledger += [{"revision": revision, **json.loads(l)} for l in path.read_text().splitlines() if l.strip()]
    out = ROOT / "results" / "prestudy" / "scores.csv"
    with out.open("w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["revision", "model", "case", "trial", "run_id", "status", "predicate_evidenced"])
        for row in ledger:
            if row["outcome"] != "completed":
                continue
            result = json.loads((ROOT / "results" / "runs" / row["run_id"] / "result.json").read_text())
            writer.writerow([row["revision"], row["model"], row["case"], row["trial"], row["run_id"], result["status"], int(score(row["case"], row["run_id"]))])
    print(out)


if __name__ == "__main__":
    main()
