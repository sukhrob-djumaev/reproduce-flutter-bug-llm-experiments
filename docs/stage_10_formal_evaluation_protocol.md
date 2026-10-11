# Stage 10 — Formal Evaluation Protocol and Public-Case Curation Specification

## Status and scope

This document specifies the formal-study design that follows the completed five-case engineering pilot (`7fa9e22`). It does not make the pilot the formal dataset and it does not change the current agent, Flutter cases, prompts, PydanticAI integration, tools, or result persistence.

The pilot established that the end-to-end path can run and persist results. It did not establish a research-ready benchmark: its cases are synthetic and simple, all recorded outcomes are positive, it has no controlled repeated trials or capability ablation, and it lacks independently stored predicates and complete reproducibility metadata. Formal evaluation begins only after the items in the freeze policy have been implemented and frozen.

The study addresses:

- **RQ1:** Can an LLM agent reproduce Flutter defects from natural-language issue reports and correctly judge whether reproduction succeeded?
- **RQ2:** Which runtime capabilities materially contribute to reproduction performance?

The research system remains a bug-reproduction agent. Root-cause diagnosis, patch generation, regression-status evaluation, multi-agent coordination, and automatic case import are outside this protocol.

## 1. Formal experiment overview

One trial gives a selected agent one public issue report and access to a pinned, running Flutter case under one capability condition. The agent may inspect and interact with the application using only that condition's tool contract. It returns one self-assessment. The evaluation runner stores the unmodified trace and evidence. Separately, a ground-truth record defines the observable predicate that determines whether the reported defect was reproduced.

The agent must not receive the ground-truth record, predicate implementation details, curator notes, expected observations, source locations, or post-run score. It receives only the issue wording, the frozen generic instruction, and the tools exposed by the assigned condition.

The primary formal study uses one selected main model. A small model-selection pre-study chooses that model before the main evaluation. Any later model comparison is a secondary robustness study, not an implicit second independent variable in the primary RQ2 experiment.

### Experimental variables

| Role | Variable | Formal treatment |
| --- | --- | --- |
| Independent | Capability condition | `FULL` and one capability-family ablation at a time, as defined in Section 3. |
| Secondary independent variable, only if separately approved | Model | Held constant in the primary study; varied only in a documented robustness study. |
| Dependent | Reproduction success | Whether the independently defined predicate was satisfied in a trial. |
| Dependent | Self-assessment correctness | Agreement between the agent's declared status and independently scored trial outcome. |
| Dependent | Efficiency | Wall-clock duration and recorded agent turns. Per-tool timing is retained for diagnosis and secondary analysis. |
| Controlled | Prompt, framework, sampling, budget, environment, tool contract, case revision, issue wording | Frozen for all primary-study trials except the intentionally varied capability condition. |

No token-based, subjective-quality, or composite score is a primary metric. Token use may be retained only if the provider exposes it reliably and comparably.

## 2. RQ1 protocol

### Unit of evaluation

A trial is one independent launch/reset of one pinned case revision, with one issue snapshot, one selected model configuration, one frozen prompt, one frozen capability condition, and one agent invocation. A trial must not reuse application state, conversation history, or an earlier trial's observations.

The planned primary design runs **five independent trials per case per capability condition**. Five is sufficient to expose obvious stochastic instability while keeping the first approximately 25-case study practical. A trial that cannot begin because the pinned app or environment is unavailable is recorded as an infrastructure exclusion with its cause; it is never silently rerun or replaced. A trial that begins and then encounters a normal tool/runtime failure remains an evaluated trial with its observed result.

### Independent reproduction outcome

For every evaluable case, curators define a binary, observable predicate before agent runs. Examples include a specified uncaught exception, a visible state value after a fixed action sequence, a widget-tree property, or a recorded silent failure signal. The scorer evaluates the run's retained evidence against that predicate without using the agent's final claim.

- **Reproduction success:** the predicate is satisfied during the trial, with the required observable evidence present and attributable to the pinned case.
- **Reproduction failure:** the case ran sufficiently to evaluate the predicate, but the predicate was not satisfied.
- **Trial not scoreable:** a documented external problem prevents evaluation of the predicate, such as a failed build, unavailable required service despite the case having passed curation, or corrupt evidence. It is excluded from the primary denominator and reported separately; it is not converted into success or failure.

