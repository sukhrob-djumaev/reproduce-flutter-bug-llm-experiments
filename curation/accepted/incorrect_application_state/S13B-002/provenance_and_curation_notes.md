# S13B-002 — curator-only record (CAND-020)

NOT agent-visible. Never expose this directory, or `curation/ground_truth/S13B-002.json`, to the evaluation agent.
Accepted into the curated candidate pool by Stage 13 only; NOT yet selected for calibration or the final formal dataset.

## Provenance
- Issue: https://github.com/bdlukaa/fluent_ui/issues/1349 (opened 2026-08-06; open)
- Case type: mre_inline (package: fluent_ui 4.16.1; independent owner repo)
- Issue body SHA-256: 48ea45c3a7bbede78decb1bffab623af8f1f6997ed77310b1494092a02090864
- main.dart SHA-256: e2701d12b89da4bbe6173875b42a113a8066c65b7cf0ae8b3aee574f9f0bad98 ; pubspec.lock SHA-256: 7564662ca27f82274a376da11d373cd1623b6a726265c4ca695472d0e049c88e
- Pinned state: Flutter 3.47.1 + fluent_ui 4.16.1 (lockfile in source/) + inline MRE; reporter says 4.16.0 behaves correctly, so keep fluent_ui pinned at 4.16.1

## Environment
Flutter 3.47.1 stable (framework 6655482ec0, engine 5d53178869), Dart 3.13.1, macOS arm64. Android emulator AVD `Medium_Phone_API_36-ext19` (1080x2400, API 36), debug, headless `-read-only -port 5556`.
Scaffolding: `flutter create --project-name f020 -e --platforms=android f020` then replace lib/main.dart with `source/lib/main.dart` (plus recorded dependency pins). 

## Reproduction steps (curator)
1. Scaffold project, `flutter pub add fluent_ui:4.16.1`, copy the sample, `flutter run -d <android emulator> --debug`.
2. The screen shows a `rebuild parent: 0` button at the top and, inside the first tab, a `counter: 0` button.
3. Tap the counter button twice (`adb shell input tap 540 1294` x2): `counter: 2`.
4. Tap `rebuild parent` (`adb shell input tap 540 80`): the label becomes `rebuild parent: 1` and the counter resets to `counter: 0`.
Reproduced in the initial run and in a fresh process.

## Reset procedure
`adb shell am force-stop com.example.f020; adb shell am start -n com.example.f020/.MainActivity`; no persisted state. Verified.

## Independent observable predicate (hidden)
{'description': "After tapping the counter button twice (counter: 2), tapping the unrelated `rebuild parent` button resets the tab body's counter to `counter: 0`.", 'evaluation_method': 'Independent scorer reads the visible texts before and after the `rebuild parent` tap: `counter: 2` -> `counter: 0` while `rebuild parent` increments by one.'}

## Difficulty / capability metadata
UI actions: 3 taps. Navigation none. Text entry none. Scrolling none. Runtime-error dependence: not useful (no exception). Visible-text inspection: required. Widget inspection: required to find buttons (one sits under the status bar area). Source inspection: supportive. Asynchrony none. Setup standard (one package). Reset restart. Proposed difficulty: low.

## potential_capability_requirements
tap; visible-text inspection; widget inspection; no wait needed.

## Leakage review
Issue body contains a full root-cause section (ValueKey<Tab> identity keys introduced in 4.16.1 changelog entry), the exact file/path and changelog quote, and a statement that 4.16.0 works - all must be removed. The 'To Reproduce' steps/sample are usable. Comments: none relevant. The sample code is the MRE and contains no hint about the cause (Tab instances are created in build(), as documented usage).
