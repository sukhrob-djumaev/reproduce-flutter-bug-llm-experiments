# S13B-001 — curator-only record (CAND-018)

NOT agent-visible. Never expose this directory, or `curation/ground_truth/S13B-001.json`, to the evaluation agent.
Accepted into the curated candidate pool by Stage 13 only; NOT yet selected for calibration or the final formal dataset.

## Provenance
- Issue: https://github.com/LahaLuhem/list_smith/issues/80 (opened 2026-09-29; open)
- Case type: mre_inline (package: list_smith 1.0.0; independent owner repo)
- Issue body SHA-256: afa3c3f64649383a60ccdc94f104d7a6538757f8d4a630bd7be73d435ce5acad
- main.dart SHA-256: aafe850c371bcbc39afeec2cc2e8c6372932ed7232917711eeb8e13c4dc7fb61 ; pubspec.lock SHA-256: e5d69a8f59644447f30e48832d1ac0d1db691ab2e73acce2558d38c1f6a9f6ea
- Pinned state: Flutter 3.47.1 + list_smith 1.0.0 (+ infinite_scroll_pagination 5.1.1 per source/pubspec.lock) + inline MRE; maintainer plans a fix in the next major release - keep list_smith pinned at 1.0.0

## Environment
Flutter 3.47.1 stable (framework 6655482ec0, engine 5d53178869), Dart 3.13.1, macOS arm64. Android emulator AVD `Medium_Phone_API_36-ext19` (1080x2400, API 36), debug, headless `-read-only -port 5556`.
Scaffolding: `flutter create --project-name d018 -e --platforms=android d018` then replace lib/main.dart with `source/lib/main.dart` (plus recorded dependency pins). 

## Reproduction steps (curator)
1. Scaffold project, `flutter pub add list_smith:1.0.0`, copy the sample, install on the Android emulator (debug).
2. Launch the app in a fresh process (`adb shell am start -n com.example.d018/.MainActivity`). The sample's fetch takes 3 s, so the first page shows a centred loading spinner for ~3 s.
3. While that centred spinner is visible, start a downward touch drag from the top of the list (e.g. `adb shell input motionevent DOWN 540 600`, then `MOVE 540 800`, `MOVE 540 1400`) and keep holding.
4. Observe: a pull-to-refresh indicator appears at the top at the same time as the centred loading spinner (two spinners).
Reproduced in 2 of 3 fresh runs; the third started the drag after loading had finished (timing of the curator's polling), so it is not a counter-example.

## Reset procedure
`adb shell am force-stop com.example.d018; adb shell am start -n com.example.d018/.MainActivity`; no persisted state. Verified (every run is a fresh process).

## Independent observable predicate (hidden)
{'description': "While the list's first page is still loading (centred loading spinner visible), a downward pull gesture at the top of the list shows the pull-to-refresh indicator (second spinner at the top) instead of being ignored.", 'evaluation_method': 'Independent scorer inspects a screenshot/widget tree captured during the pull while the first-page loading spinner is still present: both the loading spinner and the refresh indicator are present. Outside the loading window the predicate is not evaluable.'}

## Difficulty / capability metadata
UI actions: 1 downward drag (touch down, move, hold). Navigation none. Text entry none. Scrolling/drag: REQUIRED (pull gesture). Wait/polling: REQUIRED (must act inside the 3 s loading window). Runtime-error dependence: not useful. Widget inspection: required (identify two progress indicators). Source inspection: supportive. Asynchrony: bounded local async (3 s Future.delayed). Setup standard (one package). Reset restart. Timing-sensitive. Proposed difficulty: medium-high.

## potential_capability_requirements
drag/pull gesture; wait/polling (bounded loading window); widget/visible indicator inspection; launch fresh process.

## Leakage review
Issue body states the intended behavior ('should not be possible to trigger pull-to-refresh while loading/error/empty') and links 2 videos; comments: maintainer acknowledges and mentions that the upstream infinite_scroll_pagination issue #382 makes it harder and that pull-to-refresh on error/empty states is a common intended use (design context, not diagnosis). Expected behavior is partly contested by the maintainer's own note, so the agent-visible text should describe only the loading-state observation. No patch or workaround in the issue.
