# Adopting the guidance pack

## 1. Choose the solution profile before copying `AGENTS.md`

Do not assume MAF should own repository-wide guidance.

Choose:

- `ai-first` when MAF is central to the repository;
- `application-with-ai-module` when MAF lives in one project/module inside a larger product.

See `../profiles/README.md`.

## 2. Install the shared MAF knowledge layer once

Keep `.agents/skills/` and `.agents/references/` at repository root so all relevant code can discover the same MAF guidance.

Do not fork skills per project/module unless framework behavior truly differs.

## 3. Scope `AGENTS.md` hierarchically

### AI-first

Install the MAF-centric `AGENTS.md` at repository root.

### Application with AI module

Keep the root `AGENTS.md` application-centric. Merge only the supplied AI-boundary fragment into it, then put the MAF-specific `AGENTS.md` inside the AI project.

Example:

```text
src/MyProduct.AI/AGENTS.md
```

Do not duplicate the entire root file into nested directories. Nested instructions should refine the parent scope.

## 4. Populate project-specific context

Ask Codex to inspect the actual solution and fill the relevant context section. Capture package versions, commands, project boundaries, provider adapters, hosts, persistence/session choices, application dependencies, and security constraints.

## 5. Keep application/domain behavior outside the AI layer

In mixed solutions, use `.agents/references/application-boundaries.md` as the default boundary model.

MAF agents/workflows/tools may orchestrate or adapt application capabilities. They should not become a parallel domain/application layer.

## 6. Keep provider-specific rules local

If one project intentionally uses a provider-only capability, document it in project context and the provider adapter area. Do not rewrite generic MAF skills around that provider.

## 7. Add additional nested guidance only for real local differences

Examples:

```text
src/MyProduct.AI/Providers/OpenAI/AGENTS.md
src/MyProduct.AI/Workflows/AGENTS.md
```

Use these only when a subtree genuinely needs stricter/different rules.

## 8. Feed real mistakes back into the shared skills

When Codex repeatedly makes a MAF-specific mistake:

- decide which abstraction skill owns it;
- add a short rule/reference/example;
- prefer concrete “use X instead of Y when Z” guidance;
- update the changelog;
- retest skill triggering in a fresh Codex session.

If the mistake is specific to one solution shape, update the profile/boundary reference rather than every MAF skill.
