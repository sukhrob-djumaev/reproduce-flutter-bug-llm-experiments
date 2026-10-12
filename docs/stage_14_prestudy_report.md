# Stage 14 model-selection pre-study report

Two revisions: **revision 1** (default serving, three candidates; sections below) and **revision 2** (thinking disabled, four candidates; final section). Selection under the rule is in the last section.

Executed 2026-10-11/12 under protocol §9 and `docs/stage_14_prestudy_config.md`. Evidence: `results/prestudy/` (`ledger.jsonl`, `ledger_superseded_attempts.jsonl`, `scores.csv`, per-attempt logs; the logs are 6 MB and are kept locally), `results/runs/<run-id>/` (Git-ignored, local), `results/summary.csv`. Independent scoring: `curation/score_prestudy.py`; per-model metrics: `curation/summarize_prestudy.py`; revision-2 ledger `results/prestudy/ledger_r2.jsonl`.

## Design as executed
3 candidates × 7 calibration cases × 3 trials = 63 attempts, all completed (63/63 persisted runs). Fixed prompt, tools, temperature 0.2, 40-request budget, one fresh app launch per trial, Android emulator API 36. Two earlier sanity runs (S12-003, S13B-002) are not study trials.

## Results by candidate

| Metric (21 attempts each) | qwen2.5-7b-instruct | qwen/qwen3.5-9b | qwen3.5-9b-…-reasoning-distilled |
| --- | --- | --- | --- |
| Executable tool calls emitted | 21/21 attempts, 399 calls, 0 output retries | **0/21**, 0 calls | **0/21**, 0 calls |
| Valid structured final result | 14/21 (all 14 schema-valid) | 0/21 | 0/21 |
| Natural termination within budget | 14/21 (67%) | 0/21 (`invalid_output`) | 0/21 (`invalid_output`) |
| Budget exhausted (40 requests) | 7/21 (S12-001 ×3, S13-005 ×3, S13B-002 ×1) | – | – |
| Median messages / duration | 15 / 52 s | 4 / 12 s | 4 / 8 s |
| Provider cost | local, none | local, none | local, none |

**Compatibility limitation (both Qwen3.5 models).** Through LM Studio's OpenAI-compatible endpoint these models wrote their tool calls as text inside the reasoning channel (`<tool_call>…inspect_app…</tool_call>` returned as a `thinking` part), so PydanticAI received no executable tool call and ended each attempt after one output retry. This is a model/serving-template compatibility result under the fixed configuration, not a harness failure (the same harness executed 399 calls for Qwen2.5). I did not change thinking mode, templates, or prompts for these models, because that would be per-model tuning; any such change is a candidate-configuration decision for the user.

## Reproduction outcomes, revision 1 (qwen2.5 only; directional, 21 attempts)
Independent scoring checks whether the retained tool evidence satisfies the curator predicate; it does not use the model's self-assessment.

**Correction (2026-10-13):** the first scoring pass (reported as 4/21 evidenced) also counted the harness's own priming `get_runtime_errors` call. The scorer now counts agent-originated tool events only. Corrected result:

| Self-assessment | predicate evidenced | not evidenced |
| --- | --- | --- |
| REPRODUCED (3) | 1 | 2 |
| NOT_REPRODUCED (11) | 0 | 11 |
| no result / budget exhausted (7) | 0 | 7 |

Evidenced: S13B-003 in 1 of 3 trials; every other case 0/3. Self-assessment agreed with the evidence in 12/14 results (1 REPRODUCED+evidenced, 11 NOT_REPRODUCED+not evidenced) and was wrong in 2 (false REPRODUCED claims).

Limits of scoring: only evidence retained by the agent's own tool calls is scoreable. Raw runtime-error output is truncated at 20,024 characters, and for S12-003 the tap hung the Driver (five-second timeout) so the assertion text was never retained, which means "not evidenced" there is not proof the bug did not fire. Infrastructure success (63/63), independent reproduction (1/21 evidenced) and self-assessment correctness (12/14) are reported separately.

