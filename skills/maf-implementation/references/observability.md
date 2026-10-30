# Evidence across agentic boundaries

Separate instrumentation from exporters/collectors and UI presentation. Instrument meaningful agent, model, tool, workflow and external-dependency boundaries without duplicating spans. A debug UI and an OTLP destination have different evidence paths.

## Trace useful outcomes

Preserve correlation through requests, queues and resumed work. Capture cancellation, retry/repair, validation/approval decisions, retrieval outcomes, recovery and limit events at a safe metadata level. Define the signals needed for success, latency, stuck work and usage/cost objectives.

Sensitive prompt/tool bodies are opt-in according to environment/privacy policy; use redacted metadata by default. Let an incident responder connect a user-visible failure to relevant agent/provider/tool/workflow evidence without routinely exposing payloads.

## Verify transparent instrumentation

A telemetry decorator must preserve the application's observable behavior: outputs, errors, cancellation, stream progression and continuation when supported. Test important decorated/undecorated paths with controllable collaborators. Export success alone does not demonstrate correct agent behavior.

Use [official-source investigation](../../../resources/references/official-sources.md) for concrete instrumentation registration, source/meter names, continuation and trace delivery. This reference defines what to observe and preserve, not an SDK fix history.
