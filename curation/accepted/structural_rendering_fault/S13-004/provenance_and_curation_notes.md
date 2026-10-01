# S13-004 — curator-only record (CAND-013)

NOT agent-visible. Never expose this directory, or `curation/ground_truth/S13-004.json`, to the evaluation agent.
Accepted into the curated candidate pool by Stage 13 only; NOT yet selected for calibration or the final formal dataset.

## Provenance
- Issue: https://github.com/flutter/flutter/issues/192151 (opened 2026-09-02; open)
- Case type: mre_inline
- Issue body SHA-256: 10a4b03386f8d0b6b69e10544db17fc7bab970e62d4c62adc92a9f4e5d6614aa
- main.dart SHA-256: 2f5e1405724fea69388d715d624e5d292003a8a7d634f0f3f6098736bd59c79d ; pubspec.lock SHA-256: 18bd70bf50b1f0e36e76ea9b563968ddc876f859363fface8ed111daaf5fc98f
- Pinned state: Flutter SDK 3.47.1 (Material 3 default theme; SDK version is the revision) + inline MRE; no third-party packages; do not upgrade Flutter

## Environment
Flutter 3.47.1 stable (framework 6655482ec0, engine 5d53178869), Dart 3.13.1, macOS arm64. Android emulator AVD `Medium_Phone_API_36-ext19` (1080x2400, API 36), debug, headless `-read-only -port 5556`.
Scaffolding: `flutter create --project-name c013 -e --platforms=android c013` then replace lib/main.dart with `source/lib/main.dart` (plus recorded dependency pins). 

## Reproduction steps (curator)
1. `flutter run -d <android emulator> --debug` with the sample (it sets `debugPaintSizeEnabled = true`).
2. Tap `Open Date Picker` (`adb shell input tap 540 1306`); allow ~10-20 s for the debug-paint UI to render.
3. Observe the Material 3 date picker calendar grid: each day button is ~43-44 dp wide (about 115 px at 420 dpi) on a 1080x2400 phone, i.e. narrower than 48 dp, while the grid pitch is 48 dp.
Reproduced twice (initial and after force-stop + am start): identical outline geometry.

## Reset procedure
`adb shell am force-stop com.example.c013; adb shell am start -n com.example.c013/.MainActivity`; picker closes with the process. Verified once (needs a retry tap if rendering is slow).

## Independent observable predicate (hidden)
{'description': 'With the date picker open on a 1080x2400, 420 dpi (411 dp wide) phone display, the rendered width of an individual day button in the calendar grid is less than 48 dp (about 43-44 dp).', 'evaluation_method': 'Independent scorer measures the day-button width (widget/semantics bounds via inspector, or debug-paint outlines) and compares with 48 dp.'}

## Difficulty / capability metadata
UI actions: 1 tap. Navigation none. Text entry none. Scrolling none. Runtime-error dependence: not useful. Widget/geometry inspection: REQUIRED (size of day buttons; visible text alone is insufficient). Source inspection: not useful. Asynchrony: none (render latency with debug paint). Setup standard. Reset restart only. Predicate depends on display size/density; cases tied to this emulator profile. Proposed difficulty: medium (needs measurement). Suitability uncertainty: whether the geometric threshold is an accepted 'defect' (maintainer comment notes small screens may not fit 48dp tiles).

## potential_capability_requirements
tap; widget bounds/size inspection (geometry), debug-paint overlay is in the sample; possibly wait for slow render.

## Leakage review
Issue body gives the numeric threshold and observed ~43dp width (these ARE the predicate). The reference bug ID (b/244299544) and the maintainer comment (hannah-hyj: date picker entry mode as alternative; 'framework issue if big screens still lack 48x48') are context/diagnosis; exclude. The sample's `debugPaintSizeEnabled = true` is part of the MRE and visually reveals widget bounds (acceptable but note it aids detection). Candidate agent-visible text: user-level 'date picker day buttons feel too narrow to tap reliably on a phone' without the 48dp figure.
