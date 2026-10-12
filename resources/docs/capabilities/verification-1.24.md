# MAF .NET 1.24 verification evidence

Verified on 2026-10-12 against `dotnet-1.24.0` and current official documentation. All 23 matrix rows received documentary/API-surface review; this is not an application build or runtime certification.

## Package evidence

Read the complete tagged source-tree inventory, all 35 projects under `dotnet/src/`, the [central package properties](https://github.com/microsoft/agent-framework/blob/dotnet-1.24.0/dotnet/nuget/nuget-package.props), and selected public APIs. Interpret `IsReleased`, `IsReleaseCandidate`, suffixes and imported properties together. Cross-checked 20 relevant package indexes through NuGet's official flat-container API without installing/restoring packages.

| Package group | Published version evidence |
|---|---|
| Core, abstractions, workflows, Harness, OpenAI, Anthropic | 1.24.0 stable |
| Declarative agents | [1.24.0-rc1](https://www.nuget.org/packages/Microsoft.Agents.AI.Declarative/1.24.0-rc1) |
| Declarative workflows | [1.24.0](https://www.nuget.org/packages/Microsoft.Agents.AI.Workflows.Declarative/1.24.0) |
| Hooks and MAF MCP | [Hooks alpha](https://www.nuget.org/packages/Microsoft.Agents.AI.AgentHooks/1.24.0-alpha.261006.1), [MCP alpha](https://www.nuget.org/packages/Microsoft.Agents.AI.Mcp/1.24.0-alpha.261006.1) |
| Generic/Foundry hosting, A2A/AG-UI hosting, DevUI | 1.24.0-preview.261006.1 |
| OpenAI hosting | 1.24.0-alpha.261006.1 |
| Foundry adapter, Purview | Preview, RC respectively |
| Durable Task/Azure Functions integrations | Latest returned version 1.16.0-preview.260922.1; separate lifecycle from core 1.24 |

Stable packaging does not remove experimental markers from individual APIs. Publication is distinct from the adopting application's installed version. A local packability declaration in the declarative project was insufficient by itself; central imports and the published RC resolved that question.

## Row review decisions

Each [matrix row](maf-dotnet-1.24.md) links its official source. C# sections were reviewed rather than inferring .NET support from Python examples.

| Area | Evidence and decision |
|---|---|
| Agents, streaming | Tagged `AIAgent` provides async sessions, runs and streaming with cancellation; `ChatClientAgent` is the application-owned chat implementation. |
| Sessions/history | `StateBag` and agent/service-specific serialization are documented. Tagged experimental `AgentSessionStore` restores independent instances; remote IDs still require caller ownership. |
| Multimodal | C# example demonstrates text/image URI content; other modalities/uploads remain provider-specific. |
| Structured output | Tagged typed run API and Learn require compatible clients and complete streaming assembly before deserialization/validation. |
| Functions/MCP/approval | MEAI functions and official MCP C# SDK integration exist. MAF MCP integrations are alpha; approvals require pending call/session binding. |
| Background responses | Explicit Responses-provider support differs from remote tasks; current A2A hosting disallows background responses. |
| Looping/planning/background agents | C# providers/decorators exist. Loop/delegation APIs are experimental; child handles do not survive restore; mode instructions do not authorize effects. |
| Declarative agents/workflows | Separate RC agent and stable workflow packages are published; C# schemas and integrations differ. |
| Runtime skills/Harness | Tagged core has skill providers; MCP discovery is experimental. Harness is a separately published stable package with optional experimental composition. |
| Workflows/orchestrations | Graph API, typed/source-generated executors and five orchestration builders exist; Python functional workflows are not a .NET API. |
| Checkpoints/durable execution | Superstep checkpoints require matching topology/agent identities. Durable Task/Functions are independently versioned integrations. |
| Hosting/protocols/DevUI | Hosting preview, protocol alpha/preview, managed Foundry GA and development-only DevUI are distinct; hosts still own auth and durable tenant-scoped storage. |
| Observability/evaluation | Tagged instrumentation and local/evaluation adapters exist. MEAI/provider judges and telemetry capture require separate configuration/egress decisions. |
| Hooks/FIDES | Learn's Python-only Hooks claim conflicts with published .NET alpha and tagged source. FIDES remains explicitly Python-only in its C# guide and has no .NET implementation in the reviewed tree; .NET CodeAct does not supply it. |

## Limits

Current Learn may advance independently of the tag. Conflicts are checked against tagged source and publication rather than erased. Installed API compatibility, security behavior and provider runtime support require adopting-application verification. No .NET project/build, package restore, live model, native-client installation/routing, release or publication was performed here. Both fresh-session adoption profiles remain separate release checks.