The predicate is about reproducing the reported behavior, not about whether the agent used an elegant sequence, inferred a cause, or found a source line.

### Agent self-assessment outcome

The frozen output schema shall retain three statuses: `REPRODUCED`, `NOT_REPRODUCED`, and `INCONCLUSIVE`.

For a scoreable binary predicate:

| Ground-truth trial outcome | Agent status | Classification |
| --- | --- | --- |
| success | `REPRODUCED` | correct self-assessment |
| failure | `NOT_REPRODUCED` | correct self-assessment |
| failure | `REPRODUCED` | false positive |
| success | `NOT_REPRODUCED` | false negative |
| success or failure | `INCONCLUSIVE` | abstention; reported separately and counted as non-agreement in the overall self-assessment-correctness rate |

`INCONCLUSIVE` is appropriate only when the agent cannot determine the reported behavior from the available, retained evidence—for example, an unavailable observation capability or an ambiguous application outcome. It must cite that limitation in its evidence. It is not a substitute for an unsupported claim and does not make a scoreable case unscoreable.

For a trial that the independent scorer marks not scoreable, self-assessment correctness is also not scoreable. Its agent status and reason remain in the data for robustness reporting.

Primary RQ1 reporting therefore separates:

1. reproduction-success rate among scoreable trials;
2. self-assessment-correctness rate among scoreable trials, with `INCONCLUSIVE` in the denominator but not the numerator;
3. false-positive, false-negative, and abstention rates;
4. duration and turn distributions; and
5. infrastructure-exclusion count and reasons.

Results are reported both per trial and aggregated per case. The case-level summary reports the five-trial distribution rather than selecting the best run. Confidence intervals and uncertainty treatment will be chosen before data collection; at minimum, report the observed proportion and trial count. No resampling, prompt adjustment, or replacement trial is allowed because an outcome is unfavorable.

## 3. RQ2 protocol: capability conditions

### Capability families

The formal `FULL` condition is the union of the following families:

| Family | Formal meaning | Current pilot representation |
| --- | --- | --- |
| UI interaction | Discovering available UI targets and performing permitted interaction, including text entry and scrolling when formally implemented. | Partly represented: `inspect_app()`, `get_text(target)`, and `tap(target)`. Text entry and scrolling are not yet model-facing pilot capabilities. |
| Widget/runtime inspection | Inspecting widget/UI state and passive visible observations. | Represented by normalized widget inspection and passive text observations. |
| Runtime-error observation | Reading runtime-error evidence from the active app under a defined session/window contract. | Represented by `get_runtime_errors()`, but its evidence contract is not yet formal-safe; see Section 11. |
| Source inspection | Read-only, bounded access to the pinned case source without hidden ground truth. | Not represented by the current pilot tools. |
| Temporary instrumentation and hot reload | A controlled, auditable way to add temporary observation code and reload the pinned app. | Not represented by the current pilot tools. |

The pilot's label `FULL` means the tools available in that engineering pilot. It must not be treated as formal `FULL` until the intended formal capability families, their tool contracts, permissions, and logging are implemented and frozen.

### Planned conditions

The primary ablation design compares formal `FULL` with one removal at a time:

| Condition | Exposed families | Purpose |
| --- | --- | --- |
| `FULL` | All formal families | Reference condition. |
| `NO_RUNTIME_ERRORS` | All except runtime-error observation | Tests the contribution of explicit error evidence. |
| `NO_WIDGET_RUNTIME_INSPECTION` | All except widget/runtime inspection | Tests the contribution of inspectable application state. |
| `NO_SOURCE_INSPECTION` | All except source inspection | Tests whether source access materially changes reproduction. |
| `NO_INSTRUMENTATION_HOT_RELOAD` | All except temporary instrumentation and hot reload | Tests the contribution of active, temporary observation. |

