"""One-time Postgres bootstrap: create the app role and database.

Your PostgreSQL server must already be running. This connects as a superuser
(default: ``postgres``) and idempotently creates:

    role      study         (login, password 'study')
    database  study_platform  (owned by study)

Usage (PowerShell):
    $env:PG_SUPERUSER_PASSWORD = "your-postgres-password"
    python setup_db.py

Usage (bash):
    PG_SUPERUSER_PASSWORD="your-postgres-password" python setup_db.py

Optional overrides via env: PG_SUPERUSER (default 'postgres'),
PG_HOST (default 'localhost'), PG_PORT (default '5432'),
APP_DB (default 'study_platform'), APP_USER (default 'study'),
APP_PASSWORD (default 'study').
"""
import os
import sys

try:
    import psycopg
    from psycopg import sql
except ModuleNotFoundError:
    sys.exit(
        "psycopg is not installed. Run:  pip install -r requirements-postgres.txt"
    )


def main() -> None:
    superuser = os.environ.get("PG_SUPERUSER", "postgres")
    password = os.environ.get("PG_SUPERUSER_PASSWORD")
    host = os.environ.get("PG_HOST", "localhost")
    port = os.environ.get("PG_PORT", "5432")

    app_db = os.environ.get("APP_DB", "study_platform")
    app_user = os.environ.get("APP_USER", "study")
    app_password = os.environ.get("APP_PASSWORD", "study")

    if not password:
        sys.exit(
            "Set PG_SUPERUSER_PASSWORD to your Postgres superuser password first.\n"
            "  PowerShell:  $env:PG_SUPERUSER_PASSWORD = \"...\"\n"
            "  bash:        PG_SUPERUSER_PASSWORD=... python setup_db.py"
        )

    dsn = (
        f"host={host} port={port} user={superuser} "
        f"password={password} dbname=postgres"
    )
    print(f"Connecting to {host}:{port} as {superuser}…")
    with psycopg.connect(dsn, autocommit=True) as conn:
        cur = conn.cursor()

        # Role. Utility statements (CREATE ROLE/DATABASE) can't take bind
        # parameters, so compose them safely with psycopg.sql — Identifier
        # quotes the name, Literal quotes the password.
        cur.execute("SELECT 1 FROM pg_roles WHERE rolname = %s", (app_user,))
        if cur.fetchone():
            print(f"Role '{app_user}' already exists.")
        else:
            cur.execute(
                sql.SQL("CREATE ROLE {} LOGIN PASSWORD {}").format(
                    sql.Identifier(app_user), sql.Literal(app_password)
                )
            )
            print(f"Created role '{app_user}'.")

        # Database
        cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (app_db,))
        if cur.fetchone():
            print(f"Database '{app_db}' already exists.")
        else:
            cur.execute(
                sql.SQL("CREATE DATABASE {} OWNER {}").format(
                    sql.Identifier(app_db), sql.Identifier(app_user)
                )
            )
            print(f"Created database '{app_db}' owned by '{app_user}'.")

    print(
        "\nDone. Set backend/.env to:\n"
        f"  DATABASE_URL=postgresql+psycopg://{app_user}:{app_password}"
        f"@{host}:{port}/{app_db}\n"
        "Then run:  python seed.py"
    )


if __name__ == "__main__":
    main()
