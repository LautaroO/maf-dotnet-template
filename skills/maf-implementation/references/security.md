# Deterministic authority and trust boundaries

Treat user input, retrieved content, model output, tool arguments/results, remote servers/agents, media, protocol identifiers and persisted state as distinct untrusted inputs. Prompts guide semantics; code enforces authority and product invariants.

## Bound privileges and data

Authenticate callers and authorize resources at tool/service execution and state lookup. Derive tenant/user scope from trusted context. Validate typed outputs before control decisions; constrain available capabilities, network destinations and payloads. Retrieved instructions cannot grant permissions.

Require action approval where consequences warrant it, bind the decision to its invocation and scope, revalidate at execution and make effects idempotent. Protect continuation tokens and persisted state; define retention and deletion across all relevant stores.

Bound time, calls, loops, concurrency, context, files and cost. Keep secrets out of model-facing arguments and redact telemetry by default. Model-facing commands cannot control infrastructure privileges or sandbox configuration; validate actual isolation and egress rather than infer it from a container or prompt.

## Verify enforcement instead of assuming it

Test denied and adversarial inputs at real entry points, including alternate registrations, hosted tools and resumed actions. Evaluate prompt injection separately from deterministic access control. A middleware or policy hook's availability does not establish equivalent enforcement across all paths.

For selected .NET security integrations, supported interception and sandbox/host defaults, consult [official-source investigation](../../../resources/references/official-sources.md). This guide supplies architectural controls, not a current compatibility or security-certification matrix.
