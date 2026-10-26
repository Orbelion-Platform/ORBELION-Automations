# Publication scope

Allowed text files:

- README.md, PUBLICATION_SCOPE.md, SECURITY.md and .gitignore.
- docs/VERIFIED_CAPABILITIES.md, docs/MAINTENANCE.md, docs/ENGINEERING_CASE_STUDY.md and docs/EXECUTION_EVIDENCE.md.
- examples/synthetic_job.py and tests/test_synthetic_job.py.
- scripts/validate_publication.py and .github/workflows/validate.yml.

Approved binary asset: docs/assets/automations-workflow.png, supplied by the owner and visually reviewed as an architecture diagram. It is preserved byte-for-byte. SHA-256: `183bad7978c4cc25c3d2ca2b532ca406894f83c81f437b9e0389b3a284f7fb85`.

Excluded: private source history, customer configurations, legacy integrations, operational YAML, credentials, environment files, tenant identifiers, production endpoints, deployment configuration, raw logs and additional screenshots.

The example is independently written using synthetic data. Documentation includes generic private source references and an aggregate local test result, not private source files. No runtime dependency, submodule, second remote or automatic mirror connects this public repository to the private application.

Publication validation enforces the exact file allowlist, scans text for common credential patterns and checks the approved PNG signature/hash. It cannot discover all sensitive content or interpret image pixels; the image requires visual review. Review every public diff manually.
