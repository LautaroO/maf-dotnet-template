# Plugin maintainer instructions

## Repository context

This repository is the `maf-dotnet` skills-only Codex plugin. It contains no .NET application, solution, installed MAF packages, runtime Agent Skills, marketplace catalog, or installer. `plugin.json` is the root manifest; `skills/` and `resources/` are the single authoring source. Edit them directly. Do not add a generated package copy or repository-discovered duplicate skills under `.agents/skills/`.

The current plugin baseline is `0.1.0`; MAF knowledge was last verified against `dotnet-1.24.0` on 2026-10-12. Plugin and MAF versions are independent. Do not claim that illustrative C# compiles against an installed package here: there is no application or installed MAF version in this repository. When updating API guidance, verify official Microsoft sources and state version uncertainty; adopting applications must inspect their own SDK/projects/NuGet APIs.

## Structure and boundaries

- `skills/maf-*/`: fourteen portable developer skills and their local resources/scripts.
- `resources/references/`: shared guidance and official-source discipline.
- `resources/profiles/`: instruction templates for AI-first and embedded-AI applications.
- `resources/docs/`: capability matrix and pattern catalog.
- `resources/evaluations/skill-routing/`: routing and behavior fixtures.
- `docs/`: distribution, migration, maintenance and release documentation.
- `scripts/` and `tests/`: standard-library Python validation, source audit and regression checks.

The root instructions govern plugin maintenance; application adoption templates have their own context in `resources/profiles/`. Never copy this root file into an adopting application. Preserve adopting-team rules and existing root `AGENTS.md` during explicit adoption.

Keep all skill/resource links resolvable within the plugin after installation. Do not rely on the source checkout or symlinks. Plugin installation supplies skills; explicit adoption merges project instructions. MAF runtime Agent Skills are different application inputs.

## Guidance invariants

Preserve least-agentic responsibility assignment, provider/cloud neutrality, installed-version checks, typed validation, authorization/tenancy boundaries, bounded async/cancellation/retry behavior, state-lifetime distinctions and live-model-free default tests. Prefer MAF-native semantics when available. Keep provider SDK setup separate from reusable agents, tools, workflows and application behavior.

## Verification and releases

When asked to update MAF knowledge or review a source audit, Codex owns the follow-through: read `docs/maintaining-maf-knowledge.md`, review official release/tag/API evidence, edit affected guidance, record a dated review and run validation. Do not stop at telling the user to review sources manually. The source-audit script gathers evidence; it does not replace this maintenance workflow. Preserve scoped verification metadata when only part of the knowledge base has been reviewed.

Run `python3 scripts/validate-template.py`, `python3 -m compileall -q scripts`, and `python3 -B -m unittest discover -s tests -v`. Check shell syntax for embedded `.sh` scripts and use `git diff --check`. CI also verifies Markdown links.

Update `plugin.json` and `VERSION` together for a release, record the changelog, and perform the native-client and fresh-session checks in `docs/releases/fresh-session-smoke-test.md`. The external marketplace references this repository root; no catalog belongs here. Do not claim installation, routing, release or publication was verified from structural tests alone.

Report files changed, commands/results, provider coupling, MAF version certainty, and untested client behavior. This repository has no application state, provider calls or production host; do not invent operational guarantees for an adopting application.
