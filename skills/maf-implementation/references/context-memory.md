# Session, context provider, RAG notes

## AgentSession

Current docs describe `AgentSession` as the conversation state container and expose `StateBag`. Agent implementations create sessions through their session factory APIs. Some provider-backed agents may keep remote history keyed by service conversation IDs rather than local full message history.

Never assume all providers persist history the same way.

## Version-sensitive session storage

The [1.22 release](https://github.com/microsoft/agent-framework/releases/tag/dotnet-1.22.0) moved the experimental `AgentSessionStore` contract into `Microsoft.Agents.AI.Abstractions`. The [1.24 tagged contract](https://github.com/microsoft/agent-framework/blob/dotnet-1.24.0/dotnet/src/Microsoft.Agents.AI.Abstractions/AgentSessionStore.cs) distinguishes lookup from get-or-create and requires independent session instances on successful retrieval. Verify the installed contract before writing an adapter; do not reuse a cached mutable session across callers. Storage keys and host isolation wrappers still require application authentication and tenancy policy.

The [1.24 release](https://github.com/microsoft/agent-framework/releases/tag/dotnet-1.24.0) includes fixes for explicit null state roundtrips, disabled recent-search memory and cancellation. Test those semantics in the adopting application with fake providers/stores; source fixes do not prove compatibility with existing persisted state.

### Reviewed 1.25–1.26 storage changes

In 1.25, `CosmosChatHistoryProvider` replaces trailing constructor settings with `CosmosChatHistoryProviderOptions`. Migrate ownership, state-key and message-filter settings deliberately. `PartitionKeyFactory` controls write/read/count/delete keys; without it, tenant+user IDs select hierarchical partitioning, otherwise the key is the conversation ID. Tenant/user metadata is persisted independently, so a flat `/conversationId` container can retain that metadata with an explicit factory. Match the existing container schema and data; this API change neither migrates documents nor authorizes tenants.

The experimental 1.26 `AgentSessionStore` adds abstract `DeleteSessionAsync(AIAgent, AgentSessionStoreKey, CancellationToken)`, with missing sessions treated as a no-op. Update custom stores and decorators; preserve isolation-key scoping and authenticate deletion. Deleting local session state does not establish deletion of remote provider history, files, checkpoints or application data. FoundryMemory/Mem0 cancellation fixes distinguish caller cancellation from ordinary memory errors. See [tagged source evidence](../../../resources/docs/capabilities/verification-1.26.md).

## Context provider

A context provider can contribute context before model invocation and may extract/update context after runs depending on its implementation. Keep it focused on context/memory concerns.

## RAG mapping

LangChain retriever injected before chain → MAF context-provider style retrieval.

LangChain retriever tool selected by an agent → MAF function/tool wrapping the retrieval service.

A retrieval tool should return bounded source snippets/metadata, not a raw database client or unlimited corpus dump.

## Responsibility and implementation guidance

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
