# Codex setup

Codex reads repository `AGENTS.md` automatically and discovers repository-scoped skills under `.agents/skills/`.

## Skills

Invoke explicitly with `$skill-name` when you want deterministic selection, for example:

```text
$maf-workflows Implement the approved workflow design.
```

Otherwise Codex can select a skill implicitly based on its `description`.

Descriptions in this template are intentionally specific so `maf-agents`, `maf-tools`, and `maf-workflows` do not all trigger for generic MAF work.

## Progressive disclosure

Keep detailed MAF knowledge in skill references. Do not move all references back into `AGENTS.md`; that defeats progressive disclosure and consumes project-instruction budget on every task.

## Project instructions

Codex layers project instructions from repository root toward the working directory, with more local guidance taking precedence. This is why the pack uses adoption profiles instead of one universal MAF-centric root file.

For an application that contains one AI project, keep product architecture at the root and place the MAF-specific `AGENTS.md` in that AI subtree. See `../profiles/application-with-ai-module/`.

Keep root guidance concise and use skills/references for task-specific detail.

Official Codex references:

- https://developers.openai.com/codex/agent-configuration/agents-md
- https://developers.openai.com/codex/build-skills
- https://developers.openai.com/codex/learn/best-practices

## Configuration

Personal authentication/provider/model settings belong in the user's Codex home config. Commit only safe project examples.

See `.codex/config.toml.example` for a minimal reference.
