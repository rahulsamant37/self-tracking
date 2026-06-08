"""Task endpoints: list, generate, complete."""

from __future__ import annotations

from datetime import UTC, date, datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from ..database import get_session
from ..models import Goal, Task, TaskStatus
from ..schemas import GenerateRequest, TaskCreate, TaskRead, TaskUpdate
from ..services.task_generation import generate_for_date

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


def _to_read(session: Session, task: Task) -> TaskRead:
    goal = session.get(Goal, task.goal_id) if task.goal_id else None
    return TaskRead(
        id=task.id,
        date=task.date,
        goal_id=task.goal_id,
        topic_id=task.topic_id,
        title=task.title,
        description=task.description,
        type=task.type,
        estimated_minutes=task.estimated_minutes,
        actual_minutes=task.actual_minutes,
        status=task.status,
        resource_ref=task.resource_ref,
        cf_rating=task.cf_rating,
        cf_url=task.cf_url,
        notes=task.notes,
        goal_name=goal.name if goal else None,
        goal_color=goal.color if goal else None,
    )


@router.get("", response_model=list[TaskRead])
def list_tasks(
    task_date: date | None = None, session: Session = Depends(get_session)
) -> list[TaskRead]:
    query = select(Task)
    if task_date is not None:
        query = query.where(Task.date == task_date)
    tasks = session.exec(query.order_by(Task.id)).all()
    return [_to_read(session, t) for t in tasks]


@router.post("/generate", response_model=list[TaskRead])
def generate(
    payload: GenerateRequest | None = None, session: Session = Depends(get_session)
) -> list[TaskRead]:
    target = (payload.date if payload else None) or date.today()
    tasks = generate_for_date(session, target)
    return [_to_read(session, t) for t in tasks]


@router.post("", response_model=TaskRead, status_code=201)
def create_task(payload: TaskCreate, session: Session = Depends(get_session)) -> TaskRead:
    task = Task(**payload.model_dump())
    session.add(task)
    session.commit()
    session.refresh(task)
    return _to_read(session, task)


@router.patch("/{task_id}", response_model=TaskRead)
def update_task(
    task_id: int, payload: TaskUpdate, session: Session = Depends(get_session)
) -> TaskRead:
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    data = payload.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(task, key, value)
    if data.get("status") == TaskStatus.completed and task.completed_at is None:
        task.completed_at = datetime.now(UTC)
    session.add(task)
    session.commit()
    session.refresh(task)
    return _to_read(session, task)


@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: int, session: Session = Depends(get_session)) -> None:
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    session.delete(task)
    session.commit()
