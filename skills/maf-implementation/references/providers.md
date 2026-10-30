# Replaceable providers and capability boundaries

A provider supplies model/service capabilities; it should not become the architecture center. Isolate SDK construction, credentials, model/deployment selection and provider options at composition/infrastructure boundaries.

Use existing neutral MAF/MEAI abstractions when they represent required behavior. `IChatClient` and agent abstractions are useful concepts to investigate; do not create a custom port merely to duplicate them. A genuinely missing application capability can justify an explicit adapter/contract.

## Compare requirements with supported capabilities

Check tool calling, structured output, modalities, streaming fidelity, hosted capabilities, continuation/history and relevant hosting/protocol behavior. Provider neutrality does not promise feature parity. Choose a clear fallback or fail before a consequential operation begins.

Keep configuration typed and secrets external. Translate failures where application contracts need it and assign transient retries to one owner; invalid semantic output is a different failure class.

## Source interpretation

Separate a sample's MAF pattern from provider authentication, cloud setup and shortcuts. A sample using Azure, Foundry or OpenAI is not a requirement to couple reusable agents/tools/workflows to that service. Test adapters independently and keep live-provider compatibility/evaluation opt-in.

Consult [official MAF source and matching package evidence](../../../resources/references/official-sources.md) for concrete construction, capabilities and supported fallbacks; use provider documentation for the selected adapter's own contract.
