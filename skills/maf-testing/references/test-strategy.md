# Test strategy examples

## Agent-backed executor

Split the executor from the semantic dependency where practical:

```text
Workflow executor
   -> ITranslator / AIAgent adapter
   -> typed TranslationResult
```

Test executor transition logic with a fake semantic result. Test the actual agent prompt/model separately.

## Tool

Test:

- schema/argument validation;
- authorization;
- cancellation;
- timeout/failure mapping;
- idempotency;
- redacted/bounded return shape.

## Context provider

Test which context is selected/injected for known inputs without invoking the model.

## Session

Test conversation isolation, persistence/restore semantics, expiration if application-owned, and absence of cross-user leakage.

Checkpoint regression tests must rebuild the workflow with stable local agent role IDs/names and compare topology. Include changed identity/topology rejection and a fresh lineage for incompatible old checkpoints. Background child task metadata restoration must not be mistaken for restoration of the in-process task handle.

For upgrades through 1.24, include null-vs-absent state roundtrips, independent restored session instances and disabled recent-search memory. Approval tests should cover same-session resume, denial, forged/unbound responses, replay, changed arguments/tools, provider-backed MCP invocation isolation and the DevUI hosted continuation path. Use fake model/tool results for deterministic gates; reserve live-provider checks for separately requested integration/evaluation runs. Consult the release-sensitive notes in the owning references before asserting that an old/new package behaves identically.
