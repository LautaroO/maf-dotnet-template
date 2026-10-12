# AGENTS.md

## Scope and project context

This is the AI-first profile for a repository where Microsoft Agent Framework (MAF) owns the central orchestration architecture. In ordinary applications prefer `profiles/application-with-ai-module/`: preserve adopting-team root rules and scope MAF guidance to the AI subtree. Never overwrite an existing root `AGENTS.md` during adoption.

Populate this section from repository evidence: solution/projects and target SDK; exact MAF packages; build/format/test/run commands; component locations; providers/capabilities; state, persistence and durability; hosts/protocols; security/privacy/approval constraints; and intentional provider coupling. Adopting-team rules remain authoritative for style, layout, tests, analyzers, CI/CD, persistence and hosting.

In this source pack, version is `4.0.0`, the last verified MAF .NET release is `dotnet-1.18.0` on 2026-09-09, and validation is `python3 scripts/validate-template.py`. The pack contains guidance and maintenance artifacts only—no application, runtime MAF Agent Skills, plugin or installer.

Before changing MAF code or guidance, inspect `global.json`, solution/project files, central package management, nearby code/tests, and installed MAF package versions. Installed NuGet APIs outrank current documentation. Use Microsoft Learn and official Microsoft MAF source/samples, separating MAF abstractions from provider/cloud setup.

## Responsibility boundaries

Classify each responsibility and use the least-agentic fit:

- deterministic C# for exact rules, validation, authorization, calculations, persistence decisions, and deterministic routing;
- tool/function for one bounded capability an agent may call;
- `AIAgent`/`ChatClientAgent` for open-ended semantic judgment, synthesis, conversation, planning, or bounded tool choice;
- workflow executor/edge for explicit sequence, branching, fan-out/fan-in, retry, approval, pause/resume, checkpoint, or transition;
- middleware for narrow cross-cutting interception;
- `AgentSession` for conversation state; context provider/retrieval for dynamic knowledge; typed workflow messages first and shared/checkpoint/durable state only for their specific lifetimes;
- provider adapter for SDK construction and capability differences;
- host/protocol adapter for operation and client exposure.

Prefer MAF-native abstractions over custom loops, routers, state machines, registries, conversation stores, middleware chains, or workflow engines when installed packages provide the required semantics. A strong production default is: workflow owns process; agents own bounded semantic steps; tools adapt application capabilities; domain/application code owns business behavior.

Keep provider SDK types out of domain services, workflow messages, reusable tools, validators, persistence models, and default unit tests. Put provider selection and capability detection in composition/configuration. Choose managed versus self-hosted operation separately from OpenAI-compatible, A2A, AG-UI, MCP, or application-native protocols.

## Trust and runtime invariants

Model output, retrieved content, tool/MCP/remote-agent results, media, protocol IDs, continuations, and persisted session data are untrusted. Use structured output when supported, deserialize to dedicated types, validate in C#, and fail closed or repair within a bounded policy before routing, persistence, tool execution, or side effects.

Tools are security boundaries: validate arguments; enforce authorization and tenancy in code; constrain privileges and egress; pass cancellation/timeouts; require occurrence-bound approval for consequential actions; and make retried/resumed effects idempotent.

Use async end-to-end without sync-over-async. Propagate `CancellationToken`. Use correct DI lifetimes and concurrency for shared clients/state. Bound retries, iterations, tool calls, parallelism, payloads, context, time, tokens, retained state, and cost. Avoid nested retry multiplication. Serialize state safely, protect secrets, isolate tenants, and redact sensitive telemetry by default.

Default tests do not require a live model. Test deterministic rules, validators, tools/authorization, workflow routes/state/failures, middleware, sessions/context, provider adapters, hosting, streaming, durability and replay independently; keep real-model quality/safety evaluation opt-in.

## Skill routing

- `$maf-adoption`: inspect and adopt into an existing repository.
- `$maf-architecture`: classify responsibilities and boundaries.
- `$maf-agents`: agents, sessions, multimodal/streaming/background runs, bounded autonomy, declarative agents, runtime Agent Skills, Harness.
- `$maf-tools`: function tools, agent-as-tool, MCP and approvals.
- `$maf-workflows`: orchestrations, typed graphs, state, HITL, checkpoints and durability.
- `$maf-context-memory`: sessions, history, context, RAG and compaction.
- `$maf-middleware`: agent/function/chat-client interception.
- `$maf-provider-integration`: provider isolation and capabilities.
- `$maf-hosting`: operation, protocols, sessions, deployment and streaming.
- `$maf-security`: threat modeling and production hardening.
- `$maf-observability`: telemetry and incident diagnosis.
- `$maf-devui`: local DevUI development surface.
- `$maf-testing`: deterministic tests and model evaluations.
- `$maf-review`: whole-repository or change/diff evidence-first review.

Repository Codex skills are not MAF runtime Agent Skills. Load only skills relevant to the task.

## Review and completion

Review findings precede summaries and include severity, confidence, precise evidence/location, impact, correction, and MAF version certainty. Exclude formatting preferences unless repository rules or CI require them.

For MAF guidance/code changes report the abstraction and boundary choice, provider coupling, files changed, commands/results, untested/version uncertainty, and production risks involving state, retries, side effects, security, hosting, cost, latency or capabilities.
