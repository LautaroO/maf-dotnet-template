---
name: maf-implementation
description: Use when implementing or changing MAF .NET agents, tools, workflows, context, provider integrations, middleware, hosting or debugging surfaces against a new or existing application's package APIs.
---

# Implement a MAF design

Implement the requested behavior in its existing architectural boundaries. Start with a proportional assessment of relevant code/design: resolve material gaps, reuse settled decisions and proceed on adequate authorized work. For gap criteria or an active design process consult [agent design](../../resources/references/agent-design.md) or [process integration](../../resources/references/process-integration.md); a small edit needs no full architectural workflow or adoption.

Identify actual SDK/projects and installed NuGet APIs before choosing signatures. In a new solution, label package proposals and verify the selected stack when available. Use [official sources](../../resources/references/official-sources.md) for API evidence and limitations; do not silently upgrade pinned packages or claim untested compilation.

## Read only references needed by this change

| Topic | Reference |
|---|---|
| Agents, structured/multimodal/streaming runs, runtime skills/Harness | [Agents](references/agents.md) |
| Local bounded capabilities | [Function tools](references/function-tools.md) |
| MCP, approval and replay | [MCP and approval](references/mcp-and-approval.md) |
| Typed graphs, routing and executors | [Executors and edges](references/executors-edges.md) |
| Multi-agent composition and handoff | [Orchestrations](references/orchestrations.md) |
| State, checkpoints, durable waits and HITL | [State and recovery](references/state-checkpoints-hitl.md) |
| Sessions, context providers, retrieval/compaction | [Context and memory](references/context-memory.md) |
| Agent/function/model interception | [Middleware](references/middleware.md) |
| Provider construction/capabilities | [Providers](references/providers.md) |
| Runtime operation and protocols | [Hosting](references/hosting.md) |
| Threat boundaries and enforcement | [Security](references/security.md) |
| Instrumentation and telemetry privacy | [Observability](references/observability.md) |
| Local discovery/graph/debug surface | [DevUI](references/devui.md) |

For problem-oriented alternatives consult [patterns](../../resources/docs/patterns/v4.md). Keep domain rules, authorization and ordinary persistence in application services; tools/executors adapt or orchestrate them. Preserve provider-neutral contracts, validated typed model output, cancellation, bounded execution and idempotent effects. Existing reference version notes are scoped evidence, not universal guarantees for installed packages.

Verify behavior at affected deterministic boundaries, with semantic quality evaluated separately. Report the selected abstraction, changes/checks, provider coupling and specific remaining API/runtime uncertainty. Consult testing or review skills when the task actually calls for them.
