# Agent design and proportional gap analysis

Start from the user's goal, existing design and relevant project evidence. An idea, a complete design, a behavior change and a label edit need different amounts of investigation. Separate facts, settled requirements, assumptions and your recommendations.

## Assess the consequence, then choose the next action

| Assessment | Response |
|---|---|
| Evidenced problem | Explain the failure scenario and correction, with its evidence. |
| Material unresolved decision | Explain what its answer changes; ask the highest-impact focused question before dependent implementation. Continue independent work. |
| Optional improvement | Label the tradeoff; keep it from blocking an adequate requested solution. |
| Sufficiently specified | Say so briefly when useful and proceed with authorized work. |

A material gap changes behavior, access, acceptance, responsibility, integration contracts or significant operating constraints. A preference or an unspecified future capability is not automatically a defect. Ask one focused question at a time unless the project's process or user benefits from a concise batch. Reuse settled answers. When the user delegates reasonable choices, choose and label assumptions; preserve any active process requirements and surface genuinely unresolved high-impact decisions. Silence or elapsed time is not approval.

## Select relevant design topics

- Purpose/users: what outcome matters, how success/failure is recognized, what the system may do.
- Responsibilities: semantic interpretation versus exact rules, capabilities and side effects. Choose deterministic code, a bounded tool, an agent or explicit workflow control.
- Authority: authenticated principals, tenant/resource scope, tool permissions and occurrence-bound approval where consequences warrant it. Model text is not enforcement.
- Context/state: required evidence, retrieval strategy, conversation lifetime, execution recovery and durable business data. These are different stores and policies.
- Contracts: typed validated outputs, integrations, allowed failure behavior and provider capability differences.
- Execution: time/cost/tool/concurrency budgets, cancellation, retry ownership, idempotency and restart/resume needs.
- Acceptance: deterministic checks for enforced behavior, semantic evaluation for model quality, and relevant operational evidence.

Use this as a topic selector, not a questionnaire. For example, an authorized tenant-scoped read-only lookup with defined output, deadline and no history can proceed to implementation. Adding cancellation with no ownership policy creates a material authorization question. Renaming its label needs neither conversation redesign nor a new specification.

## Architecture options

A single bounded agent often suffices for interpretation plus tools. Model-selected specialist delegation fits open-ended routing; required sequence, approval, branches or recovery call for explicit control. Exact rules belong in ordinary code. Choose from requirements rather than a preferred architecture diagram or fixed folder layout; a new solution and an embedded AI module can use the same responsibility principles.

For substantial work, capture chosen responsibilities, relevant alternatives, state/trust boundaries and acceptance in the canonical design. For a settled small change, a short assessment in chat is enough. Follow [process integration](process-integration.md) and the [project's documentation convention](project-context-and-refinement.md).
