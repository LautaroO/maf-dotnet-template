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

## What belongs in AGENTS.md

Only durable invariants that should affect almost every MAF task:

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
