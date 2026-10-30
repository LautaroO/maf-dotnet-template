# Adoption workflow

## Inspect

Use `rg --files`, then inspect existing instructions, solution/project boundaries, packages and commands. Identify where MAF types appear and whether non-AI code depends on them.

Find authoritative context, architecture/ADR and feature documents, naming conventions, and existing refinement/planning skills. Bundled plugin documentation is not evidence of a product documentation convention.

## Place

Use the bundled `resources/profiles/`, conceptual references and pattern catalog relative to the installed plugin root. Merge the selected profile into the target instructions; keep the plugin knowledge layer installed instead of copying a second set of skills. These are package resources, not paths assumed to exist in the target application. Remove old repository skill copies only after reviewing local adaptations and preserving any necessary project-specific guidance.

For an embedded AI module, merge the root boundary fragment without replacing local rules and place the AI-module profile at the AI subtree. For AI-first, merge the AI-first profile into the root. Use the templates from `resources/profiles/`; the plugin repository's root `AGENTS.md` is maintainer guidance and must not be copied into an application.

For either profile, keep shared concept/pattern resources in the plugin. Check that the implementation skill can open its topic references and official-source guidance after adoption.

## Populate

Record exact SDK/target frameworks, package versions, commands, component locations, providers/capabilities, state/persistence/durability, hosting/protocols, security/privacy/approval constraints, and provider-specific exceptions.

Keep a concise context index in the applicable `AGENTS.md`, linking to existing canonical documents rather than duplicating their contents. Record the product's refinement process. If a new documentation location is needed, propose its scope and naming with a rationale; record it only after user agreement. Pending agreement does not block independent inspection or authorized instruction merging, but no new context/specification document is created yet.

## Verify

Check instruction hierarchy and budgets, broken references, generic .NET non-trigger behavior, and that removing the AI module would not remove domain rules or ordinary use cases. Run a fresh Codex session with one profile-relevant request and one generic .NET negative request.

Verify reuse of an existing documentation/process convention, proposal without new documents when no convention exists, and a small fully specified change that requires neither a new specification nor redundant questions.