## Infrastructure failures (separate from model outcomes)
Before the final run, 108 attempts were logged as infrastructure failures and retried: emulator storage exhausted by accumulated app installs (fixed by uninstalling after each trial), the LM Studio server stopping mid-study (fixed by health checks), Android package-service crashes, S13-005's curated source being a file subset (built from the SDK `dev/a11y_assessments` after a byte-identity check of `main.dart`), and two model outcomes that were initially mislabeled as infrastructure (request-limit exceeded; invalid structured output; now persisted as model outcomes). Superseded records are in `ledger_superseded_attempts.jsonl`. The first 7 completed trials ran on the earlier harness revision that differed only in this failure handling.

## Revision 2: thinking disabled, four candidates
Same cases, prompt, tools, temperature 0.2, 40-request budget and emulator; the only change is `reasoning_effort: "none"` for every model (applied uniformly, not per model), with the harness fixes below. Candidates: `qwen/qwen3-8b`, `meta-llama-3.1-8b-instruct`, `qwen/qwen3.5-9b`, `granite-4.1-8b` (Unsloth GGUF Q4_K_S; other candidates use LM Studio's default quantizations, so quantization differs by publisher). 4 models × 21 = 84 trials, all completed. Qwen2.5-7B is not re-run: it is the revision-1 baseline and its thinking-off result is identical to its default (it has no thinking mode).

| Metric (21 trials each) | qwen3-8b | llama-3.1-8b | qwen3.5-9b | granite-4.1-8b | (rev 1) qwen2.5-7b |
| --- | --- | --- | --- | --- | --- |
| Trials with executable tool calls | 21/21 | 21/21 | 21/21 | 21/21 | 21/21 |
| Valid structured final result | 16/21 | 21/21 | 6/21 (3 invalid output, 15 no result) | 21/21 | 14/21 |
| Natural termination within budget | 16/21 | 21/21 | 6/21 | 21/21 | 14/21 |
| Budget exhausted | 5 | 0 | 15 | 0 | 7 |
| Median messages / duration | 13 / 25 s | 9 / 14 s | 81 / 310 s | 11 / 21 s | 15 / 52 s |
| Self-reports REPRODUCED / NOT / INCONCLUSIVE | 13 / 3 / 0 | 3 / 16 / 2 | 3 / 0 / 0 | 12 / 4 / 5 | 3 / 11 / 0 |
| Predicate evidenced (independent) | 6/21 | 2/21 | 6/21 | 3/21 | 1/21 |
| Self-report agrees with evidence (REPRODUCED/NOT results) | 9/16 | 15/19 | 3/3 | 7/16 | 12/14 |

Evidenced by case: qwen3-8b S12-001 3/3, S13B-003 3/3; llama S13B-003 2/3; qwen3.5 S13B-002 3/3, S13B-003 3/3; granite S13B-003 3/3. No model evidenced S12-003, S12-004, S13-002 or S13-005 (see scoring limits above; S12-003 and S13-005 may be unobservable through the retained evidence).

Observations (directional, not a powered comparison):
- Disabling thinking resolved the revision-1 incompatibility: Qwen3.5 now emits executable calls. It is however slow (median 310 s) and 15/21 trials exhaust the 40-request budget.
- Qwen3-8B and Qwen3.5 report REPRODUCED often, and several claims are unsupported by retained evidence; Llama and Granite differ in style (Llama mostly NOT_REPRODUCED; Granite mixed with 5 INCONCLUSIVE).
- All models share the same four unscored cases, so the calibration set discriminates operational reliability much more than reproduction ability.

**Infrastructure failures (revision 2, separate from model outcomes):** 11 Qwen3.5 attempts, retained in the ledger as `infrastructure_failure` and retried: 10 from a harness bug (a Driver `get_text` "No element" error raised as an exception; fixed by returning driver errors as ordinary tool results, commit `d71c5b2`) and 1 connection failure. An earlier session loss (LM Studio force-quit for memory) interrupted the run; completed trials were unaffected because the driver is resumable.

**Limitations.** (1) LM Studio's default 4096-token context was left unchanged; long traces may be truncated or degrade, which could contribute to Qwen3.5's budget exhaustion and Qwen3-8B's. Addressed by the revision-3 re-check below for the two leaders only. (2) Granite uses a different quantization/publisher. (3) Launch-time runtime errors can be missed because observation starts after launch, and raw runtime-error output is truncated at 20,024 characters. (4) 3 trials per case; 7 cases; no confidence claims. (5) Calibration cases are excluded from the formal dataset.

## Revision 3: 16k-context re-check (user-approved 2026-10-13)
Revision-2 settings with the LM Studio context window raised from 4096 to 16384 tokens, for the two tied leaders only (42/42 trials completed, no infrastructure failures; `ledger_r3.jsonl`).

| Metric (21 trials) | llama-3.1-8b, 4k | llama-3.1-8b, 16k | granite-4.1-8b, 4k | granite-4.1-8b, 16k |
| --- | --- | --- | --- | --- |
| Executable tool calls / natural termination / valid output | 21/21 each | 21/21 each | 21/21 each | 21/21 each |
| Median messages / duration | 9 / 14 s | 11 / 9 s | 11 / 21 s | 11 / 20 s |
| Self-reports REPRODUCED / NOT / INCONCLUSIVE | 3 / 16 / 2 | 0 / 20 / 1 | 12 / 4 / 5 | 11 / 3 / 7 |
| Predicate evidenced | 2/21 | 3/21 | 3/21 | 3/21 |
| Self-report agrees with evidence | 15/19 | 18/20 | 7/16 | 6/14 |

The larger context did not change operational reliability or the ranking; differences in reproduction counts are within noise. Llama's agreement with evidence is higher and its latency lower at 16k, Granite's self-reports remain mostly unsupported claims. Llama still tends to report NOT_REPRODUCED (20/21 at 16k), so its low false-positive rate comes with low sensitivity; with 3/21 evidenced, no model-quality claim is made.

## Selection under the predeclared rule
Rule (§9): first tool-call and structured-output reliability, then natural termination, then directional reproduction, cost and latency; materially tied candidates → lower cost/latency.
- Tool-call reliability: all five candidates are eligible under their final configuration (Qwen3.5 only with thinking off; revision-1 Qwen3.5 and the distilled variant remain ineligible as configured and were not re-run with thinking off).
- Structured-output and natural termination: `meta-llama-3.1-8b-instruct` and `granite-4.1-8b` are both 21/21; `qwen3-8b` 16/21, `qwen2.5-7b-instruct` 14/21, `qwen3.5-9b` 6/21.
- Between the two leaders, directional reproduction is mixed: Granite evidenced 3/21 vs Llama 2/21, but Llama's self-reports agree with evidence more often (15/19 vs 7/16), and all differences are within noise. I treat them as materially tied; the tie-break is lower latency (Llama median 14 s vs 21 s; both local, no cost).

**Recommendation:** `meta-llama-3.1-8b-instruct` (user approved this as the formal model on 2026-10-13; frozen only at Stage 15) with a 16384-token context, by the predeclared rule and tie-break, confirmed by the revision-3 re-check, with `granite-4.1-8b` as the close alternative. `qwen/qwen3-8b` has the highest directional reproduction but fails the natural-termination criterion in 5 of 21 trials. The formal model needs the user's approval; larger context, other candidates or paid models are separate decisions.

## Other findings for Stage 15 (not acted on)
- The generic `text:`/`type:` target contract and Driver-timeout handling are pre-study contracts, not frozen.
- Runtime-error observation can miss assertion text after a hung tap, and raw output truncation limits scoring; both bear on the Stage 15 runtime-error contract.
- No calibration case is used in the formal dataset unless the protocol is amended before any main-study run.
