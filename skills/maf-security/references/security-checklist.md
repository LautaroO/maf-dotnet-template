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

## Agent Hooks evidence and limits

The [1.24 tagged factory](https://github.com/microsoft/agent-framework/blob/dotnet-1.24.0/dotnet/src/Microsoft.Agents.AI.AgentHooks/AgentHooksChatClientExtensions.cs) exposes `AsAIAgentWithAgentHooks` on `IChatClient`, while Learn still states Python-only. NuGet publishes the matching alpha package; verify installed package versions and APIs before using this factory. It composes enforcement across agent/model/function seams; custom middleware alone does not establish equivalent semantics. Buffered output changes streaming behavior. Provider-executed tools and service-owned durable history remain outside local pre-tool/persistence control. Sensitive request telemetry can observe pre-transform content. These are source-level boundaries, not production guarantees for an adopting host. FIDES availability is a separate question.

The reviewed [FIDES C# section](https://learn.microsoft.com/agent-framework/agents/security) says it is Python-only. .NET CodeAct host-function calls do not receive FIDES enforcement; authorization and destination controls belong inside those host tools even when generated code invokes them.
