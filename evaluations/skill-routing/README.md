# Skill-routing evaluation dataset

`v1.jsonl` is the versioned routing contract. Each line contains a realistic prompt, the minimum expected skills, optional prohibited routes, and occasional behavioral assertions.

Evaluate selection in a fresh Codex session. Extra skills are acceptable only when the prompt genuinely needs them; generic .NET negative cases must select no MAF skill. Record failures by fixture ID and correct skill descriptions/routing rather than teaching to exact wording.
