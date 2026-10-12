---
name: maf-hosting
description: Design or review how Microsoft Agent Framework agents and workflows are operated and exposed in .NET, separating managed versus self-hosted runtime choices from OpenAI-compatible, A2A, AG-UI, MCP, or application-native protocols. Use for authentication, streaming, sessions, deployment, scaling, and durability boundaries.
---

# MAF hosting

Read `../../resources/references/official-sources.md`, `references/hosting-selection.md`, and the [versioned capability matrix](../../resources/docs/capabilities/maf-dotnet-1.18.md).

Make two independent decisions:

1. operation model: embedded/in-process, self-hosted, durable self-hosted, or managed Foundry Hosted Agents;
2. client boundary: application-native API, OpenAI-compatible endpoint, A2A, AG-UI, MCP, or another explicitly supported protocol.

Do not choose a host from protocol familiarity or assume a protocol provides authentication, authorization, tenancy, persistence, or durability. For every design identify the owner of identity, request limits, session lookup, tenant partitioning, streaming disconnects, continuation tokens, checkpoints, secrets, deployment, scaling, health, telemetry, and incident recovery.

Verify installed packages and maturity. .NET self-hosting and protocol packages may be prerelease even when the underlying service is GA. Treat protocol IDs as untrusted and authorize every session/task/checkpoint lookup.
