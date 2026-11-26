# Security

## Scope

This document describes the security posture of the current milestone and the controls that will be enforced as forensic features land. Nothing here should be read as a claim that unimplemented features are active.

## Threat model

- EML files are hostile input: malformed MIME, header injection, oversized messages and deceptive authentication headers.
- Attachments are untrusted binaries and must never be executed.
- Extracted URLs and domains may point to attacker-controlled or internal infrastructure.
- API keys for threat-intel providers are sensitive and must never be logged or returned by the API.
- Analysts' notes and evidence are investigation records requiring integrity and access control.

## Implemented controls

- **Project isolation:** all source, runtime data and dependencies live under the FishTrace directory; Python packages are installed in `backend/.venv`; npm is bootstrapped into `frontend/.bin`. No global or sudo installs were used.
- **Environment file:** `.env` is gitignored and restricted to mode `600`. `.env.example` contains only safe development examples, with debug disabled and no real credential values.
- **Configuration validation:** `FISHTRACE_SECRET_KEY` must be at least 16 characters; validation errors never include the supplied value. Unknown `FISHTRACE_*` names are rejected, with explicit reserved names for the PostgreSQL bootstrap port and the test reset guard. Debug is disabled by default and rejected in production environments.
- **CORS:** origins, methods and headers come from explicit allowlists. Wildcard origins, methods and headers are rejected. Credential support is disabled unless explicitly configured.
- **Test database isolation:** the test database name is derived from the configured database and must end in `_test`. Reserved production/development names are rejected. Schema destruction requires `FISHTRACE_ALLOW_TEST_DB_RESET` to be explicitly truthy; normal tests only create missing tables and have no destructive teardown.
- **Persistence:** SQLAlchemy ORM only; no string-built SQL in application code. The single raw SQL statement in the application is the constant `SELECT 1` used by the health endpoint. `indicators` and `intel_results` have explicit uniqueness constraints.
- **Dependencies:** exact versions are recorded in `backend/requirements.lock.txt` and `frontend/package-lock.json`; Ruff, Bandit and mypy run clean.
- **Database:** the local PostgreSQL cluster listens only on loopback and a project-local Unix socket; no system service changes were made. The cluster uses development-only trust authentication.
- **No network side effects:** the engine contracts do not open extracted URLs, fetch remote content or execute attachments. No attachment or enrichment code exists yet.

## Designed controls, not yet implemented

- **Integration credential encryption:** `integration_configs.encrypted_api_key` is reserved for ciphertext only and currently contains no credentials. Provider keys require authenticated encryption (AES-GCM or an equivalent AEAD mode) using a 32-byte key supplied through a future `FISHTRACE_INTEGRATION_ENCRYPTION_KEY` setting. Keys must be versioned, non-logging and never returned by API responses. Rotation requires re-wrapping stored credentials under a new key version and retiring the old key only after verification. No encryption implementation is present because key management is not yet established.
- **SSRF protection:** resolve hostnames before connection, reject private/loopback/link-local/metadata addresses and non-HTTP(S) schemes, disable redirects, restrict ports, apply timeouts and response-size caps, and revalidate the resolved address at connection time.
- **Evidence integrity:** preserve original EML bytes with random storage names, record SHA-256, and keep source/context for every extracted indicator.
- **Authentication and authorization:** password hashing with Argon2, session tokens with configured TTL, role checks on investigation actions, and login rate limiting.
- **Attachment safety:** hash and identify MIME types without execution, flag dangerous extensions, store attachments outside the web root, and keep path-traversal-safe downloads.
- **DNS and authentication analysis:** bounded DNS lookups and timeouts; distinct verified, failed, unavailable, inconclusive and not-applicable states. A present authentication header will never be treated as independent verification.
- **Reporting:** autoescape all untrusted values rendered into HTML reports.
- **Interface:** confirmation dialogs for destructive analyst actions, clear loading/error states and no automatic navigation to external URLs.

## Known limitations

Milestone 1 and this pre-Milestone 2 hardening step have **no authentication**, no upload endpoint, no security headers, no rate limiting, no integration encryption implementation and no forensic analyzers. The local PostgreSQL cluster uses trust authentication for development convenience; it must not be exposed beyond loopback. Do not place this repository state on an untrusted network.

## Reporting security issues

Open an issue in the project repository with reproduction steps and affected version. Do not include real private email content or live credentials.
