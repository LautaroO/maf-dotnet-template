# Cross-cutting interception

Choose the narrowest supported boundary for a concern:

| Boundary | Typical concern |
|---|---|
| Whole agent invocation | Input/output policy, correlation, run telemetry |
| Tool/function invocation | Arguments, approval/audit, timing, result shaping |
| Model client | Provider-neutral request/response instrumentation or client policy |

Keep business process control and domain rules out of middleware. Prefer typed services/DI for dependencies rather than arbitrary dictionaries; use invocation and conversation metadata according to their lifetimes.

## Verify actual coverage

Order and short-circuit behavior can change semantics. Map where tools/context/providers are registered and test denied calls through those exact paths; one middleware registration does not demonstrate universal enforcement. Tools and application services must still enforce authority at execution.

When evaluating hooks or policy integrations, verify .NET availability, covered boundaries, interactions with streaming/context/hosted tools and ordering in the selected stack. Framework interception alone does not establish tenant isolation or data-egress policy.

Use [official-source investigation](../../../resources/references/official-sources.md) for precise decorators, callbacks, registration compatibility and ordering contracts; keep the result as project-specific implementation evidence instead of a plugin release catalog.
