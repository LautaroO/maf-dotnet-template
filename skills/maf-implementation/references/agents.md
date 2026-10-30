# Agents and bounded semantic behavior

An agent owns interpretation, synthesis or open-ended selection among bounded capabilities. Exact rules, authorization, persistence policy and irreversible-effect decisions remain in deterministic application code.

## Choose the smallest runtime

Start with one agent and the tools/context needed by the task. Use the framework's agent abstractions when they express the behavior; a domain-specific prompt alone rarely justifies a custom runtime. `AIAgent`, `ChatClientAgent` and `IChatClient` are useful .NET search terms, not prescribed constructors or availability guarantees.

Keep instructions focused on role, semantic task, permitted capabilities and output expectations. Bound iterations, tool calls, concurrency, time and cost. A workflow is appropriate when order, approvals or recovery must be guaranteed rather than selected by the model.

## Input, output and conversation

Validate media type, size, ownership and retrieval URLs before model access. Provider modality and streaming support are implementation questions. When code consumes a result, deserialize into a dedicated contract and validate allowed values before acting; unfinished streamed output cannot authorize effects.

Reuse conversation state only when turns belong together. An ephemeral local session does not establish provider-side retention policy. Separate provider background continuation, delegated work and recoverable workflow execution instead of calling them all durability.

## Composition and reusable instructions

A specialist agent can be exposed as a bounded capability when its parent should select it semantically. Define authority, result contracts and delegation budgets; choose explicit workflow control for mandatory sequencing. Runtime Agent Skills and an opinionated harness are application runtime choices with distinct trust/execution boundaries. This plugin's developer skills must not be loaded into that runtime store.

Verify semantic quality separately from deterministic collaborators, limits and contracts. For exact factories, run/stream APIs, session creation, runtime extensions and capabilities, use [official-source investigation](../../../resources/references/official-sources.md).
