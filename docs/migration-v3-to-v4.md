# Migration from v3 to v4

v4 is a guidance-only, manually adopted capability pack.

1. Remove copied `scripts/install-guidance.py`, `.maf-guidance/`, and installer-specific CI or documentation from the adopting repository. Remove generated `__pycache__` files too.
2. Copy or merge `.agents/skills/`, `.agents/references/`, `docs/capabilities/`, and `docs/patterns/`. Do not copy runtime guidance into an application's agent skill store.
3. Run `$maf-adoption` against the target repository. Let it inspect solution shape, installed packages, commands, conventions, and existing instructions.
4. For the recommended embedded-AI profile, merge `profiles/application-with-ai-module/AGENTS.root-fragment.md` into the existing root instructions and copy `AGENTS.ai-module.md` to the AI subtree. Never overwrite an existing root `AGENTS.md`.
5. For a genuinely AI-first repository, manually merge `profiles/ai-first/AGENTS.md` into its root instructions.
6. Populate every project-context placeholder from evidence in the target repository.
7. Run `python3 scripts/validate-template.py` in this pack and perform fresh-Codex-session smoke tests for the chosen profile.

Adopting-team rules remain authoritative for C# style, solution layout, test framework, analyzers, CI/CD, persistence, and hosting.
