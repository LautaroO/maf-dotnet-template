# Security and production-readiness checklist

- Draw trust boundaries across caller, host/protocol, agent, provider, retrieval, tools/MCP/remote agents, state stores and telemetry.
- Test indirect prompt injection from every retrieved or tool-provided payload; never let content expand tool authority.
- Bind sessions, tasks, checkpoints, approvals and uploaded files to authenticated tenancy; reject caller-selected cross-tenant identifiers.
- Give each tool the minimum capability and validate arguments, resource ownership and business authorization at invocation time.
- Bind approval to the exact tool-call occurrence and display material arguments/effects; do not reuse vague prior consent.
- Allowlist destinations and credentials; constrain uploads, MIME types, URI fetches, archive extraction, scripts and generated code.
- Bound input/output size, context, iterations, tool calls, parallelism, time, retries, spend and retained state.
- Encrypt/protect state and secrets, define retention/deletion, and avoid sensitive prompt/tool bodies in default telemetry.
- Exercise cancellation, partial failure, resume, replay, duplicate delivery, provider refusal, quota exhaustion and incident revocation.

## Reviewed 1.25–1.26 enforcement boundaries

Standing approvals survive in session state across agent/tool-instance changes; review or reset them when the tool set or MCP provenance changes. Automatic rejection occurs on the next underlying run with binding enabled, not on a wall-clock timeout. Duplicate active request IDs must fail closed. See [approval guidance](mcp-and-approval.md).

Check middleware coverage for every registration path: FICC `AdditionalTools` bypass agent callbacks, and chat-pipeline context-provider tools have specific unsupported interception combinations. Keep authorization inside tools; see [pipeline limits](middleware.md). DevUI local checks/token scope do not secure a public proxy or every execution route; see [DevUI security](devui.md).

Purview 1.25 includes text/reasoning annotations, error details and data names in checks; evaluate those payloads and egress when selecting that adapter. Docker shell 1.26 renames `ExtraRunArgs` to `UnsafeExtraRunArgs`: only trusted developer configuration may supply those options, since they can weaken isolation. Model-facing commands must not control Docker flags. Container defaults and prompt consent are not sufficient isolation guarantees. Sources: [scoped review](../../../resources/docs/capabilities/verification-1.26.md).

## Agent Hooks evidence and limits

The [1.24 tagged factory](https://github.com/microsoft/agent-framework/blob/dotnet-1.24.0/dotnet/src/Microsoft.Agents.AI.AgentHooks/AgentHooksChatClientExtensions.cs) exposes `AsAIAgentWithAgentHooks` on `IChatClient`, while Learn still states Python-only. NuGet publishes the matching alpha package; verify installed package versions and APIs before using this factory. It composes enforcement across agent/model/function seams; custom middleware alone does not establish equivalent semantics. Buffered output changes streaming behavior. Provider-executed tools and service-owned durable history remain outside local pre-tool/persistence control. Sensitive request telemetry can observe pre-transform content. These are source-level boundaries, not production guarantees for an adopting host. FIDES availability is a separate question.

The reviewed [FIDES C# section](https://learn.microsoft.com/agent-framework/agents/security) says it is Python-only. .NET CodeAct host-function calls do not receive FIDES enforcement; authorization and destination controls belong inside those host tools even when generated code invokes them.

## Responsibility and implementation guidance

Treat user input, retrieved content, model output, tool arguments/results, MCP servers, remote agents, protocol metadata, uploaded media, continuation tokens, and persisted sessions as distinct untrusted boundaries. Prompts are not authorization or isolation controls.

Build controls in deterministic C#: authenticate callers; authorize resources and tool actions; partition state by tenant/user/workspace; validate structured outputs; constrain tools and egress; require occurrence-bound approval for consequential calls; set bounded time/token/tool/iteration/payload/concurrency/cost limits; make retryable side effects idempotent; and redact telemetry by default.

Verify Agent Hooks and FIDES independently. The `dotnet-1.24.0` source and NuGet index establish a published .NET Agent Hooks alpha package while Learn still says Python-only; report the discrepancy and verify installed package versions and APIs before adoption. This does not establish .NET FIDES support. Do not invent APIs or describe alpha source as stable production support. Use supported .NET agent/function/`IChatClient` middleware for application interception plus authorization, data classification, egress policy, and fail-closed tool gates. Follow the shared official-sources conflict rule.
