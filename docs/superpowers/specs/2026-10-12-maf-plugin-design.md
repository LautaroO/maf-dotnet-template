# MAF plugin distribution design

## Intent and scope

Distribute the MAF developer guidance exclusively as a skills-only Codex plugin. This repository is the package itself; a separate marketplace will reference it. Preparing the local package is authorized; publishing, installation and updating maf-playground are separate actions.

## Layout and authoring

Use `plugin.json` at the repository root, with identity `maf-dotnet`, MIT license and publisher/repository metadata. Maintain the fourteen skills directly under `skills/`. Shared references, application adoption profiles, the capability matrix, pattern catalog and routing fixtures live under `resources/`. No generated package, generator, marketplace catalog, MCP server or application runtime skill store is included.

Skill-relative links must resolve inside an isolated installed copy. Resource files cannot rely on symlinks or the author's checkout. The root AGENTS.md governs plugin maintenance; resources/profiles contains the templates for adopting applications.

## Adoption

Installation supplies developer skills. Explicit adoption inspects the target and merges only project instructions, preserving root rules and local conventions. Shared skills/resources remain in the plugin. Existing repository skill adaptations must be reviewed before removing duplicate copies. Provider-specific setup and application NuGet versions stay in the target project.

## Validation and releases

The standard-library Python validator checks root manifest/version consistency, exactly fourteen skill contracts, resource containment, matrix/pattern/routing metadata, profiles and hygiene. Tests use temporary isolated package copies and mutation cases for invalid manifests, missing/unsafe resources, symlinks and duplicate skill copies. CI retains Markdown and shell syntax checks and source auditing.

Keep plugin.json and VERSION synchronized for releases. Existing guidance-only tags do not become plugin releases merely because the development tree changed. Native-client installation and fresh-session routing remain manual release gates; automated structural checks do not prove them.

## Acceptance criteria

1. One canonical skills/resources copy; no .agents skill copy or nested generated package.
2. All fourteen skills and existing reusable guidance are retained, with working local references.
3. External catalogs use a repository-root Git source.
4. Root maintainer instructions and application profiles have separate scopes.
5. Validator, full unittest suite, syntax checks and diff whitespace checks pass.
6. No NuGet/provider/application behavior changes or remote publication.
