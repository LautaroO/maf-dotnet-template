# Microsoft Agent Framework .NET plugin

`maf-dotnet` is a skills-only Codex plugin for designing, implementing, reviewing, testing and operating Microsoft Agent Framework (MAF) systems in C#/.NET.

This repository is the plugin: [plugin.json](plugin.json), [skills/](skills/) and [resources/](resources/) are maintained directly. There is no generated package copy or build step. It is not a marketplace, application scaffold, installer, compilable sample, or bundle of runtime Agent Skills for application agents.

## Install and adopt

Install `maf-dotnet` through a separate marketplace that references this repository's root. See [distribution](docs/plugin-distribution.md) for an external catalog example and local testing.

Installation makes the fourteen skills and resources available to Codex. Explicitly select the installed `maf-adoption` skill to inspect a target repository and merge project-specific instructions; installation itself does not edit files or update NuGet packages. Preserve existing `AGENTS.md` files and avoid duplicate repository copies of the MAF skills.

Use the [application with an AI module](resources/profiles/application-with-ai-module/README.md) profile by default; use [AI-first](resources/profiles/ai-first/AGENTS.md) only when MAF owns central orchestration. The root `AGENTS.md` here describes plugin maintenance; the files under `resources/profiles/` are the templates for adopting applications.

See [adoption](docs/adopting-the-template.md) and [migration to plugin-only distribution](docs/migration-to-plugin.md).

## Capabilities

Fourteen focused skills cover adoption, architecture, agents, tools/MCP, workflows, context/RAG, middleware, providers, hosting, security, observability, DevUI, testing/evaluation and review.

The [versioned capability matrix](resources/docs/capabilities/maf-dotnet-1.18.md) records .NET availability, maturity, packages, restrictions, official sources and verification metadata. The [pattern catalog](resources/docs/patterns/v4.md) contains 17 playbooks for common application and production scenarios.

These skills guide Codex during software development. MAF runtime Agent Skills are inputs discovered by application agents during execution. Never place this plugin in an application's runtime skill store.

## Core decisions

Use the least-agentic owner:

- deterministic C# for exact rules, authorization, validation and routing;
- tools for bounded application capabilities;
- agents for open-ended semantic work and bounded tool choice;
- workflows for explicit process, approval, recovery and durable control;
- sessions, context providers, workflow state/checkpoints and application persistence for their distinct lifetimes;
- provider and hosting adapters at replaceable boundaries.

In mixed solutions, removing the AI module must not remove business rules, ordinary use cases, authorization policy or core persistence.

## Maintain and validate

Edit `skills/` and `resources/` directly. Validate with:

```bash
python3 scripts/validate-template.py
python3 -m compileall -q scripts
python3 -B -m unittest discover -s tests -v
```

CI checks the manifest/version, skill contracts, resource paths, profiles, matrix, fixtures, Markdown links and repository hygiene. The scheduled source audit opens or refreshes a maintenance issue; it never edits guidance.

Before each release, install the plugin in a supported client and run fresh-session smoke tests for both adoption profiles using [the routing dataset](resources/evaluations/skill-routing/v1.jsonl). Structural tests do not prove native-client installation or autonomous routing.

## Version policy

The plugin uses independent Semantic Versioning. Keep `plugin.json`, [VERSION](VERSION), and [CHANGELOG.md](CHANGELOG.md) synchronized for releases. Current development baseline: `0.1.0`, with last verified MAF .NET release `dotnet-1.18.0` on 2026-09-09. Plugin versioning starts at `0.1.0` for this initial development release. Earlier `4.x` records describe the guidance pack, not plugin maturity; historical Git tags do not contain this plugin layout.

Installed NuGet APIs are authoritative for adopters. Current Microsoft Learn or `main` samples never override the installed package surface.

## License

MIT.
