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

## Scoped 1.25–1.26 application regression gates

These are tests for adopting applications using the affected APIs, not claims that this skills-only repository runs MAF:

- Approvals: empty/partial next-run input rejects unanswered saved calls without executing them; failed-run retry retains pending state; partial streamed rejection is not completion. Reject duplicate active IDs. Reassess persisted standing rules after tool/MCP changes. Assert business idempotency after partial service success.
- Middleware/declarative tools: denied agent tools cannot execute through alternate registration paths; explicitly exercise FICC AdditionalTools and chat-pipeline context-provider limitations. YAML cannot remove a registered approval-required function's gate. Reject prohibited MCP headers and retain approved AutoSend across waits/restore.
- Storage: migrate Cosmos options without losing filters/ownership/state keys; test flat and hierarchical key schemas, retained metadata, read/count/delete and cross-tenant denial. Implement experimental session deletion, including missing-session no-op and isolation. Propagate memory caller cancellation.
- Workflows: closed-list display/synonym/ID matching and invalid/default choices; handoff returns without replaying completed effects; forwarded external approval includes the completed call/result. Test reused executors, second compiled runs, checkpoint callbacks before post-load hooks, allowlisted environment restore, sensitivity/case-variant metadata, skipped required actions and deduplicated fan-out targets.
- Hosting/DevUI: verify AG-UI scoped dependencies and stable logical names across requests, selector-null 404 before storage, tenant isolation and explicit null SSE fields. Check normal Chat Completions `[DONE]` versus failure/cancellation; A2A empty input/status messages/card/transport behavior; Foundry concurrent response cache and OAuth consent isolation. Test DevUI peer/Host/Origin and separately secured standard execution routes.
- Telemetry/files/shell: compare streaming and non-streaming agent continuation with/without OpenTelemetry; distinguish file search timeout from caller cancellation; keep Docker options developer-controlled and test the actual sandbox configuration separately.

Source mapping: [scoped review](../../../resources/docs/capabilities/verification-1.26.md). Use deterministic fake clients, tools, stores and HTTP hosts where practical; run infrastructure/live-provider integration only when separately authorized.
