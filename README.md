# Codex + Microsoft Agent Framework .NET Guidance Pack

Reusable Codex guidance for building and reviewing Microsoft Agent Framework (MAF) systems in C#/.NET.

This repository is **not an application scaffold**. Its reusable core is the MAF knowledge layer under `.agents/`. Adoption profiles decide where `AGENTS.md` should live based on the target solution shape.

## Why profiles

MAF may be:

1. the central architecture of an AI-first repository; or
2. one AI project/module inside a larger product with ordinary domain/application code.

Those cases should not receive the same root instructions. Codex supports hierarchical `AGENTS.md` files, so this pack scopes MAF guidance to the part of the repository where it belongs instead of making the whole solution agent-centric.

## Adoption profiles

### AI-first

Use when the repository is primarily an agentic/AI system and MAF is central.

```text
MyAgentService/
├── AGENTS.md            # MAF-centric root guidance
└── .agents/skills/...
```

Profile: `profiles/ai-first/`

### Application with an AI module

Use when MAF is one project inside a larger application.

```text
MyProduct/
├── AGENTS.md                    # application-centric + AI boundary
├── .agents/skills/...
└── src/
    ├── MyProduct.Domain/
    ├── MyProduct.Application/
    ├── MyProduct.Infrastructure/
    └── MyProduct.AI/
        └── AGENTS.md            # MAF-specific local guidance
```

Profile: `profiles/application-with-ai-module/`

The core rule is: **MAF orchestrates/adapts application capabilities; it does not become the owner of domain behavior.**

## Install

AI-first repository:

```bash
python3 scripts/install-guidance.py \
  --profile ai-first \
  --target /path/to/repository
```

Existing application with an AI project:

```bash
python3 scripts/install-guidance.py \
  --profile application-with-ai-module \
  --target /path/to/repository \
  --ai-path src/MyProduct.AI
```

The installer is conservative. It does not silently overwrite differing guidance. In the mixed-application profile, an existing root `AGENTS.md` is preserved and a small boundary fragment is emitted for manual merge.

## MAF knowledge layer

The skills are organized around MAF abstractions rather than generic implementation phases:

- `maf-architecture`;
- `maf-agents`;
- `maf-tools` / MCP;
- `maf-workflows` / built-in orchestrations / executors / edges;
- `maf-context-memory`;
- `maf-middleware`;
- `maf-provider-integration`;
- `maf-observability`;
- `maf-devui`;
- `maf-testing` + evaluation;
- `maf-review`.

Shared references cover official sources, provider neutrality, LangChain/LangGraph mapping, and application/AI boundaries.

Skills remain the same across profiles. Only instruction placement/scope changes. This avoids maintaining separate copies such as “tools for AI-first” and “tools for enterprise app”.

## Design goals

- MAF-specific rather than generic “AI architecture”.
- Extensible across different .NET solution shapes.
- Provider/cloud neutrality by default.
- Domain/application logic stays independent of MAF when AI is only one module.
- Strong LangChain/LangGraph → MAF mental-model bridge.
- Deterministic C# for deterministic behavior.
- Explicit Agent / Tool / Workflow / Middleware / Context / Session / Checkpoint choices.
- Typed workflow messages and structured model outputs.
- No live model dependency in the default test suite.
- DevUI kept as a development surface.
- Version-aware instructions because MAF APIs evolve rapidly.

## Layout

```text
.
├── AGENTS.md                         # convenience/default AI-first guidance for this repo
├── .agents/
│   ├── references/
│   │   ├── application-boundaries.md
│   │   ├── langgraph-crosswalk.md
│   │   ├── official-sources.md
│   │   └── provider-neutrality.md
│   └── skills/maf-*/
├── profiles/
│   ├── README.md
│   ├── ai-first/
│   │   └── AGENTS.md
│   └── application-with-ai-module/
│       ├── AGENTS.root-fragment.md
│       ├── AGENTS.ai-module.md
│       └── README.md
├── docs/
│   ├── adopting-the-template.md
│   ├── application-with-ai-module.md
│   ├── codex-setup.md
│   ├── maintaining-maf-knowledge.md
│   ├── migration-v1-to-v2.md
│   └── migration-v2-to-v3.md
├── scripts/
│   ├── install-guidance.py
│   └── validate-template.py
└── .codex/config.toml.example
```

## Customize after installation

Ask Codex to inspect the actual repository and fill the project-specific sections rather than inventing structure or package versions.

For an AI module, a useful first prompt is:

```text
Inspect this solution and update only the Project-specific AI context section of the AI project's AGENTS.md.
Record the exact MAF packages/versions, AI project boundaries, application services it may call,
provider integration, session/context/persistence choices, build/test/run commands, and development surfaces.
Do not move domain/application responsibilities into the AI project.
```

## Validate the guidance pack

```bash
python3 scripts/validate-template.py
```

## Source policy

Prefer Microsoft Learn and official Microsoft Agent Framework repositories/samples. Installed NuGet versions win over `main` when API shapes differ.

Provider-specific examples are treated as adapters, not architecture defaults.

## License

MIT.
