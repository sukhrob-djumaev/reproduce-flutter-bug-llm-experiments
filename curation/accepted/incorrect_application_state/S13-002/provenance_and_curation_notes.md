# S13-002 — curator-only record (CAND-011)

NOT agent-visible. Never expose this directory, or `curation/ground_truth/S13-002.json`, to the evaluation agent.
Accepted into the curated candidate pool by Stage 13 only; NOT yet selected for calibration or the final formal dataset.

## Provenance
- Issue: https://github.com/flutter/flutter/issues/186876 (opened 2026-05-21; open, waiting for PR to land (fixed))
- Case type: mre_inline (package: two_dimensional_scrollables)
- Issue body SHA-256: b8d165a5fae64044b9f84853f60b5abc93f198fc7d1fce7827b07fdaba51c8e5
- main.dart SHA-256: c0a052479a1a482fe8163c3b957a72091037b389d70048e4c4520f054ef83c49 ; pubspec.lock SHA-256: 54f91647496827cb43d1ff004e4f999ed068e8742f3b4377a29c9e6b5d92b64e
- Pinned state: Flutter SDK 3.47.1 + two_dimensional_scrollables 0.5.2 (reporter ^0.5.2; lockfile in source/) + inline MRE; package 0.5.3+ or later may change behavior (fix pending) - keep pinned

## Environment
Flutter 3.47.1 stable (framework 6655482ec0, engine 5d53178869), Dart 3.13.1, macOS arm64. Android emulator AVD `Medium_Phone_API_36-ext19` (1080x2400, API 36), debug, headless `-read-only -port 5556`.
Scaffolding: `flutter create --project-name c011 -e --platforms=android c011` then replace lib/main.dart with `source/lib/main.dart` (plus recorded dependency pins). 

## Reproduction steps (curator)
1. `flutter run -d <android emulator> --debug`; wait for the table (column of three-dot buttons at the right edge; horizontal scroll at initial position).
2. Tap a three-dot button (e.g. row 2: `adb shell input tap 996 316`).
3. Observe: the popup menu does not open; the app logs `row tapped: 2` (row's TapGestureRecognizer received the tap) and no `popup opened` line. Same for row 4.
Reported on web/Chrome; reproduced here on Android touch. Reproduced 3 times incl. a fresh process.

## Reset procedure
`adb shell am force-stop com.example.c011; adb shell am start -n com.example.c011/.MainActivity`; no persisted state. Verified once.

## Independent observable predicate (hidden)
{'description': "At the initial horizontal scroll position, tapping the visible three-dot button in the trailing pinned column does not open the popup (no 'Action N' menu entry visible) and the app logs `row tapped: N`.", 'evaluation_method': "Independent scorer checks that no menu item 'Action N' becomes visible after the tap; supportive evidence is the debugPrint line `row tapped: N` (log, not UI) and absence of `popup opened: N`."}

## Difficulty / capability metadata
UI actions: 1 tap. Navigation none. Text entry none. Scrolling: none required for the predicate (control uses horizontal scroll). Runtime-error dependence: not useful (no exception). Widget inspection: required (find the three-dot target). Evidence channel: log lines (debugPrint) are supportive but UI absence-of-menu is the primary observable. Source inspection: not useful. Asynchrony none. Setup standard. Reset restart only. Proposed difficulty: low.

## potential_capability_requirements
tap only; visible text/widget inspection; optional horizontal scroll for the control; debug-print log reading is supportive only.

## Leakage review
Issue body states expected/actual in terms of TapGestureRecognizer/hit-testing (technical diagnosis hints: 'underlying row', 'trailing pinned column'); the sample's debug prints (`row tapped`, `popup opened`) reveal the interpretation. Comments: reproduction notes, 'also trailing pinned rows' (generalization). No fix patch in body; a fix PR is pending (label). Candidate agent-visible text: user-level steps 'tap the three-dot menu in the rightmost column; expected: menu opens' without hit-test wording.
