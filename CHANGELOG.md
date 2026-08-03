# Changelog

## 2.0.0 - 2026-08-03

Derived from the evolved guidance used in `maf-playground`.

### Added

- DevUI as an explicit local development and debugging surface.
- Clear distinction between CLI harnesses, `HarnessAgent`, sample terminal UX,
  DevUI, and external OTLP dashboards.
- Native workflow registration and visualization guidance.
- DevUI entity discovery, response protocol, graph, tracing, and security checks.
- Dedicated DevUI implementation reference.
- Workflow observability, workflow-as-agent, visualization, hosting, and DevUI
  official source references.
- Project-specific adoption section.
- Reusable `.gitignore`, MIT license, and repository adoption guide.

### Preserved

- Mandatory model-provider and cloud neutrality.
- Separation between deterministic code, tools, agents, and workflows.
- Provider adapter boundaries.
- Reliability, structured output, security, state, observability, and testing rules.

### Excluded from the reusable template

The following `maf-playground` implementation choices were intentionally not
copied:

- Ollama provider implementation.
- PostgreSQL and pgvector retrieval.
- RAG extraction and ingestion.
- Translation workflow implementation.
- CLI application code.
- Docker Compose infrastructure.
- Sample PDF and generation scripts.
- Playground-specific tests and configuration.
