"""Contract-level checks for Stage 11 formal-readiness infrastructure."""

from __future__ import annotations

import json
from pathlib import Path
import sys
import tempfile
import unittest


PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "agent"))

from formal_contracts import (  # noqa: E402
    FormalRunMetadata,
    GroundTruthRecord,
    RuntimeErrorObservation,
)
import results  # noqa: E402
from tools import FlutterRuntimeAdapter  # noqa: E402


class FormalReadinessContractTests(unittest.TestCase):
    def test_ground_truth_template_and_synthetic_example_validate(self) -> None:
        """Curator records are versioned and not part of the agent input directory."""
        template_path = PROJECT_ROOT / "curation" / "ground_truth" / "ground_truth_record_template.json"
        example_path = (
            PROJECT_ROOT
            / "curation"
            / "ground_truth"
            / "examples"
            / "synthetic_case_001_format_validation.json"
        )
        template = GroundTruthRecord.model_validate_json(template_path.read_text())
        example = GroundTruthRecord.model_validate_json(example_path.read_text())

        self.assertEqual(template.schema_version, "1")
        self.assertEqual(example.record_purpose, "format_validation_example")
        self.assertTrue(str(example_path).startswith(str(PROJECT_ROOT / "curation")))
        self.assertFalse(str(example_path).startswith(str(PROJECT_ROOT / "issues")))
        self.assertFalse(str(example_path).startswith(str(PROJECT_ROOT / "results")))

    def test_no_runtime_error_marker_is_not_an_error_entry(self) -> None:
        """Structured no-error text becomes the exact observed no-error shape."""
        adapter = FlutterRuntimeAdapter(object())
        adapter._runtime_session_id = "session-1"
        adapter._runtime_error_window_started_at = "2026-09-30T00:00:00Z"
        observation = adapter._runtime_observation_from_raw(
            json.dumps([{"type": "text", "text": "No runtime errors found."}])
        )

        self.assertEqual(observation.status, "observed")
        self.assertEqual(observation.error_count, 0)
        self.assertEqual(observation.errors, [])
        self.assertNotIn("No runtime errors found.", observation.model_dump_json())

    def test_real_runtime_error_has_consistent_count_and_audit_reference(self) -> None:
        """A CASE_002-shaped error is retained as typed observed evidence."""
        adapter = FlutterRuntimeAdapter(object())
        adapter._runtime_session_id = "session-2"
        adapter._runtime_error_window_started_at = "2026-09-30T00:00:00Z"
        raw = json.dumps(
            [
                {"type": "text", "text": "Found 1 error:\n"},
                {
                    "type": "text",
                    "text": (
                        "renderedErrorText: The following StateError was thrown.\n"
                        "Bad state: A name is required.\n"
                    ),
                },
            ]
        )
        observation = adapter._runtime_observation_from_raw(raw)

        self.assertEqual(observation.status, "observed")
        self.assertEqual(observation.error_count, len(observation.errors))
        self.assertEqual(observation.error_count, 1)
        self.assertEqual(observation.errors[0].category, "StateError")
        self.assertEqual(observation.errors[0].message, "Bad state: A name is required.")
        self.assertIn("tool_events.json#sha256:", observation.errors[0].raw_evidence_ref)

    def test_unavailable_and_tool_error_require_reasons(self) -> None:
        """Failure states cannot be silently represented as zero errors."""
        with self.assertRaises(ValueError):
            RuntimeErrorObservation.model_validate(
                {
                    "observation_id": "missing-reason",
                    "scope": {
                        "app_session_id": "session",
                        "since": "2026-09-30T00:00:00Z",
                        "until": "2026-09-30T00:00:01Z",
                        "clear_before_observation": False,
                    },
                    "status": "unavailable",
                }
            )

    def test_persistence_accepts_a_complete_formal_metadata_sidecar(self) -> None:
        """Future formal runs can persist complete metadata without hidden ground truth."""
        metadata = FormalRunMetadata.model_validate(
            {
                "identity": {
                    "run_id": "formal-run-001",
                    "study_id": "study-v1",
                    "case_id": "PUB-001",
                    "trial_number": 1,
                    "started_at_utc": "2026-09-30T00:00:00Z",
                    "ended_at_utc": "2026-09-30T00:01:00Z",
                },
                "case": {
                    "repository_url": "https://example.invalid/repository",
                    "pinned_git_revision": "abc123",
                    "entry_point": "lib/main.dart",
                    "issue_snapshot_identifier": "issue-PUB-001",
                    "issue_snapshot_sha256": "sha256:abc",
                },
                "prompt": {"version": "v1", "sha256": "sha256:prompt"},
                "model": {
                    "name": "candidate-model",
                    "provider": "provider",
                    "endpoint_class": "local-openai-compatible",
                    "model_version_identifier": "candidate-model@1",
                    "temperature": 0.0,
                    "top_p": 1.0,
                    "seed": None,
                    "settings": {"tool_choice": "auto"},
                },
                "framework": {
                    "pydantic_ai_version": "2.51.0",
                    "python_version": "3.12.13",
                    "dependency_lock_or_hash": "sha256:requirements",
                },
                "runtime": {
                    "flutter_version": "3.47.1",
                    "dart_version": "3.13.1",
                    "mcp_tool_versions": {"dart_mcp_server": "1.1.2"},
                    "os": "macOS",
                    "device": "android-emulator",
                    "platform_api_version": "API 29",
                    "architecture": "arm64",
                    "environment_image_or_version": "evaluation-image-v1",
                },
                "capability": {
                    "condition": "FULL",
                    "tool_manifest_version": "1",
                    "tool_manifest_sha256": "sha256:manifest",
                },
                "budgets": {"max_turns": 20, "max_steps": 20, "max_duration_seconds": 300},
                "result": {
                    "duration_seconds": 60,
                    "turns": 4,
                    "typed_final_status": "INCONCLUSIVE",
                    "exact_evidence": "The retained evidence was insufficient.",
                },
                "trace": {
                    "raw_trace_reference": "trace.json",
                    "tool_event_trace_reference": "tool_events.json",
                    "tool_events": [
                        {
                            "event_id": "tool-001",
                            "tool_name": "get_runtime_errors",
                            "tool_version": "dart_mcp_server@1.1.2",
                            "timestamp_utc": "2026-09-30T00:00:30Z",
                            "duration_seconds": 0.2,
                            "outcome": "success",
                            "content_reference_hash": "sha256:response",
                            "raw_arguments_reference": "tool_events.json#tool-001-args",
                            "raw_output_reference": "tool_events.json#tool-001-output",
                            "redaction_reason": None,
                        }
                    ],
                    "retained_evidence_references": ["evidence/runtime-errors.json"],
                },
                "execution": {"scoreability": "pending", "exclusion_cause": None},
            }
        )
        original_runs_directory = results.RUNS_DIRECTORY
        original_summary_path = results.SUMMARY_PATH
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_root = Path(temporary_directory)
            results.RUNS_DIRECTORY = temporary_root / "runs"
            results.SUMMARY_PATH = temporary_root / "summary.csv"
            results.SUMMARY_PATH.write_text(
                ",".join(results.SUMMARY_FIELDS) + "\n", encoding="utf-8"
            )
            try:
                _, result_path, _ = results.persist_run(
                    case="001",
                    model="candidate-model",
                    capabilities="FULL",
                    status="INCONCLUSIVE",
                    evidence="The retained evidence was insufficient.",
                    duration_seconds=60,
                    turns=4,
                    messages_json="[]",
                    tool_events=[
                        {
                            "event_id": "mcp-0001",
                            "tool_name": "get_runtime_errors",
                            "output": "raw Dart MCP response",
                        }
                    ],
                    formal_metadata=metadata,
                )
            finally:
                results.RUNS_DIRECTORY = original_runs_directory
                results.SUMMARY_PATH = original_summary_path

            run_directory = result_path.parent
            self.assertTrue((run_directory / "tool_events.json").is_file())
            persisted_metadata = json.loads(
                (run_directory / "formal_metadata.json").read_text(encoding="utf-8")
            )
            self.assertEqual(persisted_metadata["storage_schema_version"], "1")
            self.assertNotIn("ground_truth", persisted_metadata)


if __name__ == "__main__":
    unittest.main()
