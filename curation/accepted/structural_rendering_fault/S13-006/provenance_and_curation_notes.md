# S13-006 — curator-only record (CAND-016)

NOT agent-visible. Never expose this directory, or `curation/ground_truth/S13-006.json`, to the evaluation agent.
Accepted into the curated candidate pool by Stage 13 only; NOT yet selected for calibration or the final formal dataset.

## Provenance
- Issue: https://github.com/flutter/flutter/issues/188272 (opened 2026-06-20; open)
- Case type: mre_inline
- Issue body SHA-256: 4830cf5b680e212b6c1edb0696cb6c96d27a040b747e5c9ab1ce11925a8eb97f
- main.dart SHA-256: c667c8de1835860703eb3728c291c3ba089dc0fc2455a4b96ecb08edfd77e64d ; pubspec.lock SHA-256: 18bd70bf50b1f0e36e76ea9b563968ddc876f859363fface8ed111daaf5fc98f
- Pinned state: Flutter SDK 3.47.1 (SDK version is the revision) + inline MRE; no third-party packages; MUST be run as a RELEASE build (`flutter run --release`) to show the defect

## Environment
Flutter 3.47.1 stable (framework 6655482ec0, engine 5d53178869), Dart 3.13.1, macOS arm64. Android emulator AVD `Medium_Phone_API_36-ext19` (1080x2400, API 36), debug, headless `-read-only -port 5556`.
Scaffolding: `flutter create --project-name c016 -e --platforms=android c016` then replace lib/main.dart with `source/lib/main.dart` (plus recorded dependency pins). Release build required (`flutter run --release`).

## Reproduction steps (curator)
1. Scaffold project, copy sample, `flutter run -d <android emulator> --release` (release mode is required for the reported symptom).
2. Tap `Show dialog` (`adb shell input tap 540 1200`).
3. Observe: the dialog shows only the title and the `Delete` button; the content area is covered by a large grey box (Cancel/Save/'Dialog content' not visible). logcat: `type '_OverflowBarParentData' is not a subtype of type 'FlexParentData' in type cast`.
Control: in debug mode (`flutter run --debug`) the same dialog renders all texts/buttons normally, with a ParentDataWidget exception printed in the console.
Reproduced twice (release run and fresh process of the release APK).

## Reset procedure
`adb shell am force-stop com.example.c016; adb shell am start -n com.example.c016/.MainActivity` on the installed RELEASE build (no persisted state). Verified.

## Independent observable predicate (hidden)
{'description': "In a release build, tapping 'Show dialog' displays the AlertDialog without its content text and without the Cancel/Save buttons, with a large grey region in place of the content, while in a debug build the same dialog shows 'Dialog content', 'Cancel' and 'Save'.", 'evaluation_method': "Independent scorer checks (release build) that texts 'Dialog content', 'Cancel' and 'Save' are not visible after the tap (screenshot/visible text), supportive: logcat line '_OverflowBarParentData is not a subtype of type FlexParentData'."}

## Difficulty / capability metadata
UI actions: 1 tap. Navigation: dialog. Text entry none. Scrolling none. Runtime-error dependence: supportive only (release log); primary observable is visible absence of dialog content. Widget inspection: required (visible text). BUILD MODE: requires release build — the VM-service based runtime tools (inspect_app/get_runtime_errors via Dart MCP/DTD) are not available in release, so the current tool stack could not observe this case; suitability for the formal pipeline is UNCERTAIN. Source inspection: supportive (Spacer in actions). Asynchrony none. Setup: release build (specialised but supported). Reset: restart. Proposed difficulty: medium; high environment cost.

## potential_capability_requirements
tap; visible-text inspection; RELEASE-mode launch (no VM-service tools); logcat reading optional.

## Leakage review
Issue body states the expected/actual in debug vs release terms and names the exception text '_OverflowBarParentData is not a subtype of FlexParentData' and the stack (exact failure cause visible in the issue) — remove; the comment by Munawer-Ali explains Spacer(Expanded) must be under a Flex/Row and OverflowBar is expected to fail (diagnosis/workaround) — remove. The sample line comment `// ← causes silent debug / release inconsistency` points to the offending widget — must be stripped from any agent-visible code/snapshot. Candidate agent-visible text: 'dialog appears blank/grey in release builds' + steps; do not reveal Spacer.
