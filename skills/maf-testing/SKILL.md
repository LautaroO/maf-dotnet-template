---
name: maf-testing
description: Use when designing tests or evaluations for MAF .NET behavior, including agents, tools, workflows, state, integration boundaries and semantic quality.
---

# MAF testing

Use [test strategy](references/test-strategy.md) for deterministic behavior and [evaluation](references/evaluation.md) for semantic quality. Scale verification to the change and follow the active project process; a label edit does not need a new evaluation program.

## Testing pyramid

Prefer this order:

1. deterministic domain/service tests;
2. tool wrapper + validator tests;
3. workflow executor and routing tests;
4. middleware/context/session behavior tests;
5. provider-adapter integration tests;
6. MAF hosting/DevUI smoke tests;
7. opt-in real-model evaluation tests.

The default test suite should not depend on network, paid model calls, or nondeterministic language output.

## Workflow tests

Assert graph behavior from typed inputs/outputs/events. Test all branches/defaults, retry limits, cancellation, idempotency, and state isolation. Replace only semantic agent steps with controllable fakes/stubs.

## Structured output

Test valid, invalid, missing, unknown enum, out-of-range, and malicious values after deserialization. The model schema is not a substitute for validator tests.

## Provider tests

Keep provider-specific tests focused on adapter construction, supported capabilities, streaming/tool/structured-output compatibility, and failure translation. Mark live-provider tests opt-in.

## Model evaluations

Use evaluations for semantic quality: task success, groundedness, tool selection, hallucination, safety, latency/cost. Do not turn flaky model judgments into the only CI gate for deterministic behavior.

Keep a baseline dataset and record provider/model/configuration. Evaluate retrieval recall/precision and citation correctness separately from answer quality. Include adversarial prompt-injection, cross-tenant access, approval, resource-limit and data-egress cases.

For streaming and durability, test event ordering/projection, disconnect, cancellation, resume, continuation expiry, checkpoint compatibility, duplicate delivery, idempotency and restart/deployment recovery. Track latency percentiles and cost/usage budgets, not only averages.
