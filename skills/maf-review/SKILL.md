---
name: maf-review
description: Review a Microsoft Agent Framework C#/.NET repository or change/diff for architecture, abstractions, state, security, reliability, provider portability, hosting, observability, testing, durability, and production operability. Produce evidence-first findings and identify manual mechanisms that MAF should own.
---

# MAF review

Read `../../resources/references/official-sources.md`, `../../resources/references/langgraph-crosswalk.md`, and `references/review-checklist.md`. When MAF is one module inside a larger product, also read `../../resources/references/application-boundaries.md`.

## Review method

Select the review mode explicitly:

- **Whole repository** — inspect instruction hierarchy, solution/project/package boundaries, representative runtime paths, composition, state/storage, hosts, tests, CI and operations.
- **Change/diff** — inspect the diff and enough surrounding code/config/tests to establish impact; distinguish introduced regressions from pre-existing risks.

For each agentic component answer:

1. What is it currently doing?
2. Which MAF abstraction is it actually using?
3. Is that abstraction the right owner of the responsibility?
4. What has been implemented manually that MAF already models?
5. What deterministic logic has leaked into prompts/agents?
6. What provider-specific code has leaked upward?
7. What state lifetime is being assumed?
8. What happens on invalid model output, cancellation, retry, resume, duplicate delivery, or partial failure?
9. Can the important behavior be tested without a live model?

## Finding contract

Findings come before architecture summaries. Every finding must include:

- severity/category;
- confidence (`high`, `medium`, or `low`);
- evidence and precise file/location;
- impact or failure scenario;
- recommended correction;
- MAF version certainty (`verified against installed package`, `verified against matching official release`, or `uncertain`).

Do not report formatting preferences unless repository rules, analyzers or CI require them. If there are no findings, say so and identify residual/untested risks.

## Severity

Prioritize findings:

- **Bug / correctness** — behavior can fail or corrupt state/data.
- **Architecture** — wrong abstraction/coupling creates meaningful maintenance risk.
- **Reliability/security** — unsafe tool/model/state/retry behavior.
- **MAF idiom** — manual mechanism should use a framework primitive.
- **Quality** — naming, duplication, test ergonomics, observability.

Do not inflate stylistic preferences into architecture bugs.

## Required output

Keep the review actionable after findings:

- current architecture summary;
- bugs;
- misuse/missed MAF abstractions;
- recommended restructuring;
- provider portability issues;
- production risks;
- test gaps;
- hosting and production-operability gaps, including cost, latency, safety, retrieval, streaming and durability where relevant;
- top 3 changes by impact.

## Additional boundary smell for mixed solutions

When MAF is only one project/module, explicitly check whether removing the AI module would also remove domain rules, ordinary use cases, authorization policy, or core persistence behavior. If yes, recommend moving those responsibilities back to application/domain code and keeping MAF as orchestration/adaptation.
