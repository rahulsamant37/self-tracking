"""Daily task generation across active goals."""

from __future__ import annotations

from datetime import date

from sqlmodel import Session, select

from ..models import (
    Goal,
    GoalKind,
    Task,
    TaskType,
    TLELevel,
    TLETopic,
    TopicStatus,
)
from .mastery import ensure_started

# Codeforces daily problem rating range per TLE level.
CF_RATING_BY_LEVEL = {1: 800, 2: 1000, 3: 1200, 4: 1400}

PROBLEMS_PER_DAY = 5
PROBLEM_MINUTES = 16


def _current_dsa_topic(session: Session) -> TLETopic | None:
    """Return the in-progress topic, else the first not-started topic in order."""
    in_progress = session.exec(
        select(TLETopic).where(TLETopic.status == TopicStatus.in_progress)
    ).all()
    if in_progress:
        return _ordered(session, in_progress)[0]

    not_started = session.exec(
        select(TLETopic).where(TLETopic.status == TopicStatus.not_started)
    ).all()
    if not_started:
        return _ordered(session, not_started)[0]
    return None


def _ordered(session: Session, topics: list[TLETopic]) -> list[TLETopic]:
    levels = {lvl.id: lvl.number for lvl in session.exec(select(TLELevel)).all()}
    return sorted(topics, key=lambda t: (levels.get(t.level_id, 99), t.order))


def _level_number(session: Session, topic: TLETopic) -> int:
    level = session.get(TLELevel, topic.level_id)
    return level.number if level else 1


def generate_for_date(session: Session, target: date) -> list[Task]:
    existing = session.exec(select(Task).where(Task.date == target)).all()
    if existing:
        return existing

    goals = session.exec(select(Goal).where(Goal.active == True)).all()  # noqa: E712
    created: list[Task] = []

    for goal in goals:
        if goal.kind == GoalKind.dsa:
            created.extend(_dsa_tasks(session, goal, target))
        else:
            created.extend(_exam_tasks(goal, target))

    for task in created:
        session.add(task)
    session.commit()
    for task in created:
        session.refresh(task)
    return created


def _dsa_tasks(session: Session, goal: Goal, target: date) -> list[Task]:
    tasks: list[Task] = []
    topic = _current_dsa_topic(session)
    if topic is None:
        return tasks

    ensure_started(topic)
    session.add(topic)
    level_no = _level_number(session, topic)

    if topic.videos_watched < topic.video_count:
        next_video = topic.videos_watched + 1
        tasks.append(
            Task(
                date=target,
                goal_id=goal.id,
                topic_id=topic.id,
                title=f"Watch: {topic.name} - Part {next_video}",
                description=f"Lecture {next_video} of {topic.video_count} for {topic.name}.",
                type=TaskType.video,
                estimated_minutes=40,
            )
        )

    solved_so_far = topic.points_possible // 10
    remaining = max(topic.problems_assigned - solved_so_far, 0)
    batch = min(PROBLEMS_PER_DAY, remaining) if remaining else PROBLEMS_PER_DAY
    start = solved_so_far + 1
    tasks.append(
        Task(
            date=target,
            goal_id=goal.id,
            topic_id=topic.id,
            title=f"Solve: {topic.name} problems #{start}-{start + batch - 1} ({batch})",
            description=(
                f"Practice batch for {topic.name} "
                f"(mastery {topic.mastery_pct}%, {topic.problems_assigned} assigned)."
            ),
            type=TaskType.problem,
            estimated_minutes=batch * PROBLEM_MINUTES,
        )
    )

    rating = CF_RATING_BY_LEVEL.get(level_no, 1000)
    tasks.append(
        Task(
            date=target,
            goal_id=goal.id,
            topic_id=None,
            title=f"Codeforces daily problem ({rating}-{rating + 200} rating)",
            description="Daily problem-solving to keep skills sharp.",
            type=TaskType.codeforces,
            estimated_minutes=30,
            cf_rating=rating,
            cf_url="https://codeforces.com/problemset?order=BY_RATING_ASC",
        )
    )
    return tasks


def _exam_tasks(goal: Goal, target: date) -> list[Task]:
    study_min = max(goal.daily_minutes - 30, 30)
    return [
        Task(
            date=target,
            goal_id=goal.id,
            title=f"{goal.name}: Learn next syllabus topic",
            description="Watch lecture / read notes on the next uncovered topic.",
            type=TaskType.study,
            estimated_minutes=study_min,
        ),
        Task(
            date=target,
            goal_id=goal.id,
            title=f"{goal.name}: Practice 10 problems",
            description="Practice problems from the most recent topic.",
            type=TaskType.problem,
            estimated_minutes=30,
        ),
    ]
