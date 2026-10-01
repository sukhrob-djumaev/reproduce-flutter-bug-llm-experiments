# Stage 13 combined curation pool summary (Stage 12 + Stage 13)

Curator-only planning evidence. Not a dataset freeze: no calibration/formal split has been made, and "accepted" means accepted into the curated candidate pool only. Date: 2026-10-01. Environment for all cases: Flutter 3.47.1 / Dart 3.13.1, Android emulator API 36 (1080x2400, 420 dpi).

## Funnel
- Attempted: 16 (Stage 12: 9, Stage 13: 7). Accepted 10, rejected 5, deferred 1. Acceptance 10/16 = 62.5% (Stage 13 alone 6/7).
- Rejected/deferred reasons: cannot_reproduce 3 (CAND-001/002/003), subjective_predicate 1 (CAND-006), environment_mismatch 1 (CAND-015), major_reconstruction_required 1 deferred (CAND-005, test-only repro).
- Recent open issues (created 2026-05 or later) attempted 13, accepted 10; older/closed or stale issues attempted 3, accepted 0.

## Accepted cases
| Case | Candidate | Class | Type | Component |
|---|---|---|---|---|
| S12-001 | CAND-004 | unhandled_exception | mre_inline | framework (SliverCrossAxisGroup) |
| S12-002 | CAND-007 | incorrect_application_state | mre_inline (package) | go_router 17.3.0 |
| S12-003 | CAND-008 | unhandled_exception | mre_inline | framework (OverlayPortal/DropdownMenu) |
| S12-004 | CAND-009 | unhandled_exception | mre_inline (package) | go_router 17.3.0 |
| S13-001 | CAND-010 | incorrect_application_state | mre_inline | framework (focus traversal) |
| S13-002 | CAND-011 | incorrect_application_state | mre_inline (package) | two_dimensional_scrollables 0.5.2 |
| S13-003 | CAND-012 | incorrect_application_state | mre_inline derived from widget test (package) | go_router 17.5.0 |
| S13-004 | CAND-013 | structural_rendering_fault | mre_inline | Material 3 date picker |
| S13-005 | CAND-014 | unhandled_exception | small_app (SDK dev/a11y_assessments) | framework/MaterialBanner |
| S13-006 | CAND-016 | structural_rendering_fault | mre_inline | AlertDialog (release build only) |

- Class distribution: unhandled_exception 4, incorrect_application_state 4, structural_rendering_fault 2, silent_error_condition 0.
- Type distribution: inline MRE 9 (of which 4 are package-based: go_router x3, two_dimensional_scrollables x1), small app 1, linked MRE repository 0 accepted (the one tried, CAND-002, did not reproduce), plugin-specific 0 accepted (CAND-015 rejected).
- Source diversity weakness: every case comes from the single flutter/flutter issue tracker (components differ, owners/codebases do not). The Stage 10 target of several independent owners/codebases is NOT yet met.

## Capability requirements observed (planning evidence for Stage 15; nothing implemented)
| Requirement | Accepted cases needing it as part of the reproduction/predicate |
|---|---|
| launch/observe only (no action) | S12-001, S12-004 |
| tap(s) | S12-002, S12-003, S13-002, S13-003, S13-004, S13-005, S13-006 (7) |
| system Back key | S13-003 |
| system edge-swipe back gesture | S12-002 |
| hardware directional key (D-pad) | S13-001 |
| text entry, long press, drag, required scrolling | 0 accepted (CAND-001 would need long-press+drag; CAND-005 drag-scroll) |
| optional scrolling (control only) | S13-002 |
| wait/polling (slow render) | S13-004 (minor) |
| runtime-error observation (primary evidence) | S12-001, S12-003, S12-004 (required); S13-005 (supportive) |
| widget/visible-text/geometry inspection | S12-002, S12-003, S13-001..006 (S13-004 needs sizes) |
| app-lifecycle / foreground-activity observation | S13-003 |
| release-mode build (VM-service tools unavailable) | S13-006 |
| source inspection | not required by any; supportive for several |
| temporary instrumentation | not required by any |

## Indicative suitability (NOT a split)
- Cleaner candidates for a calibration pool or the formal set under current/near-term tools: S12-001, S12-003, S12-004 (runtime errors), S13-002 (tap + inspection). 
- Clean but need a new generic input: S12-002 (edge-swipe back), S13-001 (D-pad keys), S13-003 (Back key + lifecycle check).
- Uncertain: S13-004 (geometric threshold, display-profile dependent), S13-005 (hidden app filter step not in the issue; exception text), S13-006 (needs release build; VM-service tools do not work).
- Gaps: no silent_error_condition case; only 2 structural cases, both uncertain; all cases from one repository tracker; heavy reliance on runtime errors in the exception class.
