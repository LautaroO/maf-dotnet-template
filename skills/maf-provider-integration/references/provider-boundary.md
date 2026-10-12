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
