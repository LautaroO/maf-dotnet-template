# Changelog

All notable changes to this guidance pack are recorded here. The plugin follows Semantic Versioning independently of Microsoft Agent Framework (MAF). Plugin versioning starts at `0.1.0`; earlier `4.x` entries describe the historical guidance pack.

## [0.1.0] - 2026-10-12

### Changed

- Plugin-only authoring layout: `skills/` and `resources/` replace repository-scoped `.agents/` guidance; adoption merges project instructions while keeping the skills installed.
- Root maintainer instructions are separate from application adoption profiles.
- Adoption reuses existing documentation and refinement processes, recording a compact context index and proposing missing documentation conventions before creating new documents.
- Architecture tasks reuse settled requirements, verify relevant context and clarify only material open decisions, with documentation proportional to the change.

### Added

- Repository-root, skills-only `maf-dotnet` plugin for distribution through a separate marketplace; this repository is the plugin, not a marketplace.
- Plugin manifest/version validation, standalone resource checks, installation-layout regression tests, and external-marketplace documentation.
- Shared project-context/refinement guidance and three behavior evaluation fixtures for existing conventions, missing conventions and small fully specified changes.

## [4.0.0] - 2026-09-09

### Added

- `maf-adoption`, `maf-hosting`, and `maf-security` Codex skills.
- A versioned .NET capability matrix, uniform pattern catalog, and routing evaluation dataset.
- Whole-repository and change/diff review modes with evidence-first finding fields.
- CI validation and a scheduled, issue-only official-source audit.
- Regression tests for repository hygiene and malformed routing fixtures.

### Changed

- Shortened both adoption profiles and made the embedded-AI profile the default recommendation.
- Expanded agent, workflow, middleware, provider, testing, observability, and review guidance for current .NET capabilities and operational checks.
- Adoption is now a manual copy/merge workflow assisted by `$maf-adoption`.
- All adoption entrypoints include the capability and pattern documents required by skills.

### Fixed

- Invalid Lychee mail flag; link checking now includes hidden `.agents/` guidance and pins the checker version.
- Ignored local caches no longer fail pack hygiene; tracked ignored artifacts are still rejected.
- Non-object routing fixtures produce validation errors instead of crashing the validator.

### Removed

- The guidance installer and all automated-install instructions.

Last verified MAF .NET release: `dotnet-1.18.0` on 2026-09-09.

[4.0.0]: docs/releases/v4.0.0.md
