# Stage 14 model-selection pre-study report

Executed 2026-10-11/12 under protocol §9 and `docs/stage_14_prestudy_config.md`. Evidence: `results/prestudy/` (`ledger.jsonl`, `ledger_superseded_attempts.jsonl`, `scores.csv`, per-attempt logs; the logs are 6 MB and are kept locally), `results/runs/<run-id>/` (Git-ignored, local), `results/summary.csv`. Independent scoring: `curation/score_prestudy.py`.

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

## Reproduction outcomes (qwen2.5 only; directional, 21 attempts)
Independent scoring checks whether the retained tool evidence satisfies the curator predicate; it does not use the model's self-assessment.

| Self-assessment | predicate evidenced | not evidenced |
| --- | --- | --- |
| REPRODUCED (3) | 1 | 2 |
| NOT_REPRODUCED (11) | 2 | 9 |
| no result / budget exhausted (7) | 1 | 6 |

Evidenced by case: S13B-003 3/3, S12-001 1/3, all other cases 0/3. Self-assessment was correct in 10/14 results (REPRODUCED+evidenced 1, NOT_REPRODUCED+not evidenced 9), wrong in 4 (2 false REPRODUCED claims, 2 missed observed failures).

Limits of scoring: only evidence retained by the agent's own tool calls is scoreable. Raw runtime-error output is truncated at 20,024 characters, and for S12-003 the tap hung the Driver (five-second timeout) so the assertion text was never retained, which means "not evidenced" there is not proof the bug did not fire. Infrastructure success (63/63), independent reproduction (4/21 evidenced) and self-assessment correctness (10/14) are reported separately.

## Infrastructure failures (separate from model outcomes)
Before the final run, 108 attempts were logged as infrastructure failures and retried: emulator storage exhausted by accumulated app installs (fixed by uninstalling after each trial), the LM Studio server stopping mid-study (fixed by health checks), Android package-service crashes, S13-005's curated source being a file subset (built from the SDK `dev/a11y_assessments` after a byte-identity check of `main.dart`), and two model outcomes that were initially mislabeled as infrastructure (request-limit exceeded; invalid structured output; now persisted as model outcomes). Superseded records are in `ledger_superseded_attempts.jsonl`. The first 7 completed trials ran on the earlier harness revision that differed only in this failure handling.

## Selection under the predeclared rule
Rule (§9): first tool-call and structured-output reliability, then natural termination, then directional reproduction, cost and latency.
- `qwen2.5-7b-instruct` is the only candidate that meets the tool-call contract. Its weaknesses are 33% budget exhaustion and low evidenced reproduction (4/21), which the rule treats as directional.
- Both Qwen3.5 candidates are ineligible under this configuration (0% executable tool calls). Eligible candidates: 1 of 3, so no tie-break was needed.

**Recommendation (not an approval):** the rule selects `qwen2.5-7b-instruct`, the existing development baseline, by elimination rather than strength. A model-selection result this thin is a reason to consider adding or reconfiguring candidates (for example serving the Qwen3.5 models with thinking disabled, or another tool-calling model) before freezing. Both are candidate-set changes that need the user's decision.

## Other findings for Stage 15 (not acted on)
- The generic `text:`/`type:` target contract and Driver-timeout handling are pre-study contracts, not frozen.
- Runtime-error observation can miss assertion text after a hung tap, and raw output truncation limits scoring; both bear on the Stage 15 runtime-error contract.
- No calibration case is used in the formal dataset unless the protocol is amended before any main-study run.
