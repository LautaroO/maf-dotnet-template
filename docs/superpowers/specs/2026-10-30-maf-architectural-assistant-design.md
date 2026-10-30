# MAF architectural assistant design

Status: approved by the user on 2026-10-30. Date: 2026-10-30.

## Intent

Evolve the skills-only `maf-dotnet` plugin into an architectural assistant that helps develop MAF .NET agents and systems from an initial idea through implementation and verification. Support both new solutions and existing applications, including AI-first and embedded-AI architectures. Choose architecture from requirements and context rather than prescribing a universal project layout or assuming every problem needs agents.

The user selected reorganizing the plugin around the assistant's work rather than retaining subsystem skills as the main interface or creating a framework-independent product. The assistant should examine existing designs and requested changes for material gaps, accept adequate designs, and avoid inventing objections or unnecessary process.

## Goals and success criteria

- Guide discovery, architecture, implementation and review with MAF-specific judgment.
- Reuse settled requirements, repository conventions and existing components. Ask about consequential gaps rather than repeat a questionnaire.
- Support multiple architectural shapes and explain responsibility, state and trust boundaries.
- Work independently and alongside Superpowers or another project development process without duplicate brainstorming, documents or approval gates.
- Keep everyday guidance stable across MAF releases while checking actual APIs when implementing.
- Retain useful technical knowledge with explicit evidence and uncertainty, loaded only when relevant.
- Measure design and implementation assistance with observable behavior, including cases in which the correct outcome is to proceed without questions or findings.

## Non-goals and anti-goals

No generic multi-framework architecture product, MAF documentation mirror, universal solution scaffold, MCP server, runtime Agent Skill bundle, provider dependency, marketplace or publication in this change. The plugin can guide authorized scaffolding in a target application; this repository remains a guidance package with no .NET application.

Do not force multi-agent designs, create custom abstractions over sufficient MAF primitives, prescribe cloud hosting, upgrade NuGet packages silently, add approval gates to trivial work or turn preferences into defects. Do not treat silence, a question count, or elapsed time as approval. User instructions remain authoritative.

## Approaches considered

1. Evolve the existing fourteen subsystem skills. Lowest migration effort, but preserves fragmented entry points and repeated design/version guidance.
2. Reorganize around analyzing/designing, implementing and reviewing systems, with focused patterns and technical references. Selected by the user; maintains MAF specialization and gives the assistant a coherent workflow.
3. Separate framework-independent AI architecture from a MAF adapter product. Useful for a broader audience, but expands scope and maintenance beyond the selected goal.

The user approved this full design after selecting the reorganization approach; the inventory and maintenance details below are included in that approval.

## Behavioral contract

### Start with the task and available evidence

Read applicable project instructions and only the context relevant to the request. Identify whether the work concerns a new solution, an existing architecture, a new capability or a small change. Installation does not imply adoption; ordinary work does not require adoption or modification of project instructions.

For existing applications, inspect affected boundaries, contracts and installed packages. For a new solution, establish intended use, integration boundaries and relevant operational constraints without inventing existing projects or installed versions. Suggest an appropriate architectural shape and stack selection; inspect selected package APIs once available. Do not require a full production architecture for an experiment.

### Analyze before changing behavior

Perform a proportional gap assessment before designing or implementing behavior. This is a reasoning step, not a mandatory standalone skill invocation, report or approval ceremony for every edit.

Classify what matters as:

- evidenced problem: explain the concrete failure or unwanted consequence;
- unresolved decision: ask when the answer materially affects behavior, acceptance, access, architecture or significant operating constraints;
- optional improvement: explain the tradeoff without blocking the requested work;
- sufficiently specified: state briefly that no material gaps were found when useful, and continue authorized work.

Separate facts, user requirements, assumptions and recommendations. Avoid exhaustive speculative risks. Prioritize the few questions with the greatest effect; ask one focused question at a time unless the user's process calls for a concise batch. Reuse answers and continue independent work while a necessary answer is pending. Fully specified small changes proceed without an architectural document or generic questionnaire.

### Agent-design topics, selected by relevance

The assistant draws from a shared topic guide rather than requiring every topic for every request:

- purpose, intended users, success and failure criteria;
- semantic decisions versus exact rules and side effects;
- bounded tools and application capabilities, principals, permissions and approvals;
- conversation, retrieval, context and persistence lifetimes;
- single-agent, delegation and explicit workflow control;
- validated structured outputs and integration contracts;
- cancellation, retry ownership, idempotency, recovery and resource budgets;
- provider capabilities, transport and hosting ownership;
- deterministic tests and semantic evaluations.

