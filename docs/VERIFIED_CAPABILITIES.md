# Verified capabilities

Source reviewed: private framework revision 6bab643. Paths below refer to the private source; source files and history are not included here.

| Capability | Source evidence | Boundary |
| --- | --- | --- |
| Shared executor | registry/loader.py, core/executor.py | Local execution |
| Synthetic registered job | jobs/examples/synthetic.py, connectors/mock.py | Only mock connector registered |
| Validated configuration | registry/client_registry.py, core/models.py | Configuration is not identity authorization |
| Atomic reservation and snapshots | core/run_store.py | RLock and in-memory dictionaries; single process |
| Failed outcome reuse | core/run_store.py, core/executor.py | No automatic retry |
| Default authorization closure | api/dependencies/__init__.py | No tenant-bound identity provider implemented |
| CLI and HTTP interfaces | core/cli.py, api/routes/ | Synchronous execution |

The private implementation document records an earlier 35-test local run. That historical result is not presented as a fresh public test run. Public CI validates only the public example and publication boundary.
