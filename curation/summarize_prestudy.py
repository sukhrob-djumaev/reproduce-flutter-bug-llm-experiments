"""Per-model Stage 14 pre-study metrics from scores.csv and retained run evidence (curator-side)."""

import csv
import json
from collections import defaultdict
from pathlib import Path
from statistics import median

ROOT = Path(__file__).resolve().parent.parent
RUNS = ROOT / "results" / "runs"


def main() -> None:
    groups = defaultdict(list)
    with (ROOT / "results" / "prestudy" / "scores.csv").open() as handle:
        for row in csv.DictReader(handle):
            groups[(row["revision"], row["model"])].append(row)
    print("rev model n | exec_calls_trials | natural_term | valid_output | med_turns | med_sec | REPRO NOT INCON NORES | evidenced | self-report agrees")
    for (revision, model), rows in sorted(groups.items()):
        executable = natural = valid = evidenced = agree = 0
        turns, secs, statuses = [], [], defaultdict(int)
        for row in rows:
            result = json.loads((RUNS / row["run_id"] / "result.json").read_text())
            trace = json.loads((RUNS / row["run_id"] / "trace.json").read_text())
            # Executable = the model's own tool call was run and returned; harness setup calls are not in the trace.
            executable += any(part.get("part_kind") == "tool-return" for message in trace for part in message["parts"])
            status = result["status"]
            statuses[status] += 1
            natural += not status.startswith("NO_RESULT_BUDGET")
            valid += not status.startswith("NO_RESULT_INVALID")
            turns.append(result.get("turns") or 0)
            secs.append(result.get("duration_seconds") or 0)
            hit = int(row["predicate_evidenced"])
            evidenced += hit
            agree += (status == "REPRODUCED") == bool(hit) if status in ("REPRODUCED", "NOT_REPRODUCED") else 0
        n = len(rows)
        print(f"{revision} {model} {n} | {executable}/{n} | {natural}/{n} | {valid}/{n} | {median(turns)} | {median(secs):.0f} | "
              f"{statuses['REPRODUCED']} {statuses['NOT_REPRODUCED']} {statuses['INCONCLUSIVE']} {sum(v for k, v in statuses.items() if k.startswith('NO_RESULT'))} | {evidenced}/{n} | {agree}/{statuses['REPRODUCED'] + statuses['NOT_REPRODUCED']}")


if __name__ == "__main__":
    main()