The result may be a bounded agent, multiple agents, a workflow, a hybrid or deterministic application code. Explicitly describe tradeoffs when multiple viable designs exist; avoid listing alternatives for an exact, settled change.

### Design output and handoff

For substantial work, capture the agreed purpose, responsibilities, selected architecture, state/trust boundaries, acceptance criteria and material open questions at the project's established location. For small work, a concise conversation-level assessment suffices. Reuse existing ADRs/specifications rather than produce parallel documents. Preserve the current adoption rule of agreeing on a documentation convention when none exists.

Resolve material behavior decisions before dependent implementation. Honor the active process and explicit user authorization; add no plugin-wide requirement to approve every design. When the user explicitly delegates reasonable design choices, make and label them rather than reopening them as questions. Surface unresolved high-impact decisions that cannot responsibly be inferred.

## Coexistence with Superpowers and other processes

Keep one owner of the development process. Inspect applicable instructions and available/invoked skills rather than assume Superpowers is installed or mandate a namespace.

- With Superpowers: its brainstorming/planning/execution/review process owns sequencing and approvals. Supply MAF-specific questions, decision criteria and technical references within that process. A design question already answered in its conversation or artifact is settled unless new evidence contradicts it. Do not start a second brainstorming loop or create a second design document.
- With another project process: follow that process using the same MAF-specific contribution.
- Without a project process: provide lightweight discovery, alternatives when warranted, a proportional design and implementation when sufficiently specified and authorized. Do not require Superpowers as a dependency.

The MAF skills must not unconditionally invoke each other. A small assessment can occur inside implementation or review without activating a full architecture workflow. Non-MAF work must not activate this plugin merely because the repository uses it elsewhere.

## Proposed skill interface

Use five public skills, each with a brief goal-based description and a concise task router:

| Skill | Responsibility |
|---|---|
| `maf-adoption` | Explicitly inspect and merge project guidance while preserving local ownership; support the appropriate existing or new-solution context. |
| `maf-architecture` | Analyze ideas/designs/behavior changes, uncover material gaps, guide agent design and choose architectural responsibilities. |
| `maf-implementation` | Implement or change MAF behavior, consulting only relevant abstraction/API references; perform a proportional assessment without restarting discovery. |
| `maf-testing` | Design and implement deterministic verification and opt-in semantic evaluations with scope appropriate to the task. |
| `maf-review` | Review a design, repository or diff for evidence-backed issues and acceptance gaps; explicitly allow no findings. |

Retain the existing architecture, adoption, testing and review names, revise their scopes, and add implementation. Move knowledge from agents, tools, workflows, context, middleware, providers, hosting, security, observability and DevUI into conditional references owned by implementation or shared resources as appropriate. Security and other cross-cutting criteria remain part of architecture/review, with one authoritative detailed reference instead of repeated release notes.

Preserve all useful existing domain guidance. Do not mechanically concatenate former skill bodies into a giant implementation document. Provide direct topic links and load only relevant material. Architectural assessment belongs to the task; architecture skill selection is reserved for substantive architectural work.

This intentionally changes public routing. Document replacement routes for the ten removed entry points and update bundled profiles, links and fixtures atomically. Do not retain ten discoverable alias skills, duplicate installed skills or edit already-adopted applications automatically. Explain how users update explicit invocations and stored project routing. Plugin version remains unchanged during development; final release numbering is a separate decision, with no claim of backward compatibility for removed names.

## Knowledge organization

### Stable workflow guidance

Skills teach how to decide and verify. Keep framework concepts where they clarify decisions, but move exact signatures, package maturity and release discrepancies out of ordinary workflow instructions.

### Problem-oriented patterns

Maintain patterns for representative problems such as semantic extraction, authorized application queries, consequential actions, grounded assistants, conversational state, controlled delegation and recoverable processes. Each pattern explains when it fits, responsibility/state/trust boundaries, alternatives, failure behavior and acceptance examples. Include code only when it clarifies the pattern; diagrams, contracts and decision examples are valid alternatives.

Use the existing catalog as migration input. Preserve useful coverage, reorganizing it without requiring exactly seventeen patterns or a C# fragment in every entry. Keep historical documents intelligible; update active entry points rather than rewriting old review records as if they described the new interface.

### Conditional MAF technical references

Retain a concise mapping from design concepts to MAF primitives, important capability restrictions and supported-use checks. Preserve dated/tagged evidence and scoped 1.25–1.26 changes, distinguishing them from general architectural principles. Place detailed release chronology in maintenance records; surface relevant limitations in topic references without forcing every task to read the chronology.

For implementation, inspect the target's actual SDK, projects and NuGet APIs, then reconcile matching official evidence. For new solutions, distinguish proposed packages from installed ones. Never substitute current Learn or `main` for an installed API contract or silently upgrade packages. When local evidence or network access is unavailable, state the specific uncertainty and avoid inventing a signature.

