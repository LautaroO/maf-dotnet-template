# Official sources and version discipline

Use official sources in this order:

1. Microsoft Learn Agent Framework documentation: https://learn.microsoft.com/agent-framework/
2. Official repository: https://github.com/microsoft/agent-framework
3. Official samples: https://github.com/microsoft/Agent-Framework-Samples
4. Installed NuGet package XML docs / decompiled public API / local source when available.

Useful Learn areas:

- Overview: https://learn.microsoft.com/agent-framework/overview/
- Agents: https://learn.microsoft.com/agent-framework/agents/
- Agent pipeline: https://learn.microsoft.com/agent-framework/concepts/agents/agent-pipeline
- Tools: https://learn.microsoft.com/agent-framework/agents/tools/
- Function tools: https://learn.microsoft.com/agent-framework/agents/tools/function-tools
- Local MCP tools: https://learn.microsoft.com/agent-framework/agents/tools/local-mcp-tools
- Structured outputs: https://learn.microsoft.com/agent-framework/agents/structured-outputs
- Sessions: https://learn.microsoft.com/agent-framework/concepts/agents/conversations/session
- Context providers: https://learn.microsoft.com/agent-framework/concepts/agents/conversations/context-providers
- RAG: https://learn.microsoft.com/agent-framework/agents/rag
- Middleware: https://learn.microsoft.com/agent-framework/concepts/agents/middleware/
- Runtime context: https://learn.microsoft.com/agent-framework/concepts/agents/middleware/runtime-context
- Workflows: https://learn.microsoft.com/agent-framework/workflows/
- Built-in orchestrations: https://learn.microsoft.com/agent-framework/workflows/orchestrations/
- Executors: https://learn.microsoft.com/agent-framework/concepts/workflows/executors
- Edges: https://learn.microsoft.com/agent-framework/concepts/workflows/edges
- Workflow state: https://learn.microsoft.com/agent-framework/concepts/workflows/state
- Checkpoints: https://learn.microsoft.com/agent-framework/workflows/checkpoints
- HITL: https://learn.microsoft.com/agent-framework/workflows/human-in-the-loop
- Workflows as agents: https://learn.microsoft.com/agent-framework/workflows/as-agents
- Durable extension: https://learn.microsoft.com/agent-framework/hosting/azure-functions
- Agent evaluation: https://learn.microsoft.com/agent-framework/agents/evaluation
- Agent observability: https://learn.microsoft.com/agent-framework/agents/observability
- DevUI: https://learn.microsoft.com/agent-framework/integrations/by-component/ui/devui/
- Harness: https://learn.microsoft.com/agent-framework/concepts/harness
- Multimodal: https://learn.microsoft.com/agent-framework/agents/multimodal
- Background responses: https://learn.microsoft.com/agent-framework/agents/background-responses
- Declarative agents: https://learn.microsoft.com/agent-framework/agents/declarative
- Agent Skills (application runtime): https://learn.microsoft.com/agent-framework/agents/skills
- Hosting overview: https://learn.microsoft.com/agent-framework/hosting/
- Self-hosting: https://learn.microsoft.com/agent-framework/hosting/self-hosting/
- Foundry Hosted Agents: https://learn.microsoft.com/agent-framework/hosting/foundry-hosted-agent
- A2A hosting: https://learn.microsoft.com/agent-framework/hosting/self-hosting/a2a/dotnet
- AG-UI: https://learn.microsoft.com/agent-framework/integrations/by-component/ui/ag-ui/

## Repository skills vs runtime Agent Skills

The `skills/maf-*` directories in this plugin are Codex developer guidance. MAF runtime Agent Skills are instructions/resources/scripts discovered by an application agent during execution. They have different consumers and trust boundaries. Never copy this plugin into an application's runtime skill store.

## Verification baseline

The [capability matrix](../docs/capabilities/maf-dotnet-1.24.md) records `dotnet-1.24.0`, released 2026-10-07, with documentary/API-surface verification on 2026-10-12. All rows were reviewed against official C# guidance, tagged source/package metadata and published NuGet indexes; see [verification evidence](../docs/capabilities/verification-1.24.md). This is not application compilation or installed-package compatibility evidence.

A [scoped 1.25–1.26 delta review](../docs/capabilities/verification-1.26.md) dated 2026-10-24 updates approval/MCP, storage, workflow, middleware, hosting/DevUI, telemetry and Harness/file/shell guidance. It preserves the full 1.24 baseline and unchanged row metadata; do not generalize its sources into fresh verification of every capability or package. Current Learn can omit tagged fixes or contradict comments; the record distinguishes those cases and publication uncertainty.

## Conflicting official evidence

Learn and tagged source can disagree. Record the exact page, tag and package metadata; distinguish implementation in source from a published package and from the application's installed API. Prefer matching tagged API evidence for version-specific implementation questions while keeping unresolved compatibility claims qualified.

For example, [Learn Agent Hooks](https://learn.microsoft.com/agent-framework/agents/agent-hooks) still says Python-only, while [the 1.24 .NET project](https://github.com/microsoft/agent-framework/blob/dotnet-1.24.0/dotnet/src/Microsoft.Agents.AI.AgentHooks/Microsoft.Agents.AI.AgentHooks.csproj) defines an alpha package that [NuGet publishes](https://www.nuget.org/packages/Microsoft.Agents.AI.AgentHooks/1.24.0-alpha.261006.1). Do not repeat “unavailable for .NET” categorically or silently treat it as stable/installed. This evidence does not establish .NET FIDES support.

## Version rule

MAF APIs change. The repository's installed package versions are authoritative for code that must compile.

Before using an API seen in current docs or `main`:

1. identify the installed package and version;
2. inspect the package's available type/method surface;
3. find the corresponding tag/commit/sample when possible;
4. adapt examples to the installed API instead of upgrading packages silently.

Never mix APIs from current docs, old samples, and installed packages without noticing the version mismatch.

## Source interpretation rule

For every official sample separate:

1. MAF abstraction being demonstrated;
2. model-provider-specific setup;
3. cloud/hosting-specific setup;
4. sample-only shortcuts.

Azure, Foundry, Azure OpenAI, or OpenAI appearing in a sample is not permission to couple core architecture to those SDKs.
