# Hosting and protocol selection

| Decision | Choose when | You still own |
|---|---|---|
| Embedded/in-process | Agent is an internal application capability | App auth, limits, state, cancellation and deployment |
| Self-hosted | Existing infrastructure/control is important | Routes, authn/z, tenancy, storage, scaling, upgrades and protocol adapters |
| Durable self-hosted | Work must survive restarts or long waits | Domain idempotency, data retention and runtime/storage operations |
| Foundry Hosted Agents | Managed scaling, identity and session lifecycle justify platform coupling | Agent code, policy, downstream authorization, cost and service configuration |

Protocols solve interoperability, not operation. OpenAI-compatible endpoints target SDK compatibility; A2A targets remote-agent interoperability; AG-UI targets streamed web-agent interaction and approvals; MCP exposes bounded capabilities; application-native contracts preserve product-specific semantics.

Test disconnect/resume, cancellation, duplicate delivery, tenant-crossing identifiers, expired credentials, payload limits, slow consumers, partial streams, deployments with in-flight work, and storage unavailability.

For 1.24, generic/ASP.NET Core hosting, A2A/AG-UI hosting and DevUI are preview; OpenAI hosting is alpha. Foundry's managed service is GA while its MAF hosting package remains preview. The current C# Foundry guide requires .NET 10+. Verify deployment requirements independently.

Current A2A hosting disallows background responses and defaults to development-only in-memory session/task stores. AG-UI supports persisted hosted-session continuation, but `threadId` does not prove ownership. Authenticate and establish isolation before lookup across all protocols.
