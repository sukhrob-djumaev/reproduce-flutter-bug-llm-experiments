# Implementation Plan — Flutter Bug Reproduction Agent

## Purpose of This Plan

Use this file as the execution plan for building the project described in `README.md`.

This plan is intentionally staged.

**Do not implement the entire project in one pass.**

For every stage:

1. work on **this stage only**;
2. do not begin or pre-implement anything from the next stage;
3. run every test/check listed for the current stage;
4. fix failures before declaring the stage complete;
5. if manual user action is needed, stop and ask for that exact action before continuing;
6. commit the completed stage to local Git with a meaningful message;
7. verify `git status` is clean;
8. provide the required end-of-stage report;
9. **stop and wait for explicit user approval.**

One Claude/Codex chat/session should handle one stage only. The next stage should normally begin in a new chat/session after the previous stage has been approved.

Do not silently continue into later stages. Do not guess around missing prerequisites. The user may need to install software, download models, approve permissions, launch a simulator/emulator, configure LM Studio, configure MCP, or manually verify Flutter behavior. Ask for that action explicitly when needed.

---

# Stage 0 — Inspect the Environment

## Goal

Understand the current machine and directory before creating anything substantial.

## Tasks

1. Read `README.md` completely.
2. Inspect the current directory.
3. Check whether the following are installed and accessible:
   - Flutter;
   - Dart;
   - Python 3;
   - `pip`/virtual environments;
   - Git;
   - LM Studio command/server availability if detectable;
   - Android/iOS simulator or emulator tooling;
   - Flutter/Dart MCP tooling if already configured.
4. Record detected versions.
5. Do not install major dependencies automatically unless it is clearly safe and local to the repository.

## Tests

Run version/availability checks such as:

```bash
flutter --version
dart --version
python3 --version
git --version
```

Check Flutter devices:

```bash
flutter devices
```

## User attendance may be required for

- installing Flutter or Python if missing;
- opening/starting an emulator or simulator;
- installing LM Studio;
- approving macOS permissions;
- locating an already installed Flutter/Dart MCP configuration.

## Completion criteria

A short environment report exists and we know which prerequisites are present or missing.

**STOP after reporting the result. Wait for user approval.**

---

# Stage 1 — Create the Minimal Repository Structure

## Goal

Create only the simple folder/file structure defined in `README.md`.

## Target structure

```text
flutter-bug-reproduction/
│
├── README.md
├── plan.md
│
├── flutter_app/
├── issues/
├── agent/
│   ├── main.py
│   ├── models.py
│   ├── capabilities.py
│   └── tools.py
│
├── results/
│   ├── runs/
│   └── summary.csv
│
├── requirements.txt
└── .gitignore
```

## Tasks

1. Create missing directories.
2. Initialize a **local Git repository** in the project root if one does not already exist.
3. Create a Python virtual environment, preferably `.venv/`.
4. Create a clean `.gitignore` covering `.venv`, Python caches, Flutter/Dart build/generated files, IDE noise, local LM Studio/model artefacts if any, simulator/emulator noise, and temporary runtime output that should not be versioned.
5. Keep Python files minimal placeholders at this stage.
6. Initialize `results/summary.csv` with a small header only.
7. Create the initial baseline commit after the structure and files have passed the stage tests.

Suggested initial header:

```csv
case,model,capabilities,status,steps,duration_seconds
```

## Tests

- verify the directory structure;
- verify `git rev-parse --is-inside-work-tree` succeeds;
- inspect `.gitignore` and confirm expected generated/local files are ignored;
- activate the virtual environment;
- verify Python runs from the virtual environment;
- verify placeholder Python files import without syntax errors;
- create the baseline commit;
- verify `git status --short` returns no pending changes.

Example:

```bash
python -m py_compile agent/*.py
```

## Completion criteria

The repository structure exists and contains no unnecessary architecture.

**STOP after reporting the result. Wait for user approval.**

---

# Stage 2 — Create the Flutter Pilot Application

## Goal

Create one Flutter project with multiple independent case entry points.

## Tasks

1. Create the Flutter project inside `flutter_app/`.
2. Keep dependencies minimal.
3. Add five case folders under:

```text
flutter_app/lib/cases/
```

4. Add five neutral entry points:

