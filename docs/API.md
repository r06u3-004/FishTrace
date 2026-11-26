# API

Base URL: `http://127.0.0.1:8000` in development. All future business endpoints are versioned under `/api/v1/`.

## Implemented endpoints

### `GET /health`

Liveness probe. Does not touch the database.

```bash
curl -sS http://127.0.0.1:8000/health
```

```json
{"status":"ok"}
```

### `GET /api/v1/health`

Readiness probe. Executes `SELECT 1` against PostgreSQL.

```bash
curl -sS http://127.0.0.1:8000/api/v1/health
```

```json
{"status":"ok","database":"ok"}
```

If the database is unavailable, the request fails with a server error rather than reporting a false healthy state.

## Browser access

CORS origins, methods and headers are explicit allowlists from configuration. Wildcard values are rejected. Credential support is disabled unless `FISHTRACE_CORS_ALLOW_CREDENTIALS` is explicitly enabled. There is no authentication layer yet.

## Engine contract boundary

The engine package exposes typed `EmailAnalysisResult`, `Finding`, `Evidence`, `Indicator`, `AuthenticationResult`, `AttachmentAnalysis` and `RiskAssessment` contracts, plus the `EmailAnalyzer` protocol. These are implemented contracts, not operational analysis endpoints. Future API handlers will map `EmailAnalysisResult` into persistence and response models; they will not parse email or extract indicators themselves.

## Error format (planned contract)

API errors will use `{"code": "...", "message": "...", "detail": ...}` with appropriate HTTP status codes. Validation errors will keep FastAPI/Pydantic field details.

## Planned endpoints

These routes are **not implemented yet**. They are listed to document the intended contract.

| Method | Path | Purpose |
| --- | --- | --- |
| POST | `/api/v1/auth/login` | Start an analyst session |
| POST | `/api/v1/auth/logout` | End an analyst session |
| GET | `/api/v1/auth/me` | Current analyst identity and role |
| GET, POST | `/api/v1/investigations` | List and create investigations |
| GET, PATCH | `/api/v1/investigations/{id}` | Inspect and update an investigation |
| POST | `/api/v1/investigations/{id}/emails` | Import a preserved EML file |
| GET | `/api/v1/emails/{id}` | Parsed email and MIME structure |
| POST | `/api/v1/emails/{id}/analyze` | Run the forensic engine |
| GET | `/api/v1/emails/{id}/auth` | SPF/DKIM/DMARC interpretation |
| GET | `/api/v1/emails/{id}/headers` | SMTP header analysis |
| GET | `/api/v1/emails/{id}/attachments` | Attachment metadata and hashes |
| GET, POST | `/api/v1/campaigns` | Campaign listing and classification |
| GET | `/api/v1/indicators` | Filter indicators by type, value and confidence |
| GET | `/api/v1/activity` | Chronological investigation timeline |
| POST | `/api/v1/reports` | Generate an HTML or JSON report |
| GET | `/api/v1/reports/{id}` | Download a generated report |
| GET, PATCH | `/api/v1/settings` | Application and integration settings |

## Pagination and filtering

Future list endpoints will accept `page` and `page_size` and return `items`, `total`, `page` and `page_size`. Indicator filtering will accept `type`, `value` and `min_confidence`.

## Authentication

Not implemented. Future endpoints will require a session cookie or bearer token and will enforce role-based access. Do not expose the development server to untrusted networks.
