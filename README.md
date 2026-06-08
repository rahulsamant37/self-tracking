# Goal Progress Tracker

A daily progress tracking app that manages multiple concurrent goals (CAT, GATE, DSA),
generates daily tasks, and drives an **adaptive topic-mastery engine** for the
TLE Eliminator DSA course.

> **Status:** Phase 1 MVP. See [the roadmap](#roadmap) for what's next.

## Features (Phase 1 MVP)

- **Multi-goal management** — create exam / skill / DSA goals with deadlines, daily time
  budgets, priority, and color. Seeded with CAT 2026, GATE 2027, and DSA (TLE Eliminator).
- **TLE Eliminator course tracking** — all 4 levels and their topics, with per-topic
  difficulty, video counts, and mastery.
- **Daily task generation** — one click builds a balanced plan across all active goals:
  video lectures + course problems + a daily Codeforces problem (rating scaled to level).
- **Task completion tracking** — check off tasks; daily/total counts and streaks update.
- **Progress dashboard** — per-goal progress %, days remaining, on-track / at-risk / behind
  status, and streak.
- **Adaptive mastery engine** — log each problem outcome (fast / slow / partial / unsolved);
  the system scores mastery and keeps assigning more problems until a topic is mastered
  (≥90%), per the spec's `+10 / +5` algorithm.

## Tech stack

| Layer    | Tech                                              |
| -------- | ------------------------------------------------- |
| Frontend | React + Vite + TypeScript + Tailwind CSS + Router |
| Backend  | FastAPI + SQLModel (SQLite)                        |

## Project layout

```
goal-progress-tracker/
├── backend/            FastAPI app, SQLModel models, services, tests
│   └── app/
│       ├── routers/    goals, tasks, tle, dashboard
│       └── services/   mastery, task_generation, progress
└── frontend/           React + Vite app
    └── src/
        ├── pages/      Dashboard, Today, Dsa, Goals
        └── components/ Layout, ProgressBar
```

## Running locally

### Backend

```bash
cd backend
uv venv && source .venv/bin/activate
uv pip install -e ".[dev]"
uvicorn app.main:app --reload --port 8000
```

The API runs at `http://localhost:8000` (docs at `/docs`). A SQLite DB is created and
seeded on first start.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The dev server runs at `http://localhost:5173` and proxies `/api` to the backend.
To point at a non-proxied backend, set `VITE_API_BASE` (e.g. `VITE_API_BASE=https://api.example.com`).

## Tests & checks

```bash
# backend
cd backend && source .venv/bin/activate && ruff check . && pytest

# frontend
cd frontend && npm run lint && npm run build
```

## Roadmap

- **Phase 2** — Codeforces API integration, richer analytics, problem timer.
- **Phase 3** — CAT/GATE syllabus DB and mock-test engine.
- **Phase 4** — AI insights & doubt-solving (free models).
- **Phase 5** — Spaced repetition, YouTube ingestion, gamification, PWA.
