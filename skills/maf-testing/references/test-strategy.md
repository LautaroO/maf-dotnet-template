# Deterministic contracts and semantic evaluation

Test the application's enforced behavior independently of a live model. Replace only semantic collaborators with controlled results; preserve actual validators, authorization, routing and storage boundaries in the tests.

- Tools: arguments, caller/tenant/resource access, bounds, cancellation, failure mapping and result shaping; effect idempotency when applicable.
- Workflow steps: typed branches/defaults, invalid output, retry ownership, partial failure and concurrency.
- Context/retrieval: authorized corpus selection, provenance and bounded injection; evaluate retrieval quality separately from answer quality.
- Conversation/state: isolation, retention, serialization, restore and concurrent access according to the chosen contract.
- Recovery/approval: restarts, incompatible deployment, expired/changed decisions, duplicate delivery and authorization revalidation.
- Hosting/streaming: actual entry paths, disconnect/cancellation, partial output, continuation and route-specific access controls.
- Instrumentation/adapters: behavior preservation, explicit capability fallback, privacy and failure translation.

Tests assert the project's required behavior, not remembered SDK defaults. Before depending on a concrete MAF contract, use [official-source investigation](../../../resources/references/official-sources.md) and verify against installed packages. Keep real-provider compatibility tests and model-quality evaluations opt-in, with representative datasets and explicit budgets. A label edit does not need a new testing program.
