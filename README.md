# Codex + Microsoft Agent Framework .NET Template

Reusable repository guidance for building, reviewing, and experimenting with
Microsoft Agent Framework (MAF) in C#/.NET with Codex.

This repository is intentionally **not** an application template. It provides the
engineering instructions, Codex skills, review checklists, and setup documentation
that can be copied into any MAF solution.

## What this template enforces

- Provider- and cloud-neutral architecture.
- Clear separation between deterministic code, tools, agents, and workflows.
- Provider SDK isolation behind adapters and composition roots.
- Typed contracts, structured outputs, validation, cancellation, and bounded retries.
- Explicit state, memory, context, checkpointing, and durability decisions.
- Testability without requiring a live model for the default test suite.
- Security boundaries for tools, model outputs, prompt injection, and approvals.
- Development-only handling of DevUI and local harnesses.
- Independent verification of DevUI tracing and external OTLP observability.

Azure, Microsoft Foundry, Azure OpenAI, and OpenAI examples in official
documentation are treated only as concrete integration examples. They are not
architectural defaults.

## Repository layout

```text
.
├── AGENTS.md
├── .agents/
│   └── skills/
│       ├── maf-architecture/
│       ├── maf-implementation/
│       └── maf-review/
├── .codex/
│   └── config.toml.example
├── docs/
│   ├── codex-setup.md
│   └── adopting-the-template.md
├── .gitignore
├── CHANGELOG.md
├── LICENSE
└── README.md
```

## Use in a new MAF repository

Copy these entries to the root of the target repository:

```text
AGENTS.md
.agents/
.codex/config.toml.example
docs/codex-setup.md
.gitignore
```

Then customize the `Project-specific context` section in `AGENTS.md`.

Do not overwrite an existing `.gitignore` blindly. Merge the relevant entries
with the target repository's current rules.

## Recommended first Codex prompt

```text
Inspect this repository and update only the Project-specific context section of
AGENTS.md.

Document the solution structure, installed .NET and MAF versions, build and test
commands, provider-adapter boundaries, hosting model, persistence choices, and
repository-specific conventions.

Do not weaken the general MAF architecture, safety, testing, or provider-neutrality
rules.
```

For architecture work:

```text
$maf-architecture Review this solution and propose the least-agentic idiomatic MAF architecture.
```

For implementation:

```text
$maf-implementation Implement the approved design using the installed package versions.
```

For review:

```text
$maf-review Review this implementation for MAF abstraction use, provider isolation, reliability, testability, and safety.
```

## Skills

### `maf-architecture`

Helps decide between deterministic C# code, tools, agents, workflows, middleware,
context providers, memory, durability, CLI harnesses, and DevUI.

### `maf-implementation`

Guides implementation against the actual installed NuGet package versions and
official .NET source. It includes specific guidance for DevUI and local hosting.

### `maf-review`

Provides a structured architecture and code review method, including provider
isolation, workflow modeling, tool safety, observability, and DevUI checks.

## Important Codex locations

Repository-scoped skills belong in:

```text
.agents/skills/<skill-name>/SKILL.md
```

User-level Codex configuration normally belongs in:

```text
~/.codex/config.toml
~/.codex/AGENTS.md
```

The committed `.codex/config.toml.example` is only a reference.

## Updating this template

When improvements emerge in a real MAF project:

1. identify whether the change is generally reusable;
2. exclude application-specific providers, storage, commands, and domain behavior;
3. update the relevant skill or reference;
4. record the change in `CHANGELOG.md`;
5. test discovery in a fresh Codex session.

## License

MIT.
