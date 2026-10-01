# S13-003 — curator-only record (CAND-012)

NOT agent-visible. Never expose this directory, or `curation/ground_truth/S13-003.json`, to the evaluation agent.
Accepted into the curated candidate pool by Stage 13 only; NOT yet selected for calibration or the final formal dataset.

## Provenance
- Issue: https://github.com/flutter/flutter/issues/193098 (opened 2026-09-21; open)
- Case type: mre_inline (derived from widget test that fully defines the UI; package: go_router)
- Issue body SHA-256: d6a4e474388e356ffc57b6a935c049b6b0b1989515af5a16ae5a3530f2f0464a
- main.dart SHA-256: 0c43727c5cfba1a6a86fde82246a09adb163e85df7a14311f412ad59bafa5d92 ; pubspec.lock SHA-256: f1157ad144d080d9519bd655debfdabb05c59563c8f2a2a781ae594d085c6e7a
- Pinned state: Flutter SDK 3.47.1 + go_router 17.5.0 (reporter reproduced 16.2.4 and 17.5.0; pinned in source/pubspec.lock); do not upgrade go_router (18.x may change)

## Environment
Flutter 3.47.1 stable (framework 6655482ec0, engine 5d53178869), Dart 3.13.1, macOS arm64. Android emulator AVD `Medium_Phone_API_36-ext19` (1080x2400, API 36), debug, headless `-read-only -port 5556`.
Scaffolding: `flutter create --project-name c012 -e --platforms=android c012` then replace lib/main.dart with `source/lib/main.dart` (plus recorded dependency pins). 

## Reproduction steps (curator)
1. `flutter run -d <android emulator> --debug` (or launch the installed debug app). HOME text is shown; bottom row has `home` and `settings` text buttons.
2. Tap `settings` (`adb shell input tap 266 2336`), then tap the SETTINGS button at the top-left (`input tap 60 100`) -> `GENERAL` shown (sub-route inside branch B).
3. Tap `home` (`input tap 84 2336`) -> HOME shown (branch A root; branch B still holds the sub-route).
4. Press system Back (`adb shell input keyevent 4`) one to three times.
Observed: the app stays in the foreground with HOME unchanged after every Back press (Back is consumed). Expected (control): the app closes on Back.
Reproduced twice (initial run, fresh process). Control (no sub-route) closes the app on first Back.

## Reset procedure
`adb shell am force-stop com.example.c012; adb shell am start -n com.example.c012/.MainActivity`; no persisted state. Verified.

## Independent observable predicate (hidden)
{'description': 'After navigating settings -> general sub-route -> home tab and pressing system Back on the home tab, the app remains in the foreground showing HOME (Back is swallowed); in the control run without the sub-route, Back closes the app.', 'evaluation_method': 'Independent scorer checks (a) visible text remains HOME after Back and (b) the app activity is still the foreground activity (adb dumpsys activity topResumedActivity) after one Back.'}

## Difficulty / capability metadata
UI actions: 3 taps + 1-3 system Back events. Navigation: multi-branch shell. Text entry none; scrolling none. Runtime-error dependence: not useful (no exception). Widget/visible-text inspection: required (find tabs/buttons; confirm HOME). Evidence channel: foreground-activity/lifecycle state outside Flutter UI is the primary discriminator (UI looks identical before/after Back). Source inspection: not useful. Asynchrony none. Setup standard. Reset restart only. Proposed difficulty: medium.

## potential_capability_requirements
tap; system Back key (not a widget tap); visible-text read; foreground-activity/app-closed observation (lifecycle) — a new generic observation channel; runtime-error not useful.

## Leakage review
Issue body contains a full 'Root cause' section (go_router builder PopScope canPop + ModalRoute.popDisposition every), file/line names, a proposed code change, and diagnostic output `rootNav.canPop()==false / maybePop()==true` — all must be excluded. The reproduction steps + expected/actual paragraphs are separable and usable. The sample is a widget test; the app wrapper (runApp(MaterialApp.router)) is curator harness. Comment (suryaKommana2662) repeats test failure output and links #188018.
