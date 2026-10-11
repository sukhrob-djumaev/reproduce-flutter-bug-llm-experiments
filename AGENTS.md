# Local development workflow

This contract is for the lead Claude Code/Codex **development** agent. It does not change the Flutter reproduction agent, its prompt, tools, or research design. Work directly by default; keep the operating layer to Markdown and Git.

## Authority

Use this order for project truth:

1. `docs/stage_10_formal_evaluation_protocol.md` — formal research protocol.
2. `plan.md` — execution stages, scope, checks, and stop conditions.
3. `README.md` — architecture and status overview.
4. Git — durable implementation and stage history.
5. `.agent/CURRENT.md` and `.agent/HANDOFF.md` — operational continuation state.
6. Chat history — disposable convenience.

This file implements that hierarchy; it cannot amend the protocol or stage plan. Reconcile stale status text with committed artifacts, without treating implementation history as permission to change methodology. Correct stale `.agent` state from repository evidence. If a substantive conflict remains, stop and identify it.

## Fresh session / `continue`

`continue` and `continue current research stage` resume only the current approved scope. They do not authorize the next stage, repeat completed work, or clear a pending approval. An explicit instruction such as `Start Stage 14 according to plan.md` authorizes that stage within its existing boundaries; record its scope and date so future sessions can resume it.

1. Read this file, `.agent/CURRENT.md`, and the latest `.agent/HANDOFF.md`.
2. Read the relevant `plan.md` stage and README status. Read the formal protocol whenever work touches model selection, curation, capabilities, scoring, formal experiments, ground truth, or freeze policy.
3. Inspect Git before edits or execution:

   ```sh
   git status --short --untracked-files=all
   git branch --show-current
   git rev-parse HEAD
   git log -8 --oneline
   ```

4. Compare the recorded checkpoint with live Git, relevant code, and cited evidence. Inspect diffs for existing work. If state files are absent/stale, determine corrections from those sources, but defer writes until the prerequisite check below. Do not assume the highest numbered plan entry is active. Distinguish completed work, an approved active stage, and a merely proposed next stage. Never infer approval from a clean tree alone.
5. Check stage prerequisites. If a clean baseline is required and unrelated dirty files exist, **stop after a read-only audit**, list the paths and required reconciliation, and make no edits (including state files), commits, stashes, or resets. Resume approved same-stage work only where the stage's gate permits it; never call a dirty tree clean.
6. Briefly state the active task, allowed work, evidence, and next boundary. After prerequisites pass, record any new approval with the verified entry checkpoint and continue within scope without requesting earlier prompts. If approval is missing or a required external action blocks progress, request only the exact decision/action.
7. Verify the work and finish the session as below. Stop at the stage boundary.

## Scope and research boundaries

- Code changes require an approved engineering/implementation scope. Inspect code, callers, history, and tests before choosing the smallest justified change. Documentation maintenance does not authorize agent changes or trials.
- Curation requires an approved curation stage. Follow `curation/README.md`, the intake checklist, and stage stop conditions; preserve inspected/rejected/deferred records. Do not invoke or modify the reproduction agent or compare models while curating.
- Model selection follows protocol §9 and plan Stage 14: separate calibration from formal cases; fix cases/revisions, prompt, tools, sampling, budgets, and environment across candidates; retain repeated trials and traces. No per-model/per-case tuning, new curation, unrelated capabilities, or formal RQ1/RQ2 trials. Record model choice transparently and distinguish infrastructure failures from model outcomes.
- Capability implementation must remain generic; do not alter ground truth or add case-specific selectors, retries, prompts, or hints to repair model results.
- Formal evaluation requires the approved stage and complete freeze. No silent changes to frozen prompt/model/tools/environment/dataset/predicates/settings; protocol amendments need user approval, a new experiment version, and separate reporting.
- At every completed stage, **STOP for explicit approval before the next stage**. Ordinary choices within already approved scope do not need renewed permission.
- Also stop for methodology changes, finalized formal dataset membership, formal model approval, candidate-set changes, significant model additions/downloads, paid APIs/credentials, destructive actions, required manual/device/access setup, or a critical unresolved ambiguity. State what is needed and why. Do not put credentials in chat, tracked files, or handoffs.

