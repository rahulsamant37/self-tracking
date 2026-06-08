"""SQLModel database models for the Goal Progress Tracker."""

from __future__ import annotations

from datetime import UTC, date, datetime
from enum import StrEnum

from sqlmodel import Field, SQLModel


class GoalKind(StrEnum):
    exam = "exam"
    skill = "skill"
    dsa = "dsa"


class Difficulty(StrEnum):
    easy = "easy"
    medium = "medium"
    hard = "hard"


class TopicStatus(StrEnum):
    not_started = "not_started"
    in_progress = "in_progress"
    mastered = "mastered"


class TaskType(StrEnum):
    video = "video"
    problem = "problem"
    codeforces = "codeforces"
    revision = "revision"
    mock = "mock"
    study = "study"


class TaskStatus(StrEnum):
    pending = "pending"
    completed = "completed"
    partial = "partial"
    deferred = "deferred"


class Goal(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    description: str = ""
    kind: GoalKind = GoalKind.skill
    target_date: date | None = None
    daily_minutes: int = 120
    priority: int = 1  # 1 = highest
    color: str = "#2563eb"
    active: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class TLELevel(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    number: int  # 1-4
    name: str


class TLETopic(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    level_id: int = Field(foreign_key="tlelevel.id")
    name: str
    order: int = 0
    difficulty: Difficulty = Difficulty.medium
    video_count: int = 3
    videos_watched: int = 0
    problems_assigned: int = 0
    problems_solved: int = 0
    points_earned: int = 0
    points_possible: int = 0
    mastery_pct: float = 0.0
    status: TopicStatus = TopicStatus.not_started


class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    date: date
    goal_id: int | None = Field(default=None, foreign_key="goal.id")
    topic_id: int | None = Field(default=None, foreign_key="tletopic.id")
    title: str
    description: str = ""
    type: TaskType = TaskType.study
    estimated_minutes: int = 30
    actual_minutes: int | None = None
    status: TaskStatus = TaskStatus.pending
    resource_ref: str = ""
    cf_rating: int | None = None
    cf_url: str = ""
    notes: str = ""
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    completed_at: datetime | None = None
