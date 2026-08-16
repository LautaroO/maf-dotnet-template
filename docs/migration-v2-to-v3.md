# Migration from v2 to v3

v3 keeps the v2 MAF skills but changes the adoption model.

## What changed

v2 assumed the root `AGENTS.md` could serve most target repositories. v3 treats that file as the **AI-first profile** and introduces solution-shape profiles.

The new reusable core is:

```text
.agents/skills/
.agents/references/
```

`AGENTS.md` placement is now selected separately.

## If your repository is AI-first

No architectural migration is required.

Use:

```text
profiles/ai-first/AGENTS.md -> /AGENTS.md
```

and refresh `.agents/` from v3.

## If your application has one AI project

Do not keep the full MAF-centric v2 file as the only root instruction file.

Instead:

1. keep/create an application-centric root `AGENTS.md`;
2. merge `profiles/application-with-ai-module/AGENTS.root-fragment.md` into that root file;
3. copy `profiles/application-with-ai-module/AGENTS.ai-module.md` to the AI project as `AGENTS.md`;
4. keep `.agents/skills/` once at repository root.

Example:

```text
MyProduct/
├── AGENTS.md
├── .agents/skills/...
└── src/MyProduct.AI/AGENTS.md
```

## New architecture rule

The AI module is an orchestration/integration layer. MAF tools and workflows should call application capabilities rather than absorb domain rules.

See `.agents/references/application-boundaries.md`.

## Automated install

Use `scripts/install-guidance.py` for new adoptions. It refuses to overwrite differing guidance by default.
