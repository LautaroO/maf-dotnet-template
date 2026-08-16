# AGENTS.md — AI module

## Scope

These instructions apply only to this AI/MAF module and its descendants.

This module uses Microsoft Agent Framework (MAF) in C#/.NET as an orchestration/integration layer for AI capabilities. It is not the owner of the application's domain model or business rules.

Read the repository-root `AGENTS.md` first. Repository-wide architecture and domain boundaries remain authoritative. These instructions refine them for AI code.

## Project-specific AI context

Customize this section after installing the profile.

Document at least:

- AI project path and target framework;
- installed MAF package names and exact versions;
- build/test/run commands relevant to this module;
- agent, workflow, tool, middleware, context-provider, provider-adapter, and host locations;
- application/domain projects this module may depend on;
- model-provider integration and supported capabilities;
- session, retrieval, persistence, checkpoint, durability, and hosting choices;
- DevUI/evaluation setup if present;
- security/privacy/approval constraints;
- intentionally provider-specific features and portability impact.

## Source discipline

MAF evolves quickly. Before changing MAF code:

1. inspect the actual project files and installed package versions;
2. inspect nearby code/tests and repository-level architecture rules;
3. use Microsoft Learn and official `microsoft/agent-framework` source/samples;
4. prefer documentation/source matching installed packages over current `main` examples;
5. extract MAF abstractions from provider-specific samples instead of copying provider architecture wholesale.

Installed NuGet packages are authoritative for compilable APIs.

## Boundary rule: orchestrate application capabilities

Before adding logic here, ask whether it belongs in the application/domain layer.

Keep in this module:

- agent instructions/construction;
- MAF workflows, executors, edges, orchestration messages;
- AI-facing tools/adapters over application use cases;
- context providers/retrieval integration;
- structured model-output contracts and AI-specific validators;
- provider adapters;
- AI telemetry/evaluations/DevUI glue.

Keep outside this module:

- domain invariants and business policies;
- ordinary application use cases;
- authorization rules owned by the application;
- generic persistence/business integrations that exist independently of AI.

Tools should normally call application services rather than reimplement their behavior. Workflow executors should orchestrate domain/application capabilities rather than absorb business rules.

Read `.agents/references/application-boundaries.md` when boundaries are unclear.

## Mandatory MAF classification

For each AI responsibility, classify it as one of:

- deterministic C# logic;
- tool/function;
- agent;
- workflow executor/edge/orchestration;
- middleware;
- agent session state;
- context provider/retrieval;
- workflow/checkpoint/durable state;
- provider adapter;
- development/hosting surface.

Use the least-agentic design that satisfies the requirement.

### Deterministic C#

Use ordinary code for exact validation, calculations, transformations, permissions, application decisions, persistence rules, and deterministic routing.

### Tool/function

Use a tool when an agent needs a bounded application capability, lookup, API, database-backed use case, MCP capability, or other deterministic action. Keep the tool contract model-friendly and the business behavior behind an application/service boundary.

### Agent

Use an agent for open-ended semantic judgment, synthesis, conversation, planning, or bounded autonomous tool choice.

### Workflow

Use a workflow for explicit sequence, branching, fan-out/fan-in, validation, retries, approvals, pause/resume, checkpoints, or process state transitions.

A strong default is: **workflow owns the process; agents own bounded semantic steps; application/domain services own business behavior**.

## MAF-first rule

Before implementing custom agent loops, routers, state machines, tool registries, conversation stores, middleware chains, or graph engines, check whether installed MAF packages already provide the abstraction.

Evaluate, as applicable:

- `AIAgent` / `ChatClientAgent`;
- `AgentSession`;
- AI context providers;
- `AIFunction` / `AIFunctionFactory` and supported `AITool` abstractions;
- MCP integration;
- agent/function/`IChatClient` middleware;
- built-in MAF multi-agent orchestrations;
- `WorkflowBuilder`, `Executor`, typed handlers/messages, and edges;
- external request/response and approval mechanisms;
- checkpoints/durable extensions;
- structured outputs;
- DevUI as a development surface only.

Always verify concrete API names/signatures against installed packages.

## Provider neutrality inside the AI module

Keep separate:

- MAF orchestration;
- application/domain services;
- provider-specific client construction/capabilities;
- persistence/checkpoint storage;
- cloud/runtime hosting;
- tools/MCP/external integrations.

Provider SDK types must not leak into application/domain contracts, reusable workflow messages, or generic tools. Provider selection belongs in composition/configuration.

## State taxonomy

Do not use “memory” as a catch-all:

- one run → local values/options;
- one conversation → `AgentSession`/history;
- dynamic knowledge → context provider/retrieval;
- workflow communication → typed messages first;
- resumability → checkpoint/durable state;
- durable product/customer data → application persistence outside MAF.

## Untrusted model outputs

Before model output drives routing, persistence, tool execution, security-sensitive behavior, or side effects:

1. request structured output when supported;
2. deserialize to a dedicated type;
3. validate fields and invariants;
4. apply bounded repair/retry if appropriate;
5. only then act.

Business invariants do not live only in prompts.

## Reliability and tests

- Async end-to-end; propagate `CancellationToken`.
- Bound retries at the correct layer; avoid retry multiplication.
- Design side effects for idempotency when retries/resume are possible.
- Default tests must not require a live model.
- Test tools with fake application services.
- Test deterministic workflow routing independently of model quality.
- Test provider adapters separately.
- Use explicit evaluation tests for real-model behavior.

## Skill routing

Use repo-scoped skills under `.agents/skills/`:

- `$maf-architecture` — abstraction/boundary choice;
- `$maf-agents` — agents/sessions/structured agent outputs;
- `$maf-tools` — local tools, agent-as-tool, MCP, approvals;
- `$maf-workflows` — built-in orchestrations and custom workflows;
- `$maf-context-memory` — sessions/context/RAG/memory choices;
- `$maf-middleware` — cross-cutting interception;
- `$maf-provider-integration` — provider isolation/configuration;
- `$maf-observability` — telemetry/tracing;
- `$maf-devui` — DevUI development surface;
- `$maf-testing` — deterministic tests + evaluations;
- `$maf-review` — MAF/application architecture review.

Load only the skills relevant to the task.

## Definition of done

For AI/MAF changes report:

- chosen MAF abstraction and why;
- which application/domain capability is being orchestrated, if any;
- provider-specific assumptions/coupling;
- tests/commands run;
- untested behavior/version uncertainty;
- production risks involving state, retries, side effects, security, or provider capabilities.
