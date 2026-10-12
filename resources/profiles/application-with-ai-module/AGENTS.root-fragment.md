## AI / Microsoft Agent Framework boundary

This repository contains a MAF AI module; MAF is not the architecture of the whole application. Preserve all existing root instructions. Adopting-team rules remain authoritative.

- Domain/application projects do not depend on MAF/provider SDKs merely because AI exists.
- The AI module calls inward application capabilities; it does not own domain rules, ordinary use cases, authorization policy, or core persistence.
- Deterministic behavior remains C#; model output is structured and validated before it drives code or effects.
- Provider SDKs remain in adapters/composition. Hosting model and external protocol are separate decisions.
- Tools enforce validation, authorization, tenancy, limits and occurrence-bound approval; retryable/resumable effects are idempotent.
- Default application tests do not require a live model.

Place MAF-specific instructions in the AI subtree. Review AI changes for architecture, state, security, reliability, provider portability, testing, hosting and operational risk; findings require severity, confidence, evidence/location, impact, correction and MAF version certainty.
