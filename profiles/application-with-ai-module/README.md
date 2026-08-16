# Profile: application with an AI module

Use this profile when MAF lives in one project/module inside a larger product solution.

Example:

```text
MyProduct/
├── AGENTS.md
├── .agents/skills/...
└── src/
    ├── MyProduct.Domain/
    ├── MyProduct.Application/
    ├── MyProduct.Infrastructure/
    └── MyProduct.AI/
        └── AGENTS.md
```

Install the shared `.agents/` skills at repository root.

Merge `AGENTS.root-fragment.md` into the repository root `AGENTS.md` rather than replacing existing product guidance.

Copy `AGENTS.ai-module.md` to the AI project directory as `AGENTS.md`.

Because Codex resolves `AGENTS.md` from repository root toward the working directory, the root file establishes product boundaries while the nested AI file adds MAF-specific guidance only when Codex works inside the AI module.
