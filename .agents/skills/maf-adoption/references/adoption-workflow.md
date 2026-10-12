# Adoption workflow

## Inspect

Use `rg --files`, then inspect existing instructions, solution/project boundaries, packages and commands. Identify where MAF types appear and whether non-AI code depends on them.

Find authoritative context, architecture/ADR and feature documents, naming conventions, and existing refinement/planning skills. Copied pack documentation is not evidence of a product documentation convention.

## Place

For an embedded AI module, copy the shared `.agents/` knowledge layer to the repository root, merge the root boundary fragment without replacing local rules, and place the AI-module profile at the AI subtree. For AI-first, merge the AI-first profile into the root.

For both profiles, also copy/merge `docs/capabilities/` and `docs/patterns/` at their original relative paths. Preserve existing files and resolve conflicts manually. Check that the hosting skill can open the capability matrix after adoption.

## Populate

Record exact SDK/target frameworks, package versions, commands, component locations, providers/capabilities, state/persistence/durability, hosting/protocols, security/privacy/approval constraints, and provider-specific exceptions.

Keep a concise context index in the applicable `AGENTS.md`, linking to existing canonical documents rather than duplicating their contents. Record the product's refinement process. If a new documentation location is needed, propose its scope and naming with a rationale; record it only after user agreement. Pending agreement does not block independent inspection or authorized instruction merging, but no new context/specification document is created yet.

## Verify

Check instruction hierarchy and budgets, broken references, generic .NET non-trigger behavior, and that removing the AI module would not remove domain rules or ordinary use cases. Run a fresh Codex session with one profile-relevant request and one generic .NET negative request.

Verify reuse of an existing documentation/process convention, proposal without new documents when no convention exists, and a small fully specified change that requires neither a new specification nor redundant questions.
