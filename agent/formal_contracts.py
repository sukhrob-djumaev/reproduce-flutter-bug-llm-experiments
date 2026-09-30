"""Versioned, non-scoring data contracts for future formal evaluation runs."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class StrictContract(BaseModel):
    """Reject accidental, undocumented fields in versioned research records."""

    model_config = ConfigDict(extra="forbid")


class RuntimeErrorReason(StrictContract):
    """A typed reason why runtime-error evidence was not observed."""

    code: str
    message: str


class RuntimeErrorScope(StrictContract):
    """The app session and explicit window covered by one observation."""

    app_session_id: str
    since: str
    until: str
    clear_before_observation: bool


class RuntimeErrorItem(StrictContract):
    """One normalized runtime error with a private raw-evidence reference."""

    category: str
    message: str
    timestamp: str | None = None
    raw_evidence_ref: str


class RuntimeErrorObservation(StrictContract):
    """The compact, model-facing runtime-error evidence contract, version 1."""

    schema_version: Literal["1"] = "1"
    observation_id: str
    scope: RuntimeErrorScope
    status: Literal["observed", "unavailable", "tool_error"]
    error_count: int | None = Field(default=None, ge=0)
    errors: list[RuntimeErrorItem] = Field(default_factory=list)
    reason: RuntimeErrorReason | None = None

    @model_validator(mode="after")
    def validate_status_fields(self) -> "RuntimeErrorObservation":
        """Keep observed, unavailable, and tool-error states unambiguous."""
        if self.status == "observed":
            if self.reason is not None:
                raise ValueError("observed runtime evidence cannot include a failure reason")
            if self.error_count != len(self.errors):
                raise ValueError("observed error_count must equal len(errors)")
        elif self.reason is None:
            raise ValueError(f"{self.status} runtime evidence requires a typed reason")
        elif self.error_count is not None or self.errors:
            raise ValueError(
                f"{self.status} runtime evidence must not masquerade as observed errors"
            )
        return self


class GroundTruthPredicate(StrictContract):
    """Curator-owned observable predicate, never an automated score."""

    description: str
    evaluation_method: str


class ManualVerification(StrictContract):
    """Manual curator verification state for a hidden ground-truth record."""

    verified: bool
    verification_date: str | None = None
    verifier_id: str
    notes: str


class GroundTruthRecord(StrictContract):
    """Version 1 curator-only record; do not load it into agent execution."""

    schema_version: Literal["1"] = "1"
    record_purpose: Literal["formal_ground_truth", "format_validation_example"]
    case_id: str
    source_repository: str
    issue_reference: str
    case_git_revision: str
    issue_snapshot_path_or_hash: str
    flutter_version: str
    dart_version: str
    platform: str
    setup_instructions: str
    reproduction_predicate: GroundTruthPredicate
    expected_observable_evidence: list[str]
    defect_class: Literal[
        "unhandled_exception",
        "incorrect_application_state",
        "structural_rendering_fault",
        "silent_error_condition",
    ]
    subtype: str
    manual_verification: ManualVerification


class FormalRunIdentity(StrictContract):
    run_id: str
    study_id: str
    case_id: str
    trial_number: int = Field(ge=1)
    started_at_utc: str
    ended_at_utc: str


class FormalCaseMetadata(StrictContract):
    repository_url: str
    pinned_git_revision: str
    entry_point: str
    issue_snapshot_identifier: str
    issue_snapshot_sha256: str


class PromptMetadata(StrictContract):
    version: str
    sha256: str


class ModelMetadata(StrictContract):
    name: str
    provider: str
    endpoint_class: str
    model_version_identifier: str
    temperature: float | None = None
    top_p: float | None = None
    seed: int | None = None
    settings: dict[str, Any] = Field(default_factory=dict)


class FrameworkMetadata(StrictContract):
    pydantic_ai_version: str
    python_version: str
    dependency_lock_or_hash: str | None = None


class RuntimeMetadata(StrictContract):
    flutter_version: str
    dart_version: str
    mcp_tool_versions: dict[str, str]
    os: str
    device: str
    platform_api_version: str
    architecture: str
    environment_image_or_version: str | None = None


class CapabilityMetadata(StrictContract):
    condition: str
    tool_manifest_version: str
    tool_manifest_sha256: str


class BudgetMetadata(StrictContract):
    max_turns: int | None = Field(default=None, ge=1)
    max_steps: int | None = Field(default=None, ge=1)
    max_duration_seconds: float | None = Field(default=None, gt=0)


class FormalResultMetadata(StrictContract):
    duration_seconds: float = Field(ge=0)
    turns: int = Field(ge=0)
    typed_final_status: Literal["REPRODUCED", "NOT_REPRODUCED", "INCONCLUSIVE"]
    exact_evidence: str


class FormalToolEvent(StrictContract):
    """Required auditable metadata for one model-facing tool event."""

    event_id: str
    tool_name: str
    tool_version: str
    timestamp_utc: str
    duration_seconds: float = Field(ge=0)
    outcome: Literal["success", "tool_error", "timeout", "transport_error"]
    content_reference_hash: str
    raw_arguments_reference: str | None = None
    raw_output_reference: str | None = None
    redaction_reason: str | None = None


class TraceMetadata(StrictContract):
    raw_trace_reference: str
    tool_event_trace_reference: str
    tool_events: list[FormalToolEvent] = Field(default_factory=list)
    retained_evidence_references: list[str] = Field(default_factory=list)


class ExecutionMetadata(StrictContract):
    scoreability: Literal["pending", "scoreable", "infrastructure_excluded"]
    exclusion_cause: str | None = None

    @model_validator(mode="after")
    def validate_exclusion_cause(self) -> "ExecutionMetadata":
        if self.scoreability == "infrastructure_excluded" and not self.exclusion_cause:
            raise ValueError("infrastructure_excluded execution requires an exclusion cause")
        if self.scoreability != "infrastructure_excluded" and self.exclusion_cause:
            raise ValueError("only infrastructure_excluded execution may include an exclusion cause")
        return self


class FormalRunMetadata(StrictContract):
    """Version 1 run sidecar; it intentionally excludes hidden ground truth."""

    storage_schema_version: Literal["1"] = "1"
    identity: FormalRunIdentity
    case: FormalCaseMetadata
    prompt: PromptMetadata
    model: ModelMetadata
    framework: FrameworkMetadata
    runtime: RuntimeMetadata
    capability: CapabilityMetadata
    budgets: BudgetMetadata
    result: FormalResultMetadata
    trace: TraceMetadata
    execution: ExecutionMetadata
