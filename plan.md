# Implementation Plan — Flutter Bug Reproduction Agent

## Purpose of This Plan

This is the operational staged plan for the project described in `README.md`.

For every stage:

1. work on this stage only;
2. do not pre-implement a later stage;
3. run the listed checks and record actual outcomes;
4. distinguish tool success, build success, and runtime/artifact evidence;
5. commit a completed implementation stage with a meaningful local Git message;
6. verify `git status --short` is clean before declaring completion;
7. report the stage result and stop for explicit user approval.

If a stage requires manual action or an unavailable prerequisite, stop and request the exact action. Do not guess around it, replace it with unverified evidence, or continue into a later stage.

The formal protocol in `docs/stage_10_formal_evaluation_protocol.md` governs research design; this plan governs execution stages. [AGENTS.md](AGENTS.md) supplies the shared Claude Code/Codex session workflow. `.agent/CURRENT.md` and `.agent/HANDOFF.md` record operational scope and evidence only; neither can grant a later stage or override this plan. `continue` resumes an approved stage, while an explicit instruction such as `Start Stage 14 according to plan.md` opens the next one.

**Status reconciled 2026-10-11:** Git and `curation/` record completed bounded curation batches in Stages 12, 13, and 13B, most recently `a58cf58`. Stage 14 has not started and awaits explicit approval. The original Stage 12 instructions below are retained as history, not a new curation authorization.

---

# Completed Stages

The following stages are historical project checkpoints. They are complete and must not be repeated or silently redesigned while beginning later work.

## Stage 0 — Inspect the Environment

**Status: COMPLETE**

The initial machine, Flutter/Dart/Python/Git availability, local model setup, device/emulator situation, and Flutter/Dart MCP prerequisites were inspected before implementation.

## Stage 1 — Create the Minimal Repository Structure

**Status: COMPLETE**

The repository, Git baseline, Python agent area, Flutter area, issue area, result storage area, and ignore rules were established.

## Stage 2 — Create the Flutter Pilot Application

**Status: COMPLETE**

One Flutter application with independent launch entry points for five small deterministic cases was created. Each case can be reset through a fresh launch.

## Stage 3 — Create Matching Issue Files

**Status: COMPLETE**

Each synthetic case received an agent-visible natural-language issue description without source-level solution disclosure.

## Stage 4C — Preserve Investigation and Migrate Cleanly to PydanticAI

**Status: COMPLETE**

The main runtime moved to PydanticAI 2.51.0 while preserving the earlier framework investigation separately. The current development model is configurable `qwen2.5-7b-instruct` through LM Studio's OpenAI-compatible endpoint. The model-facing tool surface remained generic and the framework retained full message history and typed results.

## Stage 5 — First Reliable Flutter Interaction

**Status: COMPLETE**

CASE_001 validated the operational path from compact inspection through interaction and post-action observation. Infrastructure success and semantic self-assessment agreement were recorded separately.

## Stage 6 — First Issue-Driven Bug Reproduction

**Status: COMPLETE**

The system completed the path:

```text
agent-visible issue
→ PydanticAI agent
→ Flutter runtime tools
→ observations
→ typed agent self-assessment
```

The runner retained the model's actual conclusion rather than replacing it with hidden ground truth.

## Stage 7 — Add Result Storage

**Status: COMPLETE**

Completed runs are persisted under `results/runs/<run-id>/` with a result record, serialized trace, and summary row. Storage is append-only at the run level; prior results are not overwritten.

## Stage 8 — Run All Five Pilot Cases

**Status: COMPLETE**

The five synthetic cases were run with the common development baseline. The pilot established engineering viability across state, runtime-exception, navigation, structural, and silent-failure behavior. These results are not a formal dataset or formal evaluation result.

## Stage 8A — Add Runtime-Error Observation and Generic Robustness

**Status: COMPLETE**

Generic robustness was added based on pilot evidence:

- `get_runtime_errors()` exposes runtime-error observations;
- unsupported reads and invalid targets are normal tool outcomes instead of terminal Python failures;
- passive visible text supports structural inspection where appropriate;
- a successful tap invalidates discovered targets, requiring a new `inspect_app()` before a route-dependent read or action.

No case-specific selector, retry, or answer-correction behavior is allowed.

## Stage 9 — Review Before Expansion

**Status: COMPLETE**

The pilot was reviewed before formal expansion. The resulting decisions were:

