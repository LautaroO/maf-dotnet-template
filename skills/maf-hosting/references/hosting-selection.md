# Hosting and protocol selection

| Decision | Choose when | You still own |
|---|---|---|
| Embedded/in-process | Agent is an internal application capability | App auth, limits, state, cancellation and deployment |
| Self-hosted | Existing infrastructure/control is important | Routes, authn/z, tenancy, storage, scaling, upgrades and protocol adapters |
| Durable self-hosted | Work must survive restarts or long waits | Domain idempotency, data retention and runtime/storage operations |
| Foundry Hosted Agents | Managed scaling, identity and session lifecycle justify platform coupling | Agent code, policy, downstream authorization, cost and service configuration |

Protocols solve interoperability, not operation. OpenAI-compatible endpoints target SDK compatibility; A2A targets remote-agent interoperability; AG-UI targets streamed web-agent interaction and approvals; MCP exposes bounded capabilities; application-native contracts preserve product-specific semantics.

Test disconnect/resume, cancellation, duplicate delivery, tenant-crossing identifiers, expired credentials, payload limits, slow consumers, partial streams, deployments with in-flight work, and storage unavailability.
