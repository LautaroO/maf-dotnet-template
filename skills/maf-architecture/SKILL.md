---
name: maf-architecture
description: Use when designing MAF .NET systems, assessing an agent idea or existing design for material gaps, or choosing responsibilities and architecture for a substantial behavior change in a new or existing solution.
---

# MAF architectural assistance

Choose the smallest design that satisfies the problem. MAF specialization supplies architectural judgment inside the project's development process.

Read [agent design](../../resources/references/agent-design.md) for proportional gap assessment and [process integration](../../resources/references/process-integration.md) for coexistence with Superpowers or team workflows. Reuse relevant project instructions, canonical context and settled requirements before asking questions.

For existing solutions, inspect affected components and contracts. For new solutions, distinguish proposed SDK/packages and assumptions from installed facts; do not impose a universal project layout. Use [application boundaries](../../resources/references/application-boundaries.md) when AI is a module within a larger product.

## Assign responsibility

| Requirement | Likely owner |
|---|---|
| Exact rules, authorization, validation, persistence | Deterministic application code |
| Bounded lookup/action selected by a model | Tool adapting an application capability |
| Open-ended interpretation, synthesis or tool selection | Bounded agent |
| Guaranteed sequence, branches, approval, parallel steps or recovery | Explicit workflow |
| Model-selected specialist consultation | Agent delegation, if one agent is insufficient |
| Conversation, grounding, execution recovery, business facts | Distinct session/context/checkpoint/application lifetimes |
| SDK capabilities or transport/hosting | Replaceable provider/host boundary |

Classify semantic decisions, deterministic rules, side effects and state before picking APIs. Apply [provider neutrality](../../resources/references/provider-neutrality.md). Consult the [pattern catalog](../../resources/docs/patterns/v4.md) for matching problems; read technical evidence only for capabilities that affect the choice.

For substantial work, deliver a compact design with responsibilities, relevant alternatives/tradeoffs, state/trust boundaries, failure/retry ownership and acceptance criteria. Separate architectural recommendations from documented MAF constraints. Resolve material gaps before dependent implementation; accept adequate designs and proceed when authorized. A small exact change does not require this full workflow.

Implementation and testing can use the corresponding installed skills when needed; do not activate every skill as a fixed pipeline. For API choices, verify the target's packages using [official-source discipline](../../resources/references/official-sources.md).