UI interaction remains available in every condition. A condition removes only its named family; it must not quietly change the prompt, turn budget, model, issue wording, case revision, or another tool family. The formal tool manifest must state the exact available operations and versions for each condition.

This is a one-family-at-a-time ablation, not a factorial study. It supports interpretable first estimates without multiplying the trial count into an impractical matrix. Capability conditions that cannot be implemented with comparable safety, auditability, and reset behavior must not enter the formal study.

## 4. Public-case inclusion and exclusion criteria

### Inclusion criteria

A candidate case is eligible only when all of the following are established during curation:

1. A public source repository and public issue report (or equivalent public bug reference) are available.
2. The repository can be pinned to a reproducible commit, tag, or release revision.
3. Flutter, Dart, package, platform, and relevant build-tool versions are known or can be captured reproducibly.
4. The issue's reported behavior can be manually reproduced on the pinned state in the evaluation environment.
5. A binary observable reproduction predicate can be written independently of the agent.
6. The required setup is feasible and lawful in the evaluation environment, with no undisclosed credentials or proprietary backend.
7. The case can be reset to a known initial state between trials.
8. The issue wording can be captured as a stable snapshot without leaking curator-created hidden explanation.
9. The case fits one of the four top-level defect classes in Section 6.

Preference is given to self-contained repositories or minimal reproductions, stable build instructions, and cases whose observable predicate can be captured through formal tools or retained evidence.

### Exclusion criteria

Exclude a candidate if any of the following applies:

- the source, report, or required revision is not public;
- a proprietary, authenticated, paid, rate-limited, or hidden backend is necessary for the defect;
- the behavior requires a physical device, hardware accessory, account, sensor, push service, or third-party service not intentionally included and reproducibly provisioned;
- reproduction depends on inherently uncontrolled timing, external network content, advertising inventory, or non-deterministic remote data that cannot be controlled;
- the defect is only a subjective visual judgement with no agreed observable predicate;
- the project cannot be built/run at the pinned revision in the target environment;
- the report exposes a patch, exact source location, or other information that cannot be separated from the agent-visible issue text;
- the candidate is a duplicate of the same underlying defect/project state already selected; or
- licensing, security, or data-handling restrictions prevent evaluation.

An otherwise useful case may be deferred rather than forced into the first formal dataset when its setup or predicate is not mature.

## 5. Independent ground-truth specification

Ground truth is a curator-owned, versioned record stored separately from the agent-visible issue input and inaccessible to the evaluation agent. It is created and manually verified before any formal agent trial for that case. It is not an automated scoring implementation.

Each record shall contain at least:

```yaml
case_id: PUB-001
source_repository: https://example.invalid/owner/repository
issue_reference: https://example.invalid/owner/repository/issues/123
case_git_revision: 40-character-or-equivalent-pinned-revision
issue_snapshot_path_or_hash: sha256:...
flutter_version: 3.x.y
dart_version: 3.x.y
platform: android-emulator-api-...
setup_instructions: |
  Exact curator-verified setup and reset steps.
reproduction_predicate:
  description: Observable condition that establishes the reported defect.
  evaluation_method: Manual/evidence-based procedure for the independent scorer.
expected_observable_evidence:
  - Required UI, runtime, widget, log, or other retained observation.
defect_class: incorrect_application_state
subtype: stale_state_after_action
manual_verification:
  verified: true
  verification_date: 2026-09-30
  verifier_id: curator-identifier
  notes: Known constraints and reset expectations.
```

`reproduction_predicate` must express the external behavior, not a solution or implementation fact. `expected_observable_evidence` states what proves the predicate and does not need to be shown to the agent. A second curator review is recommended for ambiguous predicates and required before final dataset freeze where feasible.

Ground-truth outcomes, curator notes, and manual-verification evidence are stored outside the prompt, agent result directory, model context, and tool surface. Access control and path conventions must prevent accidental inclusion in source-inspection capability.

## 6. Defect taxonomy

Every public candidate receives exactly one top-level class:

