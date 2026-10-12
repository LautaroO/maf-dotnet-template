# Adoption profiles

The installed MAF plugin provides shared developer skills and resources.

For either profile, use the plugin's bundled knowledge layer and merge only project instructions. Do not copy skills or shared resources into the target repository. Review and preserve any local adaptations before removing old copies.

`AGENTS.md` placement depends on how MAF participates in the target solution. Do not force one root prompt onto every architecture.

## `application-with-ai-module` (recommended default)

Use when an existing product/application has ordinary domain/application projects plus one AI/MAF project.

- keep the product's root `AGENTS.md` application-centric;
- merge the supplied root fragment to establish the AI boundary;
- place the supplied AI-module `AGENTS.md` inside the AI project;
- keep the shared developer skills installed through the plugin.

## `ai-first`

Use when the repository is primarily an AI/agentic system and MAF is a central architecture concern.

Manually merge the packaged `resources/profiles/ai-first/AGENTS.md` at the target repository root; do not replace existing instructions blindly. Never copy the plugin repository's maintainer `AGENTS.md`.

## Adding another profile

A profile should contain only placement/scope instructions that differ by solution shape. Do not fork the MAF skills unless the framework behavior itself differs.

Good future profiles might include:

- reusable AI library/package;
- multi-service solution with several independent AI modules;
- dedicated AI service consumed over HTTP/events;
- monorepo with multiple products.

Prefer hierarchical `AGENTS.md` placement over giant conditional root instructions.
