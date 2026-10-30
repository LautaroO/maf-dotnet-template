# MAF architectural patterns

Select a pattern by the problem and required control. These are design playbooks, not compilable package samples or a mandatory production checklist. Technical references retain their dated evidence: full MAF 1.24 plus scoped 1.25–1.26 deltas; implementation checks the target’s actual APIs. For proportional questioning and process ownership use [agent design](../../references/agent-design.md). The [historical v4 catalog](v4.md) remains available.

## adoption: Fit guidance to a new or existing solution

### When it fits

An explicit request to adopt project instructions. A new solution has intended boundaries; an existing product has evidence to preserve.

### Responsibilities and boundaries

Keep the root product-centric when AI is a module; scope MAF instructions to its subtree. In AI-first solutions MAF may own central orchestration. Preserve local rules and context.

### Alternatives

Ordinary assistance needs no adoption. A reusable library, service or monorepo can use hierarchical instructions without a new universal profile.

### Failure behavior

Unknown SDK, ownership and documentation location remain unknown; do not invent project facts or overwrite instructions.

### Acceptance examples

Existing root rules survive; a generic .NET edit invokes no MAF process. New-solution assumptions are labeled. [Adoption](../../../skills/maf-adoption/SKILL.md).

## conversation-lookup: Bounded conversational application lookup

### When it fits

Natural-language questions need an authorized application query and grounded response, optionally across multiple turns or streamed to a client.

### Responsibilities and boundaries

A bounded agent interprets/redacts/presents; a narrow tool adapts the application service. Tenant/resource authorization stays in that service. Persist a conversation only when product behavior needs it.

### Alternatives

Retrieve deterministically before generation when lookup is mandatory. A single-turn assistant needs no durable history, delegation or workflow by default.

### Failure behavior

Unknown or unauthorized results fail through deterministic contracts; canceled/disconnected streams do not commit premature effects. Authenticate session lookup and define retention if stored.

### Acceptance examples

An authenticated tenant-scoped lookup returns only number/status/date within its deadline. A cross-tenant request fails, cancellation propagates, and two-turn behavior is tested only when required. [Tools](../../../skills/maf-implementation/references/function-tools.md), [agents](../../../skills/maf-implementation/references/agents.md), [sessions](../../../skills/maf-implementation/references/context-memory.md).

## multimodal: Interpret authorized media

### When it fits

An agent must interpret uploaded images or other media supported by the selected stack.

### Responsibilities and boundaries

The host owns type/size/provenance validation, ownership, scanning and retention; the model interprets approved content. Keep provider upload representations at the adapter boundary.

### Alternatives

Extract text deterministically when that meets the task. Reject unsupported modalities explicitly rather than pretending provider parity.

### Failure behavior

Reject spoofed/oversized/cross-tenant media and unrestricted fetch URLs before model access. Provider failures and unsupported media have bounded fallback behavior.

### Acceptance examples

Valid media reaches the intended run; invalid metadata or ownership cannot trigger a fetch or disclosure. [Media and agent capabilities](../../../skills/maf-implementation/references/agents.md).

## structured-decision: Extract a validated semantic decision

### When it fits

Unstructured input must become a category or typed record consumed by application code.

### Responsibilities and boundaries

The model performs extraction/classification; a typed validator owns allowed values and business invariants before routing or persistence.

### Alternatives

Exact rules use deterministic code. Provider-supported structured output is a representation mechanism, not proof of semantic correctness.

### Failure behavior

Malformed/missing/unknown values fail or enter a bounded repair policy. Free-form text never controls consequential branches directly.

### Acceptance examples

Tests cover missing fields, unknown enum values, malicious content and invalid ranges. Semantic evaluations separately measure extraction quality. [Agents](../../../skills/maf-implementation/references/agents.md), [testing](../../../skills/maf-testing/SKILL.md).

## consequential-action: Execute an approved application action

### When it fits

The assistant may cancel, refund, send or otherwise change business state.

### Responsibilities and boundaries

The model proposes a bounded capability; application code authorizes principal/tenant/resource and validates invariants. Bind required approval to the exact occurrence and material arguments; use business idempotency.

### Alternatives

Keep the assistant read-only if actions are unnecessary. A workflow fits required order or persisted approval waits; a tool alone may fit a short bounded approved action.

### Failure behavior

Expire stale approval, reject changed/replayed/cross-session requests, revalidate authority at execution, and distinguish pending/rejected/failed runs. Framework approval is not atomic business-effect deduplication.

