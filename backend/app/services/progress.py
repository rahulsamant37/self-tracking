"""Goal progress and streak computation helpers."""

from __future__ import annotations

from datetime import date, timedelta

from sqlmodel import Session, select

from ..models import Goal, GoalKind, Task, TaskStatus, TLETopic


def days_remaining(goal: Goal, today: date | None = None) -> int | None:
    if goal.target_date is None:
        return None
    today = today or date.today()
    return (goal.target_date - today).days


def goal_progress_pct(session: Session, goal: Goal) -> float:
    if goal.kind == GoalKind.dsa:
        topics = session.exec(select(TLETopic)).all()
        if not topics:
            return 0.0
        return round(sum(t.mastery_pct for t in topics) / len(topics), 1)

    tasks = session.exec(select(Task).where(Task.goal_id == goal.id)).all()
    if not tasks:
        return 0.0
    done = sum(1 for t in tasks if t.status == TaskStatus.completed)
    return round(done / len(tasks) * 100, 1)


def status_label(goal: Goal, progress_pct: float, today: date | None = None) -> str:
    today = today or date.today()
    if goal.target_date is None:
        return "on-track"
    created = goal.created_at.date()
    total_days = max((goal.target_date - created).days, 1)
    elapsed = max((today - created).days, 0)
    elapsed_pct = min(elapsed / total_days * 100, 100)
    if progress_pct >= elapsed_pct - 5:
        return "on-track"
    if progress_pct >= elapsed_pct - 20:
        return "at-risk"
    return "behind"


def current_streak(session: Session, today: date | None = None) -> int:
    """Consecutive days (ending today or yesterday) with >=1 completed task."""
    today = today or date.today()
    completed = session.exec(
        select(Task).where(Task.status == TaskStatus.completed)
    ).all()
    days_with_completion = {t.date for t in completed}
    if not days_with_completion:
        return 0

    streak = 0
    cursor = today
    if today not in days_with_completion:
        cursor = today - timedelta(days=1)
    while cursor in days_with_completion:
        streak += 1
        cursor -= timedelta(days=1)
    return streak
