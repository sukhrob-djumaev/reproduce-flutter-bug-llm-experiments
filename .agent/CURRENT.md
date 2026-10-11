# Current operational state

Updated: 2026-10-12. Operational state only; the formal protocol and `plan.md` govern.

- **Current research stage:** Stage 14 — Model-Selection Pre-Study.
- **Stage status:** EXECUTED; awaiting user review and formal-model approval. Approved 2026-10-11 (entry checkpoint `fd4a921ead41ff8f6dbb7fcf19faab794a83131f`). Stage 15 NOT started.
- **Branch:** `main`; read live HEAD/status on resume.
- **Evidence:** `docs/stage_14_prestudy_config.md` (fixed config), `docs/stage_14_prestudy_report.md` (results), `results/prestudy/{ledger.jsonl,ledger_superseded_attempts.jsonl,scores.csv}`, local runs `results/runs/` (Git-ignored), scorer `curation/score_prestudy.py`.
- **Result summary:** 63/63 attempts persisted. qwen2.5-7b-instruct: executable tool calls 21/21, natural termination 14/21, predicate evidenced 4/21. Both Qwen3.5 candidates: 0 executable tool calls (tool calls emitted in reasoning channel via LM Studio) -> ineligible as configured. Rule selects qwen2.5-7b-instruct by elimination; this is a recommendation, not an approval.
- **Approved scope now:** none beyond reviewing/answering about Stage 14. No Stage 15, new curation, candidate reconfiguration, extra trials, or formal runs without explicit user approval.

## Pending user decisions
1. Accept `qwen2.5-7b-instruct` as formal model, or change the candidate set (e.g. reserve Qwen3.5 with thinking disabled, add another tool-calling model; downloads/paid APIs need approval) and rerun.
2. Then `Start Stage 15 according to plan.md`.

## Local environment notes
LM Studio server started via `lms`; emulator `emulator-5556` (AVD Medium_Phone_API_36-ext19, headless) may still be running. Credentials: none used. Protocol file now at `docs/stage_10_formal_evaluation_protocol.md`.
