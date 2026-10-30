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

## Reviewed 1.25–1.26 protocol deltas

- OpenAI-compatible Chat Completions SSE adds `data: [DONE]` on normal completion in 1.25; failure/cancellation must not masquerade as a complete stream. This is distinct from Responses events.
- 1.25 upgrades A2A SDK dependencies to 1.0.0-preview3. In 1.26, test empty transferable-content rejection and non-routine task status messages as well as artifacts. Agent-card publication is separate from endpoint mapping. Direct gRPC requires the SDK's `A2A.Grpc` package and caller-owned client disposal; transport support does not imply background-response support.
- 1.26 AG-UI named/hosted mappings honor agent DI lifetimes and resolve stores/isolation from request services. A request selector can return null for 404 before state lookup; selection alone is not authorization. Stable registration names, or the selected agent's non-empty name, identify persisted sessions across new instances. Distinct logical agents need distinct names, plus tenant isolation. Explicit null SSE fields are preserved.
- Foundry deferred/consent toolbox resolution is response-scoped in 1.25, with a unique cache identity even if external call IDs repeat. In 1.26, OAuth consent state is preserved across streaming advances/disposal and consent details drive `oauth_consent_request`. Test concurrent callers, duplicate delivery, malformed consent URLs, cancellation and disposal; do not broaden these fixes into a universal isolation guarantee.

See [tagged implementation evidence](../../../resources/docs/capabilities/verification-1.26.md). These changes apply only to selected protocol/hosting adapters and do not require a cloud provider in reusable agents/workflows.

## Responsibility and implementation guidance

Make two independent decisions:

1. operation model: embedded/in-process, self-hosted, durable self-hosted, or managed Foundry Hosted Agents;
2. client boundary: application-native API, OpenAI-compatible endpoint, A2A, AG-UI, MCP, or another explicitly supported protocol.

Do not choose a host from protocol familiarity or assume a protocol provides authentication, authorization, tenancy, persistence, or durability. For every design identify the owner of identity, request limits, session lookup, tenant partitioning, streaming disconnects, continuation tokens, checkpoints, secrets, deployment, scaling, health, telemetry, and incident recovery.

Verify installed packages and maturity. .NET self-hosting and protocol packages may be prerelease even when the underlying service is GA. Treat protocol IDs as untrusted and authorize every session/task/checkpoint lookup.
