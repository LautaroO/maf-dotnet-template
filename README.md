# Codex + Microsoft Agent Framework .NET Guidance Pack

A guidance-only Codex capability pack for designing, implementing, reviewing, testing and operating Microsoft Agent Framework (MAF) systems in C#/.NET.

It contains repository-scoped Codex skills, references, playbooks, evaluation fixtures and maintenance checks. It is not an application scaffold, plugin, installer, compilable sample, or bundle of runtime Agent Skills for application agents.

## Adopt into an existing repository

The default recommendation is [application with an AI module](profiles/application-with-ai-module/README.md): preserve the application's root instructions and conventions, merge a small MAF boundary fragment, and place focused MAF instructions in the AI subtree.

Use [AI-first](profiles/ai-first/AGENTS.md) only when MAF genuinely owns the repository's central orchestration architecture.

Adoption is manual and non-overwriting:

1. copy/merge `.agents/`, `docs/capabilities/`, `docs/patterns/`, and the relevant profile at their original relative paths, preserving existing files;
2. invoke `$maf-adoption` in the target repository;
3. let it inspect the solution, packages, commands, boundaries and existing instructions;
4. populate project context only from evidence;
5. validate hierarchy and run fresh-session smoke tests.

See [adoption](docs/adopting-the-template.md) and [v3 migration](docs/migration-v3-to-v4.md).

## Capabilities

Fourteen focused skills cover adoption, architecture, agents, tools/MCP, workflows, context/RAG, middleware, providers, hosting, security, observability, DevUI, testing/evaluation and review.

The [versioned capability matrix](docs/capabilities/maf-dotnet-1.18.md) records .NET availability, maturity, packages, restrictions, official sources and verification metadata. The [pattern catalog](docs/patterns/v4.md) contains 17 uniform playbooks for common application and production scenarios.

Repository `.agents/skills/` are instructions for Codex while developing software. MAF runtime Agent Skills are application inputs discovered by an agent during execution. Do not copy this pack into a runtime skill store.

## Core decisions

Use the least-agentic owner:

- deterministic C# for exact rules, authorization, validation and routing;
- tools for bounded application capabilities;
- agents for open-ended semantic work and bounded tool choice;
- workflows for explicit process, approval, recovery and durable control;
- sessions, context providers, workflow state/checkpoints and application persistence for their distinct lifetimes;
- provider and hosting adapters at replaceable boundaries.

In mixed solutions, removing the AI module must not remove business rules, ordinary use cases, authorization policy or core persistence.

## Validate

```bash
python3 scripts/validate-template.py
python3 -m compileall -q scripts
python3 -B -m unittest discover -s tests -v
```

CI also checks Markdown links and repository hygiene. The scheduled source audit opens or refreshes a maintenance issue; it never edits guidance.

Before each release, run fresh-Codex-session smoke tests for both adoption profiles using [the routing dataset](evaluations/skill-routing/v1.jsonl).

## Version policy

The pack uses independent Semantic Versioning; see [VERSION](VERSION) and [CHANGELOG](CHANGELOG.md). Current baseline: pack `4.0.0`, last verified MAF .NET release `dotnet-1.18.0` on 2026-09-09.

Installed NuGet APIs are authoritative for adopters. Current Microsoft Learn or `main` samples never override the installed package surface.

## License

MIT.
