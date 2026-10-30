# Profile: application with an AI module

Use this profile when MAF lives in one project/module inside a larger product solution.

Target application example; the skills remain in the installed plugin:

```text
MyProduct/
├── AGENTS.md
└── src/
    ├── MyProduct.Domain/
    ├── MyProduct.Application/
    ├── MyProduct.Infrastructure/
    └── MyProduct.AI/
        └── AGENTS.md
```

Keep the shared skills, conceptual references and patterns in the installed plugin. Merge the project instructions below; do not create a second knowledge-layer copy in the application.

Merge `AGENTS.root-fragment.md` into the repository root `AGENTS.md` rather than replacing existing product guidance.

Copy `AGENTS.ai-module.md` to the AI project directory as `AGENTS.md`.

Use `$maf-adoption` to inspect and populate project context. There is no installer; existing root instructions must never be overwritten.

Because Codex resolves `AGENTS.md` from repository root toward the working directory, the root file establishes product boundaries while the nested AI file adds MAF-specific guidance only when Codex works inside the AI module.
