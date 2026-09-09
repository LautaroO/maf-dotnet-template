# Adoption workflow

## Inspect

Use `rg --files`, then inspect existing instructions, solution/project boundaries, packages and commands. Identify where MAF types appear and whether non-AI code depends on them.

## Place

For an embedded AI module, copy the shared `.agents/` knowledge layer to the repository root, merge the root boundary fragment without replacing local rules, and place the AI-module profile at the AI subtree. For AI-first, merge the AI-first profile into the root.

## Populate

Record exact SDK/target frameworks, package versions, commands, component locations, providers/capabilities, state/persistence/durability, hosting/protocols, security/privacy/approval constraints, and provider-specific exceptions.

## Verify

Check instruction hierarchy and budgets, broken references, generic .NET non-trigger behavior, and that removing the AI module would not remove domain rules or ordinary use cases. Run a fresh Codex session with one profile-relevant request and one generic .NET negative request.
