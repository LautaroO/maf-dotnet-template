# AGENTS.md

## Purpose

This root file is the **AI-first adoption profile**: use it when Microsoft Agent Framework (MAF) is a central architecture concern of the repository.

If MAF is only one project/module inside a larger product, do not copy this file unchanged to the product root. Use `profiles/application-with-ai-module/` so repository-wide rules stay application-centric and MAF-specific instructions are scoped to the AI subtree.

This repository uses Microsoft Agent Framework (MAF) in C#/.NET.

Treat MAF as the agent/workflow orchestration layer. Keep the LLM provider, cloud/runtime, storage, and external integrations replaceable unless the concrete project explicitly requires a provider-specific capability.

This file intentionally contains only repository-wide invariants and routing guidance. Detailed MAF implementation knowledge lives in `.agents/skills/` and should be loaded only when the task needs it.

## Project-specific context

Customize this section when adopting the template in a real repository.

Document at least:

- solution/project structure;
- target .NET SDK;
- installed MAF package names and versions;
- build, format, test, and run commands;
- locations of agents, workflows, tools, middleware, context providers, provider adapters, and hosts;
- model-provider integration and supported capabilities;
- persistence, session, checkpoint, durability, and hosting choices;
- security/privacy/approval constraints;
- intentionally provider-specific features and their portability impact.

Do not weaken the general rules below when filling this section.

## Source discipline

MAF evolves quickly. Before changing MAF code:

1. inspect `global.json`, solution files, project files, and central package management;
2. determine the exact installed MAF packages and versions;
3. inspect nearby repository code and tests;
4. use Microsoft Learn and the official `microsoft/agent-framework` source/samples;
5. prefer documentation/source matching the installed package version over current `main` examples;
6. never copy an Azure/OpenAI/Foundry sample as architectural truth—extract the MAF abstraction from the provider-specific setup.

The installed NuGet package surface is authoritative for compilable APIs.

## Mandatory architecture decision

Before implementing agentic behavior, classify each responsibility as one of:

- deterministic C# application/domain logic;
- tool/function;
- agent;
- workflow executor/edge;
- middleware;
- agent session state;
- context provider / retrieval;
- workflow shared state / checkpoint / durable state;
- provider adapter;
- hosting/development surface.

Use the least-agentic design that satisfies the requirement.

### Deterministic C#

Use ordinary C# for exact rules, validation, calculations, transformations, permissions, persistence decisions, and deterministic routing.

### Tool/function

Use a tool when an agent needs a bounded capability such as calling application logic, an API, a database, an MCP server, or another deterministic service.

### Agent

Use an agent when the model must make open-ended semantic judgments, synthesize language, plan, converse, or autonomously choose among a bounded set of tools.

### Workflow

Use a workflow when execution order, branching, fan-out/fan-in, retries, validation, approval, pause/resume, checkpoints, or state transitions must be explicit.

A common production pattern is: **workflow owns the process; agents own bounded semantic steps**.

## MAF-first rule

Before implementing custom agent loops, routers, state machines, tool registries, conversation stores, middleware chains, or workflow engines, check whether MAF already provides the abstraction.

Prefer MAF-native concepts when they fit:

- `AIAgent` / `ChatClientAgent` for application-owned model-driven agents;
- `AgentSession` for conversation-scoped state;
- AI context providers for injected context, memory, and RAG;
- `AIFunction` / `AIFunctionFactory` and supported `AITool` abstractions for local tools;
- MCP tools through the supported MCP integration rather than custom RPC wrappers when MCP is the correct boundary;
- agent, function-invocation, or `IChatClient` middleware at the narrowest appropriate pipeline layer;
- built-in MAF multi-agent orchestrations (sequential, concurrent, handoff, group chat, Magentic) when their semantics match the requirement;
- `WorkflowBuilder`, `Executor`, `[MessageHandler]`, typed messages, and edges for custom deterministic graph orchestration;
- workflow request/response mechanisms for human/external input;
- workflow checkpoints/durable extensions when restartability is required;
- structured outputs before programmatic branching on model results;
- DevUI only as a development/debug surface.

Always verify names and signatures against the installed packages.

## Provider and cloud neutrality

Provider neutrality is a hard requirement unless the concrete repository documents an explicit exception.

Keep separate:

- domain/application logic;
- MAF agent/workflow orchestration;
- model-provider integration;
- persistence/checkpoint storage;
- hosting/cloud runtime;
- tools, MCP servers, and external APIs.

Provider SDK types must not leak into domain services, workflow messages, executor contracts, reusable tools, validators, persistence models, or default unit tests.

