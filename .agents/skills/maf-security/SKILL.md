---
name: maf-security
description: Threat-model, harden, or review Microsoft Agent Framework systems in C#/.NET for prompt injection, tenant isolation, tool approval, session protection, resource limits, data egress, telemetry privacy, authorization, and production readiness.
---

# MAF security

Read `../../references/application-boundaries.md`, `../../references/official-sources.md`, `references/security-checklist.md`, and the relevant capability-matrix row.

Treat user input, retrieved content, model output, tool arguments/results, MCP servers, remote agents, protocol metadata, uploaded media, continuation tokens, and persisted sessions as distinct untrusted boundaries. Prompts are not authorization or isolation controls.

Build controls in deterministic C#: authenticate callers; authorize resources and tool actions; partition state by tenant/user/workspace; validate structured outputs; constrain tools and egress; require occurrence-bound approval for consequential calls; set bounded time/token/tool/iteration/payload/concurrency/cost limits; make retryable side effects idempotent; and redact telemetry by default.

Agent Hooks and FIDES are not available for .NET as of the matrix verification date. Do not invent APIs. Use supported .NET agent/function/`IChatClient` middleware for interception plus application authorization, data classification, egress policy, and fail-closed tool gates.
