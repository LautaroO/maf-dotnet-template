# Project context and requirement refinement

## Reuse the adopting repository's process

Inspect applicable instructions and existing architecture notes, ADRs, feature specifications, templates and development skills. Follow their scope, naming, review and approval rules. MAF guidance supplies framework decisions inside that process; it does not introduce a second brainstorming or planning workflow. Ordinary non-AI tasks continue to follow product conventions.

Distinguish bundled plugin documentation from product documentation: the conceptual references and pattern catalog describe MAF, not the application's requirements or documentation policy.

## Keep a compact context index

In the closest applicable `AGENTS.md`, record where authoritative project context and feature decisions live, their scope, and the existing refinement process. Link to canonical documents rather than copying their contents. Keep short evidence-backed technical facts there when no separate context document exists.

If the repository has no suitable documentation convention, propose a location and naming approach with a short rationale during adoption. Wait for the user's agreement before creating new project-context or feature documents. Continue independent inspection and authorized instruction merging while that choice is pending; mark the destination as undecided. Once agreed, record the convention and reuse it on subsequent tasks. Proposing a new hierarchy is not part of every feature request.

## Refine only unresolved decisions

Before a MAF design or implementation task:

1. Read the context index and the relevant existing feature or architecture documents.
2. Check technical facts that can affect this change against current code, configuration and installed packages. Reinspect only relevant gaps or stale facts; saved context is a starting point, not an API lockfile.
3. Separate documented requirements, user-specified requirements, assumptions and open decisions. Resolve conflicts according to repository instruction precedence; surface a material conflict that evidence cannot resolve.
4. Ask focused questions only when missing decisions change behavior, acceptance criteria, access/privacy, integration contracts or material operational constraints. For example, clarify whether order queries are by number or a list, and whose orders the caller may see, when those choices are not already defined. Reuse established nonfunctional requirements instead of issuing a standard questionnaire.
5. Resolve those decisions before implementing the affected behavior. Continue work independent of the answer. Follow the existing design/review process and approvals; do not add a parallel approval gate.

For a small, fully specified change, use the repository's lightweight process and proceed without a new specification or redundant questions. For a substantial feature, update its existing specification, or create one using the agreed convention when needed. Include purpose, scope, relevant functional/nonfunctional requirements, decisions, open questions and acceptance criteria at the level the task needs. Record only settled decisions as requirements.

## Keep documentation useful

Update relevant context or feature documents when the task changes their facts or decisions. Preserve unrelated content and local ownership. Avoid duplicate reports, full-tree inspection dumps, secrets and raw user/customer data. If a destination is still undecided, keep the proposed design in the conversation and the pending choice in the context index rather than silently creating a folder.

For proportional agent-specific gap analysis use [agent design](agent-design.md); for standalone versus existing process ownership use [process integration](process-integration.md). This reference owns context/document placement, not a second brainstorming workflow.
