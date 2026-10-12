# Distributing the MAF .NET plugin

This repository owns the guidance and the `maf-dotnet` plugin package. It is not a marketplace. A separate marketplace repository owns the catalog and references this package through a repository-root Git source.

## Package and authoring

The repository root is the portable plugin package: `plugin.json`, `skills/`, `resources/`, and `LICENSE` are maintained directly. Skills reference shared resources through relative paths inside this same checkout. There is no package generation step or second copy of the guidance. The plugin has no MCP server, lifecycle hook, installer or application runtime dependency.

Run these commands in the repository:

```bash
python3 scripts/validate-template.py
python3 -B -m unittest discover -s tests -v
```

CI verifies manifest/version consistency, the fourteen skills, local resource links and repository hygiene. For releases, update `plugin.json`, `VERSION` and the changelog together. The plugin version is independent of installed Microsoft Agent Framework NuGet versions.

## Entry in a separate marketplace

Create `.agents/plugins/marketplace.json` in your separate marketplace repository. The following is an example catalog, not a file to add to this guidance repository:

```json
{
  "name": "lautaro-plugins",
  "interface": {
    "displayName": "Lautaro Plugins"
  },
  "plugins": [
    {
      "name": "maf-dotnet",
      "source": {
        "source": "url",
        "url": "https://github.com/LautaroO/maf-dotnet-template.git",
        "ref": "main"
      },
      "policy": {
        "installation": "AVAILABLE",
        "authentication": "ON_INSTALL"
      },
      "category": "Productivity"
    }
  ]
}
```

The referenced Git ref must contain the root plugin manifest and its skills/resources. Existing guidance-only tags are not plugin releases. `main` is convenient during development; select a published release tag or commit (`sha` instead of `ref`) for reproducible releases. Do not point a catalog at an unpublished tag.

Once that external catalog is published, register its actual repository:

```bash
codex plugin marketplace add OWNER/MARKETPLACE_REPO
codex plugin marketplace list
```

Registering a marketplace is distinct from installing its plugins. Open the plugin directory in the supported desktop client, select the external marketplace and install `maf-dotnet`. Refresh a configured catalog with `codex plugin marketplace upgrade MARKETPLACE_NAME` when appropriate; verify which plugin version the client actually loads.

## Local test before publication

Create a disposable external directory containing a marketplace catalog and a copy of this repository under `plugins/maf-dotnet/`, excluding `.git`, ignored caches and private configuration. In that catalog, replace the Git source with:

```json
"source": {
  "source": "local",
  "path": "./plugins/maf-dotnet"
}
```

Keep the rest of the catalog metadata, then register the disposable directory with `codex plugin marketplace add /absolute/path/to/test-marketplace`. Install the plugin in the desktop directory and restart the client as required. The installed copy is cached: editing the source repository alone does not establish that the loaded package has changed.

This workflow keeps marketplace files outside this repository and does not require a separately hosted web service. See the [official packaging and marketplace documentation](https://developers.openai.com/plugins/build/plugins) for current client support and commands.

## Explicit adoption into a project

Installation supplies developer skills and resources; it does not edit project instructions, update NuGet packages, or add capabilities to application agents.

Explicitly select the installed plugin's `maf-adoption` skill and request inspection of the target repository. Use the packaged profiles to merge scoped instructions and project context while preserving the existing root `AGENTS.md`. The plugin remains the shared knowledge layer; no repository skill copy is needed.

If the target already contains `.agents/skills/maf-*`, review local changes before choosing one source of skills. Preserve project-specific rules in the applicable instructions or references before removing duplicate copies. Use the installed plugin's namespace shown by the client when selecting a skill; do not assume an unqualified invocation resolves to the installed copy.

## Release checks

1. Update `plugin.json`, `VERSION` and the changelog for a release, and run plugin validation and all tests.
2. Install the package from a disposable external catalog in a supported native client. Confirm all fourteen skills are discoverable and their resources open from the cached installation.
3. In fresh sessions, check adoption into both an existing application and an AI-first repository; confirm a generic .NET request does not spuriously trigger MAF guidance.
4. Confirm installed-plugin adoption preserves existing project rules and does not duplicate the skills or claim unverified package APIs.
5. Publish the plugin files to the intended Git ref, then update the separate marketplace's source selector and verify that installation uses that version.

Automated checks prove manifest/version consistency, reference containment and that an isolated installed copy has its required resources. They do not prove native-client installation, automatic skill selection or remote publication; those remain explicit release checks.
