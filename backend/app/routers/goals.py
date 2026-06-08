"""Goal CRUD endpoints."""

from __future__ import annotations

from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from ..database import get_session
from ..models import Goal
from ..schemas import GoalCreate, GoalRead, GoalUpdate
from ..services.progress import days_remaining, goal_progress_pct, status_label

router = APIRouter(prefix="/api/goals", tags=["goals"])


def _to_read(session: Session, goal: Goal) -> GoalRead:
    progress = goal_progress_pct(session, goal)
    return GoalRead(
        id=goal.id,
        name=goal.name,
        description=goal.description,
        kind=goal.kind,
        target_date=goal.target_date,
        daily_minutes=goal.daily_minutes,
        priority=goal.priority,
        color=goal.color,
        active=goal.active,
        days_remaining=days_remaining(goal),
        progress_pct=progress,
        status_label=status_label(goal, progress),
    )


@router.get("", response_model=list[GoalRead])
def list_goals(session: Session = Depends(get_session)) -> list[GoalRead]:
    goals = session.exec(select(Goal).order_by(Goal.priority)).all()
    return [_to_read(session, g) for g in goals]


@router.post("", response_model=GoalRead, status_code=201)
def create_goal(payload: GoalCreate, session: Session = Depends(get_session)) -> GoalRead:
    if payload.target_date is not None and payload.target_date <= date.today():
        raise HTTPException(status_code=422, detail="target_date must be in the future")
    goal = Goal(**payload.model_dump())
    session.add(goal)
    session.commit()
    session.refresh(goal)
    return _to_read(session, goal)


@router.get("/{goal_id}", response_model=GoalRead)
def get_goal(goal_id: int, session: Session = Depends(get_session)) -> GoalRead:
    goal = session.get(Goal, goal_id)
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    return _to_read(session, goal)


@router.patch("/{goal_id}", response_model=GoalRead)
def update_goal(
    goal_id: int, payload: GoalUpdate, session: Session = Depends(get_session)
) -> GoalRead:
    goal = session.get(Goal, goal_id)
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    data = payload.model_dump(exclude_unset=True)
    if data.get("target_date") and data["target_date"] <= date.today():
        raise HTTPException(status_code=422, detail="target_date must be in the future")
    for key, value in data.items():
        setattr(goal, key, value)
    session.add(goal)
    session.commit()
    session.refresh(goal)
    return _to_read(session, goal)


@router.delete("/{goal_id}", status_code=204)
def delete_goal(goal_id: int, session: Session = Depends(get_session)) -> None:
    goal = session.get(Goal, goal_id)
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    session.delete(goal)
    session.commit()
