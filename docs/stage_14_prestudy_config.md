# Stage 14 pre-study configuration (recorded before the study trials)

Recorded 2026-10-11, under protocol §9 and plan Stage 14. Identical for every candidate, case and trial.

- **Candidates (3, local LM Studio, no downloads):** `qwen2.5-7b-instruct` (Q4_K_M GGUF); `qwen/qwen3.5-9b` (lmstudio-community GGUF); `qwen3.5-9b-claude-4.6-opus-reasoning-distilled` (Jackrong GGUF). LM Studio server `http://127.0.0.1:1234/v1`, default load settings.
- **Calibration cases (7):** S12-001, S12-003, S12-004, S13-002, S13-005, S13B-002, S13B-003. Agent sees only `issues/case_<id>.md` (hashes in the ground-truth records). Calibration cases are excluded from the formal dataset unless the protocol is amended before any main-study run.
- **Trials:** 3 per model per case (63 attempts), one fresh app launch each (reset = new `flutter run`), sequential.
- **Prompt:** `REPRODUCTION_INSTRUCTIONS` in `agent/main.py`, unchanged from the pilot.
- **Tools:** `inspect_app`, `get_text`, `tap`, `get_runtime_errors`. Pre-study contract only (not a Stage 15 freeze): targets without a string `ValueKey` are exposed as `text:<visible text>` or `type:<WidgetType>` and resolved by Flutter Driver to the first match. Driver timeouts are returned to the model as ordinary tool results.
- **Sampling/budget:** temperature 0.2 (non-zero so repeated trials are independent), 40 model requests maximum, no per-attempt seed.
- **Environment:** Flutter 3.47.1 / Dart 3.13.1, Android emulator API 36 AVD `Medium_Phone_API_36-ext19` (headless, port 5556), debug builds. Case sources are byte-identical copies of `curation/accepted/**/source`, plus an Android scaffold, a `flutter_driver` dependency, and a wrapper entrypoint (`lib/main_driver.dart`).
- **Infrastructure failures:** attempts that never produce a persisted run (launch/install failure, timeout) are logged in `results/prestudy/ledger.jsonl`, retried once, and reported separately from model outcomes.
- **Selection rule:** protocol §9 as written (tool-call and structured-output reliability, then natural termination; then directional reproduction, cost, latency; lower cost/latency breaks ties). Reproduction is scored independently against the curator predicate after the trials, never by the model's self-assessment.

## Revision 2 (2026-10-12, approved by the user)
Candidate set revised per `docs/stage_14_candidate_rationale.md`. Everything above is unchanged except: (a) thinking/reasoning is disabled for every candidate through the request field `reasoning_effort: "none"` (accepted by all candidates in a compatibility check; a no-op for models without a thinking mode), and (b) the revision-2 candidates are `qwen/qwen3-8b`, `meta-llama-3.1-8b-instruct`, and `qwen/qwen3.5-9b`. Revision-1 results (thinking default) remain on record in `ledger.jsonl`; revision 2 is logged in `ledger_r2.jsonl`. The `qwen2.5-7b-instruct` revision-1 trials are kept and not rerun, because the reasoning switch does not apply to it.

Revision 2 addendum (2026-10-12): `granite-4.1-8b` added as a fifth candidate by user request; same fixed configuration. Paid/cloud models are not part of this run.

## Revision 3 (context-length re-check; user-approved 2026-10-13)
Identical to revision 2 except the LM Studio context window is 16384 tokens (`lms load --context-length 16384`) instead of the 4096 default. Candidates: `meta-llama-3.1-8b-instruct` and `granite-4.1-8b` (the two operationally tied leaders), 21 trials each, logged in `ledger_r3.jsonl`. Purpose: check whether the 4096 default confounded the revision-2 result before the formal model is frozen. Not a new candidate-set change.

## Revision 4 (paid reference run; user-approved 2026-10-13; awaiting API key and cost confirmation)
A labelled reference condition, outside the primary outcome and the §9 selection: one Anthropic model (`claude-haiku-5-5`) through PydanticAI's Anthropic provider, same prompt, tools, temperature 0.2, 40-request budget, cases and emulator, 21 trials, logged in `ledger_r4.jsonl`. Enabled by `STUDY_PROVIDER=anthropic`; the key is read only from `ANTHROPIC_API_KEY` in the environment. It does not change the formal model or the protocol. Cost is estimated and confirmed with the user before any call is made.
