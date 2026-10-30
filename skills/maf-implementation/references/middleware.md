# Agent pipeline layers

Current MAF docs describe `ChatClientAgent` as a layered pipeline:

1. agent middleware;
2. context/history layer;
3. `IChatClient` pipeline, which can itself include middleware and function invocation behavior.

This matters because a concern should intercept the smallest meaningful surface.

Examples:

- redact user input before any agent processing → agent middleware;
- deny a tool argument based on tenant policy → function middleware/tool boundary;
- record model latency/token metadata → `IChatClient` instrumentation/middleware;
- inject user profile/runbook context → context provider, not middleware;
- deterministic multi-step process → workflow, not middleware.

## Reviewed 1.26 interception limits

Agent function callbacks cover tools registered on the agent or supplied through `ChatOptions.Tools`, including per-run tools. Functions placed directly in `FunctionInvokingChatClient.AdditionalTools` bypass that callback pipeline. Do not rely on agent middleware to authorize them; enforce authorization inside the tool or use a supported registration path.

For providers registered through the chat-client `UseAIContextProviders` decorator, contributed tools are not supported with agent-level function middleware as an enforcement boundary. A function-invoking client below that decorator is required to execute them; placing it above does not see those tools. This limitation concerns providers registered on that chat pipeline, not every agent context provider. See [tagged remarks](../../../resources/docs/capabilities/verification-1.26.md). Test each actual registration path, including a tool that must be denied.

## Responsibility and implementation guidance

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

Check Agent Hooks and FIDES separately. The matrix records a published .NET Agent Hooks alpha package and implementation in the `dotnet-1.24.0` tag despite Learn's Python-only statement; reconcile tagged package metadata and the application's installed APIs before selecting it. FIDES remains Python-only in the reviewed documentation/source. Do not copy Python imports or claim equivalent enforcement. Use supported .NET agent-run, function-invocation, or `IChatClient` middleware for application interception, backed by deterministic authorization, validation, egress controls and fail-closed tool gates. Read the conflict rule in the shared official-sources reference.

## Ordering

Middleware order can change semantics. Document ordering assumptions and test them when multiple middlewares transform/short-circuit calls.
