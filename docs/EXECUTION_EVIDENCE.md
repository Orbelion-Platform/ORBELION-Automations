# Execution evidence

## Private framework validation

Date: 2026-10-26. Source revision: `6bab643197e8625ccd2803e24049de35cf2c93ee`. Python: 3.13.14.

Command run from the private checkout:

```powershell
.\.venv\Scripts\python.exe -m pytest -q --basetemp=.pytest_cache/portfolio-evidence --tb=short
```

Observed result: **35 passed, 1 warning in 0.98s**.

The warning is Starlette's deprecation of using httpx with TestClient. It did not fail this run; the test transport dependency remains a maintenance item. This used the existing local environment, not a fresh installation across all supported dependency versions.

Only this aggregate result and generic test references are published. Private source, raw logs, environment details and customer configuration are excluded.

## What was exercised

Paths and test names below refer to the private source, not files available in this public repository.

| Concern | Test reference | Observed assertion |
| --- | --- | --- |
| Client configuration and snapshots | tests/test_registry.py::test_clients_and_copy_isolation | Client configuration copies do not mutate the registry |
| Logical run separation | tests/test_executor.py::test_success_and_isolation | Same key across clients produces distinct runs |
| Duplicate YAML keys | tests/test_registry.py::test_duplicate_yaml_keys | Ambiguous configuration rejected |
| Invalid registration/configuration | tests/test_registry.py::test_invalid_registry | Unknown jobs, connector references and settings rejected |
| Concurrent duplicate submission | tests/test_executor.py::test_concurrent_idempotency | One job invocation; second caller sees same running run |
| Failed outcome reuse | tests/test_executor.py::test_failure_retained_and_idempotency | Failed run reused; changed input conflicts |
| Secret-like exception and cleanup | tests/test_executor.py::test_sanitized_failure_and_cleanup | Connector closed; sensitive marker absent from result and stderr |
| Cleanup failure | tests/test_executor.py::test_cleanup_failure | Failed status and controlled cleanup error |
| API execution and history | tests/test_health.py::test_api_endpoints | Run result, duplicate reuse and filtered history |
| Default API closure | tests/test_health.py::test_auth_fail_closed | Health stays available; operational calls return 503 |
| API request rejection | tests/test_health.py::test_api_errors | Invalid payload rejected without echoing sensitive marker |

These tests establish local behavior with synthetic fixtures. They do not prove authenticated tenant isolation, external API behavior, crash recovery, distributed idempotency, load capacity or deployment readiness. TestClient is an in-process HTTP test interface; it is not evidence of a deployed service.

## Public reproducibility

Anyone with Python 3.11+ can run from this public checkout:

```sh
python examples/synthetic_job.py
python -m unittest discover -s tests -v
python scripts/validate_publication.py
```

The public suite contains three test methods for the independent bounded-count example. It does not rerun the 35 private framework tests. The publication validator enforces a named file allowlist, text credential patterns and the approved PNG's signature and SHA-256.

GitHub Actions runs the public checks on push and pull request. A workflow file alone is not evidence that its latest run succeeded; consult the repository's Actions results.

## Visual evidence

The approved workflow PNG is included unchanged at [assets/automations-workflow.png](assets/automations-workflow.png). It is an architecture illustration, not an execution trace. Its roadmap elements are explained in the [case study](ENGINEERING_CASE_STUDY.md).
