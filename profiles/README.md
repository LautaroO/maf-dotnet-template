# Adoption profiles

The reusable asset in this repository is the MAF knowledge layer under `.agents/`.

`AGENTS.md` placement depends on how MAF participates in the target solution. Do not force one root prompt onto every architecture.

## `ai-first`

Use when the repository is primarily an AI/agentic system and MAF is a central architecture concern.

Install `profiles/ai-first/AGENTS.md` at repository root.

## `application-with-ai-module`

Use when an existing product/application has ordinary domain/application projects plus one AI/MAF project.

- keep the product's root `AGENTS.md` application-centric;
- merge the supplied root fragment to establish the AI boundary;
- place the supplied AI-module `AGENTS.md` inside the AI project;
- keep `.agents/skills/` once at repository root.

## Adding another profile

A profile should contain only placement/scope instructions that differ by solution shape. Do not fork the MAF skills unless the framework behavior itself differs.

Good future profiles might include:

- reusable AI library/package;
- multi-service solution with several independent AI modules;
- dedicated AI service consumed over HTTP/events;
- monorepo with multiple products.

Prefer hierarchical `AGENTS.md` placement over giant conditional root instructions.
