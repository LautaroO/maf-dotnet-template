---
name: maf-provider-integration
description: Implement or review provider-neutral model integration for Microsoft Agent Framework in C#/.NET. Use when constructing IChatClient/AIAgent from OpenAI, Azure OpenAI, Microsoft Foundry, Anthropic, Ollama, or another provider; isolating SDK types; handling provider capabilities; configuration/auth; structured output/tool differences; or enabling provider swaps.
---

# MAF provider integration

Read `../../resources/references/official-sources.md`, `../../resources/references/provider-neutrality.md`, and `references/provider-boundary.md`.

## Goal

The provider is a replaceable implementation plugged into MAF, not the architecture center.

## Preferred boundary

If the provider can expose `Microsoft.Extensions.AI.IChatClient` and the use case fits `ChatClientAgent`, prefer that provider-neutral boundary.

If a provider supplies its own MAF `AIAgent` implementation, isolate construction and provider-specific options in infrastructure/composition root.

Do not create a repository-owned abstraction merely to duplicate `IChatClient`/`AIAgent`. Create a custom port only for capabilities MAF does not model sufficiently for your application.

## Capability differences

Providers may differ in:

- tool calling;
- structured output;
- hosted tools/file search/code interpreter;
- server-side conversation history;
- background responses;
- reasoning/streaming event shapes;
- usage/safety metadata;
- maximum context/tool limits.

Model these as explicit capabilities. Include at least structured output, local tool calling, background execution/continuation, hosted tools, multimodal input, streaming fidelity, and required hosting/protocol support. Do not silently assume feature parity.

Detect capabilities during composition/startup where possible and expose a stable descriptor to application-owned orchestration. Fail clearly or select an explicit fallback before a run; do not discover incompatibility after a consequential action begins.

## Configuration

Keep model/deployment names, endpoints, credentials, timeouts, and provider selection in typed configuration/secret stores. Agents/workflows receive already-constructed neutral dependencies.

## Error/retry ownership

Translate provider-specific transient failures at the adapter boundary where useful. Do not leak provider exception types through the application.

Do not retry semantic validation failures as if they were network errors.
