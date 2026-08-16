# Migration from v1 to v2

v2 is intentionally a structural rewrite of the Codex guidance layer. It does not change application code because this repository is a reusable guidance template, not a MAF application scaffold.

## Remove

```text
.agents/skills/maf-implementation/
```

The old skill mixed agents, workflows, provider integration, DevUI, testing, and general .NET implementation advice. That made it broad enough to trigger for almost every MAF task while providing little abstraction-specific depth.

## Keep but replace content

```text
AGENTS.md
.agents/skills/maf-architecture/
.agents/skills/maf-review/
README.md
.codex/config.toml.example
docs/
```

`AGENTS.md` becomes the invariant/router layer. `maf-architecture` becomes the abstraction selector. `maf-review` becomes a cross-abstraction reviewer.

## Add

```text
.agents/references/
.agents/skills/maf-agents/
.agents/skills/maf-tools/
.agents/skills/maf-workflows/
.agents/skills/maf-context-memory/
.agents/skills/maf-middleware/
.agents/skills/maf-provider-integration/
.agents/skills/maf-observability/
.agents/skills/maf-devui/
.agents/skills/maf-testing/
scripts/validate-template.py
```

The previous DevUI implementation knowledge is preserved but promoted into `maf-devui` so it is independently discoverable.

## Behavioral difference for Codex

v1 asked Codex to apply a broad MAF implementation checklist.

v2 asks Codex to first classify the responsibility and then load the smallest relevant MAF skill. Examples:

```text
"Expose a database lookup to the assistant"
  -> maf-tools

"Translate -> validate -> retry <= 2 -> escalate"
  -> maf-workflows (+ maf-agents for semantic steps)

"Let specialists dynamically transfer the conversation"
  -> maf-workflows -> Handoff orchestration

"Always inject tenant policy before an agent run"
  -> maf-context-memory (context provider), not prompt-only logic

"Measure tool-selection regressions across a prompt set"
  -> maf-testing -> MAF evaluation
```

## Adoption recommendation

For repositories already using v1, replace the guidance files as a unit rather than merging the old `maf-implementation` skill into v2. Then ask Codex to repopulate only the `Project-specific context` section of `AGENTS.md` from the real target repository.
