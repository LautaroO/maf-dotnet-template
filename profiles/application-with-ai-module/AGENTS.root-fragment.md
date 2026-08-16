## AI / Microsoft Agent Framework boundary

This repository contains an AI module implemented with Microsoft Agent Framework (MAF). MAF is not the architecture of the whole application.

Repository-wide dependency rules:

- Domain and core application projects must not depend on `Microsoft.Agents.*`, model-provider SDKs, DevUI, or AI runtime abstractions solely because AI features exist.
- The AI module may depend inward on application/domain contracts and use cases.
- Business rules remain in domain/application code. Agents, tools, and workflow executors orchestrate or adapt those capabilities; they do not become a second application layer.
- Provider-specific SDKs remain inside the AI provider adapter/composition boundary.
- Provider-native response/request types must not leak into domain/application contracts.
- Deterministic behavior stays deterministic C# even when invoked from an agent or workflow.
- AI outputs that affect application behavior must be structured and validated before use.
- Default domain/application tests must run without a live model.

The AI module has its own nested `AGENTS.md`. When editing files under that module, follow those more specific MAF instructions in addition to these repository-wide boundaries.
