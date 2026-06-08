"""TLE Eliminator course tracking endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from ..database import get_session
from ..models import TLELevel, TLETopic
from ..schemas import LevelRead, ProblemResult, TopicRead
from ..services.mastery import record_problem_result

router = APIRouter(prefix="/api/tle", tags=["tle"])


@router.get("/levels", response_model=list[LevelRead])
def list_levels(session: Session = Depends(get_session)) -> list[LevelRead]:
    levels = session.exec(select(TLELevel).order_by(TLELevel.number)).all()
    result: list[LevelRead] = []
    for level in levels:
        topics = session.exec(
            select(TLETopic).where(TLETopic.level_id == level.id).order_by(TLETopic.order)
        ).all()
        avg = round(sum(t.mastery_pct for t in topics) / len(topics), 1) if topics else 0.0
        result.append(
            LevelRead(
                id=level.id,
                number=level.number,
                name=level.name,
                topics=[TopicRead.model_validate(t) for t in topics],
                mastery_pct=avg,
            )
        )
    return result


@router.post("/topics/{topic_id}/result", response_model=TopicRead)
def submit_problem_result(
    topic_id: int, payload: ProblemResult, session: Session = Depends(get_session)
) -> TopicRead:
    topic = session.get(TLETopic, topic_id)
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    try:
        record_problem_result(topic, payload.outcome)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    session.add(topic)
    session.commit()
    session.refresh(topic)
    return TopicRead.model_validate(topic)


@router.post("/topics/{topic_id}/watch", response_model=TopicRead)
def watch_video(topic_id: int, session: Session = Depends(get_session)) -> TopicRead:
    topic = session.get(TLETopic, topic_id)
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    if topic.videos_watched < topic.video_count:
        topic.videos_watched += 1
    session.add(topic)
    session.commit()
    session.refresh(topic)
    return TopicRead.model_validate(topic)
