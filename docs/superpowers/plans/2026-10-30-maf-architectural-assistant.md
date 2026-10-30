# MAF Architectural Assistant Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Deliver a MAF .NET architectural assistant that analyzes material gaps, designs and implements new/existing systems, and coexists with the project's development process.

**Architecture:** Five public task-oriented skills route to focused architectural patterns and conditional MAF technical references. Machine-readable routing and knowledge-coverage contracts drive structural validation and source-audit reporting. Behavioral evaluation remains separate from deterministic CI and native-client release verification.

**Tech Stack:** Markdown, JSON/JSONL, Python standard library, unittest, existing Bash helper and GitHub Actions/gh; no application or new runtime dependencies.

**Spec:** [Approved design](../specs/2026-10-30-maf-architectural-assistant-design.md).

## Global Constraints

- "User instructions remain authoritative."
- "Default CI stays deterministic and live-model-free"; opt-in assistant evaluations are separate from application-provider calls.
- "Keep `plugin.json` and `VERSION` at 0.1.1 until a release is requested."
- "Existing evidence remains a full 1.24 baseline plus scoped 1.25–1.26 review; this reorganization does not reverify or advance it."
- "No publication, marketplace changes, target application edits or provider calls are included."
- "Preserve the pre-existing local 1.25–1.26 changes; do not reset, overwrite or claim them as new work."
- Maintain one canonical root plugin, portable internal references, no duplicate `.agents/skills/`, no runtime Agent Skills and no mandatory Superpowers dependency.
- Keep least-agentic responsibility assignment, provider neutrality, validation/authorization/tenancy, bounded execution, cancellation/idempotency and distinct state lifetimes.
- Before editing skills, load `skill-creator` and `superpowers:writing-skills`; use their behavior-first discipline without treating text-presence checks as behavioral proof.
- At execution time use `superpowers:using-git-worktrees`. If isolating, reproduce the starting working tree including uncommitted tracked changes and the two untracked 1.26 review documents in the isolated checkout; starting from HEAD alone loses approved input knowledge. Leave the original checkout intact. Record carried-in changes separately from implementation, and stage only task files/hunks deliberately.

## Review Focus

- Adequate designs and exact edits must not generate compulsory findings, questions or documents: behavioral cases in Tasks 1/6.
- Old explicit skill invocations and links must migrate without losing technical coverage: installed-copy and migration tests in Task 4.
- Failed source requests, reordered responses and timestamps must not create false release evidence or endless notifications: deterministic tests in Tasks 2/3.
- New solutions have proposed packages, not installed APIs; existing projects retain pinned versions: paired behavioral cases in Tasks 1/6.
- Superpowers availability alone must not cause a second workflow; active project process owns approval: paired process-owner cases in Tasks 1/6.

## File and interface map

### Public skills and references

Keep `skills/maf-{adoption,architecture,testing,review}/SKILL.md`; create `skills/maf-implementation/SKILL.md`. Remove the other ten public `SKILL.md` entry points after migrating knowledge. Move their reference files to `skills/maf-implementation/references/` using these exact destinations:

| Source skill/reference | New reference filename |
|---|---|
| maf-agents/agent-patterns.md | agents.md |
| maf-tools/function-tools.md | function-tools.md |
| maf-tools/mcp-and-approval.md | mcp-and-approval.md |
| maf-workflows/executors-edges.md | executors-edges.md |
| maf-workflows/orchestrations.md | orchestrations.md |
| maf-workflows/state-checkpoints-hitl.md | state-checkpoints-hitl.md |
| maf-context-memory/session-context-rag.md | context-memory.md |
| maf-middleware/pipeline-layers.md | middleware.md |
| maf-provider-integration/provider-boundary.md | providers.md |
| maf-hosting/hosting-selection.md | hosting.md |
| maf-security/security-checklist.md | security.md |
| maf-observability/otel.md | observability.md |
| maf-devui/devui.md | devui.md |

Create shared `resources/references/agent-design.md` (proportional gap analysis/topic selection) and `resources/references/process-integration.md` (one development process). Keep `project-context-and-refinement.md` as the project-context/document-location owner and link to the new references rather than duplicate process rules. Preserve adoption/testing/review local references and the architecture inspection shell script.

### Contracts and maintenance

