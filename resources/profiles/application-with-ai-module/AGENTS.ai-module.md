# AGENTS.md — AI module

## Scope and project context

These instructions apply only to this MAF/AI subtree. Read and preserve the repository-root instructions first; adopting-team rules for C# style, solution layout, tests, analyzers, CI/CD, persistence and hosting remain authoritative. This module orchestrates/adapts application capabilities and does not own domain rules, ordinary use cases, authorization policy, or core persistence.

Populate from repository evidence: AI path/target framework; exact MAF packages; commands; agent/workflow/tool/context/provider/host locations; permitted application dependencies; provider capabilities; session/retrieval/checkpoint/durability choices; hosting/protocols; security/privacy/approval constraints; and intentional provider coupling. Installed NuGet APIs outrank current docs.

## MAF boundaries

Use deterministic C# for exact rules and routing; bounded tools over application services for capabilities; `AIAgent`/`ChatClientAgent` for open-ended semantics; workflows for guaranteed process; middleware for narrow cross-cutting concerns; `AgentSession` for conversation state; context providers/tools for retrieval; checkpoints/durable state for runtime resumption; and provider/host adapters at composition boundaries.

Prefer MAF-native abstractions over custom loops, registries, stores, middleware chains or graph engines where the installed version fits. Keep provider SDK types out of application/domain contracts, workflow messages and reusable tools. Choose hosting model separately from protocol.

Model output, retrieval, tools/MCP/remote agents, media and protocol/session/continuation IDs are untrusted. Validate structured outputs before code paths; enforce authorization/tenancy in tools and state lookup; constrain egress; require occurrence-bound approval for consequences; and make effects idempotent.

Use async without sync-over-async, propagate cancellation, choose correct service lifetimes, serialize safely, protect secrets, redact telemetry, and bound retries, loops, tools, concurrency, payloads, time, tokens and cost. Default tests remain live-model-free; evaluation is opt-in.

## Skill routing

Use the relevant installed developer skill: `$maf-adoption`, `$maf-architecture`, `$maf-agents`, `$maf-tools`, `$maf-workflows`, `$maf-context-memory`, `$maf-middleware`, `$maf-provider-integration`, `$maf-hosting`, `$maf-security`, `$maf-observability`, `$maf-devui`, `$maf-testing`, or `$maf-review`. These names identify capabilities; select the plugin namespace shown by the client. Keep the knowledge layer in the installed plugin. Codex developer skills are not application runtime Agent Skills.

## Review and completion

Findings must lead and include severity, confidence, precise evidence/location, impact, correction and MAF version certainty. Ignore formatting preferences unless repository rules/CI require them.

Report abstraction/boundary choice, provider coupling, files and commands, tests/results, uncertainty, and production risks involving state, retries, side effects, security, hosting, cost, latency or capabilities.