```text
lib/main_case_001.dart
lib/main_case_002.dart
lib/main_case_003.dart
lib/main_case_004.dart
lib/main_case_005.dart
```

5. Avoid filenames that reveal the exact bug type to the agent.
6. Each entry point must launch only its corresponding case.

## Suggested cases

### CASE 001 — State update failure

A simple counter or state value fails to update after interaction.

### CASE 002 — Runtime exception

A user action produces an unhandled exception.

### CASE 003 — Navigation/flow problem

A multi-step flow leads to an incorrect route/screen/state.

### CASE 004 — Structural widget problem

A widget becomes missing, duplicated, or otherwise structurally incorrect.

### CASE 005 — Silent async/runtime problem

An asynchronous operation fails or leaves incorrect state without crashing the app.

Keep each case small and deterministic.

## Tests

Run every entry point manually:

```bash
flutter run -t lib/main_case_001.dart
flutter run -t lib/main_case_002.dart
flutter run -t lib/main_case_003.dart
flutter run -t lib/main_case_004.dart
flutter run -t lib/main_case_005.dart
```

The user may perform the actual interaction if needed.

For every case verify:

- it starts successfully;
- only the intended scenario appears;
- the expected bug can be reproduced manually;
- restarting the app resets the case to a clean initial state.

## User attendance required

Ask the user to manually confirm each case's behavior if automatic confirmation is not straightforward.

Do not proceed until all five cases are intentionally reproducible.

## Completion criteria

Five deterministic Flutter cases exist and can be launched independently.

**STOP after reporting the result. Wait for user approval.**

---

# Stage 3 — Create the Matching Issue Files

## Goal

Give every case a natural-language issue report that can later be supplied to the agent.

## Tasks

Create:

```text
issues/case_001.md
issues/case_002.md
issues/case_003.md
issues/case_004.md
issues/case_005.md
```

Each issue should contain only information a realistic bug report might reasonably contain:

- title;
- short description;
- expected behavior;
- actual behavior;
- reproduction hints/steps only where appropriate.

Do not reveal:

- faulty file names;
- faulty line numbers;
- implementation explanation;
- hidden solution;
- internal case folder name if avoidable.

## Tests

For each issue:

1. read the issue without looking at the source;
2. confirm that a human can understand what behavior should be reproduced;
3. confirm it does not expose the implementation of the bug.

## User attendance may be required

Ask the user to review the five issue descriptions and approve their realism/difficulty.

## Completion criteria

Five issue files correspond cleanly to the five Flutter cases.

**STOP after reporting the result. Wait for user approval.**

---

# Stage 4C — Preserve Investigation and Migrate Cleanly to PydanticAI

## Goal

Preserve the Phase 4 framework investigation, restore a clean Phase 1–3 main base, and migrate only the agent layer to PydanticAI for CASE_001 infrastructure validation.

## Tasks

1. Archive the uncommitted OpenAI Agents SDK runtime work, generic Flutter adapter, framework-comparison spike, and PydanticAI traces in a meaningful commit without rewriting Phase 1–3 history.
2. Restore `main` to the clean Phase 1–3 base.
3. Use `pydantic-ai==2.51.0` and do not retain OpenAI Agents SDK lifecycle work on `main`.
4. Keep `agent/main.py`, `agent/models.py`, `agent/capabilities.py`, and `agent/tools.py` as the primary agent files.
5. Support configurable `qwen2.5-7b-instruct` through `http://127.0.0.1:1234/v1` without hardcoded secrets.
6. Keep only `FULL` and generic model-facing `inspect_app()`, `get_text(target)`, and `tap(target)` tools.
7. Use `summaryOnly: true` inspection and normalize it into ValueKey targets; keep DTD, raw inspector, and Flutter Driver details private.
8. Use typed `before_value` / `after_value` output, normal PydanticAI termination, and `result.all_messages()`; do not force tool choice, add a custom loop, or correct a wrong semantic result.
9. Validate CASE_001 three times from clean app state. Record semantic disagreement separately; do not retry merely because the answer is wrong.

## Tests

- dependency installation/check and `pip check`;
- `python -m py_compile agent/*.py`;
- `flutter analyze`, `git diff --check`, and an artifact check;
- three clean CASE_001 infrastructure validations with runtime evidence.

## Completion criteria

