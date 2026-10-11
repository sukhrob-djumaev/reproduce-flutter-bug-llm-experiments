# Current operational state

Updated: 2026-10-11. Operational state only; the formal protocol and `plan.md` govern.

- **Current research stage:** Stage 14 — Model-Selection Pre-Study (next stage).
- **Stage status:** NOT STARTED / BLOCKED on explicit start approval. Stage 13B is the last completed curation batch; there is no active approved research execution.
- **Current objective:** Await the Stage 14 start decision; the documentation-only continuation workflow is complete. Preserve the Stage 13B → Stage 14 boundary.
- **Branch:** `main` at inspection; check live branch on resume.
- **Verified research / pre-session HEAD:** `a58cf58d84ca49d2a4286c3301599bd67c2ad99e` — `stage 13b: improve curated case diversity`.
- **Workflow checkpoint:** commit containing this state/handoff; resolve with `git log -1 --format='%H %s' -- .agent/HANDOFF.md`. Read live HEAD/status, not an assumed self-hash.
- **Approved scope:** User request of 2026-10-11 authorizes the small Markdown workflow, status reconciliation, verification, and local commits only. It explicitly forbids starting the next research stage, model-selection trials, formal evaluation, or pushing.

## Completed evidence

- Engineering pilot, Stage 10 protocol, and Stage 11 contracts are committed (`7fa9e22`, `ab40aea`, `478d32c`). `agent/main.py` still supports synthetic cases `001`–`005` only; `requirements.txt` pins PydanticAI 2.51.0 and `agent/models.py` retains the development baseline, not a selected formal model.
- Stage 12/13/13B curation batches are committed (`b504bdd`, `3e64ebb`, `a58cf58`). `curation/README.md`, `curation/candidates.csv`, and `curation/stage13b_pool_summary.md` record 21 attempted / 13 accepted / 7 rejected / 1 deferred. Accepted means candidate-pool membership only.
- The Stage 13B summary lists seven indicative calibration candidates; it explicitly says **no calibration/formal split**. No candidate-model manifest, pre-study runner/report, selected formal model, or formal freeze is recorded in this checkout.
- The initial worktree was clean. Stage 13B is committed, so uncommitted curation is not the current blocker. Session verification is recorded in `HANDOFF.md`.

## Immediate next actions

1. On `continue`, read the workflow/state, Stage 14 in `plan.md`, protocol §9/§12, and live Git. Reconcile any intervening work; do not restart curation from old Stage 12 prose.
2. If no new approval is supplied, report this boundary and request: `Start Stage 14 according to plan.md`. A bare `continue` does not supply that approval.
3. After explicit approval, first inspect Stage 14's entry baseline read-only. If clean, record the approval and verified checkpoint here and update plan/README status before continuing within scope. Use the curator pool summary to prepare the bounded setup; indicative suitability is not an approved split or a completed trial. Follow stage gates before execution or external access.

## Blockers / user actions

- Required now: explicit Stage 14 start approval. No model/service/device availability was tested in this workflow session.
- Stage 14 must resolve candidate models, calibration membership, fixed configuration, leakage-reviewed issue inputs, and execution support before trials. The current synthetic runner is not public-case calibration infrastructure. Request exact downloads, credentials, paid access, or manual setup only if actually required by approved work.

## Prohibited next actions

No automatic Stage 14 start, trials, new curation, agent/prompt/tool changes, capability implementation, dataset freeze, formal RQ1/RQ2 runs, model downloads/provider spending, or push as part of this workflow task. Curator content and workflow/development context must remain outside evaluation-agent inputs and results.
