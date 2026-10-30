# Plugin maintainer instructions

## Repository context

This repository is the `maf-dotnet` skills-only Codex plugin. It contains no .NET application, solution, installed MAF packages, runtime Agent Skills, marketplace catalog, or installer. `plugin.json` is the root manifest; `skills/` and `resources/` are the single authoring source. Edit them directly. Do not add a generated package copy or repository-discovered duplicate skills under `.agents/skills/`.

The current plugin version is `0.1.1`; plugin and MAF versions are independent. This is stable architectural guidance, not an SDK compatibility catalog. Keep durable concepts and verification criteria in skills/resources; do not reintroduce release-delta notes, maturity matrices, exact overload recipes or periodic source-audit automation. The official Microsoft MAF repository is the primary external implementation reference; adopting applications inspect their own SDK/projects/resolved packages and matching .NET APIs. There is no application or installed MAF package here, so never claim illustrative guidance compiles against a local SDK.

## Structure and boundaries

- `skills/maf-*/`: five portable developer skills and their local resources/scripts.
- `resources/references/`: shared guidance and official-source discipline.
- `resources/profiles/`: instruction templates for AI-first and embedded-AI applications.
- `resources/docs/`: conceptual pattern catalog.
- `resources/evaluations/skill-routing/`: routing and behavior fixtures.
- `docs/`: distribution, migration, maintenance and release documentation.
- `scripts/` and `tests/`: standard-library Python structural validation and regression checks.

The root instructions govern plugin maintenance; application adoption templates have their own context in `resources/profiles/`. Never copy this root file into an adopting application. Preserve adopting-team rules and existing root `AGENTS.md` during explicit adoption.

Keep all skill/resource links resolvable within the plugin after installation. Do not rely on the source checkout or symlinks. Plugin installation supplies skills; explicit adoption merges project instructions. MAF runtime Agent Skills are different application inputs.

## Guidance invariants

Preserve least-agentic responsibility assignment, provider/cloud neutrality, installed-version checks, typed validation, authorization/tenancy boundaries, bounded async/cancellation/retry behavior, state-lifetime distinctions and live-model-free default tests. Prefer MAF-native semantics when available. Keep provider SDK setup separate from reusable agents, tools, workflows and application behavior.

## Verification and releases

When guidance needs maintenance, read `docs/maintaining-maf-knowledge.md`, inspect the relevant concept and official .NET evidence, update only affected guidance and evaluate the behavior that motivated the change. Do not audit or copy every new MAF release. For a concrete SDK implementation question, verify target package APIs and matching official source on demand; qualify missing/conflicting evidence instead of inventing signatures or availability. Historic review records are not current compatibility claims.

Run `python3 scripts/validate-template.py`, `python3 -m compileall -q scripts`, and `python3 -B -m unittest discover -s tests -v`. Check shell syntax for embedded `.sh` scripts and use `git diff --check`. CI also verifies Markdown links.

Update `plugin.json` and `VERSION` together for a release, record the changelog, and perform the native-client and fresh-session checks in `docs/releases/fresh-session-smoke-test.md`. The external marketplace references this repository root; no catalog belongs here. Do not claim installation, routing, release or publication was verified from structural tests alone.

Report files changed, commands/results, provider coupling, installed API/source certainty, and untested client behavior. This repository has no application state, provider calls or production host; do not invent operational guarantees for an adopting application.
