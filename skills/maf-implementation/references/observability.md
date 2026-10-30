# OpenTelemetry notes

MAF integrates with OpenTelemetry / GenAI semantic conventions. Current C# docs show instrumentation on provider-neutral chat clients via builder extensions such as `UseOpenTelemetry(...)` and agent/workflow instrumentation through their supported APIs.

Exact source names/extensions evolve. Inspect installed packages before hardcoding them.

The [1.22 release](https://github.com/microsoft/agent-framework/releases/tag/dotnet-1.22.0) exposes `OpenTelemetryAgent.DefaultSourceName`. Prefer the installed constant when available; keep a version-appropriate fallback rather than assuming this API exists in older packages.

Verification should answer separately:

1. are spans/metrics/logs being created?;
2. is the host subscribed?;
3. is the exporter configured?;
4. does the target backend receive them?;
5. does DevUI receive/show traces if DevUI is being used?

The reviewed 1.25 `OpenTelemetryAgent` fixes preservation of agent-level continuation tokens and response/update identity through its chat-client instrumentation bridge. Test both streaming and non-streaming continuation with and without the decorator; resume with the agent token, not a substituted raw provider token. Telemetry delivery alone does not verify continuation. See [tagged evidence](../../../resources/docs/capabilities/verification-1.26.md).

## Responsibility and implementation guidance

## Separate instrumentation from destination

MAF/AI components emit telemetry; OpenTelemetry providers/exporters decide where it goes.

Do not conflate:

- enabling agent/chat/workflow instrumentation;
- subscribing to relevant `ActivitySource`/meters;
- exporting OTLP to Aspire/Jaeger/other backend;
- DevUI-specific trace rendering.

## Instrument meaningful boundaries

Capture enough to diagnose:

- agent run;
- model calls;
- tool calls;
- workflow/executor transitions;
- external dependencies;
- retries/errors/cancellation;
- latency and usage metadata where supported.
- retrieval queries/results at safe metadata granularity, grounding/citation outcomes, approval decisions, continuation/checkpoint transitions, queue/wait time, duplicate suppression, safety/limit events, and cost where available.

Avoid duplicate spans from instrumenting the same layer twice.

## Sensitive data

Prompt/tool payload capture can contain PII, secrets, business data, or retrieved content. Keep sensitive-data telemetry opt-in and environment-specific. Redact/log IDs and metadata by default when possible.

## Correlation

Preserve trace/correlation context through agents, tools, workflows, HTTP calls, and background/durable boundaries. For queued/resumed executions, design correlation explicitly.

Define operational SLOs and alerts for success, latency, streaming first-event time, tool/retrieval failures, safety denials, stuck background work, checkpoint/resume failures and spend. Document how an incident responder can move from a user-visible failure to the relevant agent, provider, tool and workflow evidence without enabling sensitive-body capture by default.
