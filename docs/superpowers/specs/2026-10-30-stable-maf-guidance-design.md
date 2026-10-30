# Stable MAF architectural guidance amendment

Status: approved direction from the user's explicit instruction on 2026-10-30. This amendment supersedes version-specific knowledge retention and release-audit requirements in the architectural-assistant design and plan. The previously selected native execution and existing PR #4 remain the delivery path.

## Intent and scope

Retain the five public skills, proportional architectural assistance, problem-oriented patterns and durable implementation concepts. Remove the obligation to maintain release-specific API knowledge in this plugin. The official [MAF repository](https://github.com/microsoft/agent-framework) becomes the primary external reference for implementation details, matched to the target application's actual packages.

The alternatives discussed were retaining conditional version-specific knowledge or retaining stable concepts plus on-demand official investigation. The user selected the latter to reduce maintenance of frequently changing information.

## Decisions

- Keep conceptual topics: agents, bounded tools, MCP/approval, typed workflow control, delegation, state/recovery, context/RAG, interception, provider boundaries, hosting, security, telemetry and development UI.
- Remove release deltas, package maturity tables, constructor/overload migrations, exact release-dependent defaults and fixes, full/per-area verification metadata, and cached SDK code examples from active resources. Keep conceptual abstraction names only as orientation/search terms; verify their availability before use.
- Remove the scheduled source-audit workflow, collector, issue synchronizer, coverage helper and their tests. No automated update issues or replacement service.
- Remove the capability matrix, dated verification resources, obsolete v4 catalog and v1 routing resource. Git history preserves retired artifacts; historical review/release documents may link to the previous committed files and must be clearly labeled as historical.
- Replace release-specific active behavior fixtures with package-inspection, source-discovery and uncertainty scenarios. Preserve architecture, small-change, tenancy, state, recovery, testing and process-coexistence behavior.
- For implementation identify actual SDK/TFM/package/API evidence, consult relevant .NET source/samples in the official repository (matching tag when available), reconcile supporting Learn/package evidence, and adapt to the installed surface. For a new solution distinguish proposals from installed facts. No silent upgrades, unverified signatures or claims that unavailable network access proves a capability absent.
- Maintain guidance when an architectural principle/pattern changes or real use demonstrates a gap, not on every MAF release. No global claim of compatibility or last-verified MAF version.
- Keep plugin.json and VERSION at 0.1.1, provider neutrality and model-free default CI. No application compilation, provider calls, release, merge or publication is implied.

## Acceptance and evidence

The package has exactly its declared five skills and only concept-oriented resources. Its structural validator and default tests work without versioned capability resources or an audit workflow/helper. Local/transitive links remain valid in isolated installation. Reference application preserves useful architecture while deferring exact SDK behavior to inspected packages and official sources. Report unavailable native/runtime checks honestly. Update the existing PR's description to the final scope after deterministic checks and independent review.
