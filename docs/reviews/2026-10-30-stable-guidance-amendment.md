# Stable MAF guidance amendment evidence

This record covers the user-requested simplification after the initial architectural-assistant refactor. It supersedes the earlier retention of a versioned capability matrix, release deltas and scheduled auditing. No MAF SDK compatibility baseline is now maintained or claimed by the plugin. Plugin version remains 0.1.1.

## Scope and decisions

The five public skill names and fourteen pattern IDs remain. The thirteen implementation references now retain responsibilities, tradeoffs, conceptual MAF search terms and behavior to verify. Exact signatures, release defaults/fixes, package maturity tables and storage/adapter migrations are investigated on demand in installed package evidence and the official Microsoft MAF repository.

Deleted the compatibility matrix/dated verification/coverage resources, historical v4 and v1 installed resources, audit collector/issue synchronizer/shared coverage helper, their release-specific tests and scheduled workflow. Git retains those artifacts; dated source review/release records are labeled historical and removed-resource links point to the preceding public commit. No duplicate archive was added to the package. The former minor reference to an installed hosting skill was updated as part of removing capability-matrix adoption checks.

Active routing retains architectural/security/state/process behavior and adds source lookup, upstream/installed mismatch, unavailable-evidence and provider-sample separation scenarios. It no longer tests recall of named releases. Default test count decreases because retired audit/coverage behavior is intentionally no longer production code.

## Verification before review

A new source-export subprocess regression first failed because the validator imported the removed coverage helper. It now passes without matrix resources, coverage helpers or a scheduled audit workflow. Existing standalone installation/transitive reference, contract, catalog, routing, scenario safety and hygiene tests remain. Repository validation reports five skills, fourteen patterns and routing v2; 32 unittest tests, Python compilation, Bash syntax and whitespace checks passed before independent review.

The official repository entry point was opened to verify the reference destination; no .NET SDK API surface or latest compatibility matrix was audited. Provider coupling remains unchanged. No application restore/build/runtime, provider calls, native installation/autonomous routing, actual Superpowers execution, plugin release or merge is claimed.

## Reference observations

Baseline source: commit 89aeb87 snapshot at `/private/tmp/maf-stable-guidance-baseline`. A read-only reference application of an unknown-package session/approval task correctly refused verified signatures but still supplied remembered 1.24–1.26 contract details. That is the behavior the amendment removes. Its read-only orders architecture response remained useful and did not require another approval. Candidate response evidence is recorded below after its probe.

Optional PyYAML/Lychee helpers remain unavailable locally; standard-library package checks cover local links and CI retains external-link checking. Historical claim counts in earlier records describe their own revisions, not this candidate.
