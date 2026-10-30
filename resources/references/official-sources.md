# Official MAF source investigation

The primary external reference is the [Microsoft Agent Framework repository](https://github.com/microsoft/agent-framework). Use its .NET source, samples, tests and matching tags to answer implementation questions. The plugin keeps architectural concepts and decision criteria; it does not certify compatibility with a particular MAF release or copy a history of fixes.

## Match evidence to the task

1. Identify the target project's SDK/TFM and actual resolved MAF/provider packages, including central package files, lockfiles/assets and local XML/public API evidence where available. In a new solution distinguish proposed choices from installed facts.
2. Locate only the relevant .NET types/behavior in the official repository. Prefer the matching tag/commit for pinned packages; current `main`, README examples and Python APIs do not establish the installed .NET surface.
3. Read relevant source/sample/test contracts. Use [Microsoft Learn](https://learn.microsoft.com/agent-framework/) and published package metadata as supporting evidence; distinguish documented intent, tagged implementation, package publication and actual local availability.
4. Adapt to the installed API, verify with appropriate project checks, and record relevant evidence/uncertainty in the project's existing design or implementation record. Do not upgrade dependencies silently or copy provider/cloud setup into reusable behavior.

Repository symbols such as agent/session abstractions, typed workflow steps, function tools and model clients are useful search anchors, not a guarantee of a specific constructor, overload, registration pattern or runtime default. Verify the seam this change depends on instead of auditing every release.

## Conflicts or unavailable evidence

If docs, source and package surfaces disagree, identify the exact sources and choose an implementation supported by the target stack; keep unresolved claims qualified. When package evidence or upstream access is missing, state the specific unknown, continue independent conceptual work, and defer dependent SDK code. Failed network access is not evidence that a capability is unsupported. Do not invent signatures or imply a build was run.

## Separate framework and environment

For each sample distinguish the MAF abstraction, provider authentication/options, cloud/hosting setup and example shortcuts. Keep intentional provider capabilities at adapter boundaries. This plugin's skills are developer guidance; application runtime Agent Skills have different consumers and trust/execution boundaries.
