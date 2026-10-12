# Context and refinement behavior checks

Date: 2026-10-12. Base: `71f474f`. Codex CLI: 0.162.1.
Model: CLI default `gpt-6.1-sol`, user configuration disabled, ephemeral sessions.

These checks exercise the skill bodies with explicit invocations, not autonomous skill discovery. Temporary fixtures use the setups described in [the evaluation guide](README.md). Only fixtures outside this repository were editable; no runtime implementation or package installation was requested for adoption/design probes.

## Baseline

The original adoption/architecture skills were asked to adopt a product without a documentation convention and refine an orders-query agent. They preserved the product root but created `src/Shop.AI/project-context.md` without agreeing a documentation destination. Missing order requirements were identified, but the new documentation placement was chosen silently.

This observed placement failure is the reason for the proposal/agreement rule. It does not establish that every baseline run behaves identically.

## Modified guidance

| Scenario | Observed result |
|---|---|
| `adopt-missing-documentation` | Proposed context/feature destinations and requested agreement. Recorded pending placement and known/unknown facts in scoped `AGENTS.md`; completed independent instruction merging. Created no new context/feature documents. Identified unresolved lookup/listing, caller access, fields and query contracts before runtime implementation. |
| `adopt-existing-documentation` | Preserved root instructions and the original handbook requirements. Linked canonical `handbook/ai-context.md` and `handbook/orders.md` from instruction files; updated those existing documents with evidence and a proposed design. Followed the product's existing review process. Asked only about unresolved provider/host, actual contracts and failure/ambiguous-input behavior. No competing document hierarchy was created. |
| `small-maf-change` | Changed only the specified constant from `orders-bot` to `orders-assistant`. No extra documentation, specification or requirements questions; used the repository's small-change-in-chat convention. |

The existing-documentation probe was repeated after its first attempt stopped with a model-capacity error. The completed retry used the same model and task; the interrupted attempt is not counted as a pass.

## Inspection and limits

The coordinator manually reviewed proposals, questions, final responses and modified instruction/documents. File checks verified original root prefixes, preserved handbook requirement text, canonical context references, absence of new context/feature documents in the missing-convention fixture, and exact contents of the small-change source file. A separate read-only reviewer found no blocking contradictions or invasive requirements in the guidance changes.

Structural validation and the existing regression suite remain separate from these live, opt-in behavioral probes. No new MAF API or provider capability claim was introduced; declared fixture package versions were distinguished from restored APIs. These representative runs do not prove every model, repository convention, conflict-resolution path, stale-context update or routing fixture. This is not a release smoke-test record for a new pack version.
