# Workflow state, checkpoints, HITL

## State

Prefer typed messages. Use workflow shared state only for data that multiple executors genuinely need outside direct message flow.

Current workflow state APIs are scope-aware and visibility can follow workflow superstep semantics. Verify `ReadStateAsync` / queued update APIs against the installed package before relying on same-step visibility.

Never share mutable executor/workflow instances across concurrent runs accidentally. If a stateful executor is intentionally reused, inspect whether the installed version requires/supports reset semantics such as `IResettableExecutor`.

## Checkpoints

Checkpoints capture workflow runtime state so execution can resume from a saved point. They are useful for long workflows, pause/resume, failure recovery, and audit/replay scenarios.

Checkpoint state is not a substitute for domain/application persistence.

The [reviewed .NET checkpoint guide](https://learn.microsoft.com/agent-framework/workflows/checkpoints) requires matching topology and executor identities. Reconstructed local `ChatClientAgent` participants need stable, unique logical-role `ChatClientAgentOptions.Id` values and unchanged names when set. Regenerated IDs break compatibility; later assigning stable IDs does not repair an old lineage. Keep tenancy/session IDs separate from agent-role IDs and start a new checkpoint lineage when identities change.

Queued state updates are visible immediately to the writer and to other executors in the next superstep; use an explicit shared scope. Supported reset between runs is not concurrent-run isolation.

The [Durable hosting guide](https://learn.microsoft.com/agent-framework/hosting/azure-functions) separates Azure Functions integration from a bring-your-own-compute Durable Task worker. Their package/infrastructure versions are independent from core MAF; scheduling does not eliminate application idempotency or authorization.

## HITL / RequestPort

Current MAF workflow docs use request/response handling (`RequestPort` in C#) for interactions with external systems/humans. The workflow emits a request event and waits; the outside host returns a typed response and execution resumes.

Use this for approval or required human/external data. Persist pending requests/checkpoints when the wait may outlive the process.

## Reviewed 1.25–1.26 semantics

In 1.25, workflow-hosted external tool-approval answers are forwarded only after the agent returns the completed call and matching result, even with `ForwardIncomingMessages` disabled. Forwarded tool details come from that completed call, not caller substitutions. A custom agent that omits the pair must fail rather than forwarding an executable unfinished answer.

In 1.26, `StatefulExecutor<TState>` reads current workflow-context state; `skipCache` is retained for compatibility, not an instance-cache switch. Derived instance fields still need explicit `IResettableExecutor` handling. `RegisterCheckpointRestoringCallback` runs restoration before any post-load hook; shared callbacks deduplicate by shared key instance and require explicit shared scopes. Preserve stable topology/participant identity.

Compiled declarative workflows reset formula state and generated conversation identity between runs. Test a second independent run and restore with the same compiled graph; reset is not concurrency isolation. Environment restore remains allowlisted. Control-flow inputs and `requireApproval`/`AutoSend` must satisfy sensitivity checks; expression errors must not expose sensitive values. Per-invocation AutoSend snapshots survive waits/checkpoints, so later variable changes cannot silently change the approved output decision.

For 1.25 closed-list questions, use the supported `EmbeddedEntity` / `ClosedListEntity` schema. Trimmed, case-insensitive display names/synonyms match before item IDs; the stored value is the item ID. Invalid choices follow the configured question retry/default path. In 1.26 unsupported declarative actions emit a warning when skipped; compilation is not proof that every required action runs. Validate required actions before execution, especially authorization/approval steps. See [versioned evidence](../../../resources/docs/capabilities/verification-1.26.md).

When reviewing a 1.26 declarative workflow, include each of these checks in the result:

- State lifecycle: second independent run, checkpoint restoration before post-load hooks, stable identities and no assumed concurrent-instance isolation.
- Inputs and actions: reject sensitive condition/loop/approval/output-control inputs, preserve case-sensitive variable metadata, validate closed-list choices, and detect skipped required actions.
- Approval: honor registered approval-required functions even without YAML flags and preserve invocation-time AutoSend across waits/restore.