- PydanticAI is the development orchestration baseline;
- qwen2.5-7b-instruct is adequate for development, not yet the formal model;
- current tools are sufficient for the pilot but not the complete formal RQ2 capability set;
- synthetic positive cases do not constitute a defensible public benchmark;
- formal protocol, curation contracts, and a public-case workflow are required before formal experiments.

## Stage 10 — Define the Formal RQ1/RQ2 Evaluation Protocol

**Status: COMPLETE**

The formal protocol now defines:

- RQ1's separate outcomes: independent reproduction predicate and agent self-assessment correctness;
- resettable, independent formal trials and planned repeated runs;
- formal reporting, including reproduction rate, false positives/negatives, abstentions, duration, turns, and infrastructure exclusions;
- the prospective public dataset target of approximately 25 real cases across four defect classes;
- a bounded model-selection pre-study before selecting the formal model;
- a future `FULL` capability set and RQ2 ablation conditions;
- separation of research conclusions from engineering-pilot results.

## Stage 11 — Add Formal Readiness Contracts

**Status: COMPLETE**

Formal readiness contracts now cover:

- curator-only ground-truth records and independent observable predicates;
- agent-visible versus curator-only information separation;
- public-case intake checklist;
- formal run metadata;
- per-tool audit records;
- typed runtime-error observations, including unambiguous zero-error observations;
- templates and directory conventions for curated cases.

Stage 11 does not create the formal public dataset, select the formal model, implement missing capabilities, or run formal RQ1/RQ2 trials.

---

# Stage 12 — Experimental Stateful Public Flutter Bug Curation

**Status: COMPLETE — historical curation batch (`b504bdd`).** See `curation/README.md` and the retained ledgers for actual outcomes. Do not repeat it on `continue`.

**Historical discrepancy:** The committed Stage 12 ledger records 4 accepted / 9 attempted, exceeding the original 2 / 5 stop condition below. No corresponding scope amendment is recorded in this plan. Preserve both facts; the workflow status reconciliation does not retroactively authorize the difference.

## Goal

Test the public-case curation workflow on a small sample of real public Flutter bug reports. This is a curator experiment, not dataset collection for formal evaluation and not an evaluation of the reproduction agent.

## Scope

The curator may:

- search public GitHub issues and public repositories;
- inspect issue bodies, relevant comments, exact comment permalinks, and linked MREs;
- clone a public MRE or make a temporary project around an exact inline sample;
- build/run the candidate manually and inspect local runtime behavior;
- create/update the persistent curation tracking files and curator-only case material.

The curator must not:

- modify the reproduction agent, agent prompt, PydanticAI, development model, synthetic cases, or formal research tools;
- invoke the reproduction/evaluation agent;
- begin model selection, formal data collection, formal RQ1/RQ2 experiments, or capability implementation;
- repair, simplify, or silently rewrite a public MRE to create an easier bug.

## Preflight

1. Read `README.md`, the Stage 10 formal protocol, Stage 11 templates/checklists, and current `curation/` documentation.
2. Inspect existing `curation/search_state.csv` and `curation/candidates.csv`; create either only if absent and with the agreed headers.
3. Preserve every existing record. Do not overwrite or remove prior entries.
4. Confirm the local Flutter runtime and emulator/device available for candidate validation.

## Persistent state

Maintain `curation/search_state.csv` with at least:

```csv
source_type,url,parent_url,visited_at_utc,outcome,candidate_id,notes
```

Record every issue, comment permalink, MRE link/repository, or other candidate page substantively inspected. Canonicalize a URL before checking it. If its page or candidate has already been evaluated, rejected, deferred, or accepted, skip it unless the user explicitly asks to reopen it.

Maintain `curation/candidates.csv` with at least:

```csv
candidate_id,repository,issue_url,mre_url,status,defect_class,build_status,reproduction_status,rejection_reason,notes
```

Permitted statuses are:

```text
discovered
triaging
testing
accepted
rejected
deferred
```

Never delete rejected candidates. Search state is broad memory; the candidate table contains only material promoted to genuine candidacy.

## Candidate search and triage

Prefer public Flutter reports with an inline or linked MRE, deterministic steps, an objective outcome, and a source revision that can be recorded. Inspect relevant comments: a reproduction repository often appears only in a comment.

Initial sources may include:

- `flutter/flutter` issues;
- `flutter/packages` issues;
- public Flutter package/plugin repositories;
- public open-source Flutter applications with small supplied MREs.

