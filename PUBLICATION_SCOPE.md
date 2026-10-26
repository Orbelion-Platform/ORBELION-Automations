# Publication scope

Allowed: README.md, PUBLICATION_SCOPE.md, SECURITY.md, .gitignore, docs/VERIFIED_CAPABILITIES.md, docs/MAINTENANCE.md, examples/synthetic_job.py, tests/test_synthetic_job.py, scripts/validate_publication.py and .github/workflows/validate.yml.

Excluded: private source history, customer configurations, legacy integrations, operational YAML, credentials, environment files, tenant identifiers, production endpoints, deployment configuration, logs and screenshots.

The example is independently written using synthetic data. No runtime dependency, submodule, second remote or automatic mirror connects this public repository to the private application.

Publication validation enforces the exact file allowlist and scans text for common credential patterns. It is defense in depth, not proof that all possible sensitive information can be detected. Review every public diff manually.
