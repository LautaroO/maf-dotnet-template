# Maintaining the MAF knowledge base

MAF changes quickly. Treat this repository as version-aware guidance, not frozen API documentation.

## Update process

When a new MAF release materially changes an abstraction:

1. read current Microsoft Learn docs;
2. inspect the official release/tag/source;
3. compare with the previous template assumption;
4. update only the skill/reference that owns that abstraction;
5. avoid copying provider setup unless needed to explain the abstraction;
6. preserve “verify installed package APIs” warnings where version drift is plausible;
7. add a changelog entry.

The scheduled source audit may open or refresh a maintenance issue with release/link evidence. The script never edits guidance. When the user requests a knowledge update, Codex performs the source review and edits the guidance; the maintainer reviews the resulting diff and any release decision.

## Codex maintenance workflow

Running the script is the evidence-gathering step, not the completed update. In this plugin repository, ask Codex:

> Review the MAF audit at /tmp/maf-source-audit.md and update the affected skills, references, capability matrix and patterns against the official .NET release. Record sources, version uncertainty and validation results. Keep the plugin version unchanged until a release is requested.

Codex must then:

1. Read the audit, current Git diff and root maintainer instructions. Diagnose failed source requests before treating `unknown` or missing content as release evidence. If no usable report exists, run `python3 scripts/audit-maf-sources.py --output /tmp/maf-source-audit.md`.
2. Identify the checked-in baseline and target .NET tag. Read every intervening .NET release; exclude unrelated Python changes. Inspect matching tagged source/samples for changed public APIs, packages and maturity. HTTP 200 and phrase matches do not prove semantic correctness.
3. Reconcile Microsoft Learn with tagged source. When they disagree, record both sources, inspect package metadata and distinguish source implementation, published package and installed API availability. Keep unresolved claims explicitly qualified.
4. Map each relevant change to its owning skill/reference, matrix row, pattern and behavior fixture. Apply the supported changes directly in `skills/` and `resources/`, preserving provider neutrality and installed-package checks. Record unchanged areas and unresolved evidence rather than replacing version strings globally.
5. Save a dated review under `docs/reviews/` with baseline/target, official links, decisions, changed files and remaining verification. Update `CHANGELOG.md` under Unreleased. Advance a matrix row's verification only for evidence actually reviewed; advance the overall baseline only after the whole matrix is reviewed.
6. Run `python3 scripts/validate-template.py`, `python3 -m compileall -q scripts`, `python3 -B -m unittest discover -s tests -v`, shell syntax checks and `git diff --check`. Check changed Markdown links. Report which behavioral probes were run; fixture validation alone does not prove client routing.
7. Deliver the diff, review record, command results, provider coupling, version certainty and untested client behavior. A requested documentation update authorizes these repository edits; release, publication and native-client verification are separate outcomes.

For Python.org installations on macOS, a missing default CA bundle can cause `CERTIFICATE_VERIFY_FAILED`. Inspect `ssl.get_default_verify_paths()` and use the matching Python installation's `Install Certificates.command`; then rerun the audit. Keep HTTPS certificate verification enabled.

For every release update `plugin.json`, `VERSION`, `CHANGELOG.md`, release notes, the matrix's last-verified release/date, routing fixtures when boundaries change, and both fresh-session profile smoke-test records.

## What belongs in application AGENTS.md

The application templates in `resources/profiles/` contain durable invariants that should affect almost every MAF task. The root `AGENTS.md` here is plugin-maintenance guidance, not an application template. Keep the shared knowledge in the installed plugin. Application instructions include:

- least-agentic design;
- provider neutrality;
- state taxonomy;
- validation/security/reliability basics;
- skill routing.

## What belongs in a skill

Task-specific workflow and decision rules for one MAF abstraction.

## What belongs in references

API patterns, source links, version-sensitive notes, examples, crosswalks, and detailed checklists.

## Avoid stale API cargo culting

Prefer wording such as:

> Current MAF docs use `AIFunctionFactory.Create`; verify the installed package surface before coding.

instead of:

> Always call this exact overload.

The goal is to make Codex MAF-aware without making it confidently compile against the wrong version.

## Assessment versus verification

`resources/docs/capabilities/coverage.json` is the machine-readable coverage index. `last_assessed_release` records the latest release whose deltas were reviewed; `full_verification` and each area retain their own evidence. Record a scoped delta with its exact scope instead of promoting a whole area. A reviewed 1.26 delta does not advance the complete 1.24 baseline. A new release, request failure, redirect or missing content signal is a separate audit finding; phrase matches are not semantic verification. Diagnose connectivity before inferring an API change.

The audit preserves `--output PATH` and optionally writes `--json-output PATH`. Both contain the same finding fingerprint; timestamps, ordering, duplicate findings and transient diagnostic text do not produce new notification identities. The collector never edits guidance.

The scheduled job uses `scripts/sync-maf-audit-issue.py` to compare the canonical finding fingerprint with the exact-title open issue. Clean or unchanged findings cause no writes or comments. Changed findings update the existing issue; new actionable findings create one when none is open. Closed issues are not modified and clean reports do not close issues. Malformed/mismatched reports fail before remote mutation. Collection failures remain failing workflow results even when their diagnostics were successfully reported. Concurrent audit jobs are serialized. Local unit tests fake gh; they do not send messages.
