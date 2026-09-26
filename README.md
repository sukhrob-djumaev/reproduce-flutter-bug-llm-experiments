# Flutter Bug Reproduction Agent

## Project Overview

This project is an experimental research environment for studying whether an LLM-based agent can reproduce reported bugs in running Flutter applications.

The research focus is intentionally narrow:

- give an agent a natural-language bug report;
- let it interact with a running Flutter application;
- let it inspect the runtime through available Flutter/Dart tooling;
- ask it to determine whether the reported bug can be reproduced;
- record what it did, how long it took, and what result it reported.

The project is **not** intended to become a full coding assistant, autonomous debugger, patch generator, or root-cause analysis system. Its first purpose is to provide a controlled environment for the MSc research project on automated Flutter bug reproduction.

The research proposal defines three broader questions:

1. Can an LLM agent reproduce Flutter defects from natural-language issue reports and correctly judge whether reproduction succeeded?
2. Which runtime capabilities materially contribute to reproduction performance?
3. Can the evaluated system later determine whether a previously reported defect still persists?

This repository begins with the first goal and keeps the architecture simple enough to support later capability and model comparisons.

---

## Design Principles

The repository should remain deliberately small and transparent.

### 1. One Flutter pilot project

The initial Flutter environment is a single Flutter application containing several independent bug cases. Each case has its own entry point.

Example:

```bash
flutter run -t lib/main_case_001.dart
flutter run -t lib/main_case_002.dart
```

This makes it fast to create, run, and reset controlled cases without maintaining many separate repositories.

Later, real GitHub minimal reproducible examples may be added as separate projects if needed. They do not need to be forced into this pilot application.

### 2. One issue file per case

Each bug case has a matching Markdown issue description.

The issue file represents what the agent is allowed to know about the reported problem.

Example mapping:

```text
issues/case_001.md
        ↕
flutter_app/lib/main_case_001.dart
```

The agent should receive the issue description, not a hidden explanation of where the bug is implemented.

### 3. Thin agent layer

The project does not implement a general-purpose agent framework.

It uses the **OpenAI Agents SDK** as the orchestration layer. The SDK is installed as a Python dependency and handles the agent loop, model interaction, and tool execution.

Our code should mainly configure:

- the model;
- instructions;
- available capabilities/tools;
- the Flutter/Dart MCP connection;
- result collection.

### 4. Models and capabilities stay separate

The model is one experimental choice.

Examples:

- local model through LM Studio;
- another local model later;
- cloud model later.

Capabilities are a separate choice.

For the first implementation, there is only one capability set:

```text
FULL
```

It should expose all available functionality needed for bug reproduction.

Later, capability ablation can remove one capability at a time without changing the model implementation.

### 5. Prefer existing Flutter/Dart MCP tools

Do not reimplement Flutter UI interaction if the Flutter/Dart MCP server already exposes the required operation.

The agent should preferably use MCP-provided tools for actions such as:

- inspecting the running Flutter app;
- inspecting the widget tree;
- interacting with UI elements;
- entering text;
- scrolling;
- hot reload/restart;
- runtime inspection where supported.

Only create custom Python tools when the MCP server cannot provide the required capability.

### 6. Results are always recorded

Each execution should create a new result record. Do not overwrite previous runs.

At minimum, record:

- case ID;
- model used;
- reported result;
- number of steps/turns if available;
- duration;
- trace/tool activity where practical;
- Flutter logs where practical;
- screenshot/evidence where practical.

A simple `summary.csv` should provide an overview of all runs.

---

## Development Workflow and Git Discipline

This project must be developed in **strict phases**. One Claude/Codex chat/session should work on **one phase only**. A phase is not complete until its implementation is finished, its tests have passed, the result has been reviewed, and the user has explicitly approved moving forward.

If a phase needs manual user action — for example installing or opening LM Studio, downloading a model, starting a simulator/emulator, approving permissions, configuring MCP, or confirming behavior visually — the agent must stop and ask the user to do that exact action. It must not guess, skip the check, or silently continue.

The repository must use **local Git from the beginning**. Phase 1 initializes the repository, creates a suitable `.gitignore`, and establishes a clean baseline. Development should preserve a readable history:

- use meaningful commit messages;
- create at least one commit at each completed phase boundary;
- optional intermediate commits are allowed when they represent meaningful working checkpoints;
- do not commit generated caches, build products, virtual environments, local model files, simulator data, or noisy run artifacts unless intentionally required;
- do not rewrite or squash history automatically;
- before declaring a phase complete, run `git status` and verify the working tree is clean;
- include the final commit hash and recent Git history in the phase report.

Every phase finishes with a short report containing:

- what was implemented;
- files created or changed;
- commands executed;
- tests/runs performed and their results;
- any unresolved issue;
- any user action still required;
- Git status, final commit hash, and recent history.

Only after the user approves the report should a new chat/session begin the next phase.

## Initial Repository Structure

