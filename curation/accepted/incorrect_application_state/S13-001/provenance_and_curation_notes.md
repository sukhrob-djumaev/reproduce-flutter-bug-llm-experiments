# S13-001 — curator-only record (CAND-010)

NOT agent-visible. Never expose this directory, or `curation/ground_truth/S13-001.json`, to the evaluation agent.
Accepted into the curated candidate pool by Stage 13 only; NOT yet selected for calibration or the final formal dataset.

## Provenance
- Issue: https://github.com/flutter/flutter/issues/190653 (opened 2026-08-06; open, waiting for PR to land (fixed))
- Case type: mre_inline
- Issue body SHA-256: b5557193cd56c09eb155d6adc4a157f6b7cff322583ac0c69e6c3187e2e46472
- main.dart SHA-256: b65a7ff67c472fab8c7385f434166256b748b5adc6e2e3d6688ecc4bccce423d ; pubspec.lock SHA-256: 18bd70bf50b1f0e36e76ea9b563968ddc876f859363fface8ed111daaf5fc98f
- Pinned state: Flutter SDK 3.47.1 (framework regression; SDK version is the revision) + inline MRE; no third-party packages; do not upgrade Flutter (fix PR pending)

## Environment
Flutter 3.47.1 stable (framework 6655482ec0, engine 5d53178869), Dart 3.13.1, macOS arm64. Android emulator AVD `Medium_Phone_API_36-ext19` (1080x2400, API 36), debug, headless `-read-only -port 5556`.
Scaffolding: `flutter create --project-name c010 -e --platforms=android c010` then replace lib/main.dart with `source/lib/main.dart` (plus recorded dependency pins). 

## Reproduction steps (curator)
1. `flutter run -d <android emulator> --debug` with the sample. On start the top label reads `Focused: r0c0`.
2. Send D-pad Down: `adb shell input keyevent 20` -> label `Focused: r1c0`.
3. Send D-pad Up: `adb shell input keyevent 19` -> label shows `Focused: r0c1` instead of the expected `r0c0`.
Reproduced twice (original run and a fresh process after force-stop + am start): identical result. Evidence: `evidence/*.png`.

## Reset procedure
`adb shell am force-stop com.example.c010; adb shell am start -n com.example.c010/.MainActivity` (no persisted state). Verified once.

## Independent observable predicate (hidden)
{'description': 'After app start (label `Focused: r0c0`), one Down key press then one Up key press results in the on-screen label `Focused: r0c1` rather than `Focused: r0c0`.', 'evaluation_method': 'Independent scorer reads the visible `Focused:` label text after the key sequence.'}

## Difficulty / capability metadata
UI actions: 2 hardware key presses (Down, Up). Navigation none. Text entry none. Scrolling: focus traversal scrolls row list (implicit). Runtime-error dependence: not useful. Widget/visible-text inspection: required (`Focused:` label). Source inspection: not useful. Instrumentation: not needed (sample has the label). Asynchrony none. Setup standard. Reset restart only. Proposed difficulty: low-medium.

## potential_capability_requirements
Directional hardware key press (DPAD Up/Down) — not a tap; visible-text read; (curation note: Android needs an attached key source).

## Leakage review
Issue body names the regression commit (b46a6aa / #172875) and states expected/observed targets; the sample's own on-screen label says `Expect back on r0c0, observe r0c1` (leaks the observable outcome inside the app UI itself; the app text would need to be treated as part of the MRE or neutralized later — decision deferred). Maintainer comment (mbcorona) analyses the commit (diagnosis). Exclude: commit link, diagnosis, 'expect/observe' label text if the snapshot is user-level.
