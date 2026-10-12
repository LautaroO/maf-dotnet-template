# Migration to plugin-only distribution

The repository is now a portable plugin at its root. Plugin versioning starts at `0.1.0`, marking an initial development release. Earlier versioned migration notes and `4.x` release records describe the historical guidance pack, not the plugin's maturity.

| Previous location | Current source |
| --- | --- |
| `.agents/skills/` | `skills/` |
| `.agents/references/` | `resources/references/` |
| `profiles/` | `resources/profiles/` |
| `docs/capabilities/` | `resources/docs/capabilities/` |
| `docs/patterns/` | `resources/docs/patterns/` |
| `evaluations/skill-routing/` | `resources/evaluations/skill-routing/` |

`plugin.json` identifies `maf-dotnet` directly. There is no generated `plugins/maf-dotnet/` copy or `build-plugin.py`; edit skills and resources in place. The existing validation command remains `python3 scripts/validate-template.py` and now checks the root plugin.

The separate marketplace should use a repository-root `url` source, rather than a `git-subdir` source pointing at a generated directory. Its selected ref must contain this layout; historical guidance-only release tags do not.

For adopting applications, install the plugin first and explicitly select its `maf-adoption` skill. Preserve existing project instructions and merge the appropriate packaged profile. Do not copy this repository's root maintainer `AGENTS.md` into an application.

Review older repository-scoped skill adaptations before removing copies. Move project-specific rules into the application's instructions or references and retain the plugin as the shared knowledge layer. Migration does not update MAF NuGet packages or install runtime Agent Skills.

See [distribution](plugin-distribution.md) and [adoption](adopting-the-template.md) for the current workflow.