### Acceptance examples

A retry/resume cannot double-refund; authentication alone cannot cancel another user’s order. Test absent/partial approvals and actual registration paths against selected packages. [Approval evidence](../../../skills/maf-implementation/references/mcp-and-approval.md), [security](../../../skills/maf-implementation/references/security.md).

## retrieval: Ground answers with deterministic, agentic or hybrid retrieval

### When it fits

Answers need tenant-authorized external evidence and source provenance.

### Responsibilities and boundaries

A retrieval service controls corpus access before ranking. Context injection supplies mandatory grounding; a tool allows model-selected search; a hybrid combines common grounding with bounded additional retrieval.

### Alternatives

Deterministic two-step retrieval fits guaranteed lookup. Agentic retrieval fits optional or iterative search. No RAG is needed for authoritative structured data already supplied by a service.

### Failure behavior

No evidence or contradictory evidence needs an explicit response policy. Retrieved content cannot expand tool authority. Bound searches, payload and query latency; preserve citations.

### Acceptance examples

Test isolation and query/filter behavior without a model. Evaluate retrieval recall/precision, citation fidelity and generated answer quality separately. [Context and RAG](../../../skills/maf-implementation/references/context-memory.md).

## controlled-process: Control an ordered or conditional process

### When it fits

Sequence, branching, approval or recovery must be guaranteed across steps.

### Responsibilities and boundaries

A typed workflow controls transitions; deterministic services enforce exact rules; bounded agents handle semantic steps. Validate model decisions before edges. Use shared state only when message flow is insufficient.

### Alternatives

A direct service call fits exact simple rules. A bounded agent fits open-ended choice without mandatory sequence. Programmatic versus declarative form depends on required contracts and supported schema.

### Failure behavior

Assign retry ownership, define default/dead-end behavior and reject unsupported actions rather than hiding missing control in prompts. Restore compatibility and sensitivity rules depend on the selected API.

### Acceptance examples

Validated categories choose deterministic branches; invalid output cannot reach a posting tool. Test each branch, deadlines and applicable restore/reset semantics with fake semantic steps. [Graphs](../../../skills/maf-implementation/references/executors-edges.md), [state](../../../skills/maf-implementation/references/state-checkpoints-hitl.md).

## parallel-process: Parallelize independent observable steps

### When it fits

Independent branches and their aggregation need workflow-level state, observability or checkpoint behavior.

### Responsibilities and boundaries

Graph fan-out/fan-in represents branches; each branch has a typed result and the aggregator defines partial-failure/order expectations. Bound concurrency and independent effect keys.

### Alternatives

Local Task.WhenAll is sufficient for incidental independent I/O inside a deterministic operation when graph-level control is not required. Avoid modeling every helper call as a graph node.

### Failure behavior

Define whether one branch failure cancels others or yields partial results. Framework target deduplication within a dispatch is not business idempotency across retries.

### Acceptance examples

Out-of-order completion produces the intended aggregate; cancellation and repeated delivery cannot duplicate a business action. [Workflow edges](../../../skills/maf-implementation/references/executors-edges.md).

## recoverable-wait: Resume human/external waits and long-running work

### When it fits

The process must pause for a person or survive restart/deployment.

### Responsibilities and boundaries

Explicit request/response models the wait; selected checkpoint/durable infrastructure owns execution recovery. Application persistence remains separate, with stable logical identity, tenancy and idempotent effects.

### Alternatives

Provider background responses fit supported incremental continuation, not general durable execution. An ordinary short agent run needs neither durable host nor checkpoints.

### Failure behavior

Define continuation ownership/expiry, retention, concurrency and deployment compatibility. Reject incompatible topology/identity rather than claiming restore will work; bound reconnection and polling.

### Acceptance examples

An approval resumes after restart without repeating the side effect. Unrelated callers cannot access a session/checkpoint; fake-run tests cover duplicate delivery and stale continuation. [Recovery and HITL](../../../skills/maf-implementation/references/state-checkpoints-hitl.md), [hosting](../../../skills/maf-implementation/references/hosting.md).

## delegation: Choose bounded specialist composition

### When it fits

One agent lacks the specialist context or capability needed for open-ended semantic work.

### Responsibilities and boundaries

The parent may select specialists as tools when routing is semantic; define specialist contracts, authority and delegation limits. Required order belongs in workflow control.

### Alternatives

