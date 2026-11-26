# Changelog

All notable changes to FishTrace are recorded here.

## 0.2.0 — 2026-11-26 — Pre-Milestone 2 hardening and engine contracts

### Added

- Typed forensic contracts in `fishtrace_engine.models`: `EmailAnalysisResult`, `EmailMetadata`, `Finding`, `Evidence`, `Indicator`, `AuthenticationResult`, `AttachmentAnalysis`, `RiskAssessment` and supporting enums.
- `AnalysisRequest` and `EmailAnalyzer` protocol in `fishtrace_engine.services` as designed integration interfaces; no analyzers are implemented.
- Engine exception hierarchy and JSON-compatible `SerializableModel.to_dict()` helpers.
- Test database guard module with explicit `FISHTRACE_ALLOW_TEST_DB_RESET` opt-in and `_test` database-name validation.
- Focused engine contract tests and backend tests for configuration, CORS, environment-name validation and database guards.
- Alembic revision `c3f5a1d9b742_security_constraints` adding uniqueness on `(indicator_id, provider, queried_at)` for `intel_results`.

### Changed

- `.env` is restricted to mode `600`; `.env.example` uses safe examples with debug disabled and no password value in the database URL.
- Backend settings reject unknown `FISHTRACE_*` names, wildcard CORS values and debug in production; CORS methods and headers are explicit allowlists and credentials are disabled by default.
- Backend test setup no longer performs unconditional destructive schema cleanup.
- `integration_configs.encrypted_api_key` is documented as reserved for future authenticated encryption and currently holds no credentials.
- Architecture and security documentation distinguish implemented contracts from designed interfaces and planned analyzers.

### Validation performed

- `ruff check` and `ruff format --check` clean on 56 files.
- `mypy` clean on 45 source files; `bandit -q -r` clean.
- `pip check` reported no broken requirements.
- Engine contract tests: 11 passed.
- Backend tests: 29 passed, with one upstream Starlette TestClient deprecation warning.
- Alembic upgrade to `c3f5a1d9b742` applied; `alembic check` reported no new upgrade operations; the unique constraint is present in the database.
- Health endpoints returned `200` and expected JSON; CLI `version` and `status` commands still work.
- Docker Compose configuration validated with a locally supplied `POSTGRES_PASSWORD`.

### Not included yet

Email parsing, header analysis, SPF/DKIM/DMARC verification, IOC extraction, attachment analysis, threat-intel enrichment, reporting, authentication and frontend workflow changes.

## 0.1.0 — 2026-11-26 — Milestone 1: foundation

### Added

- Project workspace at `/home/rogue/Bureau/MyTools/FishTrace` with separated engine, backend, CLI and frontend packages.
- Python 3.13 virtual environment and exact dependency lockfile in `backend/requirements.lock.txt`.
- `fishtrace_engine` package skeleton with forensic library dependencies pinned.
- FastAPI application with liveness and database-backed health endpoints under `/api/v1/`.
- Pydantic settings with environment-file loading, path resolution and secret-key validation.
- SQLAlchemy models for users, investigations, emails, campaigns, indicators, sightings, attachments, analysis results, auth results, intel results, analyst notes, activity events, reports and integration configurations.
- Alembic baseline migration `f49482bc6da8_initial_schema`, validated with upgrade, downgrade and `alembic check`.
- Local unprivileged PostgreSQL 17 bootstrap script and Docker Compose configuration (configuration validated only).
- Typer CLI with `version` and `status` commands.
- React 18 + TypeScript + Vite application shell with Tailwind design tokens, locally bundled Inter/JetBrains Mono fonts, Lucide icons and TanStack Query.
- Unit, integration and API tests for configuration, schema and health endpoints; frontend component test.
- Documentation for architecture, security, API, user workflows and deployment.

### Validation performed

- `ruff check` and `ruff format` clean.
- `bandit -q -r` clean.
- `mypy` clean on backend, engine and CLI sources.
- `pytest`: 9 tests passed.
- Frontend `npm test`, `npm run build` and `npm run typecheck` passed.
- Live `/health` and `/api/v1/health` responses verified with `uvicorn`.
- Frontend dev server HTTP 200 verified with Vite.

### Not included yet

Email parsing, header analysis, SPF/DKIM/DMARC verification, IOC extraction, attachment analysis, threat-intel enrichment, investigations, campaigns, reports and authentication.
