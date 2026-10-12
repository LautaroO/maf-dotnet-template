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