- `resources/skill-contract.json`: schema version 1; `skills` is the five-name list, `retired_routes` maps the ten old names to `maf-implementation`, `routing_dataset` is `resources/evaluations/skill-routing/v2.jsonl`, and `pattern_catalog` is `resources/docs/patterns/catalog.md`. Paths are relative to plugin root and must remain inside it.
- `resources/docs/capabilities/coverage.json`: schema version 1; `full_verification` and `last_assessed_release` each contain `release`, ISO `date`, plugin-root-relative `evidence`; `areas` is a list of `{id, full_verification, delta_reviews}`. Each delta is `{from_release, to_release, date, evidence, scope}`; no delta upgrades the area's full verification.
- Create `scripts/maf_knowledge.py`: shared coverage loading/validation and release comparison, imported by audit and validator; not needed inside installed plugin copies.
- Existing `scripts/audit-maf-sources.py`: preserve Markdown `--output PATH`, add `--json-output PATH` for machine-readable findings and notification fingerprint.
- Create `scripts/sync-maf-audit-issue.py`: separate network mutation boundary used only by the scheduled GitHub workflow; tests replace gh with a fake callable. No local evaluation invokes this mutation.
- Create `tests/test_maf_knowledge.py`, `tests/test_audit_maf_sources.py`, `tests/test_sync_maf_audit_issue.py`; extend the two existing test modules for routing/installed layout.

### Evaluation and documentation

- Create `resources/evaluations/skill-routing/v2.jsonl`, `architectural-assistant-cases.json`, and `architectural-assistant-protocol.md`; keep v1 as historical baseline.
- Create `docs/migration-to-architectural-assistant.md` and a dated evaluation/review record under `docs/reviews/`.
- Modify active README, AGENTS, adoption/setup/distribution/maintenance/release-check docs, bundled profiles, references, workflow and validator. Preserve historical release/review content; repair only local links made stale by moves.

## Task 1: Capture behavior scenarios and the actual starting baseline

**Files:** Create `resources/evaluations/skill-routing/architectural-assistant-cases.json`, `resources/evaluations/skill-routing/architectural-assistant-protocol.md`; modify evaluation README; create `docs/reviews/2026-10-30-architectural-assistant-evaluation.md`.

**Interfaces:** Produces a `schema_version: 1` document with a `cases` list. Each case has `id`, `prompt`, `repository_files` (relative path -> file text), `process_owner` (`superpowers`, `project`, `none`), `expected_behavior` and `forbidden_behavior` string lists. New-solution cases use an empty repository mapping. The protocol defines outcome recording independent of routing skill names.

- [ ] **Step 1: Preserve baseline artifacts.** Export the current plugin/skills/resources and relevant fixtures to a temporary directory outside the repo, including carried-in changes. Record Git commit, carried-in paths, content hashes and export location in the evaluation record. Do not use only `git archive HEAD`.
- [ ] **Step 2: Author bounded cases.** Include IDs `new-idea`, `existing-app`, `adequate-design`, `small-change`, `material-gap`, `superpowers-owner`, `project-owner`, `standalone`, `architecture-choice`, `old-package`, `new-packages-unselected`, `no-findings`, `generic-dotnet`, `delegated-design`. `architecture-choice` has distinct single-agent, delegation, controlled-workflow and deterministic variants. Pin examples: an authorized tenant-scoped read-only orders lookup; a cancellation tool with missing execution authorization; an exact display-label rename. In `delegated-design`, the user explicitly authorizes reasonable architectural choices: label assumptions and proceed rather than force another approval. In `superpowers-owner`, the existing design already settles tool permissions: do not ask again.
- [ ] **Step 3: Define observable scoring.** Record each assertion as pass/fail/not-observed with evidence from transcript/actions/artifacts, question count and whether questions resolve material gaps; do not score question count alone. Separate autonomous discovery from explicit reference/skill invocation. Document model/client/config, tools, process availability, input hashes, repetitions (two fresh runs per scored case/mode), costs/usage if available, and limitations. No percentage is reported for unexecuted cases.
- [ ] **Step 4: Run pre-change reference probes.** Use the preserved export with no candidate references. Probe at least `adequate-design`, `small-change`, `material-gap`, `superpowers-owner`, `new-packages-unselected` and the four architecture variants. Capture actual failures before rewriting skills; an adequate baseline response is valid evidence, not a reason to invent a failure. These explicitly supplied-reference probes do not establish native discovery. If evaluation tools cannot run a mode, mark that mode pending with its reason and complete available modes.
- [ ] **Step 5: Verify artifacts.** Run `python3 -m json.tool resources/evaluations/skill-routing/architectural-assistant-cases.json` and `python3 scripts/validate-template.py`; expect valid JSON and current-layout validation success. Review repository files before/after for unintended artifacts.
- [ ] **Step 6: Commit only this task's evaluation/protocol changes.** Suggested message: `test: define architectural assistant behavior scenarios`. Preserve raw transcripts in temporary artifacts; commit concise evidence and limitations without machine-specific paths as runtime dependencies.

