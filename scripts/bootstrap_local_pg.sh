#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PGBIN="${PGBIN:-/usr/lib/postgresql/17/bin}"
PGDATA="$ROOT/.runtime/pgdata"
PGSOCKET="$ROOT/.runtime"
PGPORT="${FISHTRACE_PGPORT:-55432}"

mkdir -p "$PGSOCKET"

if [[ ! -f "$PGDATA/PG_VERSION" ]]; then
  "$PGBIN/initdb" -D "$PGDATA" -U fishtrace --auth=trust --encoding=UTF8 --locale=C.utf8 >/dev/null
fi

if ! "$PGBIN/pg_isready" -h "$PGSOCKET" -p "$PGPORT" >/dev/null 2>&1; then
  "$PGBIN/pg_ctl" -D "$PGDATA" \
    -o "-k $PGSOCKET -p $PGPORT -c listen_addresses=127.0.0.1" \
    -l "$ROOT/.runtime/postgres.log" -w start >/dev/null
fi

"$PGBIN/psql" -h "$PGSOCKET" -p "$PGPORT" -U fishtrace -d postgres \
  -c 'CREATE DATABASE fishtrace' >/dev/null 2>&1 || true
"$PGBIN/psql" -h "$PGSOCKET" -p "$PGPORT" -U fishtrace -d postgres \
  -c 'CREATE DATABASE fishtrace_test' >/dev/null 2>&1 || true

"$PGBIN/pg_isready" -h "$PGSOCKET" -p "$PGPORT"
