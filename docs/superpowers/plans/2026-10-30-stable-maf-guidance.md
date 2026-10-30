# Stable MAF Guidance Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans for the user-selected native execution. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Keep stable architectural MAF assistance and consult the official repository on demand instead of maintaining a release knowledge base.

**Architecture:** Preserve five task routes, concept references and problem patterns; remove release catalogs/audit automation and adapt validators/evaluations to the remaining package. Historical records point to Git history rather than installed resources.

**Tech Stack:** Markdown, JSON/JSONL, standard-library Python/unittest and existing validation CI.

**Spec:** [Approved amendment](../specs/2026-10-30-stable-maf-guidance-design.md).

## Global Constraints

- Preserve the five skill names, provider neutrality, installed-package checks, application boundaries and proportional design/process behavior.
- No fixed MAF compatibility baseline or version-specific SDK instructions in active skills/resources.
- Git history preserves retired information; no duplicate archive is added to the plugin.
- Keep plugin.json and VERSION at 0.1.1. Update PR #4 on the existing authorized branch/repository; do not merge or publish a plugin release.
- User's latest explicit simplification supersedes earlier release-retention requirements. No new design or execution approval is needed for this amendment.

## Review Focus

- References must remain useful design/implementation criteria rather than become empty links.
- Source lookup must match installed .NET APIs; current main or Python examples cannot establish compatibility.
- Unavailable evidence must produce scoped uncertainty, not fabricated signatures or unsupported-absence claims.
- Minimal installation and source validation must not depend on removed files/workflows.
- Historical records must not direct normal users into retired maintenance procedures.

## Task 1: Replace release knowledge with durable guidance

**Files:** All thirteen `skills/maf-implementation/references/*.md`; `resources/references/official-sources.md`; testing references; pattern catalog; skill/profile/adoption references as needed; README, AGENTS, maintenance/migration/setup/smoke-test docs; delete `resources/docs/capabilities/`, `resources/docs/patterns/v4.md`, `resources/evaluations/skill-routing/v1.jsonl`. Historical records link to commit 89aeb8782682253f216cffe11d1bb95427bd3290 for removed artifacts.

**Interfaces:** Preserve existing topic paths/public names and pattern IDs. Official-source guidance links the MAF repository and defines package-first, matching-.NET-source investigation and unavailable-evidence behavior. No signature/version/maturity catalog replaces the deleted one.

- [x] Capture baseline and run a reference probe before editing, with an SDK-detail prompt and an architecture prompt; record what is observed, not a fabricated failure.
- [x] Rewrite topic references around responsibilities, tradeoffs, contracts and verification questions; remove release-specific assertions/code and direct exact APIs to official investigation.
- [x] Update active docs/profiles/patterns and record the amended maintenance policy; mark superseded evidence historical and repair removed-resource links to the preceding commit.
- [x] Remove the retired resources; validate local/installed links after Task 2 removes obsolete validator requirements.

## Task 2: Remove audit infrastructure and validate the remaining contract

**Files:** `scripts/validate-template.py`, `tests/test_validate_template.py`, `tests/test_plugin_layout.py`; delete `scripts/{audit-maf-sources.py,sync-maf-audit-issue.py,maf_knowledge.py}`, their three test modules and `.github/workflows/source-audit.yml`; update routing v2 and evaluation README/protocol.

**Interfaces:** Keep `validate_plugin`, `validate_catalog`, `validate_routing`, `validate_cases` and the skill contract. Remove `validate_matrix` and coverage imports/checks. CI requires only validation workflow. Routing checks preserve core behavior IDs and scenario mapping without pinning release facts.

- [x] Write a failing subprocess test showing source validation succeeds in an export lacking the retired matrix, metadata, helpers and audit workflow. Preserve installed-copy resource checks. Remove tests whose production behavior is intentionally retired; replace historical-fixture equality with current route/case validity.
- [x] Remove audit/matrix/coverage dependencies and files; update source investigation fixtures and expected assertions without requiring historical SDK facts.
- [x] Run default tests/validator, Python compilation, shell syntax and diff whitespace checks; all must pass with no new dependency.

## Task 3: Review, verify and update the existing PR

**Files:** Dated amendment review/evaluation record, CHANGELOG, completed plan; any evidence-backed fixes.

- [x] Apply the same source/detail and architectural scenarios to candidate references; distinguish response probes from native discovery or actual upstream inspection.
- [x] Request one independent read-only review of this amendment against its spec; fix material findings with regression verification and record limitations.
- [x] Run final structural/unit/Python/shell/link/whitespace checks and confirm the working tree includes no accidental provider or version claims.
- [x] Commit and push to `codex/maf-architectural-assistant` at the already-authorized repository. Rewrite PR #4 title/body for final scope, removing claims about retained release knowledge/auditing. No merge or release.