Version-independent skills do not promise version-independent APIs. Existing evidence remains a full 1.24 baseline plus scoped 1.25–1.26 review; this reorganization does not reverify or advance it.

## Maintenance changes

Retain the official-source review discipline and Codex's responsibility to follow through on requested knowledge updates. Change the organizing question from whether every new release has been copied into the plugin to whether new evidence changes a decision, supported pattern, important restriction or implementation contract.

Use machine-readable coverage metadata as the audit's source of truth, separating the last release assessed for deltas from the last full verification and per-area evidence. A scoped review can advance the assessed-release marker without advancing unrelated capability verification. The report must display both coverage and remaining uncertainty. Migrate existing metadata from its evidence without inventing additional verification.

The audit remains a read-only evidence collector. Separate network/link failures, changed documentation signals and new release evidence. Diagnose failed requests rather than interpret them as capability changes. Fingerprint actionable findings so scheduled issues are opened/refreshed for new or changed findings, rather than commenting on identical results every week. Do not create a maintenance issue for a clean unchanged report. Retain dated review records and Unreleased entries for actual guidance changes.

Update validators to check metadata types, legitimate dates/releases, resource containment, declared skill routes and fixture consistency rather than hardcoding fourteen skills, seventeen patterns or the year 2026. Keep deliberate required behavior cases and strict checks against accidental skill duplication. The metadata file schema and helper implementation are left to the builder; use standard-library Python and no new service.

Do not run a whole new MAF source audit merely to rename or relocate existing guidance. Verify official Microsoft evidence if an API claim is changed; record that scope separately.

## Evaluation and validation

Migrate every existing routing/behavior case to the new interface while retaining its behavioral intent, including version-specific regression cases. Adjust skill-selection assertions to the new ownership; do not delete difficult cases to obtain a pass.

Add scenarios covering:

1. Vague idea for a new solution: identify the highest-impact open design question before implementation, with no invented project facts.
2. Existing application: reuse use cases and instructions, preserve boundaries and adapt architecture.
3. Adequate existing design: find no material gap and proceed when authorized, without forced alternatives or objections.
4. Small exact change: perform the change without adoption, questionnaire or new specification.
5. Material gap in an otherwise complete design: explain impact, ask only the unresolved question and pause dependent work.
6. Superpowers plus MAF: one conversation, one canonical design and one process owner; no repeated requirements or approvals.
7. Standalone MAF: useful design-to-implementation assistance without requiring Superpowers.
8. Different architectures: choose single-agent, explicit workflow, delegation or deterministic code from actual control requirements.
9. Old installed packages and a new solution with no packages yet: distinguish evidence, proposals and unavailable APIs without a silent upgrade.
10. Review with no defects: accept the design and distinguish optional preferences from blocking findings.
11. Generic .NET work: no unrelated MAF routing.

Specify a reproducible opt-in evaluation protocol with fixture inputs, expected artifacts/actions, prohibited behavior and recorded results. Evaluate autonomous selection separately from explicitly invoking a skill. For representative scenarios compare the pre-reorganization behavior with the candidate using the same inputs and disclose the model/client/configuration. Evaluate both defect detection and unnecessary questions/findings; avoid teaching an assistant that more findings is always better. Existing before/after reference probes are evidence inputs, not a complete baseline score.

Default CI stays deterministic and live-model-free: validator, Python compilation, unittest suite, shell syntax, local/CI Markdown links and whitespace checks. Add meaningful tests for audit state/deduplication and changed validator contracts. Behavioral evaluation runs separately and must not be claimed from fixture schema validation. Native-client installation and fresh-session checks remain release gates.

## Delivery boundaries and builder decisions

Implementation includes skills/references/patterns, profiles and active documentation, routing migration, maintenance metadata/audit/workflow updates, validators/tests and behavioral evaluation instructions/results within available tooling. Preserve the pre-existing local 1.25–1.26 changes; do not reset, overwrite or claim them as new work. Keep `plugin.json` and `VERSION` at 0.1.1 until a release is requested. No publication, marketplace changes, target application edits or provider calls are included.

The builder chooses reference paths, short description wording, metadata schema, audit report serialization/fingerprinting and implementation order. Avoid an unrelated documentation rewrite. Report files/commands/results, preservation of provider neutrality, version certainty and untested client behavior.

This is a repository-wide guidance refactor requiring a full implementation plan after approval. It supersedes the fourteen-skill retention requirement of the 2026-10-12 distribution design only when this design is approved; portability, canonical authoring and separation of installation/adoption remain in force.