| Top-level class | Classification rule | Typical predicate |
| --- | --- | --- |
| `unhandled_exception` | A user or lifecycle action causes an uncaught exception/error that should have been handled. | Captured runtime exception after specified action. |
| `incorrect_application_state` | The app reaches an observable state inconsistent with the issue's expected behavior. | Wrong value, route, enabled state, or persisted state. |
| `structural_rendering_fault` | The rendered/widget structure is observably missing, duplicated, misplaced, or configured incorrectly. | Visible/widget-tree presence, count, hierarchy, or layout invariant. |
| `silent_error_condition` | A failure occurs or a required operation fails without an unhandled exception, and observable state/log/runtime evidence establishes it. | Error event/log plus unchanged or failed UI state. |

The top-level classes remain fixed so results are comparable. Optional metadata may capture subtype (for example, validation exception, stale state, wrong navigation, duplication, async failure), primary observation channel, and difficulty factors. A case spanning several symptoms is classified by the first independently observable failure that the issue asks to reproduce; any secondary symptoms are recorded as metadata, not extra top-level labels.

## 7. Dataset composition target

The formal core target is approximately **25 manually verified public defect cases**:

| Class | Target range | Planning target |
| --- | ---: | ---:|
| Unhandled exception | 5–7 | 6 |
| Incorrect application state | 6–8 | 7 |
| Structural rendering fault | 5–7 | 6 |
| Silent error condition | 5–7 | 6 |

The target is balanced enough to avoid one class dominating, while allowing curation reality to take precedence over artificial equality. The final count and any deviation must be documented before formal evaluation.

The core set contains genuine defect cases. In addition, prepare a small, clearly labelled **secondary control set**—for example, three to five fixed-revision or negative-control variants—only if it can be made without confusing RQ1's defective-case denominator. Controls are reported separately and are useful for characterising false-positive behavior; they do not replace public defects in the 25-case core.

Across the core dataset, target roughly 8 low-, 11 medium-, and 6 high-observable-difficulty cases. Include both simple and multi-step flows, but do not use complexity alone as a selection criterion. Diversify repositories/packages: seek several independent owners and codebases, and avoid letting a single repository account for more than three core cases unless the final curation report justifies the exception.

## 8. Difficulty metadata policy

Difficulty is recorded as separate observable categories, not collapsed into an arbitrary score. Each case record should include:

| Metadata | Suggested values |
| --- | --- |
| UI actions | Exact known minimum number or range. |
| Navigation depth | None, one route, multi-route. |
| Text entry | None, optional, required. |
| Scrolling | None, optional, required. |
| Runtime-error dependence | Not useful, supportive, required for predicate. |
| Widget/runtime-inspection dependence | Not useful, supportive, required for predicate. |
| Source-inspection usefulness | Not useful, supportive, likely required to discover a route/condition. |
| Instrumentation usefulness | Not useful, supportive, likely required to observe the predicate. |
| Asynchrony | None, bounded local async, external/complex async. |
| Setup complexity | Standard run, additional deterministic setup, specialised but supported setup. |
| Reset complexity | Restart only, clear local state, curated reset procedure. |

The curator may assign a transparent `low`, `medium`, or `high` overall difficulty label for stratification, accompanied by the above factors. Analyses must not imply that the label is a measured interval scale.

## 9. Model-selection pre-study

The main model is not selected by the pilot. Before formal evaluation, run a bounded model-selection pre-study using **two to four eligible candidate models** and a small, held-out-from-the-main-study set of **six to eight curated calibration cases** spanning the taxonomy and difficulty levels.

Candidate models may be local or cloud-hosted, but each must support the frozen tool-calling and structured-output contract. Eligibility requires a documented provider/model identifier, version or immutable release reference where available, stable API access, acceptable research data handling, and feasible cost/latency.

For each candidate, use the same pre-study prompt, tool definitions, turn budget, sampling settings, device/platform, and calibration case revisions. Run three independent trials per calibration case. The selection report records:

- valid tool-call reliability (the model emits executable calls rather than only textual tool intent);
- structured-output completion and schema-validity rate;
- rate of clean natural termination within budget;
- reproduction and self-assessment outcomes as directional evidence, not a fully powered model comparison;
- median duration/turns, provider cost where applicable, and operational stability; and
- any compatibility limitation that prevents a fair formal run.

