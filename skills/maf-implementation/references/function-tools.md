# Bounded application capabilities

A tool adapts one application capability for model selection. Prefer a narrow query or action over a generic privileged command endpoint. Keep domain rules, authorization ownership and ordinary persistence in the application service the tool calls.

## Contract and authority

Describe what the capability does, its inputs and useful output precisely. Treat model arguments as untrusted. Resolve principal and tenant from trusted execution context; validate resource access and business invariants before accessing data or executing an effect. Bound payload, time, calls and returned data; redact internal or sensitive fields.

Propagate cancellation. Choose retry ownership and business idempotency deliberately for effects. Tool descriptions and prompts influence selection; they cannot enforce permissions. Test the actual invocation paths, including middleware, hosted execution and direct calls where used.

## Framework mapping

Look for the installed MAF/MEAI function-tool abstractions before creating a custom registry. `AIFunction` and `AITool` are conceptual search terms. A specialist agent may also expose a bounded semantic capability; required process order remains a workflow responsibility.

A retrieval tool returns authorized source snippets and provenance, not a raw database client. A cancellation tool calls an application use case, not an instruction-driven admin switch.

Test validation, denied access, cancellation, failure mapping, bounded output and idempotency without a live model. Find exact binding, metadata and invocation APIs using [official-source investigation](../../../resources/references/official-sources.md).
