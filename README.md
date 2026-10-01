# Flutter Bug Reproduction Agent

## Project Overview

This project is an experimental research environment for studying whether an LLM-based agent can reproduce reported bugs in running Flutter applications.

The research focus is deliberately narrow:

- give an agent a natural-language issue report;
- let it interact with and inspect a running Flutter application through bounded tools;
- ask it to determine whether the reported defect can be reproduced;
- retain the agent's result, trace, tool activity, and independent evidence separately.

The project is **not** a general coding assistant, autonomous debugger, patch generator, or root-cause analysis system. Its purpose is to provide a controlled environment for the MSc research project on automated Flutter bug reproduction.

The study is designed around three broader questions:

1. Can an LLM agent reproduce Flutter defects from natural-language issue reports and correctly judge whether reproduction succeeded?
2. Which runtime capabilities materially contribute to reproduction performance?
3. Can a later system determine whether a previously reported defect still persists?

RQ3 is deferred. The current work prepares a defensible RQ1/RQ2 study.

---

## Current Status

The engineering pilot and the formal-design preparation are complete. The project is now ready for a deliberately small, stateful public-case curation experiment.

| Area | Status |
| --- | --- |
| Engineering pilot | Complete |
| Five synthetic Flutter pilot cases | Complete |
| PydanticAI migration and trace persistence | Complete |
| Stage 10 formal RQ1/RQ2 protocol | Complete |
| Stage 11 readiness contracts and curation intake materials | Complete |
| Public Flutter case curation | Next: small experiment only |
| Formal dataset of approximately 25 cases | Not started |
| Model-selection pre-study | Not started |
| Formal RQ1/RQ2 trials | Not started |

The current development baseline is **PydanticAI 2.51.0** with **qwen2.5-7b-instruct** served locally through LM Studio's OpenAI-compatible endpoint. This is an engineering-development baseline, **not** the selected formal evaluation model.

---

## What Has Been Built

### Synthetic engineering pilot

The repository contains five deterministic synthetic cases used to prove the end-to-end engineering path:

- `CASE_001`: incorrect application state;
- `CASE_002`: unhandled runtime exception;
- `CASE_003`: navigation/flow error;
- `CASE_004`: structural rendering fault;
- `CASE_005`: silent error condition.

These cases established that a local LLM can receive an issue, interact with the app, make a typed self-assessment, and retain a trace. They are development and pilot evidence only. They are **not** the formal research dataset and must not be presented as public real-world benchmark cases.

### Agent and runtime baseline

The working architecture is:

```text
Agent-visible issue snapshot
        ↓
PydanticAI
        ↓
Development model: qwen2.5-7b-instruct
        ↓
Generic Flutter tool surface
        ↓
Dart MCP / DTD / Flutter runtime
        ↓
Typed agent result + persisted trace and audit evidence
```

The current model-facing tools are deliberately small and generic:

```text
inspect_app()
get_text(target)
tap(target)
get_runtime_errors()
```

`inspect_app()` exposes a compact, normalized view rather than raw Flutter Driver or inspector complexity. `get_runtime_errors()` is an observed-runtime contract, not an inference made from UI state.

The pilot also established generic robustness rules:

- unsupported reads and invalid targets return normal tool results rather than aborting a run;
- successful navigation invalidates discovered targets, so a fresh `inspect_app()` is required before later route-dependent actions;
- passive visible text may be exposed where it is needed to observe structural faults;
- the system records what the model actually concluded; it does not silently correct an incorrect self-assessment.

These are general infrastructure behaviors. They are not case-specific hints.

### Formal protocol and readiness contracts

Stage 10 defines the formal RQ1/RQ2 protocol. In RQ1, independent reproduction and agent self-assessment are separate outcomes. Future formal trials use a reset environment, fixed study settings, an independent observable predicate, and full trace/audit retention.

Stage 11 adds the contracts needed before public cases can become formal cases:

- a curator-only ground-truth template and independent-predicate record;
- formal run metadata and per-tool audit records;
- a typed runtime-error observation contract;
- a public-case intake checklist;
- explicit separation between agent-visible issue material and curator-only evidence, notes, scoring, and ground truth.

