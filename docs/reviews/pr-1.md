# PR #1 review and verification

Historical record of an earlier revision. Release-specific knowledge/auditing was retired by the [stable-guidance amendment](../superpowers/specs/2026-10-30-stable-maf-guidance-design.md); this document does not define the current maintenance policy or MAF compatibility.

Review date: 2026-10-12. Mode: change/diff. Base: `451db4a`.
Original candidate: `d053b74`. Scope: guidance-only pack 4.0.0, not application/runtime code.

## Findings and corrections

All findings have high confidence and are framework-version independent.

| Priority | Evidence | Impact | Correction |
|---|---|---|---|
| P1 correctness | `.github/workflows/validate.yml`, Lychee arguments; reproduced exit 2 | CI never reaches link validation because `--exclude-mail` is unsupported | Remove invalid flag, pin Lychee 0.24.2 and explicitly include `.agents/**/*.md` |
| P2 correctness | README adoption step 1, adoption documents, hosting skill required reference | Documented adopters omit the capability matrix that hosting requires | Copy/merge capability and pattern docs in every adoption entrypoint; use an exact validated matrix link |
| P2 correctness | `validate_hygiene`; running documented `compileall` then validation fails | Ignored local caches falsely invalidate an otherwise clean pack | Inspect tracked plus nonignored untracked files; preserve rejection of tracked ignored artifacts; inspect all files in Git-free exports |
| P2 reliability | `validate_routing`; JSON fixture `[]` raises `AttributeError` | Invalid fixture aborts validation instead of producing an actionable report | Require JSON objects and string skill names before accessing their fields |

The independent reviewer found no further correctness blockers after these fixes.

## Architecture and boundaries

The pack owns development guidance, profiles, evaluation fixtures and maintenance checks. It has no installed MAF runtime packages or .NET application. Its responsibility model remains deterministic application rules, bounded tools, semantic agents, explicit workflows, lifetime-specific state, and replaceable provider/hosting adapters. No provider SDK dependency or runtime side effect was added by these corrections.

Official sources support the principal capability restrictions: background responses are provider-limited, .NET hosting package maturity differs from service maturity, and the documented .NET alternatives to Hooks/FIDES are middleware and deterministic application controls. Current documentation does not independently establish every historical September 9 verification claim. Illustrative C# fragments are not compilation-tested samples.

## Verification

- `python3 -B -m unittest discover -s tests -v`: four regression tests pass, including ignored local caches, tracked ignored caches, nonignored untracked artifacts and non-object JSON fixtures. Cache and non-object tests failed against the original implementation before correction.
- `python3 -m compileall -q scripts` followed by `python3 scripts/validate-template.py`: passes with generated local caches present; 14 skills, 17 playbooks, routing v1.
- Shell syntax checks and `git diff --check`: pass.
- Lychee 0.24.2 with the corrected CI arguments: 74 links checked, zero errors, including hidden guidance and this report. Redirects remain allowed.
- Official-source audit with system CA verification enabled: eight sources accessible; latest published .NET release is `dotnet-1.24.0`; Harness source redirects to `concepts/harness`. No issue was published by the local audit.

## Fresh-session smoke evidence

Pack candidate: 4.0.0 with PR corrections. Codex CLI: 0.162.1. Model: CLI default `gpt-6.1-sol`; user configuration disabled. Date: 2026-10-12. Reviewer: coordinating Codex agent, with a separate read-only PR reviewer.

Three independent ephemeral CLI sessions used temporary fixtures outside this repository. The two adoption sessions permitted edits only to fixtures; the generic routing session was read-only. No package restore, live MAF model call, deployment or external message occurred.

| Fixture IDs / scenario | Observed result |
|---|---|
| `adopt-existing-app` | Application-with-AI-module selected; original root text preserved verbatim; nested AI instructions created; declared SDK/package facts separated from unknown runtime/provider/storage/commands |
| `adopt-ai-first` | AI-first selected for the orchestration-only fixture; original root text preserved; evidence-based context merged |
| `hosting-choice` | Hosting skill selected (AI-first also selected architecture); required matrix successfully opened in both fixtures; hosting and protocols treated separately |
| `middleware-dotnet` | Security/tools/middleware selected; dated .NET Hooks/FIDES limitation stated; deterministic authorization and supported middleware offered |
| `generic-dotnet-nullability`, `generic-ef-migration` | Separate fresh session selected no MAF skill for either request, without being told the expected selection |

Both profile outcomes and copied-resource paths were manually inspected. The adoption sessions also included a constrained generic routing request; the separate unconstrained negative session provides the negative-case evidence. This is representative smoke coverage, not execution of the entire 20-case dataset or a statistical model-quality evaluation. It does not publish a GitHub release.

## Remaining maintenance work

The matrix remains explicitly dated to MAF .NET 1.18.0. Updating it to 1.24.0 requires a separate release/API review, not a timestamp-only edit. Future work should expand independent routing evaluations and verify adoption against real product repositories. Production auth, persistence, durable replay, latency and cost remain adopter responsibilities because this pack supplies no running application.
