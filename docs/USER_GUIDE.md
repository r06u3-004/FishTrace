# User Guide

## What FishTrace does

FishTrace is an email forensics and phishing intelligence workspace. Once complete, it will preserve original emails, parse MIME structure, inspect SMTP headers, evaluate authentication results, extract indicators, analyze attachments safely, enrich indicators through optional threat-intel providers and generate forensic reports.

**Current release is milestone 1.** The interface shell, database and API foundation are usable; investigation and analysis workflows are not available yet.

## Accessing the application

After starting the backend and frontend as described in the [Deployment Guide](DEPLOYMENT_GUIDE.md):

- Interface: `http://127.0.0.1:5173`
- API: `http://127.0.0.1:8000`
- Health check: `http://127.0.0.1:8000/health`

The interface opens in dark mode with a fixed left rail. Sections `01`–`07` represent Overview, Campaigns, Investigations, IOC Intelligence, Email, Forensics and Reports. Settings sits at the bottom of the rail. Navigation becomes active as the corresponding workflows are implemented.

## Current command line usage

The CLI and web application share the `fishtrace_engine` package. In milestone 1, only foundation commands exist:

```bash
backend/.venv/bin/fishtrace version
backend/.venv/bin/fishtrace status
```

Expected output confirms the installed CLI and engine versions, and that analysis commands are still pending.

## Importing an email (planned)

The planned flow is: open Investigations, create an investigation, choose an `.eml` file, then review the preserved copy and its SHA-256 hash before running analysis. Original bytes will never be modified.

## Interpreting SPF, DKIM and DMARC (planned)

The engine will distinguish four states, and the interface will display them as plain language rather than relying on the presence of a header:

- **Verified** — independent verification succeeded against published DNS records.
- **Failed** — verification was attempted and did not succeed.
- **Unavailable** — no usable record or signature was present.
- **Inconclusive** — verification could not be completed, for example because DNS resolution was restricted or the message was altered in transit.

Alignment will be reported separately. A passing SPF record for a different domain does not prove the visible `From` domain is legitimate, and a `Authentication-Results` header alone is not independent verification.

## Reviewing extracted IOCs (planned)

Indicators will be grouped by IPv4, IPv6, domain, URL, email address, MD5, SHA1 and SHA256. Each entry will retain the original context, the investigation it came from, first/last seen timestamps and any enrichment results. Values will be rendered in monospace type.

## Analyzing attachments (planned)

Attachments will be identified by MIME type, hashed with MD5, SHA1 and SHA256, and checked against suspicious extension and type rules. Files are never executed and are not opened as URLs.

## Threat Intelligence integrations (planned)

VirusTotal, AbuseIPDB and URLhaus adapters will be optional and disabled without API keys. Enrichment will be serverside, network-restricted and never automatically open extracted URLs.

## Generating reports (planned)

Reports will be generated as HTML or JSON and will include investigation metadata, email information, authentication results, header analysis, IOCs, attachment details, intelligence results, findings and recommendations.

## Current limitations

There is no login, no import form, no analyzer, no IOC database view and no report generation in this release. Do not rely on milestone 1 for casework.

## Troubleshooting

| Symptom | Resolution |
| --- | --- |
| `npm: command not found` | Use the project-local shim: from `frontend/`, run `corepack enable --install-directory ./.bin npm` and call `./.bin/npm`. |
| API health check fails | Start PostgreSQL with `./scripts/bootstrap_local_pg.sh` and apply migrations with `alembic upgrade head` from `backend/`. |
| Application cannot load settings | Copy `.env.example` to `.env` and set `FISHTRACE_SECRET_KEY` to at least 16 characters. |
| Port already in use | Choose another port for `uvicorn --port` or Vite `--port` and update `FISHTRACE_CORS_ORIGINS` if the frontend origin changes. |
