# Adopting the installed MAF plugin

## 1. Choose the solution profile before copying `AGENTS.md`

Do not assume MAF should own repository-wide guidance.

Choose:

- `ai-first` when MAF is central to the repository;
- `application-with-ai-module` when MAF lives in one project/module inside a larger product.

See `../resources/profiles/README.md`.

## 2. Use the installed knowledge layer

Install `maf-dotnet` through your separate marketplace before adoption. Select its `maf-adoption` skill using the plugin namespace shown by the client. The skill uses bundled profiles, concept and pattern resources; do not copy skills or shared resources into the target repository. See [distribution](plugin-distribution.md).

If the target already has older `.agents/skills/maf-*` copies, review local adaptations and preserve project-specific instructions before removing duplicates. Installing the plugin alone does not perform that migration or edit project rules.

## 3. Scope `AGENTS.md` hierarchically

### AI-first

Manually merge the MAF-centric `AGENTS.md` at repository root. Preserve any existing rules.

### Application with AI module

Keep the root `AGENTS.md` application-centric. Merge only the supplied AI-boundary fragment into it, then put the MAF-specific `AGENTS.md` inside the AI project.

Example:

```text
src/MyProduct.AI/AGENTS.md
```

Do not duplicate the entire root file into nested directories. Nested instructions should refine the parent scope.

## 4. Populate project-specific context

Invoke `$maf-adoption` and ask Codex to inspect the actual solution and fill the relevant context section. Capture package versions, commands, project boundaries, provider adapters, hosts, persistence/session choices, application dependencies, and security constraints. Never overwrite an existing root `AGENTS.md`. Use a packaged profile rather than the plugin repository's maintainer instructions.

Reuse existing architecture, ADR and feature documentation and the team's refinement/planning process. Keep a compact index of canonical context links and the process in the closest applicable `AGENTS.md`, avoiding duplicated documentation. Saved context reduces repeated discovery; code/configuration and installed package APIs still need checks relevant to each change.

If no suitable documentation convention exists, Codex proposes a location and naming approach with a rationale and waits for agreement before creating new context or feature documents. It can continue independent inspection and authorized instruction merging, recording the destination as pending. The agreed convention is reused on later tasks; this pack imposes no `docs/architecture/` or `docs/features/` hierarchy.

For example, if a product uses `handbook/ai-context.md`, feature notes under `handbook/`, and its own brainstorming skill, adoption links to those documents and follows that skill. A later “add an agent that queries orders” request reuses documented order contracts, permissions and operational limits, asking only about unresolved decisions. A fully specified display-name change follows the team's lightweight process without generating a new specification. See the [context and refinement guidance](../resources/references/project-context-and-refinement.md).

## 5. Keep application/domain behavior outside the AI layer

In mixed solutions, use the installed plugin's `resources/references/application-boundaries.md` as the default boundary model.

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
