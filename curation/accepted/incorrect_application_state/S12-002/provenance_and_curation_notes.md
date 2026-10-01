# S12-002 — curator-only record (CAND-007)

NOT agent-visible. Never expose this directory, or `curation/ground_truth/S12-002.json`, to the evaluation agent.
Accepted by the Stage 12 curation experiment only; not automatically part of the formal ~25-case dataset.

## Provenance
- Issue: https://github.com/flutter/flutter/issues/188018 (opened 2026-06-15 by jasaw; open, label "waiting for PR to land (fixed)" at curation time 2026-10-01)
- MRE: inline sample in issue body, used verbatim as `source/lib/main.dart`; reporter-stated package version go_router 17.3.0 pinned in `source/pubspec.yaml`/`pubspec.lock`.
- Issue body SHA-256 (curator fetch): d40092854eef98957f6553de70a438013cde22aaf5f918eb37b5862b4f0d0fd2
- main.dart SHA-256: 3cb21cabbc28504739cacbd5347d52fb486ac8a70f194ebe34a982bc23306dc9 ; pubspec.lock SHA-256: 24a57dfd2b1dbe477e3a49fb5ca5733619825ea1fbe9722363731522855bf1d7
- Revision: no git history for an inline sample. Pinned state = Flutter 3.47.1 (framework 6655482ec0) + go_router 17.3.0 + the files in `source/`. A later go_router release (17.4.0+, 18.x) may contain the fix (PR flutter/packages#11910); do NOT upgrade go_router.

## Environment
- Flutter 3.47.1 stable, Dart 3.13.1, macOS arm64; reporter used Flutter 3.44.0 / Dart 3.12.0 (go_router 17.3.0) — behavior reproduced on 3.47.1.
- Device: Android emulator AVD `Medium_Phone_API_36-ext19` (1080x2400, Android 16 / API 36), `-read-only -no-window -port 5556`, debug mode.
- Scaffolding: `flutter create --project-name cand007 -e --platforms=android cand007`; `flutter pub add go_router:17.3.0`; replace lib/main.dart with `source/lib/main.dart`.
- Compatibility/config edit (documented): added `android:enableOnBackInvokedCallback="true"` to `<application>` in AndroidManifest.xml (issue step 1 lists this as an alternative to Android 16 SDK 36 default; see `source/android_manifest_edit/AndroidManifest.xml`). Could not alter bug logic (Dart code untouched).

## Reproduction steps (curator, pixel coords for 1080x2400)
Perform on the app launched in a FRESH process:
1. On "Stack A - 1" tap "Push one screen" twice (screens A2, A3 pushed). `adb shell input tap 540 1237` x2.
2. Tap bottom tab C (`input tap 900 2208`); tap "Push one screen" once (C2).
3. Tap bottom tab B (`input tap 540 2208`).
4. Perform the system back GESTURE twice: left-edge swipe `adb shell input swipe 2 1200 600 1200 400` (x2, ~3 s apart).
5. Tap tab A (`input tap 180 2208`).
Observed: tab A shows "Stack A - 1" (title and body) instead of "Stack A - 3" with a back arrow. Logcat shows `/A didPop /A3 -> /A2`, `/C didPop /C2 -> /C1`, `/A didPop /A2 -> /A1` while the active branch is B.
Evidence: `evidence/branch_A_after_gesture_back_shows_A1.png`, `evidence/logcat_navigation_events.txt`.
NOT equivalent: `adb shell input keyevent 4` (system Back key) did NOT reproduce — back was handled by B's PopScope (`didPop=false`) and tab A still showed "Stack A - 3". Only the swipe (predictive back gesture path) reproduces. Record for tool design.
Secondary symptom in the issue (dispose order) was observed as "A3 dispose, then A2 dispose" in our run, which differs from the issue text; not used in the predicate.

## Reset procedure
`adb shell am force-stop com.example.cand007; adb shell am start -n com.example.cand007/.MainActivity` (no persisted state; verified: a fresh process after the failed Back-key attempt then reproduced).

## Independent observable predicate (hidden)
After steps 1-5 above, the visible screen on tab A shows the text "Stack A - 1" (and no "Stack A - 3"/back arrow), although no back action was performed while branch A was active.
Evaluation: inspect visible text after the final tab A selection; supportive: navigator observer log lines `/A didPop /A3 -> /A2` and `/C didPop /C2 -> /C1` while on tab B.

## Difficulty metadata
UI actions: ~7 taps + 2 system-edge-swipe gestures. Navigation: multi-route, multi-branch. Text entry: none. Scrolling: none. Runtime-error dependence: not useful (no exception). Widget inspection: required (visible text). Source inspection: supportive. Instrumentation: supportive (observer logs already in sample). Asynchrony: none. Setup: standard + Android manifest flag. Reset: restart only. Proposed label: high (requires non-tap system gesture and a long order-dependent sequence).

## Leakage review
Issue body contains the full numbered steps (acceptable as agent-visible input, minus the manifest instruction), the "Expected/Actual" paragraphs (describe the symptom, and the actual-results text names dispose-order details and 'inactive branches' diagnosis). Comments contain log lines `/A didPop ...`, a maintainer-style diagnosis ("inactive StatefulShellBranch navigators being included in system back handling") and the fix PR flutter/packages#11910 (must be excluded). Agent-visible candidate (NOT finalized): title + steps 1-7 + "Expected: screens from inactive tabs should not be removed". Exclude: diagnosis, dispose-order claim, PR link, observer logs.
The app source contains LoggingObserver/debugPrint output which could serve as retained evidence (a source-inspection capability would not reveal the bug location).

## potential_capability_gap
System back gesture / left-edge swipe (not a widget tap); bottom-navigation taps work as normal taps; possibly app-launch with manifest flag (curation-time only).
