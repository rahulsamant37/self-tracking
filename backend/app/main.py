"""FastAPI application entrypoint."""

from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session

from .database import create_db_and_tables, engine
from .routers import dashboard, goals, tasks, tle
from .seed import seed_all


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    with Session(engine) as session:
        seed_all(session)
    yield


app = FastAPI(title="Goal Progress Tracker API", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(goals.router)
app.include_router(tasks.router)
app.include_router(tle.router)
app.include_router(dashboard.router)


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
