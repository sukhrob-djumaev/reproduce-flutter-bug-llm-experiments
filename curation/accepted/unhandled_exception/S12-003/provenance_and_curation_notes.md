# S12-003 — curator-only record (CAND-008)

NOT agent-visible. Never expose this directory, or `curation/ground_truth/S12-003.json`, to the evaluation agent.
Accepted by the Stage 12 curation experiment only; not automatically part of the formal ~25-case dataset.

## Provenance
- Issue: https://github.com/flutter/flutter/issues/192861 (opened 2026-09-16 by fujidaiti; open at curation time 2026-10-01)
- MRE: inline sample in issue body, verbatim as `source/lib/main.dart` (no third-party packages).
- Issue body SHA-256: e0d9d8bcc968f92ba82f9631da60bb70fb33aeb6ed5d2e23ebb8d7e0db9b340b ; main.dart SHA-256: 10be7870df8a2d6d0398ecc9baf522919863eb75a9be72ca9c7cc55d297dc6a4 ; pubspec.lock SHA-256: 18bd70bf50b1f0e36e76ea9b563968ddc876f859363fface8ed111daaf5fc98f
- Revision: no git history for inline sample. Pinned state = Flutter 3.47.1 (framework 6655482ec0, engine 5d53178869) + `source/`. Defect is in the framework (OverlayPortal / _RenderTheater), so the SDK version is the revision; do not upgrade Flutter (a fix would change behavior). Commenter reproduced on Flutter 3.47.4; we reproduced on 3.47.1.

## Environment
Flutter 3.47.1 stable, Dart 3.13.1, macOS arm64; Android emulator AVD `Medium_Phone_API_36-ext19` (1080x2400, API 36), debug mode, headless `-read-only -port 5556`.
Scaffolding: `flutter create --project-name cand008 -e --platforms=android cand008`; replace lib/main.dart with `source/lib/main.dart`. No dependency or code edits.

## Reproduction steps (curator)
1. `flutter run -d <android emulator> --debug`; wait for the light-blue 300x300 box with a "Tap to reproduce" DropdownMenu at its bottom (no exception at launch).
2. Tap the DropdownMenu (`adb shell input tap 540 1520`).
3. Observe: trailing arrow flips to "up", no menu items appear, and the console prints `EXCEPTION CAUGHT BY RENDERING LIBRARY ... RenderBox.size accessed beyond the scope of resize, layout, or permitted parent access ... Failed assertion: line 2268 pos 11: 'sizeAccessAllowed'` (during performLayout, stack through _RenderLayoutSurrogateProxyBox.performLayout, overlay.dart:2795).
Evidence: `evidence/runtime_exception_excerpt.txt`, `evidence/after_tap_menu_not_opened.png`.

## Reset procedure
`adb shell am force-stop com.example.cand008; adb shell am start -n com.example.cand008/.MainActivity`. No persistent state. Verified once: after reset and the same tap, the identical symptom appeared (arrow up, no menu items). Caveat: assertion text appears only with a tool attached (flutter run / VM service / get_runtime_errors); plain logcat after a bare am start showed no framework error text (same behavior as S12-001).

## Independent observable predicate (hidden)
After launch, with the DropdownMenu tapped once, the runtime records a rendering assertion whose message contains "RenderBox.size accessed beyond the scope of resize" / "sizeAccessAllowed", and none of the entries "Item 1", "Item 2", "Item 3" is visible.
Evaluation: runtime-error observation (status observed) contains the message; supportive: visible text lacks Item 1-3 after the tap.

## Difficulty metadata
UI actions: 1 tap. Navigation: none. Text entry: none. Scrolling: none. Runtime-error dependence: required (primary evidence; symptom alone = menu silently not opening). Widget inspection: required to find the target ("Tap to reproduce" field). Source inspection: not useful. Instrumentation: not useful. Asynchrony: none. Setup: standard. Reset: restart only. Proposed label: low.

## Leakage review
Issue body contains: the exact assertion text (= predicate; exclude), a "Tap to reproduce" label that gives the action away (acceptable: it is in the UI itself), setup description mentioning Overlay canSizeOverlay / unbounded constraints (diagnostic wording; exclude from snapshot). Comment 5696519316 (reporter) contains root-cause analysis with a source link and a fix proposal (exclude). Comment 5697323459 contains the same assertion text and "_RenderLayoutSurrogateProxyBox.performLayout" (exclude). Agent-visible candidate (NOT finalized): "Tapping the dropdown in this layout does not open its menu; an error appears" plus the reproduction as steps without technical cause. Source contains Overlay(canSizeOverlay)/UnconstrainedBox — the construct that triggers the bug is visible to a source-inspection capability (inherent to the MRE).

## potential_capability_gap
None for the tap itself. Requires get_runtime_errors to observe the primary evidence.
