# S13B-003 — curator-only record (CAND-021)

NOT agent-visible. Never expose this directory, or `curation/ground_truth/S13B-003.json`, to the evaluation agent.
Accepted into the curated candidate pool by Stage 13 only; NOT yet selected for calibration or the final formal dataset.

## Provenance
- Issue: https://github.com/imaNNeo/fl_chart/issues/2115 (opened 2026-07-30; open (fix PR #2119 proposed))
- Case type: mre_inline (package: fl_chart 1.2.0; independent owner repo)
- Issue body SHA-256: 6b479850a2760ceb2fd8948e00387441ef6a96a98686f844b2df4c7ee506d35c
- main.dart SHA-256: 2054a97f12c85ee1dac0f0c72093cd0f2724cab6ab108dd8adc66f22fd5e8929 ; pubspec.lock SHA-256: 8e251b5d2209c550e467b2cfcf44f7d66db96d0d952afc814cafea8716977b0f
- Pinned state: Flutter 3.47.1 + fl_chart 1.2.0 (reporter version; lockfile in source/) + inline MRE; a fix PR (#2119) exists, so keep fl_chart pinned at 1.2.0

## Environment
Flutter 3.47.1 stable (framework 6655482ec0, engine 5d53178869), Dart 3.13.1, macOS arm64. Android emulator AVD `Medium_Phone_API_36-ext19` (1080x2400, API 36), debug, headless `-read-only -port 5556`.
Scaffolding: `flutter create --project-name f021 -e --platforms=android f021` then replace lib/main.dart with `source/lib/main.dart` (plus recorded dependency pins). 

## Reproduction steps (curator)
1. Scaffold project, `flutter pub add fl_chart:1.2.0`, copy the sample, run on the Android emulator in debug mode.
2. Observe immediately after launch (no interaction): below the `FlChart Test` app bar the body shows the red error widget with `LateInitializationError: Field 'mostRightSpot' has not been initialized.`; the console prints `EXCEPTION CAUGHT BY WIDGETS LIBRARY ... LateInitializationError ... LineChartBarData.mostRightSpot`.
Reproduced twice (initial run and a fresh process).

## Reset procedure
`adb shell am force-stop com.example.f021; adb shell am start -n com.example.f021/.MainActivity` (wait a few seconds; one immediate relaunch after force-stop landed on the launcher). No persisted state. Verified.

## Independent observable predicate (hidden)
{'description': "On launch with no interaction, the screen body shows the framework error widget text `LateInitializationError: Field 'mostRightSpot' has not been initialized.` instead of a rendered chart, and the runtime records that exception.", 'evaluation_method': 'Independent scorer checks the retained runtime-error observation (or the visible error-widget text) for `LateInitializationError ... mostRightSpot`; in a debug build the same text is visible in the widget tree.'}

## Difficulty / capability metadata
UI actions: 0 (launch only). Navigation none. Text entry none. Scrolling none. Runtime-error observation: supportive-to-primary (the same text is also visible on screen in debug, so visible-text inspection alone suffices). Widget/visible-text inspection: sufficient. Source inspection: not useful. Asynchrony none. Setup standard (one package). Reset restart. Debug build assumed (release shows a grey widget instead). Proposed difficulty: low.

## potential_capability_requirements
launch only; visible-text (error widget) inspection; runtime-error observation optional.

## Leakage review
The exact exception text is the predicate and is also in the issue body title/description ('late initialization error'); remove the field name `mostRightSpot` and the method name `calculateMaxAxisValues` from any agent-visible snapshot. A comment (omid-io) explains the root cause (late final spots uninitialized when all spots are null, spots.isEmpty check) and links fix PR #2119 - must be hidden. The sample itself reveals the trigger (a bar containing only FlSpot.nullSpot), which a source-inspection capability would expose.
