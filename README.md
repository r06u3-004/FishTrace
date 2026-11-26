# FishTrace

Phishing threat intelligence and email forensics platform for SOC analysts and DFIR investigators.

**Status: Milestone 1 foundation complete; pre-Milestone 2 security and engine contracts complete.** The repository contains the project structure, an independent forensic engine with typed contracts, the SQLAlchemy schema and Alembic migrations, a versioned FastAPI health endpoint, a Typer CLI foundation, and a React/Vite application shell with the official visual tokens. Forensic analysis, investigations, IOC enrichment, attachments and reporting are **not yet implemented** and are planned for milestones 2–8.

## What works today

- Independent `fishtrace_engine` package with typed, serializable forensic contracts and explicit engine exceptions.
- Forensic contracts for email results, findings, evidence, indicators, authentication, attachments and explainable risk.
- `EmailAnalyzer` protocol and `AnalysisRequest` contract for future backend/CLI integration; no analyzer is implemented yet.
- FastAPI app with `GET /health` and `GET /api/v1/health`, explicit CORS allowlists, and strict environment-name validation.
- 15-table PostgreSQL schema with indexes, foreign keys and two Alembic migrations.
- Test database guards that require an explicit opt-in before any destructive schema reset.
- Local, unprivileged PostgreSQL 17 bootstrap script (no sudo).
- `fishtrace` CLI with `version` and `status` commands reusing the engine package.
- React 18 + TypeScript + Vite + Tailwind shell using the specified dark palette, Inter and JetBrains Mono, Lucide icons, and TanStack Query.
- Python and frontend test suites, Ruff, Bandit and mypy checks.

## Layout

```
engine/       independent forensic analysis package and typed contracts
backend/      FastAPI application, SQLAlchemy models, Alembic migrations, tests
cli/          Typer command line interface
frontend/     React/TypeScript application
docs/         architecture, security, API, user and deployment guides
scripts/      local PostgreSQL bootstrap
samples/      synthetic email samples (added in milestone 2)
reports/      generated reports (added in milestone 7)
```

## Quick start (validated on Kali Linux 2025.3)

```bash
cd /home/rogue/Bureau/MyTools/FishTrace
cp .env.example .env
python3.13 -m venv backend/.venv
backend/.venv/bin/python -m pip install -e ./engine -e './backend[dev]' -e ./cli
./scripts/bootstrap_local_pg.sh
cd backend && ../backend/.venv/bin/alembic upgrade head && cd ..
cd backend && ./.venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000
```

The frontend is bootstrapped locally without a global npm installation:

```bash
cd frontend
corepack enable --install-directory ./.bin npm
./.bin/npm install
./.bin/npm run dev
```

Open `http://127.0.0.1:5173`. The API is at `http://127.0.0.1:8000`.

## Verification

```bash
backend/.venv/bin/ruff check --no-cache engine backend cli
backend/.venv/bin/ruff format --check --no-cache engine backend cli
backend/.venv/bin/bandit -q -r backend/app engine/fishtrace_engine cli/fishtrace_cli
backend/.venv/bin/mypy --config-file backend/pyproject.toml backend/app engine/fishtrace_engine cli/fishtrace_cli
cd engine && ../backend/.venv/bin/pytest -q -p no:cacheprovider && cd ..
cd backend && ./.venv/bin/pytest -q -p no:cacheprovider && cd ..
cd frontend && ./.bin/npm test && ./.bin/npm run build && cd ..
```

Normal backend tests never drop a schema. A destructive test reset requires `FISHTRACE_ALLOW_TEST_DB_RESET` to be explicitly set to a truthy value and a database name ending in `_test`.

## Documentation

- [Architecture](docs/ARCHITECTURE.md)
- [Security](docs/SECURITY.md)
- [API](docs/API.md)
- [User Guide](docs/USER_GUIDE.md)
- [Deployment Guide](docs/DEPLOYMENT_GUIDE.md)
- [Changelog](CHANGELOG.md)

Licensed under the MIT License.
