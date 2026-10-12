# Changelog

All notable changes to this guidance pack are recorded here. The pack follows Semantic Versioning independently of Microsoft Agent Framework (MAF).

## [Unreleased]

### Changed

- Adoption reuses existing documentation and refinement processes, recording a compact context index and proposing missing documentation conventions before creating new documents.
- Architecture tasks reuse settled requirements, verify relevant context and clarify only material open decisions, with documentation proportional to the change.

### Added

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
