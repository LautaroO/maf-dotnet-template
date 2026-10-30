# State lifetimes, external waits and recovery

Keep conversation history, per-run metadata, workflow coordination, recovery checkpoints and durable product facts distinct. Storage convenience does not determine responsibility.

## Define recovery as a requirement

For a human/external wait, specify identity, authority, deadline, continuation ownership, retention and cancellation. Use explicit request/response or equivalent runtime mechanisms when supported instead of blocking or busy-waiting inside a step.

A checkpoint can preserve execution state; durable execution additionally needs an operating/storage model that can recover work across process loss and long waits. Provider background continuation has its own lifecycle and is not a universal durable runtime. Domain persistence remains separate.

## Compatibility and effects

Define stable logical component identities and concurrency rules. Establish what topology, contracts and stored formats can resume across deployments, and reject incompatible recovery rather than guess. Revalidate authorization when resuming; expire stale approval and deduplicate effects at the application boundary.

Reset state for independent runs and verify isolation for concurrent runs. Check restore ordering, serialization, sensitive data and shared-state behavior in the actual runtime instead of assuming previous instance fields are restored correctly.

## Verification

Use deterministic cases for restart, changed deployment, partial failure, duplicated delivery, cancellation and expired continuation. Verify approvals across every relevant hosting/tool path. Find exact state stores, checkpoint APIs, restore hooks and durable integrations using [official-source investigation](../../../resources/references/official-sources.md); this guide prescribes required behavior, not a particular storage API.
