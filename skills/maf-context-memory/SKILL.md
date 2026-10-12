---
name: maf-context-memory
description: Design or implement Microsoft Agent Framework conversation state, AgentSession, history/storage, AI context providers, RAG/retrieval, compaction, and memory boundaries in C#/.NET. Use when deciding what data belongs in a session, context provider, retrieval tool, workflow state, checkpoint, or application database.
---

# MAF context and memory

Read `../../resources/references/official-sources.md` and `references/session-context-rag.md`.

## Start with lifetime, not the word memory

Classify the data:

- conversation identity/history → `AgentSession` / history provider;
- per-run metadata → run options / runtime context;
- proactively injected knowledge/context → context provider;
- searchable external knowledge → retrieval service exposed via context provider or tool;
- workflow coordination → workflow messages/state;
- execution recovery → checkpoint/durable state;
- durable user/business facts → application database/service.

Do not store everything in `AgentSession.StateBag` because it is convenient.

## Sessions

Use an `AgentSession` across related agent runs in one conversation. Current C# sessions expose a state bag and concrete agent/provider implementations may carry remote conversation identifiers/history behavior.

Define who creates, persists, restores, expires, and isolates sessions.

Treat every caller/protocol-supplied session or continuation identifier as untrusted. Bind stored state to authenticated tenant/user/workspace scope before lookup, and define encryption, retention and deletion.

## Context providers

Context providers participate in the agent pipeline and can supply/transform context around invocation. Use them for controlled context that should be consistently available, not for arbitrary hidden business logic.

## RAG strategy

Choose explicitly:

- deterministic/2-step RAG → retrieve before model invocation; a context provider is a natural MAF abstraction;
- agentic RAG → expose retrieval as a tool so the agent decides whether/what to search;
- hybrid → deterministic common grounding via context provider + retrieval tools for ambiguous/on-demand lookup.

Current MAF includes `TextSearchProvider` as a RAG context-provider implementation. Verify installed package availability and avoid coupling domain logic to its storage implementation.

Authorize corpus access before ranking, preserve source provenance, constrain retrieved content, and treat it as untrusted data that cannot expand tool authority. Measure retrieval recall/precision and citation correctness separately from generated-answer quality.

## Compaction/storage

Conversation history growth is an operational concern. Use supported history storage/compaction mechanisms instead of manually truncating arbitrary messages inside prompts. Define retention and privacy policy separately from token-window management.

## Testing

Test context selection/retrieval independently of the LLM. Test session isolation and serialization/restoration if persisted. Evaluate retrieval quality separately from answer generation quality.
