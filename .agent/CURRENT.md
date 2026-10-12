# Current operational state

Updated: 2026-10-13. Operational state only; the formal protocol and `plan.md` govern.

- **Current research stage:** Stage 14 — Model-Selection Pre-Study.
- **Stage status:** EXECUTED (revision 1 and approved revision 2); awaiting user review and formal-model approval. Approved 2026-10-11 (entry checkpoint `fd4a921ead41ff8f6dbb7fcf19faab794a83131f`); revision 2 (thinking off, added qwen3-8b, llama-3.1-8b, granite-4.1-8b) approved 2026-10-12. Stage 15 NOT started.
- **Branch:** `main`; read live HEAD/status on resume.
- **Evidence:** `docs/stage_14_prestudy_config.md`, `docs/stage_14_prestudy_report.md`, `docs/stage_14_candidate_rationale.md`, `results/prestudy/{ledger.jsonl,ledger_r2.jsonl,ledger_superseded_attempts.jsonl,scores.csv}`, local runs `results/runs/` (Git-ignored), scorers `curation/score_prestudy.py` and `curation/summarize_prestudy.py`.
- **Result summary:** all candidates emit executable calls under thinking-off. Natural termination: llama-3.1-8b 21/21, granite-4.1-8b 21/21, qwen3-8b 16/21, qwen2.5-7b 14/21, qwen3.5-9b 6/21. Independent evidence of reproduction is low everywhere (1-6 of 21; four cases never evidenced). Rule recommendation (not an approval): meta-llama-3.1-8b-instruct by latency tie-break over granite-4.1-8b. Rev-1 qwen2.5 evidenced count corrected from 4/21 to 1/21.
- **Approved scope now:** none beyond reviewing/answering about Stage 14. No Stage 15, new curation, further trials, or formal runs without explicit user approval.

## Docs-only research
`docs/bug_evidence_review.md` (user-approved 2026-10-12). Options A/B/C in that file await the user's choice.

## Pending user decisions
1. Approve the formal model (recommendation above) or change candidates; whether to rerun with a larger LM Studio context (4096 default is a recorded limitation); paid/cloud models need explicit approval and an adapter.
2. Bug-evidence option A/B/C.
3. Then `Start Stage 15 according to plan.md`.

## Local environment notes
LM Studio server started via `lms` (models unloaded); emulator `emulator-5556` may still be running; a user-owned iOS simulator/fvm process also runs. Credentials: none used.