The future formal `FULL` condition is planned to cover five capability families:

```text
UI interaction
Widget/runtime inspection
Runtime-error observation
Source inspection
Temporary instrumentation and hot reload
```

Only the first three are presently available in the development baseline. Source inspection, temporary instrumentation/hot reload, formal capability conditions, and their freeze remain later work.

---

## Repository Areas

```text
flutter-bug-reproduction/
├── README.md
├── plan.md
├── flutter_app/                 # synthetic pilot app and cases
├── issues/                      # synthetic agent-visible issue files
├── agent/                       # PydanticAI runner, model/configuration, tools
├── results/                     # persisted pilot/formal run records
└── curation/                    # curator-only intake, ground truth, public cases
```

The `curation/` area is intentionally separate from the evaluation path. A curator may inspect public issue discussions, comments, MRE repositories, fixes, and local validation evidence. The later evaluation agent must not receive information that leaks the answer, including curator notes, expected evidence, exact predicates, root-cause explanations, patches, workarounds, or scoring outcomes.

---

## Public-Case Direction

The planned formal dataset is approximately **25 real public Flutter cases**, balanced across:

- unhandled exception;
- incorrect application state;
- structural rendering fault;
- silent error condition.

A formal case will require, at minimum:

- a public issue and public MRE or source repository;
- a recorded, pin-able tested revision;
- known Flutter/Dart environment;
- resettable manual reproduction;
- an objective, independent observable predicate;
- provenance and compatibility changes recorded;
- a leakage-reviewed agent-visible issue snapshot;
- no private credentials, uncontrolled backend, inaccessible hardware, or subjective-only judgement.

The next step is deliberately **not** formal dataset collection. It is a small experiment to test whether this workflow works against real public reports.

### Stateful curation experiment

The curator will use persistent files:

```text
curation/search_state.csv  # every substantively inspected issue, comment, MRE link, or repository
curation/candidates.csv    # actual candidates and their triage/validation outcome
```

Before deep inspection, the curator canonicalizes the URL and checks `search_state.csv`. Previously inspected, accepted, or rejected material is skipped unless explicitly reopened. Rejected work remains recorded; it is benchmark-construction evidence, not disposable noise.

The first experiment stops at the first of:

- two accepted, manually reproduced public cases; or
- five previously unseen candidates fully attempted.

Each outcome is recorded as `accepted`, `rejected`, or `deferred`, with a precise reason. Accepted cases are stored under `curation/accepted/<defect_category>/<case_id>/` with provenance, pinned revision, curator reproduction notes, evidence, and hidden ground truth. The reproduction agent, its prompt, PydanticAI, the development model, and formal-study settings must not be changed during this experiment.

---

## Development and Research Workflow

Work remains phase-gated. One chat/session works on one approved stage only. A stage is complete only after its scoped work and checks are complete, the working tree is reviewed and clean, and the user has approved proceeding.

If manual action is needed—such as starting an emulator, making a public repository available, selecting a model, or confirming runtime behavior—the agent must stop and request that action. It must not substitute unverified static evidence for runtime evidence.

Use local Git throughout. Preserve meaningful stage-boundary commits. Do not rewrite history, commit generated noise, or claim a runtime result from a build, analyzer, tap acknowledgement, or model statement alone.

Every completed stage reports:

- work implemented and files changed;
- commands/checks and their actual results;
- runtime or artifact evidence where applicable;
- unresolved issues and required user action;
- Git status, commit hash, and relevant recent history.

See `plan.md` for the operational stages, including the small public-case curation experiment and the later formal-study sequence.

---

## Scope Boundaries

Until the formal study is frozen:

- do not tune the agent to individual public cases;
- do not use curator ground truth in the evaluation-agent context;
- do not treat synthetic pilot results as formal evidence;
- do not select the formal model before the bounded pre-study;
- do not begin formal RQ1/RQ2 experiments before the dataset, capability set, model, and environment are frozen;
- do not implement patch generation, root-cause analysis, a multi-agent system, RAG, or broad autonomous debugging.

The priority is a small, observable, reproducible research platform and a transparent public-case derivation process—not fast accumulation of attractive-looking bugs.
