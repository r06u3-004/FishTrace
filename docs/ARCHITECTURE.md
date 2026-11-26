# Architecture

## Status

This document describes the implemented architecture, the designed integration interfaces for Milestone 2, and the features that remain planned. Items marked **designed** have typed contracts only; they are not operational analyzers.

## Layers

### 1. Forensic engine (`engine/fishtrace_engine`)

**Implemented:** independent Python package, version `0.1.0`, with pinned dependencies for DNS (`dnspython`), DKIM (`dkimpy`), HTTP enrichment (`httpx`), file identification (`python-magic`) and reporting (`Jinja2`). The package has no FastAPI, SQLAlchemy, React or database-model imports.

Implemented contracts:

| Module | Contracts |
| --- | --- |
| `models/email.py` | `EmailAnalysisResult`, `EmailMetadata`, `AnalysisStatus` |
| `models/findings.py` | `Finding`, `FindingCategory`, `FindingSeverity` |
| `models/evidence.py` | `Evidence`, `EvidenceType` |
| `models/indicators.py` | `Indicator`, `IndicatorType` |
| `models/authentication.py` | `AuthenticationResult`, `AuthStatus` |
| `models/attachments.py` | `AttachmentAnalysis`, `AttachmentAnalysisStatus` |
| `models/risk.py` | `RiskAssessment`, `RiskLevel` |
| `services/protocols.py` | `AnalysisRequest`, `EmailAnalyzer` |
| `exceptions.py` | Engine-specific exception hierarchy |

Contracts are frozen dataclasses with timezone-aware timestamps, explicit enums, validation and `to_dict()` serialization. Severity and confidence are separate concepts. Indicator normalization is stored separately from the original value. Authentication uses explicit states such as `NOT_CHECKED`, `NONE`, `INDETERMINATE` and `FAIL`; missing data is never coerced to failure. `RiskAssessment` carries reasons, contributing findings and recommendations without implementing scoring rules.

**Designed, not implemented:** `EmailAnalyzer.analyze(request: AnalysisRequest) -> EmailAnalysisResult`. This is a protocol for future analyzers; no parser, extractor or enrichment adapter exists yet.

**Planned:** EML/MIME parsing, header analysis, SPF/DKIM/DMARC verification, IOC extraction, attachment hashing and safety flags, modular intel adapters with SSRF protection, transparent risk scoring, and HTML/JSON report rendering.

### 2. Backend (`backend/app`)

**Implemented:**

- `app/core/config.py`: environment-driven settings, explicit environment-name validation, project-root path resolution, strict secret validation, and explicit CORS allowlists for origins, methods and headers.
- `app/db/base.py` and `app/db/session.py`: declarative base and SQLAlchemy session factory.
- `app/models/`: full relational schema, including uniqueness on `(type, normalized_value)` for `indicators` and `(indicator_id, provider, queried_at)` for `intel_results`.
- `app/api/v1/router.py`: versioned health endpoint.
- `app/main.py`: FastAPI application, CORS from settings, liveness endpoint.
- `alembic/`: baseline migration and a follow-up uniqueness migration.

**Designed, not implemented:** backend adapters will call an `EmailAnalyzer`, map `EmailAnalysisResult` into ORM records, persist evidence with integrity hashes, and emit activity events. The backend must not implement email parsing, header interpretation or IOC extraction itself.

**Planned:** auth, investigation/email/campaign/IOC/activity/report/settings endpoints, evidence storage service, activity recording, ORM repositories, rate limiting and security headers.

### 3. CLI (`cli/fishtrace_cli`)

**Implemented:** Typer app with `version` and `status`, installed as `fishtrace`.

**Designed, not implemented:** future commands will construct `AnalysisRequest`, call the same `EmailAnalyzer` used by the backend, and serialize `EmailAnalysisResult`. The CLI must not implement its own parsing or IOC extraction.

**Planned:** `analyze`, `headers`, `auth`, `ioc`, `attachments`, `intel` and `report` commands with JSON-capable output.

### 4. Frontend (`frontend`)

**Implemented in Milestone 1 and unchanged by this preparation:** React 18, TypeScript, Vite, Tailwind CSS, locally bundled fonts, Lucide icons, TanStack Query provider and the primary navigation shell.

**Planned:** all analyst sections, structured tables, drawers, filters, import flow, confirmation dialogs and report downloads.

## Engine integration design

```text
EML Input
    |
    v
AnalysisRequest(raw_eml, filename)
    |
    v
FishTrace Forensic Engine -> EmailAnalyzer.analyze()
    |
    v
EmailAnalysisResult
    |
    +------> FastAPI Backend  (map to ORM records and responses)
    |
    +------> Typer CLI        (render analyst-facing output)
    |
    +------> Report Generation (future milestone)
```

The engine is the single source of forensic analysis logic. Backend and CLI consumers receive the same typed result object; they must not duplicate parsing, normalization, authentication interpretation or IOC extraction. Report generation will consume `EmailAnalysisResult.to_dict()` or the typed object directly.

## Data flow (planned)

```text
EML upload
  -> original bytes preserved with SHA-256 in backend/evidence
  -> engine parsing / header / auth / IOC / attachment analysis
  -> EmailAnalysisResult with findings, evidence and risk explanation
  -> PostgreSQL records + activity events
  -> API responses -> UI tables and detail views
  -> HTML/JSON report generation
```

## Database

Fifteen domain tables are created, plus `alembic_version`:

| Domain | Tables |
| --- | --- |
| Identity | `users` |
| Investigations | `investigations`, `analyst_notes`, `activity_events`, `reports` |
| Email evidence | `emails`, `attachments` |
| Campaigns | `campaigns`, `campaign_investigations` |
| Intelligence | `indicators`, `indicator_sightings`, `intel_results` |
| Analysis | `analysis_results`, `auth_results` |
| Configuration | `integration_configs` |

Indexes cover common filters (status, severity, dates, hashes, indicator type/value, foreign keys). `indicators` enforces uniqueness on `(type, normalized_value)`; `intel_results` enforces uniqueness on `(indicator_id, provider, queried_at)`. The `integration_configs.encrypted_api_key` column is reserved for future authenticated encryption and currently holds no credentials.

## Test database isolation

Test setup derives a `_test` database name from the configured database, validates that the name follows the test convention, and never drops a schema unless `FISHTRACE_ALLOW_TEST_DB_RESET` is explicitly set to a truthy value. Reserved names such as `production`, `development` and their `_test` forms are rejected. Normal test runs only create missing tables and are non-destructive.

## Extension points

- Intel providers will implement a common adapter interface and be enabled by configuration; the platform works without API keys.
- Report templates will live in the engine and consume `EmailAnalysisResult`.
- Finding producers will append structured `Finding` records; risk assessment will aggregate them rather than rely on a single heuristic.
- Integration credentials require an authenticated-encryption key and rotation design before any provider adapter is implemented.

## Milestone status

| Milestone | Status |
| --- | --- |
| 1 Architecture and foundation | Complete |
| Pre-2 Security remediation and engine contracts | Complete |
| 2 Email parsing and core forensics | Planned |
| 3 IOC extraction and attachments | Planned |
| 4 Threat intelligence | Planned |
| 5 API and database integration | Foundation only |
| 6 Frontend and complete UI | Shell only |
| 7 Reporting, CLI and workflows | Foundation only |
| 8 Security, docs, deployment | In progress |
