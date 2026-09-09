---
name: maf-observability
description: Configure or review Microsoft Agent Framework observability in C#/.NET using OpenTelemetry for agents, IChatClient calls, tools, workflows, executors, logs, metrics, traces, sensitive-data settings, OTLP export, and correlation. Use when debugging or instrumenting MAF runtime behavior; pair with maf-devui for DevUI-specific trace display.
---

# MAF observability

Read `../../references/official-sources.md` and `references/otel.md`.

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
