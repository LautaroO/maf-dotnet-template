# Skill-routing evaluation dataset

`v1.jsonl` is the versioned routing contract. Each line contains a realistic prompt, the minimum expected skills, optional prohibited routes, and occasional behavioral assertions.

Evaluate selection in a fresh Codex session. Extra skills are acceptable only when the prompt genuinely needs them; generic .NET negative cases must select no MAF skill. Record failures by fixture ID and correct skill descriptions/routing rather than teaching to exact wording.

## Context and refinement scenarios

The three context/refinement fixtures require repository inputs as well as their prompts. Use temporary product fixtures with a MAF project under `src/Shop.AI`, the installed plugin available to the session, and existing root instructions. Do not copy plugin skills into the fixtures. No live MAF model call or package restore is required.

| Fixture | Repository setup | Behavior to inspect |
|---|---|---|
| `adopt-existing-documentation` | Root rules point to `handbook/ai-context.md` and `handbook/orders.md`, with an existing refinement/review process. The order note defines lookup by number, caller-owned orders, output fields, cancellation and a deadline. | Canonical links and existing process reused; no competing folders or repeated questions about settled requirements. |
| `adopt-missing-documentation` | Product instructions and a MAF project exist, but no product documentation convention or order requirements. Capability/pattern assets are available in the installed plugin. | A destination is proposed and agreement requested; authorized instruction merging continues; no new context/feature document is created; material query/access decisions remain open. |
| `small-maf-change` | An existing agent label and root rules allowing small exact edits in chat. | Only the requested label changes; no new specification, adoption rerun or requirements questionnaire. |

Inspect changed files as well as the final response. To test the modified skill bodies independently of discovery, explicitly invoke the relevant skill in a separate behavioral probe and record that invocation; it does not prove autonomous routing. For documentation reuse, compare original document contents and verify the persisted context links. For a missing convention, inspect both the proposal and the absence of new product documents. For the small change, verify exact file contents and absence of extra artifacts.

See the [context/refinement behavior check record](context-refinement-smoke.md) for the baseline and representative modified-guidance results.
