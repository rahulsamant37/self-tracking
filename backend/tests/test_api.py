"""Smoke and behavior tests for the Goal Progress Tracker API."""

from __future__ import annotations

import os
import tempfile

import pytest


@pytest.fixture()
def client():
    # Use an isolated temp database per test session.
    db_fd, db_path = tempfile.mkstemp(suffix=".db")
    os.close(db_fd)
    os.environ["DATABASE_URL"] = f"sqlite:///{db_path}"

    # Import after setting DATABASE_URL so the engine picks it up.
    import importlib

    from app import database, main

    importlib.reload(database)
    importlib.reload(main)

    from fastapi.testclient import TestClient

    with TestClient(main.app) as c:
        yield c

    os.remove(db_path)


def test_health(client):
    assert client.get("/api/health").json() == {"status": "ok"}


def test_seeded_goals_and_levels(client):
    goals = client.get("/api/goals").json()
    names = {g["name"] for g in goals}
    assert {"CAT 2026", "GATE 2027", "DSA (TLE Eliminator)"} <= names

    levels = client.get("/api/tle/levels").json()
    assert len(levels) == 4
    assert sum(len(lvl["topics"]) for lvl in levels) > 0


def test_generate_tasks_is_idempotent(client):
    first = client.post("/api/tasks/generate", json={}).json()
    assert len(first) > 0
    second = client.post("/api/tasks/generate", json={}).json()
    assert {t["id"] for t in first} == {t["id"] for t in second}


def test_mastery_progression(client):
    levels = client.get("/api/tle/levels").json()
    topic = levels[0]["topics"][0]
    tid = topic["id"]

    # 10 fast solves -> 100% mastery, marked mastered, batch satisfied.
    last = None
    for _ in range(10):
        last = client.post(f"/api/tle/topics/{tid}/result", json={"outcome": "solved_fast"}).json()
    assert last["mastery_pct"] == 100.0
    assert last["status"] == "mastered"


def test_low_mastery_assigns_more_problems(client):
    levels = client.get("/api/tle/levels").json()
    topic = levels[0]["topics"][0]
    tid = topic["id"]

    # First attempt starts the topic and assigns the initial batch.
    started = client.post(f"/api/tle/topics/{tid}/result", json={"outcome": "unsolved"}).json()
    initial_batch = started["problems_assigned"]
    assert initial_batch > 0

    # Fail the remaining problems in the initial batch -> assign 10 more.
    last = started
    for _ in range(initial_batch - 1):
        last = client.post(f"/api/tle/topics/{tid}/result", json={"outcome": "unsolved"}).json()
    assert last["mastery_pct"] < 70
    assert last["problems_assigned"] == initial_batch + 10


def test_create_goal_rejects_past_date(client):
    resp = client.post("/api/goals", json={"name": "Past", "target_date": "2000-01-01"})
    assert resp.status_code == 422


def test_task_completion_updates_dashboard(client):
    tasks = client.post("/api/tasks/generate", json={}).json()
    tid = tasks[0]["id"]
    client.patch(f"/api/tasks/{tid}", json={"status": "completed", "actual_minutes": 30})
    dash = client.get("/api/dashboard").json()
    assert dash["today_completed"] >= 1
    assert dash["streak"] >= 1