One agent is the default when it can satisfy the task. Built-in sequential/concurrent/handoff/group patterns are candidates only when their control semantics fit; avoid custom orchestration by habit.

### Failure behavior

Bound call/depth/time budgets, avoid recursive delegation and preserve session ownership. Handoff continuation must not replay the original command and duplicate effects.

### Acceptance examples

A logistics/contracts coordinator chooses a relevant specialist; an exact invoice threshold uses code instead. Verify handoff and approval forwarding with fake agents when applicable. [Orchestrations](../../../skills/maf-implementation/references/orchestrations.md).

## runtime-instructions: Choose instructions, runtime skills, tools or Harness

### When it fits

Reusable instructions or an opinionated agent runtime are being proposed.

### Responsibilities and boundaries

Instructions frame semantic behavior; runtime Agent Skills supply trusted application-agent inputs; tools expose bounded capabilities; workflows control process. Codex developer skills are a different installation/input boundary.

### Alternatives

Use Harness only for deliberately chosen runtime behavior. A reusable prompt or terminal interface alone does not justify its full runtime.

### Failure behavior

Review source trust, script execution, sandbox/egress, tool authority and resource budgets. A stable package does not make every composed experimental API stable.

### Acceptance examples

The plugin is never loaded into an application runtime skill store. Untrusted skill content cannot grant execution permission; selected file/shell behavior is verified at its boundary. [Runtime selection](../../../skills/maf-implementation/references/agents.md), [security](../../../skills/maf-implementation/references/security.md).

## hosting: Separate runtime operation from protocol

### When it fits

The assistant must be exposed to clients or operated beyond an in-process use case.

### Responsibilities and boundaries

Choose embedded/self-hosted/durable/managed operation separately from native API, OpenAI-compatible, A2A, AG-UI or MCP transport. Identify identity, session storage, limits, streaming and incident owners.

### Alternatives

A product-native API may suffice without another interoperability protocol. Managed hosting is intentional cloud coupling at the adapter boundary; DevUI is a local development surface.

### Failure behavior

Client IDs and selectors do not authorize resource access. Check DI lifetimes, stable logical names and route-specific authentication; a protected UI does not secure separately mapped execution endpoints.

### Acceptance examples

Cross-tenant/session access is denied; disconnect behavior is tested; DevUI and production routes have distinct intended controls. Verify relevant package maturity. [Hosting](../../../skills/maf-implementation/references/hosting.md), [DevUI](../../../skills/maf-implementation/references/devui.md).

## migration: Swap providers or change framework packages

### When it fits

The target changes providers, packages or capabilities.

### Responsibilities and boundaries

Keep provider SDK setup in composition/infrastructure and MAF/application contracts stable where they fit. Compare capability needs and actual installed API surface with matching official evidence.

### Alternatives

A provider-only feature may justify an explicit adapter and reduced portability. A compatible fallback can avoid an unnecessary upgrade; do not wrap IChatClient/AIAgent merely to duplicate them.

### Failure behavior

Fail before consequential execution on unsupported capabilities. Distinguish package maturity, experimental APIs and published/installed availability. A source fix does not prove persisted-state migration compatibility.

### Acceptance examples

Pinned old packages remain unchanged unless authorized. New solutions label proposed versions; adapter tests cover stream/tool/output differences. [Providers](../../../skills/maf-implementation/references/providers.md), [source discipline](../../references/official-sources.md).

## verification-operations: Evaluate behavior and diagnose incidents

### When it fits

A system needs acceptance gates or evidence about a user-visible failure.

### Responsibilities and boundaries

Test exact rules/tools/state/workflow behavior deterministically. Evaluate semantic task success, retrieval and quality separately. Correlate agent/model/tool/workflow evidence with privacy-preserving telemetry.

### Alternatives

Instrument meaningful boundaries rather than duplicating spans. DevUI visualization and OTLP export solve different debugging needs; live-model judges are opt-in, not the only correctness gate.

### Failure behavior

Capture cancellation/retry/resume and safety denials without sensitive bodies by default. Telemetry export alone does not establish continuation correctness. Compare representative cases before adding broad process.

### Acceptance examples

Default tests use no live model; an incident can be traced to relevant boundaries; an adequate design can receive no review findings. [Testing](../../../skills/maf-testing/SKILL.md), [telemetry](../../../skills/maf-implementation/references/observability.md), [review](../../../skills/maf-review/SKILL.md).
