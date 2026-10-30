# Conversation, supplied context and retrieval

Begin with data lifetime and access, not the word memory.

| Data | Architectural owner |
|---|---|
| Related conversation turns | Agent session/history |
| Invocation metadata | Per-run context |
| Consistently supplied knowledge | Context provider or explicit preparation step |
| Searchable external knowledge | Authorized retrieval service |
| Process coordination | Typed workflow messages/state |
| Execution recovery | Checkpoint/durable infrastructure |
| Business/user facts | Application persistence |

`AgentSession` is an orientation term for conversation state, not a general database. Define creation, lookup, restore, expiration, deletion and concurrent access. Authenticate and scope every externally supplied identifier before state access. Local deletion does not by itself define deletion of remote history, files or domain data.

## Retrieval strategy

Use deterministic retrieval before generation when grounding is mandatory; expose a retrieval tool when search is a semantic choice; combine them for common context plus on-demand lookup. A context provider should supply context, not hide business workflows.

Authorize corpus access before ranking. Return bounded evidence and provenance; treat retrieved text as untrusted data. Measure retrieval quality/citations separately from answer quality. Define explicit behavior for absent or conflicting evidence.

## History and storage

Choose retention/privacy policy separately from context-window compaction. Preserve coherent conversation/tool-call relationships and test isolation, serialization/restore, cancellation and concurrent writes when persisted. Do not assume local and provider-backed history have identical semantics.

Find actual session factories, storage contracts, context-provider and compaction APIs through [official-source investigation](../../../resources/references/official-sources.md). Storage-specific options and schema migrations belong in the adopting project's implementation evidence.
