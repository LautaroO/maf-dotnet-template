# MAF evaluation vs deterministic tests

Do not collapse unit/integration tests and model-quality evaluation into one test strategy.

## Deterministic tests

Use normal .NET tests for code contracts that can be asserted exactly: validators, tools, routing, middleware, persistence, provider adapters, and deterministic executors.

These should remain the default fast CI suite and should not require a live model.

## Agent Framework evaluation

Investigate the evaluation facilities supported by the selected MAF/MEAI stack through [official-source guidance](../../../resources/references/official-sources.md); do not assume particular evaluator types or extension methods.

Use MAF evaluation for behavior that is inherently model-dependent, for example:

- task completion/quality across representative prompts;
- required or forbidden tool usage;
- expected tool-call patterns;
- groundedness/relevance/coherence where a deterministic oracle is not available;
- regressions after changing model, prompt, tools, context strategy, or orchestration.

Prefer local/deterministic evaluation checks when they express the criterion. LLM-as-judge evaluators introduce their own model/provider/cost/variance boundary and should be isolated from the core unit suite.

Provider-hosted evaluators such as Foundry evaluation are integrations, not architectural requirements. Keep evaluation datasets and acceptance criteria provider-neutral where practical.

Pin/version evaluation datasets and judge configuration for reproducible regression gates.
