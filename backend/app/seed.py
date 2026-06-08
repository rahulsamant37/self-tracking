"""Seed data: TLE Eliminator course structure and starter goals."""

from __future__ import annotations

from datetime import date

from sqlmodel import Session, select

from .models import Difficulty, Goal, GoalKind, TLELevel, TLETopic

# (level number, level name, [(topic, difficulty, video_count)])
TLE_STRUCTURE: list[tuple[int, str, list[tuple[str, Difficulty, int]]]] = [
    (
        1,
        "Level 1 (Beginner)",
        [
            ("C++ Fundamentals", Difficulty.easy, 4),
            ("Math for Competitive Programming", Difficulty.medium, 3),
            ("Time & Space Complexity", Difficulty.easy, 2),
            ("Searching & Sorting", Difficulty.medium, 4),
            ("C++ STL & Strings", Difficulty.easy, 3),
            ("Debugging Techniques", Difficulty.easy, 2),
        ],
    ),
    (
        2,
        "Level 2 (Pre-Intermediate)",
        [
            ("Prefix Sums", Difficulty.easy, 3),
            ("Bit Manipulation", Difficulty.medium, 3),
            ("Adhoc Problems", Difficulty.medium, 2),
            ("Recursion", Difficulty.medium, 4),
            ("Backtracking", Difficulty.medium, 3),
            ("Number Theory", Difficulty.medium, 4),
            ("Stacks & Queues", Difficulty.easy, 3),
            ("Advanced Sorting", Difficulty.medium, 3),
        ],
    ),
    (
        3,
        "Level 3 (Intermediate)",
        [
            ("Advanced Binary Search", Difficulty.medium, 3),
            ("Interactive Problems", Difficulty.medium, 2),
            ("2 Pointers Technique", Difficulty.medium, 3),
            ("Advanced Number Theory", Difficulty.hard, 4),
            ("Combinatorics", Difficulty.hard, 4),
            ("Greedy Algorithms", Difficulty.medium, 3),
            ("Hashing", Difficulty.medium, 3),
            ("Tries", Difficulty.medium, 3),
        ],
    ),
    (
        4,
        "Level 4 (Advanced)",
        [
            ("Dynamic Programming", Difficulty.hard, 6),
            ("Generic Trees", Difficulty.medium, 3),
            ("Graphs", Difficulty.hard, 6),
            ("Disjoint Set Union (DSU)", Difficulty.hard, 3),
            ("Segment Trees", Difficulty.hard, 4),
            ("Sparse Tables", Difficulty.hard, 2),
        ],
    ),
]

INITIAL_PROBLEMS = {Difficulty.easy: 10, Difficulty.medium: 15, Difficulty.hard: 20}


def seed_tle(session: Session) -> None:
    existing = session.exec(select(TLELevel)).first()
    if existing:
        return
    for number, name, topics in TLE_STRUCTURE:
        level = TLELevel(number=number, name=name)
        session.add(level)
        session.commit()
        session.refresh(level)
        for order, (tname, difficulty, vcount) in enumerate(topics):
            topic = TLETopic(
                level_id=level.id,
                name=tname,
                order=order,
                difficulty=difficulty,
                video_count=vcount,
            )
            session.add(topic)
        session.commit()


def seed_goals(session: Session) -> None:
    existing = session.exec(select(Goal)).first()
    if existing:
        return
    goals = [
        Goal(
            name="CAT 2026",
            description="CAT exam preparation (Quant, LRDI, VARC).",
            kind=GoalKind.exam,
            target_date=date(2026, 11, 30),
            daily_minutes=120,
            priority=1,
            color="#dc2626",
        ),
        Goal(
            name="GATE 2027",
            description="GATE CS exam preparation.",
            kind=GoalKind.exam,
            target_date=date(2027, 2, 1),
            daily_minutes=90,
            priority=2,
            color="#7c3aed",
        ),
        Goal(
            name="DSA (TLE Eliminator)",
            description="TLE Eliminator course, Levels 1-4.",
            kind=GoalKind.dsa,
            target_date=None,
            daily_minutes=150,
            priority=1,
            color="#16a34a",
        ),
    ]
    for g in goals:
        session.add(g)
    session.commit()


def seed_all(session: Session) -> None:
    seed_tle(session)
    seed_goals(session)
