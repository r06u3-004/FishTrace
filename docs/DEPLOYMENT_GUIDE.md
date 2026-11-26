# Deployment Guide

This guide covers the validated development deployment on Kali Linux and the planned production posture. Commands listed under "Validated setup" were executed successfully on the target environment. Production commands are intentionally omitted until the corresponding milestones are validated.

## System requirements

Validated environment:

- Kali GNU/Linux Rolling 2025.3, kernel `6.12.38+kali-amd64`.
- Python 3.13.7 (3.14.8 is also installed but 3.13 is used for wheel compatibility).
- Node.js 20.19.2, npm bootstrapped locally via Corepack 0.24.0 with `npm@10.9.2`.
- PostgreSQL 17.5 client and server binaries installed at `/usr/lib/postgresql/17/bin`.
- Git 2.53.0, Docker 28.5.2 with Compose plugin.
- 51 GB free disk, 3.8 GB RAM plus 4 GB swap.

## Validated setup

Work from the project root:

```bash
cd /home/rogue/Bureau/MyTools/FishTrace
cp .env.example .env
chmod 600 .env
```

Copying the example creates a local `.env` with a placeholder secret key and debug disabled. Replace `FISHTRACE_SECRET_KEY` with a long random value before any shared deployment. Never print or commit its value.

### Python environment

```bash
python3.13 -m venv backend/.venv
backend/.venv/bin/python -m pip install --upgrade pip setuptools wheel
backend/.venv/bin/python -m pip install -e ./engine -e './backend[dev]' -e ./cli
```

The virtual environment contains the engine, backend and CLI as editable packages, so all three share one contract implementation. Exact resolved versions are pinned in `backend/requirements.lock.txt`. No packages are installed globally and no sudo is used.

### Frontend environment

The system has Node.js but no `npm` executable. Corepack provides a project-local shim:

```bash
cd frontend
corepack enable --install-directory ./.bin npm
./.bin/npm install
```

`frontend/package.json` declares `npm@10.9.2`, which supports Node 20. Dependencies are pinned in `frontend/package-lock.json`.

### PostgreSQL

The installed PostgreSQL service is not active. A dedicated cluster is initialized under `.runtime/pgdata` and run as the current user without sudo:

```bash
cd /home/rogue/Bureau/MyTools/FishTrace
./scripts/bootstrap_local_pg.sh
```

The script creates two databases, `fishtrace` and `fishtrace_test`, listens on `127.0.0.1:55432` and uses a Unix socket in `.runtime/`. It uses trust authentication for local development only; do not expose it beyond loopback. The bootstrap script reads the reserved variable `FISHTRACE_PGPORT` when a non-default port is needed.

An alternative Compose configuration is provided. It requires a locally supplied `POSTGRES_PASSWORD`; no password is stored in the file:

```bash
docker compose config -q
```

Starting the Compose stack is not exercised in milestone 1.

### Migrations

```bash
cd backend
../backend/.venv/bin/alembic upgrade head
../backend/.venv/bin/alembic current
```

Two revisions are applied:

- `f49482bc6da8_initial_schema` creates all 15 domain tables.
- `c3f5a1d9b742_security_constraints` adds uniqueness on `(indicator_id, provider, queried_at)` for `intel_results`. It checks for duplicate rows first and refuses to proceed if duplicates exist; it does not delete data.

### Backend startup

```bash
cd backend
./.venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Verify from another terminal:

```bash
curl -sS http://127.0.0.1:8000/health
curl -sS http://127.0.0.1:8000/api/v1/health
```

### Frontend startup

```bash
cd frontend
./.bin/npm run dev
```

The interface is served at `http://127.0.0.1:5173`. A production bundle is written to `frontend/dist/` by `./.bin/npm run build`.

## Environment variables

| Variable | Purpose |
| --- | --- |
| `FISHTRACE_ENVIRONMENT` | Deployment label (`development` by default). |
| `FISHTRACE_DEBUG` | FastAPI debug flag; defaults to false and is rejected in production. |
| `FISHTRACE_SECRET_KEY` | Application secret; minimum 16 characters and required at startup. |
| `FISHTRACE_DATABASE_URL` | SQLAlchemy connection string for the main database. |
| `FISHTRACE_CORS_ORIGINS` | Comma-separated trusted browser origins; wildcards are rejected. |
| `FISHTRACE_CORS_ALLOW_CREDENTIALS` | Credential support; false unless explicitly enabled. |
| `FISHTRACE_CORS_ALLOW_METHODS` | Explicit HTTP method allowlist. |
| `FISHTRACE_CORS_ALLOW_HEADERS` | Explicit HTTP header allowlist. |
| `FISHTRACE_UPLOAD_MAX_BYTES` | Configured upload ceiling for the future import endpoint. |
| `FISHTRACE_EVIDENCE_DIR` | Directory for preserved original evidence. |
| `FISHTRACE_REPORT_DIR` | Directory for generated reports. |
| `FISHTRACE_ACCESS_TOKEN_TTL_MINUTES` | Configured session lifetime for future authentication. |

