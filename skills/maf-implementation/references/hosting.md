# Runtime operation and client protocols

Make two separate decisions: who operates the runtime, and how clients communicate. Embedded execution, self-hosting, recoverable execution infrastructure and managed services have different ownership costs. Product-native APIs and interoperability protocols solve client boundaries; protocol familiarity is not a hosting decision.

## Assign operational ownership

Identify authentication, resource authorization, tenant/session partitioning, storage, secrets, streaming/disconnect behavior, continuation lifecycle, recovery, scaling, health and incident response. Externally supplied session/task identifiers are untrusted; logical routing or agent selection cannot authorize access.

Use request/service lifetimes deliberately and stable logical identities when persisted conversations or recovery require them. Distinguish transport representation from typed application contracts, including partial streaming output and terminal events.

A development UI or in-memory example store is not evidence of production durability or route protection. Independently check every execution route and adapter rather than infer protection from a secured UI or discovery endpoint.

## Validate the selected integration

Test isolation, lifetimes, cancellation/disconnect, errors, limits, continuation and recovery as applicable. Hosted operation is intentional provider/cloud coupling at an adapter boundary, not an assumption for reusable components.

Find precise registrations, endpoint/protocol support, authentication defaults and persistence behavior through [official-source investigation](../../../resources/references/official-sources.md) and the selected host's documentation. Do not maintain package maturity promises here.
