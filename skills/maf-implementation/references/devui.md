# Development UI and diagnostic hosts

Distinguish a product/CLI experience, an opinionated agent runtime, a local development UI and a telemetry backend. DevUI helps inspect/discover/run supported agent or workflow entities; it does not determine the product's core architecture.

## Keep debug integration thin

Preserve reusable agent/workflow identity and typed contracts. Register native graph entities when graph inspection is the requirement, using workflow-as-agent only when agent invocation semantics are independently needed. Avoid duplicate logical entities.

A typed workflow input may need a host adapter for a chat-oriented execution surface. Test native execution and the actual hosted entry path separately rather than stringify internal state just to satisfy the UI. Verify entity discovery, graph visibility, cancellation, errors and approval continuation where required.

## Security and traces

Treat the UI as a trusted development surface. Choose deliberate network exposure and authentication policy; verify protection for each execution route rather than assume a UI token or proxy protects all mapped endpoints. Development conveniences do not certify production access control.

Check instrumentation delivery to the UI separately from external telemetry export and keep sensitive-data capture controlled.

Find current .NET registration, discovery/execute protocols, security defaults and trace integration through [official-source investigation](../../../resources/references/official-sources.md). Exact endpoints, options and adapter limitations belong to the selected project stack, not this conceptual guide.
