# Latest session handoff

Session: 2026-10-11 — repository-native development workflow (documentation only), complete.

## Changes and findings

- Added `AGENTS.md`, the small `CLAUDE.md` import, and `.agent/CURRENT.md` / this packet. Updated README/plan status and continuation guidance without changing the protocol, research implementation, cases, or result conventions.
- Inspected README, the full plan/protocol, curation documentation and ledgers, `agent/`, `tests/`, local result inventory, branch/status, and recent history. No prior repository AGENTS/CLAUDE/state files or Stage 14 implementation/report were found.
- Research HEAD on entry was `a58cf58d84ca49d2a4286c3301599bd67c2ad99e` on `main`; the tree was clean. README/plan status lagged the committed Stage 12/13/13B batches. Stage 14 has not started; a clean baseline alone does not authorize it.
- Curation ledger: 21 attempted, 13 accepted, 7 rejected, 1 deferred; 13 case directories and 13 corresponding ground-truth records. The pool is not a frozen dataset, and suitability is not a calibration split.
- Historical discrepancy: Stage 12's original written cap was 2 accepted / 5 attempted, while the committed ledgers record 4 / 9. The tracked plan contains no corresponding scope amendment. Original criteria and actual records are preserved; this session does not infer prior approval or retroactively change methodology.
- Existing persistence retains actual model results and raw message traces. The tracked summary has six synthetic pilot rows; local run contents are ignored and may be absent on another clone. No model-selection or formal outcome was established.

## Checks actually run

- `.venv/bin/python -m unittest discover -s tests -v`: all 5 existing offline contract tests passed (no model, MCP server, or Flutter app invocation).
- Read-only CSV/artifact inventory matched the curation totals above; `results/summary.csv` contains synthetic cases only. No study trial was run.
- Native entrypoint documentation checked; local versions: Claude Code 2.1.296, Codex CLI 0.149.1. The Claude import keeps one shared contract even when direct AGENTS loading is unavailable/configured differently.
- Relative Markdown links and the native `@AGENTS.md` import validated; the shared contract fits Codex's default discovery limit. `git diff --check` passed. Diff/scope review found only the six intended Markdown files changed; protocol, implementation, curated material, and tracked results are unchanged.
- A focused read-only reviewer, given repository files without prior chat, identified the same research boundary. Its approval/preflight ordering finding was corrected: inspect the clean entry baseline before writing state. No subagent work remains outstanding.

| Workflow scenario | Walkthrough outcome |
| --- | --- |
| A: fresh `continue` | Reconcile files/Git, identify Stage 14 as next, stop for missing start approval. |
| B: unrelated dirty work at a clean gate | Stop read-only before state edits or execution; report exact paths. |
| C: curation | Keep curator and development context outside evaluation inputs/results/tools. |
| D: model selection | Fix cases/prompt/tools/settings/budget across candidates; no tailored repairs. |
| E: stage completion | Verify and commit permitted work, then stop before the next stage. |
| F: external blocker | Request the exact model/API/device/manual action without proceeding through it. |

These are document walkthroughs, including independent review, not executed fresh Claude Code/Codex CLI sessions or technical access-control tests. No runtime/model-selection/formal trial was used to validate the workflow.

## Git commits

- Prior research checkpoint: `a58cf58d84ca49d2a4286c3301599bd67c2ad99e` — `stage 13b: improve curated case diversity`.
- Workflow commit: the commit containing this packet; obtain its exact hash/message with `git log -1 --format='%H %s' -- .agent/HANDOFF.md`. Verify live `git status --short` at resume; this packet cannot embed its own commit hash.

## Unresolved issues / exact continuation point

Workflow checks are complete. Research remains at the completed Stage 13B / not-started Stage 14 boundary. No candidate set, approved calibration split, public-case runner, pre-study report, formal model, or formal freeze exists in repository evidence. The historical Stage 12 scope discrepancy remains documented; it does not authorize new work.

After this workflow is committed, `continue` should reconcile live Git and request only explicit Stage 14 start approval if it is still absent. Once the user says `Start Stage 14 according to plan.md`, check the entry baseline read-only first; after the clean gate passes, record approval/checkpoint, update plan/README status, and continue within that stage. Do not ask for old chat transcripts or begin later capabilities/formal trials.

**User action required:** approve Stage 14 when ready. No external model/API/device action was requested or performed in this session.
