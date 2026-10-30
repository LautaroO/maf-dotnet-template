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

All references below are under `skills/maf-implementation/references/`. These references retain stable concepts and investigation criteria; exact SDK behavior is looked up on demand in the official repository and installed packages.

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

## Stable guidance and source investigation

The user-selected final scope removes the compatibility matrix, release verification resources, coverage metadata and scheduled audit/issue automation. Exact signatures, fixes and integration defaults are checked in the target stack using [official-source investigation](../resources/references/official-sources.md). There is no global MAF version certification or routine per-release update obligation.

The five public skills and fourteen problem patterns remain. Active routing v2 now evaluates package inspection, official source matching and scoped uncertainty instead of testing recall of named releases. Git history preserves retired v1/version-specific resources and prior review records are historical. Existing applications keep their installed package versions unless the user authorizes a change. Installation/routing and SDK/runtime correctness remain separate checks.

## Historical playbook coverage

| v4 playbook | Active pattern ID |
|---|---|
| 1 adoption | adoption |
| 2 sessions/streaming and 5 read-only tools | conversation-lookup |
| 3 multimodal | multimodal |
| 4 extraction | structured-decision |
| 6 side effects | consequential-action |
| 7 two-step and 8 agentic/hybrid RAG | retrieval |
| 9 sequential/conditional workflow | controlled-process |
| 10 fan-out/fan-in | parallel-process |
| 11 HITL and 12 background/durable | recoverable-wait |
| 13 orchestration | delegation |
| 14 runtime skills/Harness | runtime-instructions |
| 15 hosting/protocol | hosting |
| 16 provider/package migration | migration |
| 17 evaluation/observability/incidents/review | verification-operations |

The active catalog retains concepts from seventeen historical playbooks into fourteen problem patterns. The validator checks meaningful sections and unique IDs, not that chosen count or the presence of C#.
