# Typed workflow steps and control

Use explicit workflow control when the process must guarantee sequence, branches, parallelism, approvals or recovery. An executor performs a bounded step using an application service or an agent; not every step needs a model.

## Contracts before topology

Prefer dedicated typed inputs/results between steps. Validate semantic model decisions before deterministic routing. Use shared workflow state for genuinely shared coordination rather than one universal mutable dictionary. Keep domain data in its owning application persistence.

Model meaningful parallel branches and aggregation in the graph when their lifecycle needs workflow observability, state or recovery. Incidental independent I/O inside one deterministic operation can remain ordinary asynchronous code. Define concurrency, ordering, cancellation and partial-failure behavior.

## Retry and failure ownership

Distinguish transient dependency retries, bounded semantic repair and business-effect retries. Avoid multiplying retry layers. Specify default branches, dead ends and invalid-output behavior; test them with controllable semantic collaborators. Graph deduplication or replay handling does not establish business-effect idempotency.

## Implementation lookup

`Executor`, workflow builders, typed handlers, edges and workflow context are orientation terms. Find their exact installed registration, dispatch, state and run/event contracts using [official-source investigation](../../../resources/references/official-sources.md); do not copy a remembered generator, attribute, constructor or overload.