## Task 2: Make audit coverage explicit without advancing verification

**Files:** Create coverage JSON, `scripts/maf_knowledge.py`, `tests/test_maf_knowledge.py`, `tests/test_audit_maf_sources.py`; modify audit script, validator metadata validation, capability matrix prose and maintenance docs.

**Interfaces:** `load_coverage(path: Path) -> dict` raises `ValueError` with actionable field context for invalid JSON/types, dates, tags or evidence paths; `release_key(tag: str) -> tuple[int, int, int]` accepts exactly `dotnet-X.Y.Z`; `coverage_errors(data: object, root: Path) -> list[str]` validates evidence containment/existence and chronology. Audit defines `build_audit(coverage: dict, source_checks: list[dict], latest_release: str | None, release_error: str | None) -> dict` and `render_report(audit: dict) -> str`.

Audit schema: `{schema_version: 1, audit_date, full_verification, last_assessed_release, latest_release, source_checks, findings, needs_review, fingerprint}`. Findings are `{kind, source, detail}` with kinds `new_release`, `request_failure`, `redirect`, `content_signal`. `fingerprint` is SHA-256 of sorted canonical JSON for deduplicated findings plus assessed-release marker, excluding audit time, successful response ordering and incidental exception text. Request failures use stable categories (DNS/TLS/timeout/HTTP/unavailable); display diagnostics separately. `needs_review = bool(findings)`.

- [ ] **Step 1: Write failing coverage tests.** Assert full 1.24 / `2026-10-12`, assessed 1.26 / `2026-10-24`, evidence files contained/existing; a sessions delta to 1.26 leaves its full verification at 1.24; a genuine `2027-01-15` date validates; invalid calendar dates, invalid tags, reversed deltas, assessed-before-full, absent evidence, path escape, booleans/non-object JSON and malformed nested lists produce errors, not crashes. Use temporary files and copied metadata; no network.
- [ ] **Step 2: Write failing audit tests.** Assert latest 1.26 with assessed 1.26 and full 1.24 has no release finding; 1.27 produces `new_release`; unknown latest on TLS failure yields request failure, not a fabricated release; lower latest does not request a downgrade. Equal finding sets on different dates/orders have equal fingerprints; changed missing signal or release changes fingerprint; changed transient diagnostics in the same failure category do not. CLI `--output` remains valid and optional JSON matches Markdown decisions. Patch `request` and `latest_dotnet_release` for all tests.
- [ ] **Step 3: Run `python3 -B -m unittest discover -s tests -p 'test_*knowledge.py' -v` and the analogous `test_audit_maf_sources.py` discovery.** Expect failures from missing interfaces or old audit semantics.
- [ ] **Step 4: Implement coverage and audit interfaces.** Keep existing source URLs and request timeout. Populate per-area full verification at 1.24; attach only the deltas supported by the current scoped record, with explicit scope text. Give unchanged areas no new delta. Use `date.fromisoformat`, numeric release comparison and contained evidence paths. Audit never edits coverage or guidance; return nonzero on request/metadata failures while writing usable reports for request failures. Metadata validation errors fail before fetching sources.
- [ ] **Step 5: Integrate validator and maintenance prose.** Validate coverage JSON; replace the statement that every newer-than-full-baseline release must be flagged with the assessed/full distinction. Keep the versioned historical matrix and row evidence. Explain how reviewed deltas are recorded without whole-area promotion. No fresh MAF API verification is inferred.
- [ ] **Step 6: Run new tests, full unittest discovery, validator, compileall and `git diff --check`; expect all pass.** Commit task-owned files deliberately: `feat: track assessed releases separately from full verification`.

## Task 3: Notify only new actionable audit findings

**Files:** Create `scripts/sync-maf-audit-issue.py`, `tests/test_sync_maf_audit_issue.py`; modify `.github/workflows/source-audit.yml` and maintenance docs.

