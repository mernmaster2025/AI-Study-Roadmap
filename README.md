# AI Study Platform

A hands-on learning platform for a 12-phase AI roadmap (Python Fundamentals →
Production AI): sign in, read a lesson, write Python in the browser, run it
against hidden test cases, and watch your progress update.

## What's built

| Area | Status |
| --- | --- |
| **Full 12-phase curriculum — 106 lessons, 289 auto-graded challenges** | ✅ |
| **Quizzes — 633 questions (MC + fill-blank), instant grading + explanations** | ✅ |
| Auth: dev-login **and** GitHub/Google OAuth (via Authlib) | ✅ |
| Phases → Lessons → Challenges → Quizzes content model + modular seed | ✅ |
| In-browser code editor with syntax highlighting | ✅ |
| Server-side Python execution + test grading (approx float compare) | ✅ |
| Progress tracking (per-phase %, challenges solved, quizzes passed) | ✅ |
| PostgreSQL (via psycopg 3) with SQLite fallback | ✅ |
| **Alembic migrations** (schema versioned, verified in sync) | ✅ |
| Projects, Community, Certificates | ⏳ scaffolded to grow into |

### The 12 phases

| # | Phase (lessons) | # | Phase (lessons) |
| --- | --- | --- | --- |
| 1 | Python Fundamentals (16) | 7 | Natural Language Processing (6) |
| 2 | Computer Science Basics (11) | 8 | Large Language Models (9) |
| 3 | Mathematics for AI (13) | 9 | AI Engineering (8) |
| 4 | Python for Data Science (5) | 10 | MLOps (7) |
| 5 | Machine Learning (9) | 11 | AI Agents (5) |
| 6 | Deep Learning (9) | 12 | Production AI (8) |

Each **topic** is its own deeply-explained lesson (~600–800 words with `## Key
ideas`, a step-by-step example walk-through, `## Common pitfalls`, and `## Why it
matters for AI`), plus **1–3 auto-graded challenges** of increasing difficulty
and a **5–6 question quiz**. Even the infra/ops phases (9–12) carry stdlib "logic"
challenges (rate limiters, LRU cache, batching, drift scores, …). All **289**
challenge reference solutions are verified to pass their own tests.

> The curriculum was authored by a 12-agent workflow (one per phase) and lives in
> [backend/seed_data/curriculum.json](backend/seed_data/curriculum.json).

## Tech stack

- **Frontend:** Next.js 14 (App Router) · TypeScript · Tailwind CSS
- **Backend:** FastAPI · SQLAlchemy · **PostgreSQL** (psycopg 3), SQLite fallback
- **Code execution:** sandboxed Python subprocess (see the security note below)

## Prerequisites

- Python 3.11+  (tested on 3.14)
- Node.js 18+   (tested on 26)

## Run it locally

Two terminals. **Backend first** (it seeds the DB and serves the API).

### 1. Backend → http://localhost:8000

```bash
cd backend
python -m venv .venv
# Windows:  .venv\Scripts\activate       macOS/Linux:  source .venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-postgres.txt   # psycopg 3 driver
```

**Point at a database.** Copy `.env.example` to `.env`. The default
`DATABASE_URL` uses Postgres:

```
DATABASE_URL=postgresql+psycopg://study:study@localhost:5432/study_platform
```

Create that role + database once (needs your Postgres superuser password):

```bash
# PowerShell:  $env:PG_SUPERUSER_PASSWORD = "your-postgres-password"
PG_SUPERUSER_PASSWORD="your-postgres-password" python setup_db.py
```

> Prefer zero setup? Set `DATABASE_URL=sqlite:///./study_platform.db` in `.env`
> instead and skip `setup_db.py` — everything else is identical.

**Create the schema, seed, and run:**

```bash
alembic upgrade head               # create all tables (schema is Alembic-managed)
python seed.py                     # load 12 phases, 106 lessons, 289 challenges, 633 quiz Qs
uvicorn app.main:app --reload      # API on :8000
```