Choose one main model using a predeclared rule: select the eligible model with the strongest combined operational reliability—first tool-call and structured-output reliability, then natural termination—and acceptable calibration reproduction performance, cost, and latency. If candidates are materially tied, choose the lower-cost/lower-latency model and record the tie-break. Do not tune prompts or tools uniquely for a candidate. Calibration cases are not included in the primary formal outcome unless the protocol is amended before any main-study run.

## 10. Reproducibility metadata

Every formal run must persist an immutable run directory and a structured record containing at least:

- `run_id`, study ID, case ID, trial number, and UTC start/end timestamps;
- case repository URL and pinned Git revision;
- issue snapshot identifier and SHA-256 hash;
- frozen prompt version and SHA-256 hash;
- model name, provider, provider endpoint class, model/version identifier, and client/framework versions;
- complete model settings, including temperature, seed when supported, top-p, and any tool-choice/response settings;
- PydanticAI/framework version, Python version, and relevant dependency lock/hash;
- Flutter/Dart versions, project dependency lock/hash, and tool/MCP server versions;
- capability condition plus a hash/version of its exact tool manifest;
- OS, device/emulator/simulator model and ID, platform/API version, architecture, and environment image/version;
- configured turn/step/time budgets;
- duration, turns, final typed status, and the agent's exact evidence;
- raw model/message trace and ordered model-facing tool-call/return trace;
- retained predicate-relevant evidence references, with hashes where practical;
- trial execution state: scoreable, reproduction success/failure when independently scored, or infrastructure exclusion with cause; and
- storage schema version.

The ground-truth outcome and curator material are stored in a separate scorer-owned record, linked by case ID and revision but not copied into the agent-visible run record before scoring.

Per-tool timing and failure metadata are **required** for formal reproducibility because tool availability and latency can affect a bounded agent's behavior. For every model-facing tool event, record a stable event ID, tool name/version, timestamp, duration, outcome (`success`, `tool_error`, `timeout`, or `transport_error`), and a content/reference hash. Store raw arguments and outputs when permitted; otherwise store a redacted representation and its reason. This is audit evidence, not a new primary performance metric.

## 11. Runtime-error evidence contract

### Observed pilot ambiguity

The persisted CASE_004 and CASE_005 traces contain the contradictory compact result:

```json
{"error_count":1,"errors":["No runtime errors found."]}
```

The current adapter converts Dart MCP output by string-pattern parsing. It recognises a literal `No runtime errors found.` only when an individual decoded list item exactly equals that string. A structured MCP content item can instead reach the fallback path as a non-literal string and be counted as one generic error. The stored trace confirms the contradiction, but it does not retain the raw MCP response needed to establish the precise upstream envelope. This is a data-contract/formatter ambiguity, not evidence that either case had a runtime error.

### Required formal contract

The formal runtime-error tool must return a versioned, typed observation with mutually consistent fields. It must never represent a no-error message as an error entry.

```json
{
  "schema_version": "1",
  "observation_id": "runtime-errors-...",
  "scope": {
    "app_session_id": "...",
    "since": "2026-09-30T00:00:00Z",
    "until": "2026-09-30T00:00:10Z",
    "clear_before_observation": true
  },
  "status": "observed",
  "error_count": 0,
  "errors": []
}
```

Rules:

1. `status` is one of `observed`, `unavailable`, or `tool_error`.
2. When `status` is `observed`, `error_count` equals `errors.length` exactly.
3. A no-error observation is exactly `error_count: 0` and `errors: []`; no prose no-error marker belongs in `errors`.
4. Each non-empty error item has a stable type/category, normalized message, timestamp when available, and a raw-evidence reference or hash. Deduplication rules must be documented.
5. `unavailable` and `tool_error` carry a typed reason and do not masquerade as zero errors.
6. The observation window and clearing/reset semantics are recorded, so an error can be attributed to the current trial/action sequence rather than a prior run.
7. The raw Dart MCP response is retained privately with the tool-event metadata for audit, while the model sees only the compact typed contract.

