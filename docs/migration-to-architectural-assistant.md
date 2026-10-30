# Migrating to the architectural assistant

This is an Unreleased public-routing change. The package manifest and VERSION remain 0.1.1 during development; this checkout does not prove a new cached installation is active. Publishing a release, changing an external marketplace and updating an adopting application are separate actions.

## Public entry points

| Task | Skill |
|---|---|
| Explicitly merge project guidance | `$maf-adoption` |
| Analyze an idea/design or substantial architectural change | `$maf-architecture` |
| Implement or integrate the selected behavior | `$maf-implementation` |
| Design deterministic checks and semantic evaluation | `$maf-testing` |
| Review a design/repository/diff | `$maf-review` |

The retired entry points `maf-agents`, `maf-tools`, `maf-workflows`, `maf-context-memory`, `maf-middleware`, `maf-provider-integration`, `maf-hosting`, `maf-security`, `maf-observability` and `maf-devui` now route to implementation topic references. A substantive design or review request can instead use architecture or review directly; these are task distinctions, not a compulsory pipeline. No discoverable aliases are retained.

Update explicit invocations and the routing section of existing project instructions deliberately. Preserve local adaptations and context; do not rerun adoption or replace root instructions just to implement a change. Use the client-displayed plugin namespace. Existing clients stay on their installed version until refreshed and verified; a renamed source folder does not migrate their cache.

## Technical coverage

All references below are under `skills/maf-implementation/references/`. Existing scoped release evidence remains intact; these paths identify the current knowledge owner, not a fresh API verification.

| Former owner/reference | Current reference |
|---|---|
| agents / agent-patterns | agents.md |
| tools / function-tools | function-tools.md |
| tools / mcp-and-approval | mcp-and-approval.md |
| workflows / executors-edges | executors-edges.md |
| workflows / orchestrations | orchestrations.md |
| workflows / state-checkpoints-hitl | state-checkpoints-hitl.md |
| context-memory / session-context-rag | context-memory.md |
| middleware / pipeline-layers | middleware.md |
| provider-integration / provider-boundary | providers.md |
| hosting / hosting-selection | hosting.md |
| security / security-checklist | security.md |
| observability / otel | observability.md |
| devui / devui | devui.md |

## Design and project processes

The assistant analyzes material gaps before dependent implementation. It accepts adequate designs, treats optional improvements separately and uses the small-change process for exact edits. It supports new solutions without inventing installed SDK/packages and existing products without moving domain behavior into AI.

With an active Superpowers or team process, contribute MAF decisions inside its conversation, canonical design and approval rules. Availability alone does not activate a process. Without one, use lightweight agent-specific discovery and proportionate documentation; no Superpowers dependency or universal approval ceremony is added.

## Evidence and maintenance

`resources/docs/capabilities/coverage.json` distinguishes the fully verified 1.24 baseline from the last assessed 1.26 release and narrowly scoped area deltas. The audit reports new releases and source problems without relabeling complete verification. Repeated/clean findings cause no GitHub writes; actual changes are reviewed through the maintenance workflow. Structural tests and supplied-reference probes do not prove native installation, autonomous routing, compilation or runtime application behavior.
