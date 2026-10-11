# Latest session handoff

Session: 2026-10-11/12 — Stage 14 opened and executed.

- Moved the protocol into `docs/` and removed the stray `.docx` (`bc7a5b0`, `fd4a921`). Approved Stage 14 start, candidates (3 local models) and 7 calibration cases.
- Wrote and user-approved symptom-only issue snapshots `issues/case_<id>.md`; hashes recorded in the ground-truth records.
- Added public-case execution support: `agent/public_cases.py`, generic `text:`/`type:` targets and Driver-timeout handling in `agent/tools.py`, public-case/budget/outcome handling in `agent/main.py`, `agent/prestudy.py`; fixed config in `docs/stage_14_prestudy_config.md`.
- Ran 63 trials; fixed harness issues (emulator storage, LM Studio stopping, S13-005 source subset, mislabeled model outcomes). 108 infrastructure-failure attempts are retained in `results/prestudy/ledger_superseded_attempts.jsonl`.
- Results and limits: `docs/stage_14_prestudy_report.md`.

Checks run: 5 offline unit tests (before the study); two sanity runs; full 63-attempt study; independent scoring script run. Offline unit tests re-run after the final edits: 5 passed. Not run: Flutter analysis.

**Continuation point / user action:** review the report and decide the formal model / candidate changes (see CURRENT.md). Do not start Stage 15 without `Start Stage 15 according to plan.md`.
