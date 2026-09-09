---
name: maf-agents
description: Implement or review Microsoft Agent Framework agents in C#/.NET when the model owns open-ended semantic behavior, including AIAgent/ChatClientAgent, sessions, streaming or multimodal runs, structured outputs, bounded autonomy, background responses, declarative agents, runtime Agent Skills, Harness Agent, and agent composition.
---

# MAF agents

## Before coding

Read `../../references/official-sources.md` and verify installed packages. Then read `references/agent-patterns.md`.

## Default model

For application-owned chat/model agents, prefer the framework's normal `AIAgent`/`ChatClientAgent` path over a custom model loop when the installed provider can expose a compatible `IChatClient` or agent implementation.

`AIAgent` is the common agent abstraction. `ChatClientAgent` is the important application-owned implementation for a provider-neutral `IChatClient` pipeline. Verify constructor/options signatures against installed packages.

Only derive a custom `AIAgent` when the runtime behavior genuinely cannot be represented by an existing MAF agent type. Do not create a custom agent merely to wrap one prompt call.

## Input, streaming and long-running runs

Use MAF/MEAI content types for multimodal input and validate media before model access. Treat supported modality, upload, URI and size behavior as provider capabilities.

Stream with `RunStreamingAsync` when the caller benefits from incremental events. Cancellation, disconnect, partial-output persistence and safe event projection remain application/host responsibilities.

Background responses use continuation tokens and are provider-limited. Do not equate them with workflow durability. Protect tokens, bound polling/reconnection, and use durable execution when work must survive process loss.

## Bounded autonomy

Looping, planning, todos and background-agent delegation require explicit stop conditions and hard limits for iterations, tool calls, parallelism, time, tokens and cost. Prefer a workflow where sequence, branching, approval or recovery must be guaranteed.

Declarative agents/workflows are configuration forms with their own supported schema and maturity; do not assume parity with programmatic APIs. Validate configuration and version support before adoption.

MAF runtime Agent Skills are application-agent inputs discovered during a run. Repository `.agents/skills/` are Codex developer guidance. Never load this guidance pack into an application agent as runtime skills. Use Harness Agent only when its opinionated runtime behavior is deliberately required, not merely for terminal UX.

## Agent responsibility

An agent should own semantic behavior, not application invariants.

Keep outside the agent:

- exact business rules;
- persistence rules;
- permissions/authorization;
- deterministic routing;
- retry/idempotency policy;
- irreversible side-effect decisions;
- data validation that can be expressed in C#.

## Instructions

Use instructions for role, task framing, semantic constraints, tool-use guidance, and output expectations. Do not use the prompt as the only enforcement mechanism for security or business rules.

## Structured outputs

When another component consumes the result programmatically, use provider/MAF-supported structured output where available, deserialize to a dedicated type, validate, and only then act.

Do not assume every agent/provider supports the same structured-output mechanism. The provider adapter/capability layer must expose limitations.

## Sessions

Create/reuse an `AgentSession` when multiple runs belong to the same conversation. Do not use session state as general application persistence.

Use `$maf-context-memory` when deciding history/context/storage behavior.

## Agent composition

When a parent agent should decide whether to delegate to another specialized agent, consider exposing the child agent with `AsAIFunction()` when supported by the installed API. This is analogous to agent-as-tool delegation in LangChain: routing remains model-driven.

If delegation order/branching must be guaranteed, prefer a workflow instead.

## Testing

- Keep the agent's deterministic collaborators injectable.
- Test prompt-independent rules outside the LLM.
- Use fake/stub agents or chat clients where the installed abstractions permit it.
- Real-model quality belongs in opt-in evaluations/integration tests.

## Completion check

Confirm that the implementation uses a real MAF agent abstraction, provider types do not leak into core contracts, session lifetime is intentional, structured output is validated, multimodal/continuation inputs are protected, autonomy and tools are bounded, cancellation propagates, and deterministic process control has not been hidden inside the prompt.
