# Public-case intake checklist

Use one copy of this checklist per candidate before creating a hidden ground-truth record. This is preparation only: do not add a public case, run an agent, score a trial, or choose a model during Stage 11.

## Candidate identity

- [ ] Public repository URL and license recorded.
- [ ] Public issue/reference URL recorded and issue wording snapshot saved separately from curator notes.
- [ ] Immutable repository revision, entry point, dependency lock/hash, Flutter/Dart version, platform, and build-tool versions recorded.
- [ ] Candidate is not a duplicate project state or underlying defect already selected.

## Feasibility and reset

- [ ] The pinned revision builds and launches in the intended evaluation environment.
- [ ] Required setup uses no hidden credentials, proprietary service, paid account, hardware, sensor, push service, or uncontrolled remote content.
- [ ] The case can be reset to a known initial state between trials; exact reset steps are recorded.
- [ ] Network, timing, asynchronous behavior, and third-party dependencies are sufficiently controlled for repeatable observation.

## Independent predicate

- [ ] A curator has manually reproduced the reported behavior on the pinned revision.
- [ ] A binary, externally observable reproduction predicate is written without source locations, patch knowledge, or a proposed fix.
- [ ] Required UI, runtime, widget, log, or other evidence is listed for independent scoring.
- [ ] One top-level class is selected: `unhandled_exception`, `incorrect_application_state`, `structural_rendering_fault`, or `silent_error_condition`.
- [ ] A subtype and observable difficulty factors are recorded.
- [ ] The proposed hidden record is stored only in `curation/ground_truth/`, not in an issue, prompt, result directory, or tool response.

## Leakage and exclusion review

- [ ] Agent-visible issue text excludes patches, exact source locations, curator explanations, workarounds, and hidden predicate details where separable.
- [ ] The candidate is excluded or deferred if the report cannot be separated from such leakage.
- [ ] The candidate is excluded or deferred if its predicate is subjective or cannot be independently observed.
- [ ] The candidate is excluded or deferred if the source/revision is not public, reproducible, lawful, or buildable in the target environment.

## Handoff status

- [ ] Intake accepted for later manual verification.
- [ ] Intake deferred (record reason):
- [ ] Intake excluded (record reason):

No intake status authorizes an agent trial. Curation and manual verification require a separately approved stage.
