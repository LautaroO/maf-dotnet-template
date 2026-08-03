# Adopting the template

## 1. Copy the shared guidance

Copy `AGENTS.md`, `.agents/`, and the relevant setup files into the target
repository root.

## 2. Customize project context

Update only the project-specific section first. Include:

- solution and project names;
- target framework and SDK;
- MAF packages and versions;
- provider-neutral interfaces and concrete adapters;
- source and test layout;
- build, test, format, and run commands;
- checkpoint, memory, retrieval, and persistence choices;
- hosting model and deployment constraints;
- security, approval, and data-retention requirements.

## 3. Keep shared rules stable

Avoid rewriting general rules to match a shortcut in one application. If a
project needs an exception, document it locally and explain:

- why the exception is required;
- where it is isolated;
- how it affects portability;
- how it is tested.

## 4. Merge `.gitignore`

Do not replace an established `.gitignore` automatically. Preserve project rules
and add missing entries for:

- .NET build outputs;
- IDE state;
- secrets and local environment files;
- local databases;
- workflow checkpoints and agent state;
- logs, traces, and generated files;
- personal Codex configuration.

## 5. Verify Codex discovery

Start a fresh Codex session at the repository root and ask:

```text
List the instruction files and MAF skills you loaded, then summarize their scope.
```

## 6. Let Codex inspect real package versions

The template deliberately does not pin a MAF package version. The target
repository's installed NuGet packages are authoritative for compilable APIs.
