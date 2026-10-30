---
name: maf-adoption
description: Use when explicitly adopting MAF developer guidance into a new or existing .NET solution while preserving project instructions and architectural ownership.
---

# MAF adoption

Read [adoption workflow](references/adoption-workflow.md), [application boundaries](../../resources/references/application-boundaries.md) and [project context](../../resources/references/project-context-and-refinement.md) for instruction placement. Use [process integration](../../resources/references/process-integration.md) to contribute within the team’s existing process.

For a new solution, separate intended architecture and proposed dependencies from nonexistent installed facts. Preserve existing starter instructions; this guidance does not prescribe a scaffold. For an existing solution, inspect before proposing changes: existing `AGENTS.md` files, solution/project files, `global.json`, central package management, build/test/format/CI configuration, MAF packages, AI boundaries, hosts, storage, providers, and security constraints.

Classify the repository as:

- application with an AI module (default when domain/application behavior exists independently of MAF);
- AI-first (only when MAF owns the central orchestration architecture); or
- ambiguous, in which case preserve the existing root and scope MAF rules narrowly.

Adoption is explicit inspection and copy/merge of project instructions. Use this installed plugin's skills/resources and merge only the applicable project guidance; do not duplicate the skills in the target repository. Never overwrite an existing root `AGENTS.md`. Adopting-team rules remain authoritative for C# style, solution layout, tests, analyzers, CI/CD, persistence, and hosting.

Populate project-context placeholders only from repository evidence. Report unknowns instead of inventing package versions, commands, ownership, or operational choices. Add concise code-review rules at the closest applicable `AGENTS.md`.

Reuse existing project documentation and refinement/planning processes. Record canonical context links and the documentation convention in the applicable `AGENTS.md`. If no suitable convention exists, propose one and wait for agreement before creating new context or feature documents; continue independent adoption work and record the pending choice.

Do not install a plugin, create a runtime MAF Agent Skill, or scaffold an application.
