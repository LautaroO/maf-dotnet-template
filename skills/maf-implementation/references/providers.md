# Provider boundary

A useful project shape is:

```text
Application / Domain
    ↓
MAF Agents + Workflows + Tools
    ↓
Microsoft.Extensions.AI / MAF-neutral contracts
    ↓
Infrastructure.ProviderX
    ↓
Provider SDK
```

Composition root responsibilities:

- bind provider/model configuration;
- create authenticated provider client;
- adapt to `IChatClient` or provider-specific `AIAgent` implementation;
- decorate with supported middleware/telemetry;
- register agent/workflow factories.

Do not pass provider SDK request/response types into workflow messages or tools.

Provider-specific hosted tools are capabilities, not universal MAF primitives. If used, isolate them behind a feature boundary and make fallback/unsupported behavior explicit.

## Reviewed upgrade signals through 1.24

The [1.21 release](https://github.com/microsoft/agent-framework/releases/tag/dotnet-1.21.0) replaces the deprecated Bedrock MEAI dependency and removes the Azure.AI.OpenAI dependency. [1.23](https://github.com/microsoft/agent-framework/releases/tag/dotnet-1.23.0) reports breaking dependency upgrades for Azure AI Projects, OpenAI and MEAI; [1.24](https://github.com/microsoft/agent-framework/releases/tag/dotnet-1.24.0) stabilizes the Anthropic agent package. These are adapter/package changes, not a reason to introduce those SDKs into reusable tools or workflows. Inspect direct/transitive package versions, matching samples, capability differences and persisted provider state before upgrading an adopting application.

The scoped [1.25–1.26 review](../../../resources/docs/capabilities/verification-1.26.md) adds A2A SDK preview3/gRPC and Cosmos constructor migration signals, plus Foundry toolbox consent/cache and Purview payload checks. Apply only to selected adapters. AgentMemory updates are unofficial sample dependency changes, not a core persistence requirement. Verify dependency/security constraints independently; do not copy upstream sample pins or infer equal protocol/provider capabilities.

## Responsibility and implementation guidance

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