The archive is safe, the PydanticAI migration passes all checks and three CASE_001 infrastructure validations, and the working tree is clean after the Stage 4C commit.

**STOP after reporting the result. Wait for user approval.**

---

# Stage 5 — First Reliable Flutter Interaction

## Goal

Validate the clean PydanticAI implementation on CASE_001 with a simple operational instruction, without using the issue report yet.

## Tasks

Use CASE_001 only.

1. Start CASE_001 from a clean/reset state.
2. Give the agent a simple operational instruction equivalent to:

```text
Inspect the running application.
Read the current counter value.
Press the + button once.
Read the counter value again.
Return the observed before and after values.
```

3. Use only the existing `FULL` capability set.
4. Keep the model-facing tools generic:
   - `inspect_app()`
   - `get_text(target)`
   - `tap(target)`
5. Do not hardcode CASE_001 selectors, expected values, or a fixed Python workflow.
6. Do not load `issues/case_001.md` yet.
7. Do not automatically correct a wrong typed result.

## Tests

Run three clean attempts and record the real tool sequence, selected targets, before/after runtime observations, typed result, semantic agreement, duration/turns where available, termination behavior, trace retention, and any redundant or unexpected actions.

Infrastructure PASS means inspection, interaction, post-interaction observation delivery, typed output, natural termination, and trace retention all work. A semantically wrong model result is not automatically an infrastructure failure.

## Completion criteria

Three clean CASE_001 interaction-validation runs complete successfully at the infrastructure level, with semantic disagreement recorded separately.

Suggested commit:

```text
phase 5: validate flutter interaction flow
```

**STOP after reporting the result. Wait for user approval.**

---

# Stage 6 — First Issue-Driven Bug Reproduction

## Goal

Run the first actual research-style bug-reproduction attempt from a natural-language issue report.

## Tasks

1. Launch CASE_001 in a clean/reset state.
2. Load `issues/case_001.md`.
3. Give the issue to the agent with a concise, generic reproduction instruction.
4. Let the agent decide how to inspect and interact with the app.
5. Do not reveal implementation details, hidden selectors, expected values, or the known reproduction outcome.
6. Return a typed self-assessment, for example:

```text
status:
  REPRODUCED | NOT_REPRODUCED | INCONCLUSIVE

confidence:
  optional bounded value if useful

evidence:
  short supporting explanation
```

7. Do not automatically correct the model's final judgement against runtime evidence.
8. Keep runtime/tool evidence separate from the agent-reported result.

## Tests

Verify whether the agent understood the issue report, used the available Flutter runtime tools, attempted the relevant interaction, observed the resulting behavior, terminated naturally, produced a typed self-assessment, and retained a complete trace.

For this first pilot, independently verify whether the agent's conclusion matches the actual CASE_001 behavior.

## Completion criteria

One complete path works:

```text
issue file
→ PydanticAI agent
→ Flutter runtime tools
→ runtime observations
→ typed self-assessment
```

Suggested commit:

```text
phase 6: add first issue driven reproduction
```

**STOP after reporting the result. Wait for user approval.**

---

# Stage 7 — Add Simple Result Storage

## Goal

Persist each run in a consistent but lightweight format.

## Tasks

For each run create:

```text
results/runs/<run-id>/
```

At minimum save:

```text
result.json
trace.txt
```

When available also save:

```text
flutter.log
screenshot.png
```

Suggested `result.json` fields:

```json
{
  "case": "001",
  "model": "local",
  "capabilities": "full",
  "status": "reproduced",
  "steps": 0,
  "duration_seconds": 0
}
```

Use actual values. Do not fabricate token counts or step counts when the framework/runtime does not expose them reliably.

Append one row to:

```text
results/summary.csv
```

## Tests

Run CASE_001 once and confirm a unique run folder is created, previous runs are not overwritten, `result.json` is valid JSON, `summary.csv` receives one matching row, and the stored result matches the actual run.

## Completion criteria

One complete run is persisted successfully.

**STOP after reporting the result. Wait for user approval.**

---

# Stage 8 — Run All Five Pilot Cases

## Goal

Determine whether the basic system works across more than one bug type.

## Tasks

Run each case once using:

- the same local model;
- the same agent instructions;
- the same FULL capabilities;
- a clean app state before each run.

Cases:

