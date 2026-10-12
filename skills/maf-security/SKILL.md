---
name: maf-security
description: Threat-model, harden, or review Microsoft Agent Framework systems in C#/.NET for prompt injection, tenant isolation, tool approval, session protection, resource limits, data egress, telemetry privacy, authorization, and production readiness.
---

# MAF security

Read `../../resources/references/application-boundaries.md`, `../../resources/references/official-sources.md`, `references/security-checklist.md`, and the relevant capability-matrix row.

Treat user input, retrieved content, model output, tool arguments/results, MCP servers, remote agents, protocol metadata, uploaded media, continuation tokens, and persisted sessions as distinct untrusted boundaries. Prompts are not authorization or isolation controls.

Build controls in deterministic C#: authenticate callers; authorize resources and tool actions; partition state by tenant/user/workspace; validate structured outputs; constrain tools and egress; require occurrence-bound approval for consequential calls; set bounded time/token/tool/iteration/payload/concurrency/cost limits; make retryable side effects idempotent; and redact telemetry by default.

Verify Agent Hooks and FIDES independently. The `dotnet-1.24.0` source and NuGet index establish a published .NET Agent Hooks alpha package while Learn still says Python-only; report the discrepancy and verify installed package versions and APIs before adoption. This does not establish .NET FIDES support. Do not invent APIs or describe alpha source as stable production support. Use supported .NET agent/function/`IChatClient` middleware for application interception plus authorization, data classification, egress policy, and fail-closed tool gates. Follow the shared official-sources conflict rule.
