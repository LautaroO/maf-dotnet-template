# Codex setup

Install the `maf-dotnet` plugin through a separate marketplace, including when testing changes in this repository. Portable skills live in `skills/`; they are discovered through plugin installation rather than repository-scoped `.agents/skills/` discovery. See [distribution](plugin-distribution.md).

Codex reads the target application's `AGENTS.md` hierarchy separately. Plugin installation does not edit those instructions.

## Skills

Select the installed skill explicitly when you want deterministic selection. The names below identify capabilities; use the plugin namespace shown by the client. For example:

```text
$maf-implementation Implement the approved workflow design.
```

Otherwise Codex can select a skill implicitly based on its `description`.

Select architecture for substantive design, implementation for coding/integration, testing for verification design, and review for evidence-backed assessment. Small exact edits and generic .NET work need no compulsory MAF pipeline.

## Progressive disclosure

Keep detailed MAF knowledge in skill references. Do not move all references back into `AGENTS.md`; that defeats progressive disclosure and consumes project-instruction budget on every task.

## Project instructions

Codex layers project instructions from repository root toward the working directory, with more local guidance taking precedence. This is why the pack uses adoption profiles instead of one universal MAF-centric root file.

For an application that contains one AI project, keep product architecture at the root and place the MAF-specific `AGENTS.md` in that AI subtree. See [the packaged profile](../resources/profiles/application-with-ai-module/README.md).

Keep root guidance concise and use skills/references for task-specific detail.

This plugin's `skills/` are developer guidance consumed by Codex. MAF runtime Agent Skills are application content discovered by an executing agent. Keep their storage, provenance and security policies separate; never load this pack into the application runtime.

Official Codex references:

- https://developers.openai.com/codex/agent-configuration/agents-md
- https://developers.openai.com/codex/build-skills
- https://developers.openai.com/codex/learn/best-practices

## Configuration

Personal authentication/provider/model settings belong in the user's Codex home config. Commit only safe project examples.

See `.codex/config.toml.example` for a minimal reference.
