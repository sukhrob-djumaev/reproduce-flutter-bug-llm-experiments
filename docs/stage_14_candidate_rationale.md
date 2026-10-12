# Stage 14 candidate-set rationale (revision 2)

Recorded 2026-10-12 after the first pre-study run (`docs/stage_14_prestudy_report.md`). The user approved the four-model shortlist and the two downloads on 2026-10-12. Evidence quality is limited: the sources below are third-party, mix BFCL versions, and no single study compares these exact models, so they justify the shortlist; the pre-study itself (protocol §9) is the primary evidence for selection.

## Constraints
- 16 GB Apple M1 Pro; the emulator runs alongside the model, so roughly ≤ 9B parameters at Q4. This excludes 14B+ models and gpt-oss-20b.
- Must emit executable tool calls and structured output through LM Studio's OpenAI-compatible endpoint (LM Studio 0.4.12).
- Local only, no credentials, no per-request cost.

## Shortlist
| Candidate | Reason | Source |
| --- | --- | --- |
| `qwen2.5-7b-instruct` (Q4_K_M) | Existing development baseline; only candidate to pass the tool-call contract in run 1. | Pre-study report |
| `qwen/qwen3-8b` (lmstudio-community GGUF, 5.03 GB) | Qwen3 family repeatedly named as the strongest small open tool-calling models. | [d-central](https://d-central.tech/local-llm-agent-capability/), [jacar.es](https://jacar.es/?p=4566), [KDnuggets](https://www.kdnuggets.com/5-small-language-models-for-agentic-tool-calling) |
| `Meta-Llama-3.1-8B-Instruct` (lmstudio-community Q4_K_M, 4.92 GB) | Different family and tool-call format, so the result is not Qwen-specific; Meta reports best-in-class 8B tool-use scores (self-reported, Llama 3). | [Llama 3 paper](https://arxiv.org/pdf/2407.21783) |
| `qwen/qwen3.5-9b` (lmstudio-community GGUF) | Highest third-party BFCL-v4 figure among sub-10B models (0.661); failed in run 1 because tool calls were emitted inside the reasoning channel, so it is rerun under the uniform thinking setting below. | [d-central](https://d-central.tech/local-llm-agent-capability/); LM Studio parsing fix in 0.4.7 [changelog](https://lmstudio.ai/changelog/lmstudio-v0.4.7) did not resolve run 1 on 0.4.12 |

Reserve (not run unless a shortlisted model cannot load): Granite 4.1 8B ([Labellerr](https://labellerr.com/blog/best-small-language-models-under-10b-parameters/)).

## Excluded
- `qwen3.5-9b-claude-4.6-opus-reasoning-distilled`: no independent tool-calling evidence; run 1 result (0/21 executable calls) stays on record.
- gpt-oss-20b and xLAM-2: about 56% and 53% malformed tool-call/schema errors in an MCP-based benchmark ([MCP-GRANITE](https://arxiv.org/pdf/2609.24161)); gpt-oss-20b also exceeds the memory budget.
- Models under about 4B: reliability drops sharply ([d-central](https://d-central.tech/local-llm-agent-capability/)).

## Run plan
Fixed configuration unchanged (`docs/stage_14_prestudy_config.md`). Qwen2.5-7B run-1 trials are kept. New runs: qwen3-8b, llama-3.1-8b, and qwen3.5-9b (rerun), 7 cases × 3 trials each. Run 1's Qwen3.5 results are kept as a separate finding. Any thinking-mode setting must be applied identically to every candidate that has one, and recorded before the runs.