```text
flutter-bug-reproduction/
│
├── README.md
├── plan.md
│
├── flutter_app/
│   ├── lib/
│   │   ├── cases/
│   │   │   ├── case_001/
│   │   │   ├── case_002/
│   │   │   ├── case_003/
│   │   │   ├── case_004/
│   │   │   └── case_005/
│   │   │
│   │   ├── main_case_001.dart
│   │   ├── main_case_002.dart
│   │   ├── main_case_003.dart
│   │   ├── main_case_004.dart
│   │   └── main_case_005.dart
│   │
│   └── pubspec.yaml
│
├── issues/
│   ├── case_001.md
│   ├── case_002.md
│   ├── case_003.md
│   ├── case_004.md
│   └── case_005.md
│
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

This structure is intentionally small. New folders should be added only when an actual need appears.

---

## Initial Flutter Cases

Start with approximately five synthetic cases covering different bug behavior.

Suggested first set:

### CASE 001 — State update failure

Example behavior:

- user presses `+`;
- counter is expected to increase;
- displayed value remains unchanged.

Purpose:

- simplest possible interaction;
- validates tool calling and UI observation.

### CASE 002 — Runtime exception

Example behavior:

- user opens a form;
- submits invalid/empty input;
- application throws an unhandled runtime exception.

Purpose:

- validates runtime-error observation.

### CASE 003 — Navigation/flow bug

Example behavior:

- user navigates through several screens;
- one action takes the user to the wrong destination or incorrect state.

Purpose:

- requires a multi-step reproduction flow.

### CASE 004 — Structural UI bug

Example behavior:

- a widget is missing, duplicated, or incorrectly configured after an action.

Purpose:

- validates widget-tree inspection.

### CASE 005 — Silent async/runtime problem

Example behavior:

- an asynchronous operation fails;
- application does not crash;
- runtime output or state reveals the failure.

Purpose:

- validates non-crash runtime investigation.

These cases are for development and pilot testing. They are not automatically the final research dataset.

---

## Issue Files

Each case should have a simple natural-language issue description.

Example `issues/case_001.md`:

```markdown
# Counter does not update

When the user presses the + button, the displayed counter remains at 0.

Expected:
The displayed value should increase.

Actual:
The displayed value remains unchanged.
```

The issue should describe the reported behavior but should not reveal implementation details such as the faulty file or line number.

---

## Agent Layer

The agent layer should remain small.

### `main.py`

Responsibilities:

- accept/select the case;
- load the corresponding issue;
- choose the model;
- connect the agent to the full capability set;
- run the agent;
- save the result.

Target usage can eventually look like:

```bash
python agent/main.py --case 001 --model local
```

### `models.py`

Contains model/provider configuration.

Initially, support one local model through LM Studio's OpenAI-compatible endpoint.

Later, additional local or cloud providers may be added without changing the Flutter cases or agent instructions.

### `capabilities.py`

Initially expose only:

```text
FULL
```

`FULL` represents all currently available tools/capabilities.

Do not implement ablation conditions yet.

### `tools.py`

Responsibilities:

- configure/connect to Flutter/Dart MCP;
- expose MCP tools to the agent through the Agents SDK;
- contain only small custom tools that are genuinely missing from MCP.

Do not create Python wrappers for every Flutter action if MCP already supports them.

---

## OpenAI Agents SDK

The OpenAI Agents SDK is a Python dependency, not a repository module that needs to be copied into the project.

It should be installed into the project's Python virtual environment and imported by the code under `agent/`.

Its role is to provide:

- the agent execution loop;
- tool invocation;
- model interaction;
- result handling/tracing where available.

The repository should use the SDK rather than implementing a custom reasoning loop.

---

## Local Model Setup

The first implementation should use LM Studio as the local inference server.

The architecture is:

```text
Python agent
    ↓
OpenAI Agents SDK
    ↓
LM Studio OpenAI-compatible endpoint
    ↓
Local model
```

Model configuration should be isolated in `agent/models.py` so it can later be replaced without changing the rest of the system.

Exact model selection should remain configurable rather than hardcoded into the project architecture.

---

## Flutter Tooling

Preferred architecture:

```text
LLM
 ↓
OpenAI Agents SDK
 ↓
Flutter/Dart MCP tools
 ↓
Running Flutter app
```

If the MCP server provides a required operation, use it directly.

If something required for the research is missing, add a small custom tool only for that missing operation.

Potential capabilities needed by the research include:

- UI interaction;
- widget-tree/runtime inspection;
- runtime error capture;
- source inspection;
- temporary instrumentation and hot reload.

The first implementation does not have to provide every final research capability. It only needs enough functionality to prove the end-to-end loop.

---

## Results

Keep results simple.

Suggested structure:

```text
results/
├── runs/
│   ├── <run-id>/
│   │   ├── result.json
│   │   ├── trace.txt
│   │   ├── flutter.log
│   │   └── screenshot.png
│   └── ...
│
└── summary.csv
```

Not every file has to exist in the earliest prototype. Add evidence files as the corresponding capability becomes available.

Example `result.json`:

```json
{
  "case": "001",
  "model": "local",
  "capabilities": "full",
  "status": "reproduced",
  "steps": 8,
  "duration_seconds": 61
}
```

Example `summary.csv`:

```csv
case,model,capabilities,status,steps,duration_seconds
001,local,full,reproduced,8,61
```

---

## Development Strategy

Do not attempt to build the final research platform at once.

Development should progress through small verified stages:

1. create the repository and environment;
2. make the Flutter pilot application run;
3. verify multiple case entry points;
4. make a local model respond through LM Studio;
5. make the Agents SDK call one simple tool;
6. connect the agent to Flutter/Dart MCP;
7. let the agent inspect/interact with the Flutter app;
8. let the agent attempt one bug reproduction;
9. record the result;
10. repeat for several cases;
11. only then expand toward real GitHub issues and formal experiments.

Each stage must be tested before continuing.

See `plan.md` for the execution plan.

---

## Current Scope

For the first implementation, success means:

> A local LLM receives a Flutter bug report, uses an existing agent framework and Flutter runtime tools to interact with the corresponding running test case, reports whether it reproduced the issue, and the system stores the run result.

Anything beyond that is secondary until this end-to-end loop works reliably.