Provider selection belongs in the composition root/configuration, not in prompts, agents, workflow executors, or business logic.

If a capability exists only on some providers, model that as an explicit capability/adapter and define fallback or unsupported behavior. Do not redesign the whole application around one provider's SDK.

A normal provider swap should require changes only to configuration, DI registration, the provider adapter, and provider-specific integration tests.

## State taxonomy

Do not use “memory” as a catch-all.

Ask what lifetime and owner the data has:

- one method/run only → local variables / run options;
- one conversation → `AgentSession` state/history;
- dynamically supplied knowledge/context → context provider / retrieval;
- data shared between workflow steps → typed workflow messages first, shared workflow state only when justified;
- resumable workflow execution → checkpoint/durable state;
- long-term application/customer data → application persistence outside the agent runtime.

Prefer explicit typed message flow over hidden shared state when practical.

## Model outputs are untrusted

If model output drives code, routing, persistence, tool execution, security-sensitive behavior, or external side effects:

1. request structured output when supported;
2. deserialize into a dedicated type;
3. validate required fields, allowed values, and invariants;
4. fail closed or use a bounded repair/retry policy;
5. only then branch or execute actions.

Do not put business invariants only in prompts.

## Tools are security boundaries

Tools must be narrow, explicit, and independently testable.

- Validate arguments in code.
- Enforce authorization and business rules in code.
- Pass cancellation/timeouts through external calls.
- Do not expose unrestricted database contexts, generic HTTP clients, shells, filesystem access, or administrative SDKs unless the task explicitly requires and constrains them.
- Treat MCP servers and tool responses as external/untrusted integrations.
- Use approval for consequential/irreversible actions when appropriate.

## Reliability and .NET rules

- Nullable reference types on.
- Async end-to-end; no `.Result` / `.Wait()`.
- Propagate `CancellationToken` through agent, workflow, tool, HTTP, persistence, and long-running calls.
- Use bounded retries only for retryable failures and at the correct boundary.
- Avoid nested retry multiplication between provider, agent, tool, and workflow layers.
- Prefer immutable records for messages and structured outputs.
- Keep side effects idempotent when retries/resume are possible.
- No static mutable runtime state.
- Never commit secrets.

## Testing contract

Default tests should not require a live LLM.

Test separately:

- deterministic services and validators;
- tool contracts and authorization;
- structured-output parsing/validation;
- workflow routing, branch behavior, failure paths, and state transitions;
- middleware behavior;
- provider adapters with focused integration tests;
- real-model behavior with explicit opt-in/evaluation tests.

If an executor is deterministic, its behavior should be testable without model access.

## Development surfaces

Keep CLI harnesses and DevUI out of reusable core projects.

- CLI: simple repository-owned local test UX.
- Harness agent: opinionated MAF runtime; do not introduce it merely for terminal UX.
- DevUI: local discovery/execution/visualization/debugging surface.
- OTLP backend: external observability destination.

Do not conflate these surfaces.

## Skill routing

Use the matching repository skill for MAF work:

- `$maf-architecture` — classify a requirement and choose the MAF abstraction.
- `$maf-agents` — create/change `AIAgent` / `ChatClientAgent`, agent sessions, structured agent outputs, agent composition.
- `$maf-tools` — local function tools, agent-as-tool, MCP integration, tool approvals/safety.
- `$maf-workflows` — built-in orchestrations plus custom executors, typed messages, edges, branching, fan-out/fan-in, state, checkpoints, HITL, workflow-as-agent.
- `$maf-context-memory` — sessions, history, context providers, RAG, memory/storage/compaction decisions.
- `$maf-middleware` — agent/function/chat-client middleware and runtime context.
- `$maf-provider-integration` — isolate and configure model-provider SDKs and capabilities.
- `$maf-observability` — MAF/OpenTelemetry instrumentation and trace boundaries.
- `$maf-devui` — DevUI registration, hosting, workflow visualization, execution protocol, trace/debug setup.
- `$maf-testing` — deterministic tests, workflow tests, fake agents/clients, MAF/MEAI evaluation, integration/evaluation strategy.
- `$maf-review` — architecture/code review across all of the above.

A task may require more than one skill. Load only the relevant skills/references.

## Definition of done

For MAF code changes, report:

- MAF abstraction chosen and why;
- provider-specific assumptions/coupling;
- files changed;
- commands/tests run and results;
- untested behavior or version uncertainty;
- any production risk involving state, retries, side effects, security, or provider capabilities.
