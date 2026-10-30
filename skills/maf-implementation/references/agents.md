# Agent implementation patterns

## Common application-owned path

Conceptually:

```csharp
IChatClient chatClient = /* resolved from provider adapter */;

AIAgent agent = new ChatClientAgent(
    chatClient,
    /* options/name/instructions/tools according to installed MAF version */);
```

The exact overloads/options are version-sensitive. Inspect installed APIs before copying current Learn snippets.

## Run model

MAF agent calls typically use `RunAsync` / streaming variants and may accept an `AgentSession` plus run options. Treat the session as the conversation-scoped state owner.

## Custom agent threshold

A custom `AIAgent` is justified when you are implementing a genuinely different agent runtime/protocol/remote service behavior. It is not the default way to make a domain-specific assistant.

## Agent vs workflow

Use an agent when the model chooses what happens next. Use a workflow when the application must guarantee what happens next.

Examples:

- "Use whichever of these 4 tools helps answer the question" → agent.
- "Translate, validate, retry at most twice, then escalate" → workflow containing agent steps.
- "Choose between SQL schema lookup and glossary lookup based on ambiguity" → potentially agentic retrieval tool choice.
- "Always load tenant policy before answering" → context provider / deterministic pre-step, not agent discretion.

## Agent as tool

`AIAgent.AsAIFunction()` is useful for a focused child agent exposed to a parent agent. Keep the child responsibility narrow and description explicit. If the parent accumulates many child agents/tools, reconsider workflow orchestration or hierarchical boundaries because tool selection quality degrades as the surface grows.

## Reviewed 1.24 capability boundaries

`Microsoft.Agents.AI.Harness` is a separately published stable 1.24 package; optional experimental looping/background APIs retain their own maturity. Its [guide](https://learn.microsoft.com/agent-framework/concepts/harness) documents default skills, todos/modes and approvals. Todo tracking does not re-invoke the agent; plan/execute instructions are not authorization.

[Background agents](https://learn.microsoft.com/agent-framework/agents/background-agents) have in-process child task handles that do not survive metadata restore. Results are text and do not proxy structured child approval requests to the parent. Host child approvals explicitly and bound task lifetimes; delegation is distinct from provider continuation and durability.

[Structured-output streaming](https://learn.microsoft.com/agent-framework/agents/structured-outputs) requires assembling updates before typed deserialization/validation. Intermediate JSON cannot authorize effects. Declarative agents have a 1.24 RC package while declarative workflows have a stable package; inspect their schemas and integrations separately.

## Scoped 1.25–1.26 updates

Harness standing approvals persist in sessions across changed tool instances; review them before reusing a session with a different tool set or MCP source. Saved unanswered approvals are rejected on the next underlying run with binding enabled, not while merely waiting. See [approval contracts](mcp-and-approval.md).

The 1.26 file store adds bounded multi-step search and cancellation; handle search timeout separately from caller cancellation and keep custom file-store scope/size limits. The Docker shell option rename to `UnsafeExtraRunArgs` makes trusted configuration ownership explicit. The 1.25 progress-instruction change was reverted; do not migrate instructions based on that intermediate commit. See [scoped evidence](../../../resources/docs/capabilities/verification-1.26.md).

## Responsibility and implementation guidance

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

MAF runtime Agent Skills are application-agent inputs discovered during a run. This plugin's `skills/` are Codex developer guidance. Never load this plugin into an application agent as runtime skills. Use Harness Agent only when its opinionated runtime behavior is deliberately required, not merely for terminal UX.

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
