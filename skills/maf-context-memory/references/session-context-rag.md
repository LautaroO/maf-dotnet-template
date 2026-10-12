# Session, context provider, RAG notes

## AgentSession

Current docs describe `AgentSession` as the conversation state container and expose `StateBag`. Agent implementations create sessions through their session factory APIs. Some provider-backed agents may keep remote history keyed by service conversation IDs rather than local full message history.

Never assume all providers persist history the same way.

## Version-sensitive session storage

The [1.22 release](https://github.com/microsoft/agent-framework/releases/tag/dotnet-1.22.0) moved the experimental `AgentSessionStore` contract into `Microsoft.Agents.AI.Abstractions`. The [1.24 tagged contract](https://github.com/microsoft/agent-framework/blob/dotnet-1.24.0/dotnet/src/Microsoft.Agents.AI.Abstractions/AgentSessionStore.cs) distinguishes lookup from get-or-create and requires independent session instances on successful retrieval. Verify the installed contract before writing an adapter; do not reuse a cached mutable session across callers. Storage keys and host isolation wrappers still require application authentication and tenancy policy.

The [1.24 release](https://github.com/microsoft/agent-framework/releases/tag/dotnet-1.24.0) includes fixes for explicit null state roundtrips, disabled recent-search memory and cancellation. Test those semantics in the adopting application with fake providers/stores; source fixes do not prove compatibility with existing persisted state.

## Context provider

A context provider can contribute context before model invocation and may extract/update context after runs depending on its implementation. Keep it focused on context/memory concerns.

## RAG mapping

LangChain retriever injected before chain → MAF context-provider style retrieval.

LangChain retriever tool selected by an agent → MAF function/tool wrapping the retrieval service.

A retrieval tool should return bounded source snippets/metadata, not a raw database client or unlimited corpus dump.
