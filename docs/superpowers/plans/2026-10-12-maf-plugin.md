# Direct MAF plugin implementation plan

> Use superpowers:executing-plans in the current session.

**Goal:** Make this repository the canonical plugin package, distributed through a separate marketplace.

**Architecture:** Root plugin.json identifies maf-dotnet. Skills and resources are authored directly and installed without a generation step. Root maintenance instructions are separate from adoption profiles.

**Tech Stack:** Python standard library, unittest, JSON, Markdown, GitHub Actions.

**Spec:** [Plugin design](../specs/2026-10-12-maf-plugin-design.md).

## Constraints and review focus

Fourteen skills; plugin-only distribution; no marketplace/catalog, provider dependency, runtime skill store, installer or publication. Validate isolated links, version drift, malformed file types, symlinks, duplicate copies and preservation of moved guidance.

## Task 1: Direct package layout

- [x] Add isolated plugin-layout tests and observe failure before migration.
- [x] Move canonical skills/shared guidance into skills/ and resources/, preserving tracked files and adapting relative links.
- [x] Place plugin.json at root and remove the generated copy and builder.
- [x] Separate maintainer root instructions from application profile templates.

## Task 2: Validation and operational documentation

- [x] Validate root manifest/version, required file types, skill set and resource references.
- [x] Update hygiene, source audit and CI for the new paths.
- [x] Document root-source external catalogs, installed-only adoption and migration.
- [x] Run main validation, full unittest suite, Python/shell syntax and diff whitespace checks.
- [x] Complete independent review of final files and resolve actionable findings.

## Execution record

User selected plugin-only distribution after reviewing the direct layout. Implemented in the shared workspace without creating a marketplace, installing the plugin, publishing, or committing. New isolated-layout tests failed before the root manifest existed, then passed. Additional malformed-file tests failed before type checks were added, then passed. Current suite: eighteen passing tests. Existing tracked guidance was checked against the relocation map. Native-client installation and fresh-session routing remain explicit untested release checks.

Independent review found no actionable defects in the final direct layout; it confirmed all relocated guidance, installed-only adoption, CI/audit paths and the eighteen passing tests.