```text
001
002
003
004
005
```

Do not optimize the prompt for individual cases unless a genuinely general problem is discovered.

## Tests

For every case record:

- final agent status;
- whether independent/runtime evidence agrees;
- rough duration;
- step/turn count if available;
- obvious failure reason if unsuccessful.

Inspect `results/summary.csv` after all five runs.

## Completion criteria

The system has attempted all five cases and produced a small first dataset of results.

**STOP after reporting the result. Wait for user approval.**

---

# Stage 9 — Review Before Expanding

## Goal

Do not add more architecture until the pilot tells us what is actually missing.

## Review questions

After the five-case pilot, report:

1. Is the local model capable enough?
2. Does tool calling work reliably?
3. Does Flutter/Dart MCP expose the capabilities we actually need?
4. Which actions still require custom tools, if any?
5. Are agent traces understandable enough for research analysis?
6. Are result files sufficient?
7. Are issue descriptions too easy, too difficult, or realistic enough?
8. Which failures are caused by:
   - model reasoning;
   - tool limitations;
   - Flutter environment;
   - issue wording;
   - agent configuration?
9. Is PydanticAI still sufficiently neutral and unobtrusive for the formal study?
10. What must be frozen before formal evaluation?

## Do not implement yet

Do not automatically add:

- multiple-model experiments;
- capability ablation;
- automated ground-truth evaluation;
- complex experiment definitions;
- separate benchmark framework;
- real GitHub case importers;
- multi-agent architecture;
- vector databases/RAG;
- autonomous patching/debugging.

Those decisions come only after reviewing the pilot.

## Completion criteria

Produce a short pilot review and recommendation for the next phase.

**STOP and wait for user approval.**

---

# Required End-of-Stage Report

Every stage must end with a compact report in this exact spirit:

```text
Stage: <number and name>
Status: COMPLETE / BLOCKED

Implemented:
- ...

Files changed:
- ...

Commands/tests run:
- ...

Results:
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

If the stage is blocked because the user must do something, do **not** create a completion commit or claim success. Ask for the action, wait, then finish the same stage in the same chat if practical.

# Later Research Phases — Not Part of the Initial Build

Only after the pilot is stable should the project expand toward the formal MSc research design.

Possible later work includes:

- adding real public Flutter/GitHub minimal reproductions;
- selecting and freezing the main evaluation model;
- adding independent reproduction predicates;
- repeating runs for non-determinism;
- adding capability-ablation configurations;
- comparing selected models using the same runner/tools;
- measuring false positives/false negatives in agent self-assessment;
- regression-status evaluation on current project versions.

These later phases should preserve the proposal's requirement that model/tool versions, prompt, sampling settings, and step budget are fixed and recorded during formal evaluation.

---

# Operating Rules for Claude/Codex

When executing this plan:

1. **Read `README.md` first.**
2. Work on **one stage only in the current chat/session**.
3. Follow stages in order.
4. Never start, scaffold, or pre-implement the next stage.
5. Do not redesign the repository unless the current stage proves the design insufficient.
6. Do not introduce frameworks or folders that are not needed yet.
7. Prefer existing Flutter/Dart MCP capabilities over custom Flutter automation code.
8. Use PydanticAI rather than creating a custom agent loop.
9. Keep model configuration separate from capabilities.
10. Keep only one `FULL` capability set during the pilot.
11. Keep only one local model during the initial implementation.
12. Never continue to the next stage without completing and testing the current stage.
13. If user action is required, **stop immediately** and give exact step-by-step instructions; continue only after the user confirms completion.
14. Use local Git throughout the project. Keep commits meaningful and history readable. At minimum, create a commit for every completed stage.
15. Do not automatically squash, rewrite, or clean history.
16. Before declaring a stage complete, verify the working tree is clean with `git status`.
17. At the end of every stage, report:
    - stage completed;
    - work implemented;
    - files created/changed;
    - commands run;
    - tests/runs performed;
    - test results;
    - unresolved problems, if any;
    - user action required, if any;
    - `git status`;
    - final commit hash;
    - recent Git history (`git log --oneline` for the latest relevant commits).
18. Then **stop and wait for explicit user approval**.

The priority is not to build quickly. The priority is to build one small, observable, reproducible step at a time, with a clean Git checkpoint after every completed stage.