**Interfaces:** `notification_action(audit: dict, issues: list[dict]) -> tuple[str, int | None]`, returning `none`, `create` or `update` plus issue number; exact title `MAF source audit`; body marker `<!-- maf-source-audit:<fingerprint> -->`. `sync_issue(audit: dict, report_path: Path, run_gh: Callable[[list[str]], str]) -> str` calls gh without a shell and returns its action. CLI consumes `--audit-json PATH --report PATH`; it must not publish malformed, mismatched or missing reports.

- [ ] **Step 1: Write failing tests.** Clean report -> no mutation; actionable/no exact-title open issue -> create; same fingerprint -> no mutation/comment; changed fingerprint -> update existing issue body; similarly named issues remain untouched; multiple exact-title issues -> deterministic lowest number; closed issue ignored. Reject invalid schema/fingerprint or report mismatch before remote writes. Fake gh listing/error paths and assert no shell interpolation and no issue comments. An actionable recurring finding after a closed issue may create a new issue; clean reports never close issues automatically.
- [ ] **Step 2: Run `python3 -B -m unittest discover -s tests -p test_sync_maf_audit_issue.py -v`; expect missing-module/interface failures.**
- [ ] **Step 3: Implement helper and workflow.** Validate input fingerprint against Task 2 canonical calculation (reuse that helper, expose `audit_fingerprint(findings: list[dict], assessed_release: str) -> str`). Add/check the marker when rendering Markdown so JSON and report agree. Use argument lists and `--body-file` for gh. Keep read-only collection and `issues: write` notification responsibilities separate. Workflow requests both outputs and invokes sync only if valid reports exist; collector failures remain visible. No report -> explicit job failure, not a fabricated clean audit. Skip duplicate/clean writes without requiring a new persistent service or checked-in run state.
- [ ] **Step 4: Run helper/audit tests, full unit suite, compileall, validator and diff whitespace check.** Inspect workflow conditions using mocked CLI runs for clean, changed, repeated and collection-failure reports; do not send real GitHub messages. Commit: `fix: deduplicate scheduled MAF audit notifications`.

## Task 4: Migrate the public skill interface and all active consumers atomically

**Files:** Five skill roots; moved references from the file map; two new shared design/process references; `resources/skill-contract.json`; v2 routing dataset; validator and both existing test modules; active docs/profiles/README/AGENTS/CHANGELOG; historical local links affected by moves.

**Interfaces:** Contract exactly declares `maf-adoption`, `maf-architecture`, `maf-implementation`, `maf-testing`, `maf-review`. Add validator `load_skill_contract(root: Path, errors: list[str]) -> dict | None`, `validate_routing(known_skills: set[str], errors: list[str], routing: Path | None = None) -> None`, and keep `validate_plugin(root: Path, errors: list[str]) -> None` read-only for isolated installed copies. Contract errors must be actionable without crashing callers; retired names cannot be active skills or v2 expected/prohibited routes. v1 remains an explicitly historical resource and is not validated against current skill names.

