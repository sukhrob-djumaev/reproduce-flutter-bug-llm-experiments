"""Small local persistence helpers for agent-run evidence."""

import csv
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any, Mapping, Sequence

from formal_contracts import FormalRunMetadata


PROJECT_ROOT = Path(__file__).resolve().parent.parent
RUNS_DIRECTORY = PROJECT_ROOT / "results" / "runs"
SUMMARY_PATH = PROJECT_ROOT / "results" / "summary.csv"
SUMMARY_FIELDS = [
    "case",
    "model",
    "capabilities",
    "status",
    "steps",
    "duration_seconds",
]


def persist_run(
    *,
    case: str,
    model: str,
    capabilities: str,
    status: str,
    evidence: str,
    duration_seconds: float,
    turns: int,
    messages_json: str,
    tool_events: Sequence[Mapping[str, Any]] = (),
    formal_metadata: FormalRunMetadata | None = None,
) -> tuple[str, Path, Path]:
    """Persist pilot evidence plus optional versioned formal-run sidecars."""
    json.loads(messages_json)
    run_id, run_directory = _create_run_directory(case)
    result_path = run_directory / "result.json"
    trace_path = run_directory / "trace.json"
    result_payload = {
        "run_id": run_id,
        "case": case,
        "model": model,
        "capabilities": capabilities,
        "status": status,
        "evidence": evidence,
        "duration_seconds": duration_seconds,
        "turns": turns,
    }
    result_path.write_text(
        json.dumps(result_payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    trace_path.write_text(messages_json + "\n", encoding="utf-8")
    if tool_events:
        (run_directory / "tool_events.json").write_text(
            json.dumps(list(tool_events), ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    if formal_metadata is not None:
        (run_directory / "formal_metadata.json").write_text(
            formal_metadata.model_dump_json(indent=2) + "\n",
            encoding="utf-8",
        )
    _append_summary_row(
        case=case,
        model=model,
        capabilities=capabilities,
        status=status,
        duration_seconds=duration_seconds,
    )
    return run_id, result_path, trace_path


def _create_run_directory(case: str) -> tuple[str, Path]:
    """Create a timestamped run directory without overwriting an existing run."""
    RUNS_DIRECTORY.mkdir(parents=True, exist_ok=True)
    base_run_id = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    suffix = 1
    while True:
        extra = "" if suffix == 1 else f"-{suffix}"
        run_id = f"{base_run_id}-case-{case}{extra}"
        run_directory = RUNS_DIRECTORY / run_id
        try:
            run_directory.mkdir()
        except FileExistsError:
            suffix += 1
        else:
            return run_id, run_directory


def _append_summary_row(
    *,
    case: str,
    model: str,
    capabilities: str,
    status: str,
    duration_seconds: float,
) -> None:
    """Append one matching summary row without inventing a step count."""
    with SUMMARY_PATH.open(newline="", encoding="utf-8") as summary_file:
        header = next(csv.reader(summary_file), [])
    if header != SUMMARY_FIELDS:
        raise RuntimeError(
            f"Unexpected summary.csv header: {header!r}; expected: {SUMMARY_FIELDS!r}"
        )

    with SUMMARY_PATH.open("a", newline="", encoding="utf-8") as summary_file:
        writer = csv.DictWriter(
            summary_file,
            fieldnames=SUMMARY_FIELDS,
            lineterminator="\n",
        )
        writer.writerow(
            {
                "case": case,
                "model": model,
                "capabilities": capabilities,
                "status": status,
                "steps": "",
                "duration_seconds": duration_seconds,
            }
        )
