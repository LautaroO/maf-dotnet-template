# Architectural assistant refactor evaluation

Date: 2026-10-30. Starting commit: 13d462d, with the pre-existing local 1.25–1.26 guidance changes, approved design status and implementation plan. Full starting files, Git status/patch and SHA-256 hashes were exported locally to `/private/tmp/maf-assistant-baseline-20261030`; this temporary export is evaluation evidence, not a plugin dependency. The baseline has 14 skills, 17 playbooks and routing v1; all 18 deterministic tests passed.

Only explicitly supplied-reference batch probes are initially available. These do not establish native installation, autonomous discovery, actual Superpowers execution, implementation correctness or two independent samples per case. Candidate versus baseline probe observations and unexecuted modes are recorded below as execution proceeds. No provider coupling or MAF verification baseline changes are inferred.

## Baseline observations

Two independent fresh agents applied the same 17 raw scenarios in batch, with task-relevant baseline references and no scoring rubric or candidate guidance. Both accepted the adequate design, proposed the exact label edit, identified the cancellation authorization gap, preserved the stated process owner, distinguished proposed from installed packages, allowed no findings and selected single-agent/delegation/workflow/deterministic owners appropriately. No material baseline failure was observed in these supplied-reference responses. The migration is justified by the approved interface/maintenance design, not a claimed behavioral failure or measured quality gain.

Raw transcripts: local `/private/tmp/maf-baseline-probe-a.md` and `maf-baseline-probe-b.md`. The prompts are preserved in the cases JSON; their repository mappings were supplied as evidence, not actual edited projects. This is two fresh batch runs, not two fresh independent sessions per case. Model/runtime inherited the parent session; exact resolved model/version, token cost and client-routing metadata were not exposed. Actual Superpowers execution, autonomous discovery, per-case scoring and application implementation remain untested.

## Candidate observations

Two fresh candidate-reference batch agents used the same 17 raw scenario inputs without rubric or baseline transcripts. Both retained the adequate-design/no-findings outcome, proposed the exact label edit, identified the cancellation permission gap, respected the specified process owner, accepted delegated design decisions, distinguished proposed from installed packages and chose the four responsibility variants appropriately. Responses describe intended next actions, not executed application changes. No material response regression was observed; neither a quality gain nor an autonomous routing pass rate is claimed. One generic-.NET response consulted boundary references to delimit scope, while the other needed no MAF reference: explicit supplied-reference runs cannot measure discovery precision.

A separate candidate-reference application exercised adoption and testing plus eight release-sensitive prompts (unanswered approval, standing rules, Cosmos/deletion, middleware coverage, declarative state/approval, DevUI route security, AG-UI identity and telemetry continuation). It preserved root/handbook ownership, proposed narrow instruction merging without skill copies, separated deterministic tests from semantic evaluation, and recovered the scoped technical contracts from their new topic locations. The declarative response included sensitive control inputs, closed-list IDs, state reset/restore and registered approval/AutoSend. These are observed reference applications, not installed API or provider tests.

The active source interface has five skills and fourteen problem patterns; all thirty-three historical v1 scenarios and their behavioral assertions remain represented in v2 alongside the architecture scenarios (old-package is shared). Historical v4 remains readable and its seventeen playbooks have an explicit coverage mapping.

## Validation and remaining modes

- Repository validator: five skills, fourteen patterns, routing v2; isolated installed-copy resource tests pass.
- Python compilation, unittest suite (57 tests at this stage), Bash syntax and git diff whitespace checks pass. Audit/notification tests use controlled sources and fake gh; no real GitHub writes occurred.
- The optional skill-creator quick_validate helper could not run because its external PyYAML dependency is absent. The repository's standard-library frontmatter, naming, contract and resource checks did run; no dependency was installed.
- Lychee is unavailable locally: external HTTPS link reachability was not rerun; local Markdown/resource links are validated and existing CI retains the external-link check.
- Native candidate installation/discovery, two fresh per-case scored sessions, real Superpowers process execution and application implementation/compilation/provider behavior remain unexecuted. The batch/reference limits above are intentional disclosures, not passing client checks. No release/publication or MAF verification advancement is asserted.

Static instruction-size observation: public skill bodies total 4904 whitespace-delimited words in the baseline and 1476 in the candidate. This is a source-size comparison, not measured token cost, latency or execution quality.

## Local artifact hashes

- `maf-assistant-probe-inputs.json`: `85ac7a86fcbca8547a2ea1a3cd4c32b834dc3434acc3f2a4abcfc05d976afe87`
- `maf-baseline-probe-a.md`: `69c566ad361abaa7daf132fb18fe2e26518d53121d30c70821bd72fb744ee091`
- `maf-baseline-probe-b.md`: `908919c300736c4b0c7ea4d91c4e56fae32813044f26dc286aa5196b9d2ecd1d`
- `maf-candidate-probe-a.md`: `cd5b7b3c1211530be305853134ea10a09138cdd66aeed55bf4a3fe79752cc497`
- `maf-candidate-probe-b.md`: `89e88b424de76769a50bff90efda886aeb4dc6207415101241ad979abf68e616`
- `maf-candidate-technical-probe.md`: `d6101ad82213bb01014085e6c73517a9aa9434645d056634d5a7d5a23b2b99ba`
