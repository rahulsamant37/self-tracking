"""Dashboard summary endpoint."""

from __future__ import annotations

from datetime import date

from fastapi import APIRouter, Depends
from sqlmodel import Session, func, select

from ..database import get_session
from ..models import Goal, Task, TaskStatus
from ..schemas import DashboardStats
from .goals import _to_read

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("", response_model=DashboardStats)
def get_dashboard(session: Session = Depends(get_session)) -> DashboardStats:
    from ..services.progress import current_streak

    today = date.today()
    today_tasks = session.exec(select(Task).where(Task.date == today)).all()
    today_completed = sum(1 for t in today_tasks if t.status == TaskStatus.completed)

    total_completed = session.exec(
        select(func.count()).select_from(Task).where(Task.status == TaskStatus.completed)
    ).one()

    goals = session.exec(select(Goal).order_by(Goal.priority)).all()

    return DashboardStats(
        streak=current_streak(session, today),
        today_total=len(today_tasks),
        today_completed=today_completed,
        total_tasks_completed=int(total_completed),
        goals=[_to_read(session, g) for g in goals],
    )
