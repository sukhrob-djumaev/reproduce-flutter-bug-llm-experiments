# S12-001 — curator-only record (CAND-004)

NOT agent-visible. Never expose this directory, or `curation/ground_truth/S12-001.json`, to the evaluation agent.
Accepted by the Stage 12 curation experiment only; not automatically part of the formal ~25-case dataset.

## Provenance
- Issue: https://github.com/flutter/flutter/issues/191275 (opened 2026-08-18 by zemanux; open at curation time 2026-10-01)
- MRE: inline code sample in the issue body (no separate repository). Used verbatim as `source/lib/main.dart`.
- Issue body SHA-256 (curator fetch, github.com page JSON): 77abdd0eed77a48f96b74cabc404cc2ab68e94a216ef7503bace0180ef13abfe
- main.dart SHA-256: cab3dd56417c8db2555a14221d175d93a9e6abedc2d83643d59ddec7b83a5d83
- pubspec.lock SHA-256: 18bd70bf50b1f0e36e76ea9b563968ddc876f859363fface8ed111daaf5fc98f
- Revision: there is no git history for an inline sample. The pinned state = Flutter SDK 3.47.1 (framework 6655482ec0, engine 5d53178869) + the files in `source/` (sample code + lockfile). The sample uses only the `flutter` SDK, no third-party packages.
- Defect lives in the Flutter framework (`RenderSliverCrossAxisGroup`), so the SDK version IS the revision. A fix PR (#191287) exists in draft; a future Flutter release will make this case non-reproducible, so the SDK must stay pinned at 3.47.1.

## Environment
- Flutter 3.47.1 stable, Dart 3.13.1, DevTools 2.60.0, macOS 26 (Darwin 25.6.0) arm64
- Device: Android emulator AVD `Medium_Phone_API_36-ext19` (1080x2400, API 36), started `-read-only -no-window -port 5556`, debug mode
- Scaffolding: `flutter create --project-name cand004 -e --platforms=android cand004`, then replace `lib/main.dart` with `source/lib/main.dart`. No dependencies added. No compatibility edits to the sample code.

## Reproduction steps (curator)
1. Scaffold project as above, copy `source/lib/main.dart`, `flutter run -d <android-emulator> --debug`.
2. Wait for first frame. No user interaction is required.
3. Observe: app bar title shows, body is blank, and the flutter run console prints `EXCEPTION CAUGHT BY RENDERING LIBRARY ... SliverCrossAxisGroup ran out of extent before child could be laid out.` (assertion thrown during performLayout, `sliver_group.dart:179`). Evidence: `evidence/runtime_exception_excerpt.txt`, `evidence/after_launch_blank_body.png`.

## Reset procedure
`adb shell am force-stop com.example.cand004` then `adb shell am start -n com.example.cand004/.MainActivity` (or re-run `flutter run`). No persistent state. Verified once: relaunch gave the identical blank body. Note: the exception text itself is visible only when a tool is attached (flutter run / VM service / Dart MCP get_runtime_errors); plain logcat after a bare `am start` did not show it, so scoring evidence must come from the attached runtime-error channel.

## Independent observable predicate (hidden)
After app start on the pinned state, with no further action, a RenderingLibrary assertion containing the text "SliverCrossAxisGroup ran out of extent before child could be laid out" is recorded in the runtime errors, and the Scaffold body shows none of the texts "Expanded (Left)", "Expanded (Right)", "Center item 1".
Evaluation: runtime-error observation (status observed) contains that message; supportive: inspect_app/visible text lacks the three strings.

## Difficulty metadata
UI actions: 0. Navigation: none. Text entry: none. Scrolling: none. Runtime-error dependence: required (primary evidence; the visible symptom is only a blank body, which alone is weak). Widget inspection: supportive. Source inspection: not useful. Instrumentation: not useful. Asynchrony: none. Setup: standard run. Reset: restart only. Overall difficulty label (proposal): low for action, medium for the agent because the failure is observable mainly through runtime errors.

## Leakage review
Issue body contains: the exact exception message (equals the predicate; must be removed or paraphrased in any agent-visible snapshot), the sample source code (contains the SliverCrossAxisGroup layout that causes the bug), a "Expected results" paragraph comparing to RenderFlex/Expanded (conceptual diagnosis), and in the comments a reference to a fix PR #191287 plus maintainer remarks ("should work the same way as Flex/Expanded"). Candidate agent-visible content (NOT finalized): title + the user-level description "a page that shows a CustomScrollView with SliverCrossAxisGroup children throws on a narrow (<=300 wide) layout; the list/columns do not appear". Must NOT include: exception text, the "ran out of extent" wording, RenderSliverCrossAxisGroup internals, fix PR link, Flex/Expanded explanation.
Because the app source is the MRE itself, a future source-inspection capability would expose the buggy construction; this is inherent to the sample (record for RQ2 analysis).

## potential_capability_gap
None for reproduction (launch only). Requires get_runtime_errors to observe the primary evidence.
