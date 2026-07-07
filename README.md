# AI Study Platform

A hands-on learning platform for a 12-phase AI roadmap (Python Fundamentals →
Production AI). This repository currently contains a **working Phase 1 vertical
slice**: sign in, read a lesson, write Python in the browser, run it against
hidden test cases, and watch your progress update.

## What's built (Phase 1 slice)

| Area | Status |
| --- | --- |
| Auth (dev login → JWT; NextAuth seam ready) | ✅ |
| Phases → Lessons → Challenges content model + seed | ✅ (Phase 1: 2 lessons, 2 challenges) |
| In-browser code editor with syntax highlighting | ✅ |
| Server-side Python execution + test grading | ✅ |
| Progress tracking (per-phase %, challenges solved) | ✅ |
| Quizzes, Projects, Community, OAuth, Certificates | ⏳ scaffolded to grow into |

## Tech stack

- **Frontend:** Next.js 14 (App Router) · TypeScript · Tailwind CSS
- **Backend:** FastAPI · SQLAlchemy · SQLite (swap to Postgres/Supabase via `DATABASE_URL`)
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

python seed.py                     # load Phase 1 content
uvicorn app.main:app --reload      # API on :8000  (docs at /docs)
```

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
    main.py            # FastAPI app + CORS + table creation
    config.py          # env-driven settings
    database.py        # SQLAlchemy engine/session
    models.py          # User, Phase, Lesson, Challenge, progress, submissions
    schemas.py         # Pydantic request/response models
    auth.py            # JWT mint/verify (dev-login for now)
    progress.py        # progress recomputation
    routers/           # auth, content, execute, progress
    services/
      code_executor.py # runs + grades submissions   <-- SECURITY-SENSITIVE
  seed.py              # Phase 1 content + demo data
  requirements.txt

frontend/
  app/                 # landing, dashboard, phase, lesson pages (App Router)
  components/          # CodeEditor, ProgressBar, Navbar
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
to `eval(expected)`. Using a call expression (rather than a fixed `main()`
signature) lets every challenge name its own function.

## Extending beyond Phase 1

- **More content:** add phases/lessons/challenges in `backend/seed.py`.
- **Quizzes & Projects:** add the models from the spec next to the existing ones
  in `models.py`, mirror the router pattern in `routers/`.
- **Real OAuth:** swap `auth.py`'s dev-login for GitHub/Google via NextAuth on
  the frontend; the JWT shape the backend expects is unchanged.
- **Postgres/Supabase:** set `DATABASE_URL` and
  `pip install -r requirements-postgres.txt` (or `docker compose up -d` for a
  local Postgres).

## Deployment sketch

- **Frontend →** Vercel (`frontend/`), set `NEXT_PUBLIC_API_URL`.
- **Backend →** Railway/Render (`backend/`), set `DATABASE_URL`, `JWT_SECRET`,
  `FRONTEND_ORIGIN`.
- **Database →** Supabase Postgres.
