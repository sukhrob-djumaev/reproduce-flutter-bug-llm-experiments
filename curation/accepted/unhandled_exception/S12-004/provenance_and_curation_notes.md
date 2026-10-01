# S12-004 — curator-only record (CAND-009)

NOT agent-visible. Never expose this directory, or `curation/ground_truth/S12-004.json`, to the evaluation agent.
Accepted by the Stage 12 curation experiment only; not automatically part of the formal ~25-case dataset.

## Provenance
- Issue: https://github.com/flutter/flutter/issues/189582 (opened 2026-07-16 by davidmigloz; open, label "waiting for PR to land (fixed)" at 2026-10-01)
- MRE: inline sample in issue body, verbatim as `source/lib/main.dart`. Package: go_router 17.3.0 (reporter version, pinned in pubspec.yaml/lock).
- Issue body SHA-256: a5784b73d055e6150ec2b253e9bcb5616d86766f485cf68791988851ce70cab9 ; main.dart SHA-256: 0d782e6de4c39a43d92c8dcfe5826461684766b71ebee245baf968d77666af69 ; pubspec.lock SHA-256: 24a57dfd2b1dbe477e3a49fb5ca5733619825ea1fbe9722363731522855bf1d7
- Revision: no git history. Pinned state = Flutter 3.47.1 + go_router 17.3.0 + `source/`. Fix PR flutter/packages#12216 is draft; later go_router releases (17.4.0+, 18.x) may contain a fix — do NOT upgrade.
- Note: assertion appears at delegate.dart line 228 with 17.3.0 (issue text cites line 221, from main); same assertion text.

## Environment
Flutter 3.47.1 stable, Dart 3.13.1, macOS arm64 (reporter: Flutter 3.44.4). Android emulator AVD `Medium_Phone_API_36-ext19` (API 36), debug.
Scaffolding: `flutter create --project-name cand009 -e --platforms=android cand009`; `flutter pub add go_router:17.3.0`; replace lib/main.dart. No code edits.

## Reproduction steps (curator)
1. Run on the Android emulator (debug). No interaction.
2. Observe: screen stays black (no route ever built), and the console / logcat shows `E/flutter ... Unhandled Exception: 'package:go_router/src/delegate.dart': Failed assertion: line 228 pos 12: 'configuration.isNotEmpty || configuration.isError': is not true.` via GoRouterDelegate.setNewRoutePath <- RouterDelegate.setInitialRoutePath.
Evidence: `evidence/runtime_exception_excerpt.txt`, `evidence/blank_black_screen_after_launch.png`.

## Reset procedure
`adb shell am force-stop com.example.cand009; adb shell am start -n com.example.cand009/.MainActivity`. Verified: relaunch gave the same black screen and the same assertion in plain logcat (exception is an Unhandled Exception, visible without a tool attached).

## Independent observable predicate (hidden)
After launch with no action, the runtime records an unhandled assertion whose message contains "configuration.isNotEmpty || configuration.isError", and the screen shows no content (no widget text; SizedBox pages are intentionally empty, so the absence of any error-recovery navigation cannot be told from the screen alone).
Evaluation: runtime-error observation or logcat contains the assertion message at startup. The visible state alone is NOT sufficient (both /protected and /fallback render empty SizedBox).

## Difficulty metadata
UI actions: 0. Navigation: none. Text entry/scroll: none. Runtime-error dependence: required (screen blank both when buggy and when fixed/fallback). Widget inspection: not useful (both pages empty). Source inspection: supportive. Instrumentation: not useful. Asynchrony: none. Setup: standard. Reset: restart only. Proposed label: low action, but evidence-dependent: high reliance on get_runtime_errors.

## Leakage review
Issue body contains: exact assertion text (= predicate; exclude), full root-cause explanation (parserExceptionHandler returns routerDelegate.currentConfiguration; fix PR described in two parts) — exclude entirely, Steps text ("onEnter returns Block.stop() ... provide onException") is itself technical and describes the construct; user-level rewrite required ("app crashes on startup when the initial location is blocked and an error handler is provided"). Comments: fix PR flutter/packages#12216, related #189581 — exclude. Source: the MRE source is tiny and shows the exact configuration that triggers the crash (inherent).

## potential_capability_gap
None (launch only); requires get_runtime_errors to observe primary evidence.
