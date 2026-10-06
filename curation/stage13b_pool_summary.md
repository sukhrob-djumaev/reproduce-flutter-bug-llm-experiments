# Stage 13B combined pool summary (Stage 12 + 13 + 13B)

Curator-only planning evidence. Not a dataset freeze: no calibration/formal split has been made. "Accepted" = accepted into the curated candidate pool only. Date: 2026-10-02. Environment for all cases: Flutter 3.47.1 / Dart 3.13.1, Android emulator API 36 (1080x2400, 420 dpi).

## Funnel
- Attempted 21 (Stage 12: 9, Stage 13: 7, Stage 13B: 5). Accepted 13, rejected 7, deferred 1. Acceptance 13/21 = 62%. Stage 13B alone: 3/5.
- Rejection/defer reasons: cannot_reproduce 4 (CAND-001/002/003/019), subjective_predicate 1 (006), environment_mismatch 1 (015), external_service_required 1 (017, account login), major_reconstruction_required 1 deferred (005).

## Stage 13B outcome
| Candidate | Case | Repo (owner) | Class | Type | Result |
|---|---|---|---|---|---|
| CAND-017 | - | openfoodfacts/smooth-app (openfoodfacts) | silent_error_condition | small_app | rejected: external_service_required (editing nutrition needs an account) |
| CAND-018 | S13B-001 | LahaLuhem/list_smith (LahaLuhem) | incorrect_application_state | mre_inline (package) | accepted (provisional: timing + drag) |
| CAND-019 | - | juliansteenbakker/flutter_secure_storage | silent_error_condition | plugin harness | rejected: cannot_reproduce (no biometric prompt appears on API 36 emulator) |
| CAND-020 | S13B-002 | bdlukaa/fluent_ui (bdlukaa) | incorrect_application_state | mre_inline (package) | accepted |
| CAND-021 | S13B-003 | imaNNeo/fl_chart (imaNNeo) | unhandled_exception | mre_inline (package) | accepted |

## Combined accepted pool (13)
| Case | Class | Type | Code under test |
|---|---|---|---|
| S12-001 | unhandled_exception | mre_inline | flutter/flutter framework |
| S12-002 | incorrect_application_state | mre_inline (package) | flutter/packages go_router |
| S12-003 | unhandled_exception | mre_inline | flutter/flutter framework |
| S12-004 | unhandled_exception | mre_inline (package) | flutter/packages go_router |
| S13-001 | incorrect_application_state | mre_inline | flutter/flutter framework |
| S13-002 | incorrect_application_state | mre_inline (package) | flutter/packages two_dimensional_scrollables |
| S13-003 | incorrect_application_state | mre_inline (from widget test, package) | flutter/packages go_router |
| S13-004 | structural_rendering_fault | mre_inline | flutter/flutter Material |
| S13-005 | unhandled_exception | small_app (SDK dev app) | flutter/flutter dev/a11y_assessments |
| S13-006 | structural_rendering_fault | mre_inline | flutter/flutter Material (release build) |
| S13B-001 | incorrect_application_state | mre_inline (package) | LahaLuhem/list_smith |
| S13B-002 | incorrect_application_state | mre_inline (package) | bdlukaa/fluent_ui |
| S13B-003 | unhandled_exception | mre_inline (package) | imaNNeo/fl_chart |

- Class distribution: unhandled_exception 5, incorrect_application_state 6, structural_rendering_fault 2, silent_error_condition 0.
- Type distribution: mre_inline 12 (7 of them package-based), small_app 1, mre_repo 0, plugin_example 0.
- Unique GitHub owners 4 (flutter, LahaLuhem, bdlukaa, imaNNeo). Issue-tracker repositories 4 (flutter/flutter 10 cases, list_smith, fluent_ui, fl_chart). Code repositories 5 (flutter/flutter, flutter/packages, list_smith, fluent_ui, fl_chart). flutter/flutter still holds 10 of 13 cases (Stage 10 guideline: at most 3 per repository for the formal core).
- Recent open (created 2026-05 or later) attempted 18, accepted 13; older/stale attempted 3, accepted 0.

## Capability requirements across the 13 accepted cases (nothing implemented)
| Requirement | Cases |
|---|---|
| launch only | S12-001, S12-004, S13B-003 |
| tap(s) | S12-002, S12-003, S13-002, S13-003, S13-004, S13-005, S13-006, S13B-002 |
| system Back key | S13-003 |
| edge-swipe back gesture | S12-002 |
| hardware directional key | S13-001 |
| drag / pull gesture | S13B-001 |
| wait/polling (bounded window) | S13B-001 (required), S13-004 (minor) |
| text entry, long press, required scrolling | none |
| runtime-error observation | required: S12-001, S12-003, S12-004; supportive/visible alternative: S13-005, S13B-003 |
| visible-text / widget inspection | S12-002, S12-003, S13-001..006, S13B-001..003 |
| geometry inspection | S13-004 |
| lifecycle/foreground observation | S13-003 |
| release build | S13-006 |
| source inspection / instrumentation | not required by any |

## Indicative suitability (NOT a split)
- Calibration-suitable with current/near-term tools (launch/tap, clear UI or runtime predicate): S12-001, S12-003, S12-004, S13-002, S13-005, S13B-002, S13B-003 (7).
- Formal-dataset candidates that need a new generic input first: S12-002 (edge swipe), S13-001 (D-pad), S13-003 (Back + lifecycle check) (3).
- Provisional/uncertain: S13-004 (geometric threshold, display-profile dependent), S13-006 (release build), S13B-001 (timing window + drag, partly contested expectation) (3).

## Assessment
1. Source diversity improved modestly: 3 new independent owners/repos, all package repos with inline MREs; no accepted real standalone app and no accepted plugin-native case.
2. No convincing silent_error_condition accepted. The two strongest silent candidates were blocked: smooth-app (account required) and flutter_secure_storage (prompt never shown on the emulator).
3. Pool is large enough to pause curation for model-selection calibration (7 clean cases across 3 classes); it is not yet diverse enough for the formal ~25-case set (silent 0, structural thin, 10/13 from one tracker).
4. Recurring capabilities: tap (8) and launch-only (3) dominate; system back/edge swipe (2), hardware key (1), drag (1) and bounded wait (2) are one-to-two-case needs; runtime-error observation matters for 3 cases.
5. Should stay provisional: S13-004, S13-006, S13B-001.
6. Clearly unsuitable for the model-selection pre-study as-is: S13-006 (release build, VM-service tools unavailable).
