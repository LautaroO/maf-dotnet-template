# Architectural assistant refactor evaluation

Date: 2026-10-30. Starting commit: 13d462d, with the pre-existing local 1.25–1.26 guidance changes, approved design status and implementation plan. Full starting files, Git status/patch and SHA-256 hashes were exported locally to `/private/tmp/maf-assistant-baseline-20261030`; this temporary export is evaluation evidence, not a plugin dependency. The baseline has 14 skills, 17 playbooks and routing v1; all 18 deterministic tests passed.

Only explicitly supplied-reference batch probes are initially available. These do not establish native installation, autonomous discovery, actual Superpowers execution, implementation correctness or two independent samples per case. Candidate versus baseline probe observations and unexecuted modes are recorded below as execution proceeds. No provider coupling or MAF verification baseline changes are inferred.

## Baseline observations

Two independent fresh agents applied the same 17 raw scenarios in batch, with task-relevant baseline references and no scoring rubric or candidate guidance. Both accepted the adequate design, proposed the exact label edit, identified the cancellation authorization gap, preserved the stated process owner, distinguished proposed from installed packages, allowed no findings and selected single-agent/delegation/workflow/deterministic owners appropriately. No material baseline failure was observed in these supplied-reference responses. The migration is justified by the approved interface/maintenance design, not a claimed behavioral failure or measured quality gain.

Raw transcripts: local `/private/tmp/maf-baseline-probe-a.md` and `maf-baseline-probe-b.md`. The prompts are preserved in the cases JSON; their repository mappings were supplied as evidence, not actual edited projects. This is two fresh batch runs, not two fresh independent sessions per case. Model/runtime inherited the parent session; exact resolved model/version, token cost and client-routing metadata were not exposed. Actual Superpowers execution, autonomous discovery, per-case scoring and application implementation remain untested.
