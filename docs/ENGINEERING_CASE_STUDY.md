# Engineering case study

## Problem and implementation boundary

The project addresses a recurring automation problem: sharing connector and execution logic while allowing each client to enable its own jobs and configuration. The implemented solution is a synchronous Python framework with CLI and FastAPI entry points, typed client configuration, explicit registries and an in-memory run store.

The demonstrated implementation executes a synthetic job through a mock connector. It is not evidence of live customer integrations, n8n workflows or a deployed container platform.

## Execution lifecycle

1. Resolve the client and registered automation; reject missing or disabled entries.
2. Copy and validate parameters, settings, connector compatibility and the optional idempotency key.
3. Fingerprint parameters, job configuration and connector configuration using canonical JSON and SHA-256.
4. Atomically reserve a run scoped to client, automation and key. Reuse a matching reservation; reject changed input under an existing key.
5. Mark the run as running, record correlation fields and resolve credential references from the environment.
6. Instantiate and connect a connector for this run, check job health and execute with an explicit context.
7. Translate the result into a controlled status; convert external exceptions into a public error code.
8. Close the connector in a finally block, record cleanup failures, finalize UTC timestamps and duration, and store a snapshot.

A repeated request can observe the existing running result. It does not launch a second job. There is no automatic retry after a failed result.

## Design decisions and tradeoffs

| Decision | Benefit | Cost or limitation |
| --- | --- | --- |
| One executor behind every transport | Shared behavior and testable business boundary | Synchronous calls occupy the caller |
| IDs mapped to trusted Python registrations | YAML remains data, not an import mechanism | New implementations require code registration |
| Validated client directories | Client-specific configuration without duplicating execution code | Changes require reload at process startup |
| Copies of configuration and stored results | Callers cannot mutate registry/store objects accidentally | Copying adds overhead |
| Per-run connector lifecycle | Limits shared mutable connection state | Connection setup may be repeated |
| RLock-protected reservations in memory | Atomic duplicate suppression inside one process | No cross-worker coordination or restart recovery |
| Failed results retain their key | Prevents an implicit replay after ambiguous effects | Recovery requires deliberate investigation |
| Sanitized external failures | Avoids returning raw exceptions containing secrets | Operators need controlled diagnostic instrumentation |

The input fingerprint covers configuration and credential-reference names, not resolved secret values. Rotating a referenced secret does not constitute a new business execution key. Integration-specific recovery must make that decision explicitly.

## Design for failure

| Failure scenario | Current behavior / evidence | Production follow-up |
| --- | --- | --- |
| Unknown, disabled or malformed configuration | Rejected before job execution | Change review and configuration versioning |
| Two callers submit the same key concurrently | Same run returned; one job invocation | Durable uniqueness across workers |
| Same key, different input | Conflict | Define client-facing conflict and recovery policy |
| A job fails after possible side effects | Failed outcome retained; no automatic retry | Reconcile external state before replay |
| Raw exception contains a sensitive value | Public error code; tested output sanitization | Safe internal diagnostics and access controls |
| Connector close fails | Run marked failed with cleanup error code | Reconcile business effects separately from resource cleanup |
| Process exits during a run | In-memory state is lost | Durable state transitions and interrupted-run recovery |
| Multiple identities access different clients | No identity-to-client authorization implemented | Authenticate and enforce tenant scopes on every route |
| Job blocks indefinitely | No timeout/cancellation mechanism implemented | Bounded workers, deadlines and backpressure |

Configuration separation is not a security boundary between callers. Likewise, process-local duplicate suppression does not guarantee exactly-once behavior in an external system.

## Reading the architecture image

The [workflow image](assets/automations-workflow.png) communicates activation, configuration, coordination, execution, connectors and results. CLI and API are implemented entry points; YAML is configuration rather than executable code. The actual executor resolves the registries and calls jobs.

n8n activation, live REST connectors, Docker images and container registries are integration/distribution options. They have not been verified as delivered in this revision. The image is preserved as supplied, with this status explanation outside the asset.

## Next production gates

Persist execution state with atomic reservations and a recovery protocol; define business idempotency with each external system; bind authenticated identities to authorized tenants; add timeouts, capacity controls and retention; then validate integration behavior and deployment observability in a controlled environment.

These gates follow from the failure model. They are not implied to be complete by a successful local test run.