- [ ] **Step 1: Write failing installed-layout/routing tests.** Temporary fixtures include the contract under copied resources. Assert current five entries match contract; missing/extra/duplicate declaration, malformed/escaping contract path, invalid route target, missing resource and symlink fail; `maf-implementation` is allowed. Update old tests to reference surviving/new files. Assert v2 preserves every v1 case ID and behavioral assertion while mapping old routes to implementation, deduplicating lists and removing expected/prohibited conflicts. Add regression for a deliberately declared extra test skill: a valid contract-driven temporary fixture passes without a hardcoded five-name constant. This tests flexible contracts, not expanding the shipped interface.
- [ ] **Step 2: Run affected tests to capture old-validator failures.** Record that current code forbids `maf-implementation`, requires fourteen skills and knows only v1.
- [ ] **Step 3: Migrate reference knowledge.** Move the thirteen files exactly as mapped; integrate durable guidance from removed skill bodies into topic references without losing current 1.25–1.26 details. Preserve tags, dates, maturity and provider qualifications. Keep no alias SKILL.md files. Repair relative links throughout the plugin and local links in historical docs without rewriting historical claims. Record old->new coverage in migration docs so every removed abstraction retains an owner.
- [ ] **Step 4: Author the five public skill bodies.** Architecture routes to proportional design/gap assessment and relevant patterns; implementation routes directly to topic references with a small assessment and installed-version checks; testing/review retain substantive contracts and no-findings outcomes; adoption remains explicit and supports greenfield context without scaffolding the plugin or forcing adoption before work. Descriptions express user goals with boundaries; no root requires every technical reference or unconditionally starts another skill.
- [ ] **Step 5: Write shared design/process guidance.** Encode facts/problem/open decision/optional improvement/sufficient design; select questions by material consequence, respect delegation and settled requirements, and allow deterministic solutions. Superpowers/project process owns sequencing/documents/approvals when active; standalone operation supplies a lightweight fallback. Reuse canonical project context and existing documentation policy. No new generic approval gate.
- [ ] **Step 6: Switch validator, contract and all active consumers together.** Remove `REQUIRED_SKILLS`, the explicit implementation prohibition and fixed routing path assumptions; load the contract for package/main validation and dynamic output counts. Update bundled profiles, adoption/setup/distribution/smoke-test docs and root maintainer rules to five skills, new routing and one-process behavior. In active pattern v4 text, replace retired invocation names and repair paths without changing MAF claims; the new catalog comes next. At this intermediate checkpoint the contract's `pattern_catalog` points to `resources/docs/patterns/v4.md`; Task 5 changes it to the final mapped `catalog.md` only once that file exists and its validator is ready. README temporarily keeps its working v4 link and current baseline. CHANGELOG records unreleased public-route migration; plugin versions stay 0.1.1.
- [ ] **Step 7: Run all deterministic checks and inspect retired-name occurrences.** Use `rg -n 'maf-(agents|tools|workflows|context-memory|middleware|provider-integration|hosting|security|observability|devui)' skills resources docs README.md AGENTS.md scripts tests`. Remaining occurrences must be explicit migration mappings, historical cases/records or source topic names, not active invocation instructions. Validate an isolated installed copy with no scripts/source checkout. Commit coherent migration: `refactor: organize MAF skills around architectural assistance`.

## Task 5: Make patterns and validation express design decisions

**Files:** Create `resources/docs/patterns/catalog.md`; modify patterns README, active README/profile/reference links, contract, `scripts/validate-template.py`, `tests/test_validate_template.py`; retain v4 as historical catalog with repaired resource links.

**Interfaces:** Active catalog uses `## <stable-id>: <title>` with sections `When it fits`, `Responsibilities and boundaries`, `Alternatives`, `Failure behavior`, `Acceptance examples`. `validate_catalog(errors: list[str]) -> None` reads the contract's catalog path; requires at least one unique pattern and the five sections, no fixed count or mandatory code. `validate_matrix` retains field/source requirements but parses dates/tags instead of searching for `2026-`.

- [ ] **Step 1: Write failing catalog/matrix tests.** Temporary catalogs with one or eighteen valid patterns pass; duplicate IDs, missing alternatives/acceptance examples or an escaped path fail; a valid pattern containing only prose/contracts and no C# passes. Matrix dates in 2027 pass; `2026-02-30`, invalid release and missing source fail. Retain all current capability rows rather than asserting an arbitrary minimum as evidence of completeness; validate nonempty unique feature rows and consistency with documented coverage.
- [ ] **Step 2: Run focused tests; expect current fixed seventeen/C# heading/year checks to fail.**
- [ ] **Step 3: Build the active problem-oriented catalog.** Map all seventeen existing playbooks into cases or conditional technical references and record that mapping in the migration doc. Cover adoption, conversational streaming, multimodal input, extraction, read-only lookup, consequential action, deterministic/agentic/hybrid retrieval, controlled workflow, recovery/HITL, delegation, runtime skills/Harness choice, hosting, provider migration, evaluation and incident diagnosis. Group where decisions overlap; do not force a target count. Include direct links from patterns to relevant technical evidence and from architecture/implementation routers to the catalog.
- [ ] **Step 4: Implement catalog/matrix checks and switch active entry links.** Update required README link checks to consume the contract and retain coverage/evaluation entry points. Keep historical v4 facts and evidence dates intelligible; no wholesale version string replacement.
- [ ] **Step 5: Run all deterministic checks and compare old->new pattern coverage.** Confirm MAF technical limitations remain conditionally reachable, architecture can load a pattern without the whole release history, and no claim has been silently broadened. Commit: `docs: center MAF patterns on architectural decisions`.

## Task 6: Evaluate the assistant and finish the migration evidence

