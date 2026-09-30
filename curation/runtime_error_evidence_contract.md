# Runtime-error evidence contract, version 1

The model-facing return from `get_runtime_errors()` is a compact `RuntimeErrorObservation` JSON object. It is always one of `observed`, `unavailable`, or `tool_error`.

- `observed` has `error_count == len(errors)`. A no-error observation is exactly `error_count: 0` and `errors: []`.
- `unavailable` and `tool_error` have a typed `reason`; neither represents absence of errors.
- Before the agent invocation, the adapter reads and clears pre-existing runtime errors. The reported scope records that start point, the active app-session identifier, the end time, and `clear_before_observation: true`.
- The raw Dart MCP response and call arguments are retained in the private `tool_events.json` audit trace. They are never returned in the model-facing observation.
- Error entries preserve source order. No de-duplication is performed: each normalized entry points to its source response hash and fragment index, so repeated errors remain auditable.

The contract reports evidence only. It neither changes the agent's decision logic nor interprets a runtime error as proof of reproduction.