## Curator / evaluation separation

The development lead may inspect curator material when its task requires it. The evaluation agent may receive only the approved issue snapshot, generic prompt, and permitted tools. Never send it hidden predicates, expected evidence, curator notes, fixes/PRs, source-level diagnoses, or scoring outcomes.

Keep all `curation/` material, these workflow files, `.agent/`, and development conversation/review context out of evaluation prompts, tool output, result records, and future source-inspection allowlists. Any approved case-source exposure must be separately bounded and leakage-reviewed. Store only operational facts and evidence paths in `.agent`, not hidden answers. Do not reuse a curator-informed conversation as an evaluation trial.

## Verification and evidence

Use the strongest checks applicable to the approved change, and report their limits:

- Engineering: existing Python tests (`.venv/bin/python -m unittest discover -s tests -v`), schema checks, Flutter analysis where relevant, and actual runtime/tool-trace evidence for runtime changes. Check prerequisites; do not download/install or invoke a model just to verify docs.
- Curation: pinned provenance, manual reproduction, reset verification, independent predicate, and retained evidence.
- Model selection: executable tool calls, schema-valid output, natural termination, repeated trials, independent scoring, and trace retention under the fixed configuration.
- Formal evaluation: frozen configuration, independently scoreable evidence, complete metadata, and no hidden post-hoc repairs.
- Workflow/docs: check links, status against Git/artifacts, diff scope, and the fresh-session, dirty-tree, leakage, fixed-calibration, stage-stop, and external-blocker scenarios. A walkthrough is not an executed Claude/Codex session test.

A compile, launch, tap acknowledgement, model claim, or promising issue is insufficient proof of reproduction. Report infrastructure success, independent reproduction success, and self-assessment correctness separately. Preserve the actual result and raw `result.all_messages()` serialization; never correct the model's answer in storage.

Existing persistence is in `agent/results.py`: unique `results/runs/<run-id>/` directories contain `result.json`, `trace.json`, and optional `tool_events.json` / `formal_metadata.json`; `results/summary.csv` is append-only. Run contents are Git-ignored local evidence: verify referenced artifacts exist, and explicitly report missing ones on a fresh clone. Do not overwrite earlier runs, copy curator material into them, or invent a new persistence system for this workflow.

## Focused delegation

The lead owns context, implementation, integration, Git, final verification, state, and communication. Use a native subagent only for independent investigation/review that materially helps (for example, leakage, methodology consistency, code review, or isolated MCP/model compatibility debugging). Give it only the objective, constraints, relevant files, and expected deliverable. Keep evaluation context free of curator knowledge. Do not delegate trivial/sequential steps, create role chains, or add research-agent coordination. Integrate findings and finish or stop all subagents before ending the session.

## Session finish

1. Review `git status`, the full intended diff, relevant checks, and evidence. Exclude unrelated work, generated noise, and secrets; stage explicit paths only.
2. Update `.agent/CURRENT.md` with stage/status, bounded objective and approval scope, branch, verified checkpoint, evidence paths, next actions, blockers, and prohibitions. Keep plan/README status consistent when it changes, without rewriting stage criteria. Do not create a second plan or record an anticipated approval as granted.
3. Rewrite/compact `.agent/HANDOFF.md` to the latest substantial session: changes, findings, checks actually run, commits, unresolved issues, exact continuation point, and required user action. Record skipped checks honestly. Respect a read-only dirty-tree stop above.
4. Create coherent local commits when the stage permits; never mix stages. A blocked stage gets no completion claim/commit. Never rewrite/squash history, discard user changes, or push without explicit authorization.
5. Verify the resulting HEAD, recent history, and worktree. A completed stage requires a clean tree under `plan.md`. Report active/blocked/complete, checks and limitations, commit hashes, and the next boundary.

Record the verified pre-session or research checkpoint explicitly. For the commit containing a state update, use `git log -1 --format='%H %s' -- .agent/HANDOFF.md`; do not chase a self-referential commit hash by making endless state commits. Always read live HEAD/status at the next session. Durable approval scope, evidence paths, and Git history must suffice without the prior chat.
