---
name: maf-middleware
description: Implement or review Microsoft Agent Framework middleware in C#/.NET. Use for agent-run middleware, function/tool invocation middleware, IChatClient middleware, runtime context, policy/validation/logging interception, or when deciding which pipeline layer should own a cross-cutting concern.
---

# MAF middleware

Read `../../resources/references/official-sources.md` and `references/pipeline-layers.md`.

## Choose the narrowest layer

MAF's agent pipeline distinguishes multiple interception layers. Do not create one generic middleware abstraction for everything.

### Agent-run middleware

Use when the concern applies to an entire agent invocation: input/output policy, run-level telemetry, correlation, top-level validation/transformation.

### Function-invocation middleware

Use when the concern is specifically tool calls: argument inspection, authorization guardrails, approval/audit, tool timing, result filtering.

### `IChatClient` middleware

Use when the concern applies to model-client calls regardless of agent behavior: model request/response instrumentation, provider-neutral chat policies, caching where safe, lower-level retries if appropriate.

## Runtime context/state

Use the narrowest supported runtime metadata surface. Current docs distinguish per-run `AgentRunOptions.AdditionalProperties`, function invocation context for tool-call arguments, and session state for conversation-scoped persistence.

Do not smuggle application dependencies through arbitrary dictionaries when DI/typed services are more appropriate.

## Avoid middleware abuse

Do not put core business workflows or hidden routing in middleware. Middleware should remain cross-cutting and composable.

## .NET availability boundary

Agent Hooks and Agent Security with FIDES are not available for .NET as of the versioned capability matrix. Do not copy Python imports or claim equivalent enforcement. Use supported .NET agent-run, function-invocation, or `IChatClient` middleware for interception, backed by deterministic authorization, validation, egress controls and fail-closed tool gates. Recheck the matrix and installed packages before changing this statement.

## Ordering

Middleware order can change semantics. Document ordering assumptions and test them when multiple middlewares transform/short-circuit calls.
