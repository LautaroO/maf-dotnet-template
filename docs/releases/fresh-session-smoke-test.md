# Fresh-session release smoke test

This is a mandatory manual release gate for both profiles; structural CI cannot prove Codex routing behavior.

For each candidate release:

1. Install the candidate root plugin from a separate test marketplace and confirm its five skills/resources are available. Start a fresh Codex session against a representative existing application and adopt the embedded-AI profile. Confirm its root `AGENTS.md` is preserved, project context is evidence-backed, and a generic .NET fixture selects no MAF skill.
2. Start another fresh session against an AI-first repository. Confirm `$maf-adoption` selects that profile only when central MAF ownership is evidenced.
3. Run representative positive and negative cases from `resources/evaluations/skill-routing/v2.jsonl`.
4. Confirm SDK-specific requests inspect target packages and consult matching official .NET evidence; unavailable evidence produces scoped uncertainty rather than guessed signatures or support claims.
5. Record the installed plugin version, Codex version/model, date, fixture IDs, results and reviewer in release evidence.

Do not mark a release complete without both profile results. This repository does not claim that a manual smoke test was performed merely because the structural validator passes.
