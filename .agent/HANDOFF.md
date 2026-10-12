# Latest session handoff

Session: 2026-10-12/13 — Stage 14 revision 2 completed and reported.

- Ran revision 2 (thinking off, `STUDY_REVISION=2`) for qwen3-8b, llama-3.1-8b, qwen3.5-9b, granite-4.1-8b: 84/84 trials completed; 11 qwen3.5 infrastructure failures retained (10 from a Driver get_text exception bug fixed in `d71c5b2`, 1 connection). LM Studio was force-quit once for memory; the driver resumed from the ledger.
- Added `curation/summarize_prestudy.py`; scorer counts agent-originated events only, which corrected rev-1 qwen2.5 evidenced from 4/21 to 1/21.
- Updated `docs/stage_14_prestudy_report.md` (rev-2 section, limitations, selection under rule, recommendation), plan/README/.agent status.
- Checks run: 5 offline unit tests pass; scorer and summary scripts run. Not run: Flutter analysis.

- Later 2026-10-13: user approved Llama-3.1-8B as formal model, ran revision 3 (16k context, llama + granite, 42/42; ranking unchanged), added Anthropic reference adapter (`STUDY_PROVIDER=anthropic`, revision 4; no API call made).

**Continuation point / user action:** user sets ANTHROPIC_API_KEY and confirms the budget for revision 4; bug-evidence option A/B/C pending. Do not start Stage 15 without `Start Stage 15 according to plan.md`.