Formal scoring may use runtime-error evidence only when the condition exposes the capability and the observation has `status: observed`. Absence of runtime errors is not itself proof that a non-exception defect was not reproduced.

## 12. Freeze policy

| Item | Freeze before formal evaluation? | Policy |
| --- | --- | --- |
| Framework and dependency versions | Yes | Pin PydanticAI, Python, Flutter/Dart, MCP/tool versions, and dependency locks. |
| Generic prompt and output schema | Yes | Version and hash; no case- or condition-specific wording. |
| Tool contracts | Yes | Freeze model-facing names, schemas, error semantics, capability manifests, and logging behavior. |
| Result/evidence schema | Yes | Freeze storage schema and raw-trace retention rules. |
| Capability definitions | Yes | Freeze `FULL` and every ablation's allowed/blocked operations. |
| Environment | Yes | Freeze supported OS/device image, reset procedure, platform/API, and network policy. |
| Main model settings | Yes | Freeze selected model/provider and all sampling/budget settings after the pre-study. |
| Scoring rules | Yes | Freeze predicate evaluation, scoreability, self-assessment, and exclusion rules before agent trials. |
| Candidate model | No, until pre-study concludes | Remains configurable only for the bounded pre-study. |
| Curated public cases | No, until curation concludes | Add, verify, and freeze the dataset manifest before the main run. |
| Missing capability implementations | No, until formal readiness | Implement and validate them before the freeze; do not evaluate a partial `FULL` as formal `FULL`. |
| RQ3 regression-status evaluation | Deferred | No implementation in this study stage. |
| Patch generation and root-cause diagnosis | Deferred | Outside the reproduction-agent scope. |
| Multi-agent architecture | Deferred | Not needed for the controlled first study. |
| Automatic case importer | Deferred | Manual, verified curation comes first. |

Any post-freeze change to a frozen item requires a new experiment version, explicit rationale, and separate reporting. It must not be mixed silently with already collected formal trials.

## 13. Risks and open questions

- **Capability feasibility:** source inspection and temporary instrumentation/hot reload must be implemented in a generic, auditable manner before formal `FULL` can exist. Their availability may vary by case and platform.
- **Case setup burden:** public repositories frequently drift or rely on discontinued packages. Curation time and environment maintenance may dominate the study.
- **Issue leakage:** public issue threads can include patches, source locations, and workarounds. The issue snapshot policy must define the agent-visible text carefully.
- **Ground-truth independence:** predicates must be behavior-focused and prepared before agent runs. Source-inspection capability must not expose hidden ground-truth files.
- **Non-determinism:** Flutter timing, asynchronous UI, emulator load, and model sampling can vary. Five independent trials, reset evidence, and explicit exclusions mitigate but do not eliminate this risk.
- **Ablation validity:** a capability removal may make a predicate unobservable rather than simply reduce reasoning ability. Results must be interpreted by defect class and observation dependence.
- **Runtime-error semantics:** the typed contract in Section 11 must be implemented and manually validated against both no-error and real-error cases before formal data collection.
- **Statistical power:** an approximately 25-case dataset supports a controlled MSc-scale evaluation but may yield wide intervals for class-level or ablation conclusions. Report uncertainty and avoid claims of universal superiority.
- **Cloud/local comparability:** provider changes, model aliases, cost, latency, and data governance may make candidate models non-comparable. The pre-study records these constraints before selection.
- **Controls:** fixed/negative controls are valuable for false-positive analysis but must not contaminate the genuine-defect core metrics.

## 14. Recommended Stage 11

Stage 11 should be a **formal-readiness implementation and curation-preparation stage**, not an agent experiment. Its goal is to implement and validate the frozen-ready data/tool contracts required by this specification: the independent ground-truth record format and separation boundary, the versioned runtime-error evidence contract, complete formal-run metadata, and a manual public-case intake/checklist.

Stage 11 should not run model comparisons or formal agent trials. After those contracts have been verified, a separate approved stage can curate and manually verify a candidate public-case pool, followed by the bounded model-selection pre-study. Only then should the final model, dataset manifest, capability implementations, and scoring rules be frozen for formal evaluation.
