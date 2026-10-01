# S13-005 — curator-only record (CAND-014)

NOT agent-visible. Never expose this directory, or `curation/ground_truth/S13-005.json`, to the evaluation agent.
Accepted into the curated candidate pool by Stage 13 only; NOT yet selected for calibration or the final formal dataset.

## Provenance
- Issue: https://github.com/flutter/flutter/issues/193226 (opened 2026-09-23; open)
- Case type: small_app (SDK dev app: flutter/dev/a11y_assessments, no inline MRE)
- Issue body SHA-256: 17073f972ff4269ab9af51ac3f89345d253c71be4c5cf5701b559940d1684b65
- main.dart SHA-256: 89287fd35a1f22201f579ee2b2c04d1b202ec98cad7c73e75913dad9b0dc8e79 ; pubspec.lock SHA-256: 7c7f4e3ec5106001a49d04e209d260ed0b0bd4c1bf733a8c8808c11ff720d0d2
- Pinned state: Flutter SDK repo commit 6655482ec06e547f90abf8ae7590466f4415978d (tag 3.47.1), path dev/a11y_assessments, copied out of tree; lib/ byte-identical to SDK (diff -rq clean)

## Environment
Flutter 3.47.1 stable (framework 6655482ec0, engine 5d53178869), Dart 3.13.1, macOS arm64. Android emulator AVD `Medium_Phone_API_36-ext19` (1080x2400, API 36), debug, headless `-read-only -port 5556`.
Scaffolding: `flutter create --project-name c014 -e --platforms=android c014` then replace lib/main.dart with `source/lib/main.dart` (plus recorded dependency pins). Compat change (recorded): removed the line `resolution: workspace` from pubspec.yaml so the app resolves outside the SDK workspace; lib/ unchanged (verified identical to the SDK checkout).

## Reproduction steps (curator)
1. Copy `dev/a11y_assessments` from the SDK checkout to a scratch dir, remove the single line `resolution: workspace` from its pubspec.yaml, `flutter pub get`, `flutter run -d <android emulator> --debug`.
2. In the app, open the top-right filter menu, check `batch1` and uncheck `batch2` (AND semantics: batch1+batch2 shows nothing); tap outside the menu. Tap `MaterialBanner` in the list (`adb shell input tap 540 1906`).
3. Tap `Show a MaterialBanner` (`input tap 540 1305`), then the AppBar back arrow (`input tap 72 136`): the banner stays visible on the home list.
4. Tap the banner's `DISMISS` (`input tap 902 331`).
Observed: the banner is not dismissed, and the framework logs `EXCEPTION CAUGHT BY GESTURE ... This widget has been unmounted, so the State no longer has a context` (MainWidgetState.hideBanner). Reproduced twice (initial and fresh process).

## Reset procedure
`adb shell am force-stop dev.flutter.a11yassessments`, relaunch via launcher; filter state resets to batch2 default (repeat step 2). Verified once: same visible symptom (banner stays); exception text is only visible with a tool attached.

## Independent observable predicate (hidden)
{'description': "After showing the MaterialBanner, navigating back to the list without dismissing it, and tapping DISMISS, the banner remains visible and a framework exception 'This widget has been unmounted, so the State no longer has a context' is recorded.", 'evaluation_method': "Independent scorer checks that the visible text 'Hello, I am a Material Banner' / 'DISMISS' is still shown after the DISMISS tap, and that the runtime-error observation contains the unmounted-State message."}

## Difficulty / capability metadata
UI actions: ~9 taps (filter menu, list item, show, back, dismiss). Navigation: one route and back. Text entry none. Scrolling: none needed (MaterialBanner visible after filter; app default filter hides it). Runtime-error dependence: supportive-to-required (primary exception text); visible symptom (banner not dismissed) is independently observable. Widget inspection: required. Source inspection: supportive (use case in SDK app). Asynchrony none. Setup: copy of SDK dev app (specialised but supported). Reset: restart + re-select filter. Proposed difficulty: medium-high due to hidden filter step.

## potential_capability_requirements
tap; visible-text inspection; filter-menu/checkbox UI interaction; runtime-error observation; app-specific hidden filter default.

## Leakage review
Issue body (step list + 'Actual results' mention 'FocusNode was used after being disposed' and the iOS stack trace naming `MainWidgetState.hideBanner` in material_banner.dart:47) — the exception text and method names are diagnostic and must be removed; the issue says repro on all platforms. The in-app filter step (batch1) is NOT in the issue and is curator-discovered; the issue assumes the use-case list is already reachable. Source of the app is part of the SDK repo and contains the buggy code (hideBanner uses context after dispose) — inherent to a source-inspection capability. Comments: none substantive.