**Files:** Extend v2 JSONL and evaluation README/protocol; update dated evaluation record and `docs/migration-to-architectural-assistant.md`; adjust owning skill/reference when an observed behavior fails; add schema tests in `tests/test_validate_template.py`; update Unreleased validation notes as warranted.

**Interfaces:** v2 retains `{id, prompt, expected_skills, must_not_route, assertions?}`; add new IDs from Task 1 with explicit material behavior assertions and reference each architecture variant. Scenario repository inputs remain in the cases JSON. Validate cases schema and referenced IDs separately from model behavior; no text-presence test purports to establish brainstorming quality.

- [ ] **Step 1: Write failing evaluation-schema tests.** Duplicate case IDs, unexpected process owner, absolute/traversing fixture file paths, malformed repository mappings and absent behavior lists fail; empty repository for greenfield passes. Every migrated v1 case/behavior survives and new IDs have matching scenarios; generic .NET and small-edit routes remain allowed to select no MAF skill. Implementation cases do not require architecture selection merely to perform a proportional assessment.
- [ ] **Step 2: Run schema tests, then add minimal validation and final v2 fixtures.** Every design-spec scenario has an observable expected/prohibited behavior, including no-findings and delegated design. Commit no sample application code into this repository; fixture file text can materialize into disposable temp repos during evaluation.
- [ ] **Step 3: Run the Task 1 protocol against the candidate.** Use the same cases, input hashes and two fresh runs per scored mode. Compare representative explicitly invoked/reference runs with baseline; run new version-specific regression probes against moved references. Test process-owner scenarios using actual process skills when available; a textual stand-in is disclosed as a reference probe. Run autonomous discovery in a real candidate plugin session only when available; never infer it from a supplied path.
- [ ] **Step 4: Correct material observed failures in their owning skill/reference and rerun affected cases.** Record failures, edits and reprobes, including unnecessary questioning and invented objections. Do not broaden testing after passing without a new failure/change/uncertainty; do not change fixture expectations to excuse a bad response. Label unexecuted modes/cases pending rather than giving fabricated scores. Native-client smoke checks remain explicitly pending unless performed; no release is part of this plan.
- [ ] **Step 5: Complete migration and maintenance documentation.** Explain ten retired invocation replacements, profile/context updates for existing users, new-solution operation, standalone/Superpowers behavior, coverage update procedure, clean/repeated audit behavior and unchanged version certainty. Document the installed cache is not automatically updated by checkout changes. Preserve pre-existing review evidence and distinguish carried-in content from this refactor.
- [ ] **Step 6: Run final verification.** Commands: `python3 scripts/validate-template.py`; `python3 -m compileall -q scripts`; `python3 -B -m unittest discover -s tests -v`; `bash -n skills/maf-architecture/scripts/inspect-maf.sh`; `git diff --check`. Expect dynamic five-skill/active-pattern/v2 success, all tests passing, no syntax/whitespace errors. Run Markdown link verification through the existing CI tool when available; otherwise report external-link checks unrun and retain local containment validation. Do not run a live source audit simply for a structural refactor.
- [ ] **Step 7: Review final diff against the approved spec and request independent code/skill review.** Verify no lost 1.26 evidence, duplicated process, hidden provider coupling, accidental version bump, missing historical links or newly broad compile/runtime claims. Resolve material review findings and rerun only affected checks. Commit task-owned evidence/fixes: `test: evaluate MAF architectural assistant behavior`.

## Self-review and handoff

Spec coverage: behavioral contract and coexistence -> Tasks 1/4/6; five-skill interface and migration -> Task 4; stable/problem/technical layers -> Tasks 4/5; assessed/per-area evidence and audit deduplication -> Tasks 2/3; deterministic/behavioral/client distinction -> Tasks 1/6; preservation and release boundaries -> global constraints and all completion checks.

Dependencies: Task 1 precedes behavioral rewrites. Task 3 consumes Task 2's report/fingerprint. Task 4 is the atomic public-interface cutover. Task 5 consumes Task 4's contract. Task 6 compares the preserved baseline with the final candidate. Each task ends with a working structurally validated repository; default tests never depend on paid models, live sources or GitHub writes.

The implementation method has not yet been selected. Recommend native execution for this tightly coupled prose/routing migration, with an independent final review; subagent-driven execution remains an option with fresh implementation/review contexts per task. Implementation starts after plan review and method selection, following the writing-plans handoff.
