# Curator-owned material

This directory is not an agent input or result surface. The running agent receives an issue file and model-facing runtime tools only; it must never load, enumerate, or receive content from `curation/ground_truth/`.

`ground_truth/` holds independent predicate records and must remain excluded from any future source-inspection allowlist. `public_case_intake_checklist.md` is a manual preparation aid only. No public case has been added or curated in Stage 11.

## Stage 12 curation experiment (2026-10-01)

- `search_state.csv`: append-only memory of every substantively inspected issue, comment permalink, and MRE; the `*_final` rows record each issue's final outcome. Check it before inspecting anything.
- `candidates.csv`: ledger of every attempted candidate (accepted, rejected, deferred), never deleted.
- `accepted/<defect_class>/<case_id>/`: curator-only case material (provenance, pinned source, evidence, leakage review). Ground-truth records for these cases are in `ground_truth/S12-*.json`. Both are hidden from the evaluation agent.
- Accepted here = accepted by the curation experiment only; none is automatically part of the formal ~25-case dataset, and no agent-visible issue snapshot has been finalized.

## Stage 13 (2026-10-01)

- Pool is now 10 accepted cases (S12-001..004, S13-001..006); see `stage13_pool_summary.md` for the combined funnel, class/type distribution, capability requirements, and indicative suitability. No calibration/formal split has been made.
- `candidates.csv` / `search_state.csv` line endings were normalized to LF in Stage 13 (content of all earlier rows unchanged).
- Case IDs: `S12-*` from Stage 12, `S13-*` from Stage 13; candidate IDs `CAND-001..016`.
