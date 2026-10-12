---
name: maf-adoption
description: Adopt the Codex MAF guidance pack into an existing C#/.NET repository by inspecting its solution shape, preserving local conventions, placing hierarchical AGENTS.md guidance, and recording evidence-based project context. Do not use for ordinary MAF implementation after adoption.
---

# MAF adoption

Read `../../references/official-sources.md`, `../../references/application-boundaries.md`, and `references/adoption-workflow.md`.

Inspect before proposing changes: existing `AGENTS.md` files, solution/project files, `global.json`, central package management, build/test/format/CI configuration, MAF packages, AI boundaries, hosts, storage, providers, and security constraints.

Classify the repository as:

- application with an AI module (default when domain/application behavior exists independently of MAF);
- AI-first (only when MAF owns the central orchestration architecture); or
- ambiguous, in which case preserve the existing root and scope MAF rules narrowly.

Adoption is manual copy/merge. Never overwrite an existing root `AGENTS.md`. Adopting-team rules remain authoritative for C# style, solution layout, tests, analyzers, CI/CD, persistence, and hosting.

Populate project-context placeholders only from repository evidence. Report unknowns instead of inventing package versions, commands, ownership, or operational choices. Add concise code-review rules at the closest applicable `AGENTS.md`.

Do not install a plugin, create a runtime MAF Agent Skill, or scaffold an application.
