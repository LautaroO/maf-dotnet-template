# External tools and consequential-action approval

MCP is an interoperability boundary for external capabilities. Expose only the capabilities the task needs. Review server provenance, credentials, destination access, descriptions, argument/result data and side effects; remote content cannot expand local authority.

## Approval as an execution contract

For actions whose consequences require approval, bind the decision to the principal, intended invocation, material arguments and relevant session/resource scope. Define expiry, rejection, cancellation and recovery behavior. Revalidate authorization at execution and use a business idempotency key for retried/resumed effects.

Approval does not replace resource authorization or make history persistence atomic with a business transaction. Define how unanswered, partial, late or changed decisions are handled and test those requirements against the selected runtime. Reassess reusable approvals when capability provenance or authority changes.

## Integration verification

Check approval propagation through actual model/provider, MCP, middleware and hosting paths. Test that denial and fabricated/replayed responses cannot execute a protected action. Protect credentials/headers and constrain allowed destinations. Treat long-running external tasks as explicit lifecycle/continuation contracts with bounded waits and cancellation.

Use supported framework/SDK mechanisms where they meet the contract rather than rebuilding a gate in prompts. The exact approval types, pending-request semantics, persistence rules and transport extensions must be checked through [official-source investigation](../../../resources/references/official-sources.md) for the target stack.