Reserved variables consumed outside backend settings:

| Variable | Purpose |
| --- | --- |
| `FISHTRACE_PGPORT` | Port override for `scripts/bootstrap_local_pg.sh`. |
| `FISHTRACE_ALLOW_TEST_DB_RESET` | Explicit opt-in for destructive test-schema reset; never set in development or production. |
| `POSTGRES_PASSWORD` | Required by Docker Compose for the database container; supply locally and never commit. |

Paths may be absolute or relative to the project root. Unknown `FISHTRACE_*` names are rejected by settings validation.

## Test database safety

Normal backend tests derive a database name ending in `_test`, validate the name, create missing tables and perform no destructive teardown. Schema destruction requires all of:

- a valid `_test` database name,
- no reserved production/development name,
- `FISHTRACE_ALLOW_TEST_DB_RESET` set to `1`, `true`, `yes` or `on`.

Do not set the reset variable while using the development database configuration.

## Verification commands

```bash
backend/.venv/bin/ruff check --no-cache engine backend cli
backend/.venv/bin/ruff format --check --no-cache engine backend cli
backend/.venv/bin/bandit -q -r backend/app engine/fishtrace_engine cli/fishtrace_cli
backend/.venv/bin/mypy --config-file backend/pyproject.toml backend/app engine/fishtrace_engine cli/fishtrace_cli
backend/.venv/bin/pip check
cd engine && ../backend/.venv/bin/pytest -q -p no:cacheprovider && cd ..
cd backend && ./.venv/bin/pytest -q -p no:cacheprovider && ./.venv/bin/alembic check && cd ..
cd frontend && ./.bin/npm test && ./.bin/npm run build && cd ..
```

Do not run the destructive test reset unless you intentionally want to recreate the test schema.

## Production deployment (planned)

Production will require authentication, TLS, restricted database credentials, a non-trust PostgreSQL configuration, secret management outside the working tree, security headers and a process supervisor. Do not reuse the development trust authentication or the generated local database password.

A future `FISHTRACE_INTEGRATION_ENCRYPTION_KEY` setting is planned for authenticated encryption of provider credentials. It is not implemented and must not be configured as if it were active.

### Reverse proxy and HTTPS (planned)

A reverse proxy should terminate TLS, forward `/api/` to the FastAPI process and serve the built frontend assets, with strict CORS limited to the public application origin. Automated certificate renewal and HSTS should be configured before exposure to analysts.

### Backup and recovery (planned)

Evidence files and the PostgreSQL cluster must be backed up together to preserve referential integrity and evidence hashes. Restore procedures and retention policy will be documented when the evidence service is implemented.

### Updating FishTrace (planned)

Updates should apply Alembic migrations forward only after a verified backup, reinstall pinned dependencies from the lockfiles, rebuild the frontend and rerun the full verification suite.

## Troubleshooting

| Symptom | Resolution |
| --- | --- |
| `npm` not found | Use `frontend/.bin/npm` created by Corepack, or rerun `corepack enable --install-directory ./.bin npm` from `frontend/`. |
| PostgreSQL not responding | Run `./scripts/bootstrap_local_pg.sh` again; it starts the existing cluster if present. |
| Migration connection refused | Confirm the cluster is listening on `127.0.0.1:55432` and that `FISHTRACE_DATABASE_URL` points to `fishtrace`. |
| Settings validation error | Ensure `.env` exists, contains only known `FISHTRACE_*` names, and that `FISHTRACE_SECRET_KEY` has at least 16 characters. |
| Tests refuse to reset schema | Leave `FISHTRACE_ALLOW_TEST_DB_RESET` unset for normal runs; set it only for an intentional `_test` database reset. |
| Frontend renders but API calls fail | Confirm CORS origins include the frontend URL and that the backend is running. |