Useful discovery phrases include `minimal reproducible`, `minimal reproduction`, `minimal example`, `minimal code sample`, `reproduction repository`, `reproduction repo`, `sample project`, and `reproducible example`. Do not restrict discovery to these exact phrases.

For each previously unseen candidate:

1. record it immediately in `candidates.csv` as `discovered` or `triaging`;
2. record each substantively inspected page in `search_state.csv`;
3. locate the MRE and capture provenance;
4. classify provisionally as `unhandled_exception`, `incorrect_application_state`, `structural_rendering_fault`, or `silent_error_condition`;
5. identify whether a binary, independently observable predicate appears possible;
6. reject early when the intake criteria are clearly not met, recording the precise reason.

Reject or defer candidates requiring proprietary/authenticated backends, paid services, private credentials, uncontrolled external data, push services, inaccessible hardware/sensors, unsupported/discontinued toolchains, subjective-only visual judgement, engine/compiler rebuilding, security-sensitive workflows, or huge applications without an MRE.

## MRE handling and validation

For a linked repository:

- record public URL and exact tested revision;
- clone/obtain it only for local curator validation;
- do not silently modify behavior;
- record any compatibility modification and reject/defer when substantial reconstruction is necessary.

For an inline sample:

- use supplied code faithfully in a temporary Flutter project;
- record scaffolding and version assumptions;
- do not create a new bug or make substantive code changes.

For a viable candidate, build and run it, follow the reported steps, reset it as needed, and collect sufficient local evidence to decide whether the reported behavior occurs. A build or successful tap alone is not reproduction evidence.

If manually reproduced:

1. set status to `accepted` and reproduction status to `reproduced`;
2. assign a defect class;
3. store it under `curation/accepted/<defect_class>/<case_id>/` using the Stage 11 contract;
4. retain issue/MRE/revision/environment provenance;
5. record concise curator reproduction notes and the independent predicate;
6. keep ground truth, expected evidence, and curator knowledge hidden from the later evaluation agent;
7. flag solution-leakage risks in the issue material, without finalizing the agent-visible snapshot.

If not reproduced, record `rejected` or `deferred` and one precise reason such as:

```text
missing_mre
build_failure
dependency_obsolete
cannot_reproduce
environment_mismatch
external_service_required
subjective_predicate
solution_leakage
unsupported_platform
```

## Stop condition

Stop immediately at the first of:

- two accepted, manually reproduced cases; or
- five previously unseen candidates fully attempted.

Do not continue searching just to improve acceptance numbers.

## Checks

- tracking CSVs retain all existing rows and parse consistently;
- every substantive inspected URL is represented in search state;
- every attempted candidate has an outcome and reason;
- every accepted case has pinned provenance, environment record, manual reproduction evidence, objective predicate, and hidden ground truth;
- no evaluation-agent, agent-runtime, model, or formal-study files changed;
- Git diff confirms the stage stayed within curation scope.

## Completion criteria

The experiment reaches its stop condition with a transparent ledger of accepted, rejected, and deferred candidates, and an evidence-backed final report. Do not claim the output is the formal dataset.

Suggested commit:

```text
stage 12: run stateful public-case curation experiment
```

**STOP after reporting the result. Wait for user approval.**

---

# Later Research Stages — Respect Each Approval Boundary

## Stage 13 — Broader Public-Case Curation

**Status: COMPLETE — bounded expansion batch (`3e64ebb`), not completion of the approximately 25-case formal dataset.** Evidence: `curation/stage13_pool_summary.md`.

**Goal:** Scale only the validated curation workflow toward the approximately 25-case public dataset, preserving defect-class balance, difficulty distribution, multi-repository coverage, provenance, resetability, manual reproduction, independent predicates, leakage review, and a full rejected/deferred ledger.

**Boundary:** This remains curation. It does not evaluate the agent, tune the agent to cases, or select the model.

## Stage 13B — Improve Curated Case Diversity

**Status: COMPLETE — bounded diversity batch (`a58cf58`).** Evidence: `curation/stage13b_pool_summary.md` and `curation/README.md`.

The committed combined pool contains 13 accepted candidates from 21 attempted (7 rejected, 1 deferred). No calibration/formal split or formal dataset freeze has been made. The summary's seven calibration-suitable cases are indicative candidates, not an approved split. This historical checkpoint does not authorize further curation or model trials.

## Stage 14 — Model-Selection Pre-Study

