# Latest session handoff

Session: 2026-10-11 — Stage 14 approved and opened (setup phase). No trials run, no code changed.

- Cleaned worktree: moved protocol to `docs/` (`bc7a5b0`, `fd4a921`), removed untracked `.docx`. Entry checkpoint `fd4a921ead41ff8f6dbb7fcf19faab794a83131f`. Approval recorded in `81c9044`.
- User approved candidates (3 local LM Studio models on disk) and 7 calibration cases (see CURRENT.md).
- Finding: no agent-visible issue snapshots exist for public cases; upstream titles/bodies leak diagnoses. Fetched read-only copies into scratchpad only (not committed).
- Checks run: git status/diff reads, LM Studio probe (server off), adb shows two devices attached. No tests/models run.

**Continuation point / user action:** decide snapshot policy — recommended: curator-independent, symptom-only issue text per case (title + steps + expected/actual, no root cause, code names, fixes, or comments), written once, hashed, recorded in ground truth, applied identically to all candidates. Then build the public-case workspace runner.
