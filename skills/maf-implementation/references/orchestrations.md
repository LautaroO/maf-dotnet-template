# Single-agent, delegation and workflow composition

Start with one bounded agent when it meets the task. Add specialists for distinct semantic responsibilities or authority/context boundaries, not to fill a standard multi-agent diagram.

## Select the owner of control

- A parent selecting a specialist as a tool keeps routing semantic and retains responsibility for the final response.
- Handoff transfers a conversational responsibility; establish who owns session/context and how control returns.
- A sequential, concurrent or collaborative orchestration fits only when its control semantics meet the requirement.
- Required order, approvals or recovery belong in explicit workflow control around bounded semantic steps.

Check available built-in MAF patterns before implementing an orchestration loop. Define typed results, authority and budgets for calls, recursion, concurrency, time and cost. Shared conversation visibility must be intentional.

## Recovery and evaluation

Specify what continuation means, which identity/context is preserved, and which completed effects must not replay. Test delegation selection semantically and deterministic cancellation, limits, approval propagation and effect idempotency independently.

Exact composition helpers, built-in orchestration availability and handoff behavior require [official-source investigation](../../../resources/references/official-sources.md) for the selected packages. A familiar pattern name is not proof of compatible runtime semantics.
