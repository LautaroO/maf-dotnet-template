---
name: maf-review
description: Use when reviewing a MAF .NET design, repository or change for architectural fit, correctness, security, reliability, provider coupling and verification gaps.
---

# Review MAF systems

Select the review scope: design, whole repository or change/diff. Inspect enough relevant evidence to establish impact; distinguish new regressions from existing concerns. For design gaps use [agent design](../../resources/references/agent-design.md); follow the [active project process](../../resources/references/process-integration.md).

Use [review checklist](references/review-checklist.md) selectively for relevant responsibilities, state/trust boundaries, failure/retry/resume behavior and testability. When AI is one module, check [application boundaries](../../resources/references/application-boundaries.md): removing AI must not remove ordinary use cases, domain rules, authorization policy or core persistence.

Ask what each component does, why its abstraction owns that responsibility, what manual mechanism MAF can sufficiently supply, and what deterministic rule or provider SDK has leaked into the wrong layer. For a disputed API/capability inspect the relevant implementation topic reference and [official evidence](../../resources/references/official-sources.md); match installed packages when reviewing code.

Lead with material findings. Each finding includes severity/category, confidence, precise evidence/location, concrete impact, recommended correction and MAF certainty (installed API verified, matching official release verified, or uncertain). Separate implementation defects, unresolved design decisions and optional improvements. Ignore formatting preferences unless project rules require them.

An adequate design or change can have **no findings**: say so, with the actual review scope and untested behavior. Missing future capabilities are not defects without a relevant requirement. Summarize architecture, test/operational gaps and prioritized changes only where evidence warrants them; do not require a minimum number of issues or a generic top-three list.
