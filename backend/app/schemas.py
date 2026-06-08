"""Pydantic request/response schemas."""

from __future__ import annotations

from datetime import date as Date

from pydantic import BaseModel

from .models import Difficulty, GoalKind, TaskStatus, TaskType, TopicStatus


class GoalCreate(BaseModel):
    name: str
    description: str = ""
    kind: GoalKind = GoalKind.skill
    target_date: Date | None = None
    daily_minutes: int = 120
    priority: int = 1
    color: str = "#2563eb"


class GoalUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    target_date: Date | None = None
    daily_minutes: int | None = None
    priority: int | None = None
    color: str | None = None
    active: bool | None = None


class GoalRead(BaseModel):
    id: int
    name: str
    description: str
    kind: GoalKind
    target_date: Date | None
    daily_minutes: int
    priority: int
    color: str
    active: bool
    days_remaining: int | None = None
    progress_pct: float = 0.0
    status_label: str = "on-track"

    class Config:
        from_attributes = True


class TaskCreate(BaseModel):
    date: Date
    goal_id: int | None = None
    topic_id: int | None = None
    title: str
    description: str = ""
    type: TaskType = TaskType.study
    estimated_minutes: int = 30
    resource_ref: str = ""
    cf_rating: int | None = None
    cf_url: str = ""


class TaskUpdate(BaseModel):
    status: TaskStatus | None = None
    actual_minutes: int | None = None
    notes: str | None = None


class TaskRead(BaseModel):
    id: int
    date: Date
    goal_id: int | None
    topic_id: int | None
    title: str
    description: str
    type: TaskType
    estimated_minutes: int
    actual_minutes: int | None
    status: TaskStatus
    resource_ref: str
    cf_rating: int | None
    cf_url: str
    notes: str
    goal_name: str | None = None
    goal_color: str | None = None

    class Config:
        from_attributes = True


class TopicRead(BaseModel):
    id: int
    level_id: int
    name: str
    order: int
    difficulty: Difficulty
    video_count: int
    videos_watched: int
    problems_assigned: int
    problems_solved: int
    mastery_pct: float
    status: TopicStatus

    class Config:
        from_attributes = True


class LevelRead(BaseModel):
    id: int
    number: int
    name: str
    topics: list[TopicRead] = []
    mastery_pct: float = 0.0

    class Config:
        from_attributes = True


class ProblemResult(BaseModel):
    """Records the result of attempting a single problem on a topic."""

    outcome: str  # "solved_fast" | "solved_slow" | "partial" | "unsolved"


class GenerateRequest(BaseModel):
    date: Date | None = None


class DashboardStats(BaseModel):
    streak: int
    today_total: int
    today_completed: int
    total_tasks_completed: int
    goals: list[GoalRead]
