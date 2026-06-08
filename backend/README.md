# Backend — Goal Progress Tracker API

FastAPI + SQLModel (SQLite) service.

## Setup

```bash
uv venv && source .venv/bin/activate
uv pip install -e ".[dev]"
uvicorn app.main:app --reload --port 8000
```

Interactive docs: `http://localhost:8000/docs`.

## Key endpoints

| Method | Path                              | Description                          |
| ------ | --------------------------------- | ------------------------------------ |
| GET    | `/api/dashboard`                  | Streak + per-goal progress summary   |
| GET/POST | `/api/goals`                    | List / create goals                  |
| GET    | `/api/tasks?task_date=YYYY-MM-DD` | Tasks for a date                     |
| POST   | `/api/tasks/generate`             | Generate a daily plan (idempotent)   |
| PATCH  | `/api/tasks/{id}`                 | Update task status / time / notes    |
| GET    | `/api/tle/levels`                 | TLE levels with topics + mastery     |
| POST   | `/api/tle/topics/{id}/result`     | Log a problem outcome (mastery)      |
| POST   | `/api/tle/topics/{id}/watch`      | Increment videos watched             |

## Tests & lint

```bash
ruff check .
pytest
```

Configure the database via `DATABASE_URL` (defaults to `sqlite:///./goal_tracker.db`).