**Status: ACTIVE (approved 2026-10-11; entry checkpoint `fd4a921ead41ff8f6dbb7fcf19faab794a83131f`, clean tree on `main`).** Setup phase: candidate set, calibration membership, and fixed configuration are not yet recorded; no trials run.

**Goal:** Use a bounded calibration set (approximately 6–8 suitable non-formal cases) to compare a small predefined set of candidate models under one fixed generic prompt, tools, and budget. Select the formal model by the recorded pre-study criteria, not by anecdote.

**Boundary:** Calibration cases must be segregated from the final formal evaluation dataset. Do not alter agent behavior because one model struggles on one case.

**Preflight after approval:** Inspect the entry baseline read-only and verify it is clean before updating approval/state files, checking model availability, changing execution support, or running sanity checks/trials. If unrelated dirty work exists, stop after that audit and request reconciliation. Record the verified entry checkpoint, then continue approved stage work. Inspect the committed pool, existing runner, and persistence; record the predefined model/calibration set and fixed execution configuration before trials. The current runner accepts only synthetic `001`–`005`; public calibration execution support has not been implemented.

**Controls and stop:** Follow protocol §9's candidate eligibility, repeated trials, and selection rule with the same cases/revisions, prompt, tools, sampling, budget, and environment. Keep infrastructure failures, independent reproduction outcomes, and model self-assessment separate. Retain traces and record the model choice transparently. No new curation, per-model/per-case tuning, unrelated capability work, or formal RQ1/RQ2 trials. Stop for candidate-set changes, significant model additions/downloads, paid APIs/credentials, required external setup, or formal model approval. Complete and report only this stage, then wait for approval before Stage 15.

## Stage 15 — Implement Missing Formal Capabilities and Freeze

**Goal:** Implement only genuinely missing generic formal capabilities, such as text entry/scrolling when justified, source inspection, and temporary instrumentation/hot reload. Define and test the future `FULL` and ablation manifests; then freeze prompt, tool definitions/versions, model, sampling settings, budgets, environment, dataset, predicates, and analysis plan.

**Boundary:** A missing general capability may justify infrastructure work. A model's inability to solve a particular case is a research result, not a reason for case-specific adaptation.

## Stage 16 — Formal RQ1/RQ2 Evaluation

**Goal:** Run the frozen protocol on the frozen public dataset. For RQ1, report independent reproduction and self-assessment correctness separately. For RQ2, run only the pre-specified capability ablations. Retain traces, audit events, metadata, predicates, exclusions, and analysis artifacts.

**Boundary:** No capability, prompt, model, or dataset changes after formal trials start without a documented protocol amendment and a new clearly separated study phase.

---

# Required End-of-Stage Report

Every stage ends with a concise report in this form:

```text
Stage: <number and name>
Status: COMPLETE / BLOCKED

Implemented:
- ...

Files changed:
- ...

Commands/checks run:
- ...

Evidence/results:
- ...

Remaining issues:
- none / ...

User action required:
- none / exact action

Git:
- status: clean / not clean
- commit: <hash> <message>
- recent history:
  <git log --oneline output>

STOP: waiting for user approval before the next stage.
```

If a stage is blocked by required user action, do not create a completion commit or claim success. Report the exact blocker and remain in the same stage.

---

# Operating Rules for Local Development Agents

Claude Code and Codex share [AGENTS.md](AGENTS.md). These rules and the stage/protocol boundaries apply to both; focused native development review does not add multi-agent coordination to the research system.

1. Read `README.md` and the current stage before acting.
2. Work on one stage only and respect the stated scope boundaries.
3. Preserve completed-stage decisions unless the user explicitly opens them for revision.
4. Prefer existing Flutter/Dart MCP capabilities to new custom automation.
5. Keep the agent-facing tool surface generic and keep low-level Flutter details private.
6. Keep development-model work, model selection, curation, and formal evaluation separate.
7. Treat successful command execution, a tap acknowledgement, a build, analyzer output, and a model statement as distinct from runtime reproduction evidence.
8. Never expose curator ground truth, predicates, expected evidence, notes, patches, or solution leakage to the evaluation agent.
9. Never discard rejected public candidates or re-inspect known material without a reason recorded in persistent state.
10. Do not add retries, selectors, prompts, or behavior tailored to a single public case.
11. Use local Git, preserve readable history, and verify a clean tree before completion claims.
12. Stop for explicit user approval after every stage.
