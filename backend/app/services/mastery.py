"""Adaptive topic mastery logic (TLE Eliminator)."""

from __future__ import annotations

from ..models import Difficulty, TLETopic, TopicStatus

INITIAL_PROBLEMS = {Difficulty.easy: 10, Difficulty.medium: 15, Difficulty.hard: 20}

POINTS = {
    "solved_fast": 10,
    "solved_slow": 5,
    "partial": 3,
    "unsolved": 0,
}
MAX_POINTS_PER_PROBLEM = 10


def initial_batch_size(topic: TLETopic) -> int:
    return INITIAL_PROBLEMS.get(topic.difficulty, 15)


def ensure_started(topic: TLETopic) -> None:
    """Move a topic into progress and assign its first batch of problems."""
    if topic.status == TopicStatus.not_started:
        topic.status = TopicStatus.in_progress
        if topic.problems_assigned == 0:
            topic.problems_assigned = initial_batch_size(topic)


def recompute_status(topic: TLETopic) -> None:
    topic.mastery_pct = (
        round(topic.points_earned / topic.points_possible * 100, 1)
        if topic.points_possible > 0
        else 0.0
    )
    if topic.mastery_pct >= 90 and topic.problems_solved >= initial_batch_size(topic):
        topic.status = TopicStatus.mastered
    elif topic.points_possible > 0:
        topic.status = TopicStatus.in_progress


def record_problem_result(topic: TLETopic, outcome: str) -> str:
    """Apply a single problem outcome, recompute mastery, and adapt the batch.

    Returns a human-readable message describing the next action.
    """
    if outcome not in POINTS:
        raise ValueError(f"Unknown outcome: {outcome}")

    ensure_started(topic)
    topic.points_earned += POINTS[outcome]
    topic.points_possible += MAX_POINTS_PER_PROBLEM
    if outcome in ("solved_fast", "solved_slow"):
        topic.problems_solved += 1

    recompute_status(topic)
    return _next_action(topic)


def _next_action(topic: TLETopic) -> str:
    """If the current batch is exhausted, assign more problems based on mastery."""
    remaining = topic.problems_assigned - topic.points_possible // MAX_POINTS_PER_PROBLEM
    if remaining > 0:
        return f"{remaining} problem(s) remaining in current batch for {topic.name}."

    if topic.mastery_pct >= 90:
        topic.status = TopicStatus.mastered
        return f"\U0001f389 {topic.name} mastered ({topic.mastery_pct}%)! Move to the next topic."
    if topic.mastery_pct >= 70:
        topic.problems_assigned += 5
        return f"Almost there! 5 more problems assigned for {topic.name}."
    topic.problems_assigned += 10
    return f"Keep going! 10 more problems assigned for {topic.name}."