**API docs:** open **`http://localhost:8000/scalar`** — the primary reference UI
([Scalar](https://scalar.com), a modern Swagger alternative with a built-in
request playground). Swagger UI (`/docs`) and ReDoc (`/redoc`) are also served
from the same OpenAPI schema.

### 2. Frontend → http://localhost:3000

```bash
cd frontend
npm install
cp .env.local.example .env.local   # points at http://localhost:8000
npm run dev
```

Open http://localhost:3000 → **Start learning** → open Phase 1 → a lesson →
edit the code → **Run & Submit**. The first run auto-signs-in a demo user so
progress is saved.

## Project layout

```
backend/
  app/
    main.py            # FastAPI app + CORS + session middleware + Scalar docs
    config.py          # env-driven settings
    database.py        # SQLAlchemy engine/session
    models.py          # User, Phase, Lesson, Challenge, progress, submissions
    schemas.py         # Pydantic request/response models
    auth.py            # backend JWT mint/verify
    oauth.py           # Authlib registry (GitHub/Google)
    progress.py        # progress recomputation (challenges + quizzes)
    routers/           # auth, oauth, content, execute, quizzes, progress
    services/
      code_executor.py # runs + grades submissions   <-- SECURITY-SENSITIVE
  alembic/             # migrations (env.py + versions/0001, 0002)
  alembic.ini
  seed_data/           # curriculum.json (all content) + loader
  seed.py              # walks the curriculum and writes rows (idempotent)
  setup_db.py          # one-time Postgres role + database bootstrap
  requirements.txt
  requirements-postgres.txt

frontend/
  app/                 # landing, dashboard, phase, lesson, quiz, auth pages
  components/          # CodeEditor, Quiz, ProgressBar, Navbar
  lib/                 # api.ts (typed client), auth.tsx (context)
```

## ⚠️ Security note on code execution

`backend/app/services/code_executor.py` runs untrusted learner code in a
subprocess with only a wall-clock timeout (Python `-I` isolated mode). That is
fine for **local development**, but it is **not a real sandbox** — the code can
touch the filesystem and network. Before exposing this to real users, run each
submission inside a locked-down boundary (Docker container with no network +
dropped capabilities + memory cap, nsjail/firejail, or move execution to the
browser with Pyodide). The grading contract stays the same; only the execution
environment changes.

## How the challenge grading works

Each challenge stores `test_cases` as `{"call": "add(2, 3)", "expected": "5"}`.
The executor runs the learner's code, then evaluates each `call` and compares it
to `eval(expected)` — using an **approximate** comparison for floats (and
recursively into lists/tuples/dicts), so `mean`, `sigmoid`, `softmax`, and
cosine-similarity challenges grade robustly. Using a call expression (rather than
a fixed `main()` signature) lets every challenge name its own function.

## Database migrations (Alembic)

The schema is managed by Alembic (`backend/alembic/`), not `create_all`.

```bash
alembic upgrade head        # apply all migrations
alembic downgrade -1        # roll back one
alembic history             # list revisions
alembic check               # assert models match the DB (CI-friendly)
alembic revision -m "..."   # start a new migration after changing models.py
```

Revisions so far: `0001` initial schema · `0002` quiz tables. After editing
`models.py`, create a new revision and `alembic upgrade head`.

> Reseeding regenerates content with fresh UUIDs, so `seed.py` also clears
> dependent user rows (submissions, quiz attempts, progress). User **accounts**
> are preserved.

## Authentication & OAuth

The API is guarded by a backend-issued JWT. Two ways to obtain one:

- **Dev-login** (`POST /api/auth/dev-login`) — no password; always available.
- **GitHub / Google OAuth** (Authlib) — set the client credentials in
  `backend/.env` (`GITHUB_CLIENT_ID/SECRET`, `GOOGLE_CLIENT_ID/SECRET`). The
  flow: the SPA hits `/api/auth/login/{provider}` → provider → backend
  `/api/auth/callback/{provider}` upserts the user, mints the JWT, and redirects
  to the frontend `/auth/callback?token=…`.

`GET /api/auth/providers` reports which providers are configured; the sign-in
page shows only those. Unconfigured providers return `503` and dev-login still
works, so the app runs with zero OAuth setup.

Callback URLs to register with the providers:
`http://localhost:8000/api/auth/callback/github` and `.../google`.

## Adding & editing content

All content lives in one file: **`backend/seed_data/curriculum.json`** — a list
of 12 phase objects, each with lessons that carry `content_markdown`, `examples`,
`challenges`, and an inline `quiz` (schema docstring in `seed_data/__init__.py`).

To add or change content, edit `curriculum.json` and re-run `python seed.py`.
Every challenge ships a `solution_code`; keep the invariant that the solution
passes its own `test_cases` (all 289 are verified to). The repo includes the
verify/repair pass used to enforce that after generation.

## Extending the platform

- **Projects:** add `Project` / `UserProjectSubmission` models next to the
  existing ones in `models.py`, a migration, and a router mirroring
  `challenges` + `execute`.
- **Certificates / community:** new tables + routers following the same pattern.
- **Supabase / hosted Postgres:** point `DATABASE_URL` at the hosted instance —
  no code changes; run `alembic upgrade head` there. (`setup_db.py` is only for
  creating a local role/database.)

## Deployment sketch

- **Frontend →** Vercel (`frontend/`), set `NEXT_PUBLIC_API_URL`.
- **Backend →** Railway/Render (`backend/`), set `DATABASE_URL`, `JWT_SECRET`,
  `FRONTEND_ORIGIN`.
- **Database →** Supabase Postgres.
