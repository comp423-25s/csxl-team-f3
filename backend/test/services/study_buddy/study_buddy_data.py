"""Mock data for study buddy entities."""

from datetime import datetime, timezone
from uuid import UUID, uuid4
from typing import List
from ....entities.study_buddy.study_buddy_entity import (
    Course as CourseEntity,
    PracticeProblem as PracticeProblemEntity,
    StudySession as StudySessionEntity,
    StudentProgress as StudentProgressEntity,
    StudyGuide as StudyGuideEntity,
)

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"

# Mock courses
COURSES = [
    CourseEntity(
        id=uuid4(),
        name="Introduction to Computer Science",
        description="Fundamental concepts of computer science and programming",
        topics=["Data Structures", "Algorithms", "Object-Oriented Programming"],
    ),
    CourseEntity(
        id=uuid4(),
        name="Data Structures and Algorithms",
        description="Advanced data structures and algorithm analysis",
        topics=["Sorting Algorithms", "Graph Theory", "Dynamic Programming"],
    ),
]

# Mock practice problems
PRACTICE_PROBLEMS = [
    PracticeProblemEntity(
        id=uuid4(),
        course_id=COURSES[0].id,
        topic="Data Structures",
        difficulty="easy",
        question_type="multiple_choice",
        question_text="What is the time complexity of accessing an element in an array?",
        answer="O(1)",
        explanation="Arrays provide constant time access to any element using its index.",
    ),
    PracticeProblemEntity(
        id=uuid4(),
        course_id=COURSES[0].id,
        topic="Algorithms",
        difficulty="medium",
        question_type="free_response",
        question_text="Explain the difference between BFS and DFS.",
        answer="BFS explores all neighbors at the current depth before moving to the next level, while DFS explores as far as possible along each branch before backtracking.",
        explanation="BFS uses a queue and is good for finding shortest paths, while DFS uses a stack and is good for exploring all possibilities.",
    ),
]

# Mock study sessions
STUDY_SESSIONS = [
    StudySessionEntity(
        id=uuid4(),
        user_id=uuid4(),  # This will be replaced with actual user ID in reset_demo.py
        course_id=COURSES[0].id,
        start_time=datetime.now(timezone.utc),
        end_time=datetime.now(timezone.utc),
        topics_covered=["Data Structures", "Algorithms"],
        score=0.8,
        feedback="Good understanding of basic concepts, but need more practice with advanced topics.",
    ),
]

# Mock student progress
STUDENT_PROGRESS = [
    StudentProgressEntity(
        id=uuid4(),
        user_id=uuid4(),  # This will be replaced with actual user ID in reset_demo.py
        course_id=COURSES[0].id,
        topic="Data Structures",
        proficiency_score=0.8,
        problems_attempted=10,
        problems_correct=8,
        last_updated=datetime.now(timezone.utc),
    ),
]

# Mock study guides
STUDY_GUIDES = [
    StudyGuideEntity(
        id=uuid4(),
        course_id=COURSES[0].id,
        topic="Data Structures",
        content="# Data Structures Study Guide\n\n## Arrays\n- O(1) access time\n- Contiguous memory allocation\n\n## Linked Lists\n- O(n) access time\n- Dynamic memory allocation",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    ),
]


def insert_fake_data(session):
    """Insert mock data into the database."""
    # Insert courses
    for course in COURSES:
        session.add(course)

    # Insert practice problems
    for problem in PRACTICE_PROBLEMS:
        session.add(problem)

    # Insert study sessions
    for study_session in STUDY_SESSIONS:
        session.add(study_session)

    # Insert student progress
    for progress in STUDENT_PROGRESS:
        session.add(progress)

    # Insert study guides
    for guide in STUDY_GUIDES:
        session.add(guide)

    session.commit()
