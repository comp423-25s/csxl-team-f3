# backend/api/study_buddy/routes.py

from fastapi import APIRouter, Depends, HTTPException, Body
from typing import List, Optional, Dict
from uuid import UUID, uuid4
from datetime import datetime, timezone
from pydantic import BaseModel

from ...models.study_buddy.study_buddy_models import (
    PracticeProblem,
    StudySession,
    StudentProgress,
    StudyGuide,
    Course,
)
from ...models.user import User
from ...services.study_buddy.study_buddy_service import StudyBuddyService
from ...api.authentication import registered_user

router = APIRouter(prefix="/api/study-buddy", tags=["study-buddy"])

# --- Mock courses & descriptions ---

MOCK_COURSES: Dict[str, Course] = {
    "COMP401": Course(
        id=uuid4(),
        name="Introduction to Computer Science",
        description="Fundamental concepts of computer science and programming",
        topics=["Data Structures", "Algorithms", "Object-Oriented Programming"],
    ),
    "COMP402": Course(
        id=uuid4(),
        name="Data Structures and Algorithms",
        description="Advanced data structures and algorithm analysis",
        topics=["Sorting Algorithms", "Graph Theory", "Dynamic Programming"],
    ),
}

COURSE_DESCRIPTIONS: Dict[str, str] = {
    "COMP401": "Introduction to Computer Science - Fundamental concepts of computer science and programming",
    "COMP402": "Data Structures and Algorithms - Advanced data structures and algorithm analysis",
}

# Temporary storage
STUDY_SESSIONS: Dict[str, StudySession] = {}
STUDENT_PROGRESS: List[StudentProgress] = []

# --- Standard Study‑Buddy endpoints ---

@router.get("/courses")
async def get_courses() -> List[Course]:
    return list(MOCK_COURSES.values())

@router.get("/courses/{course_id}")
async def get_course(
    course_id: str,
    current_user: User = Depends(registered_user)
) -> Course:
    course = MOCK_COURSES.get(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@router.get("/courses/{course_id}/topics")
async def get_course_topics(
    course_id: str,
    current_user: User = Depends(registered_user)
) -> List[str]:
    course = MOCK_COURSES.get(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course.topics

@router.get("/courses/{course_id}/practice-problems")
async def get_practice_problems(
    course_id: str,
    topic: Optional[str] = None,
    difficulty: Optional[str] = None,
    question_type: Optional[str] = None,
    study_buddy_service: StudyBuddyService = Depends(),
) -> List[PracticeProblem]:
    try:
        course_description = COURSE_DESCRIPTIONS.get(course_id, "Computer Science Course")
        return await study_buddy_service.generate_practice_problems(
            course_id=course_id,
            course_description=course_description,
            topic=topic,
            difficulty=difficulty,
            question_type=question_type,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/study-guides")
async def generate_study_guide(
    course_id: str = Body(...),
    topics: List[str] = Body(...),
    study_buddy_service: StudyBuddyService = Depends()
) -> StudyGuide:
    try:
        student_progress = [
            p for p in STUDENT_PROGRESS if p.course_id == UUID(course_id)
        ]
        course_description = COURSE_DESCRIPTIONS.get(course_id, "Computer Science Course")
        return await study_buddy_service.generate_study_guide(
            course_id=course_id,
            course_description=course_description,
            topics=topics,
            student_progress=student_progress,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/study-sessions")
async def start_study_session(
    course_id: str,
    topics: List[str],
    current_user: User = Depends(registered_user)
) -> StudySession:
    session = StudySession(
        id=uuid4(),
        user_id=UUID(int=current_user.id) if current_user.id else uuid4(),
        course_id=UUID(course_id),
        topics_covered=topics,
        start_time=datetime.now(timezone.utc),
    )
    STUDY_SESSIONS[str(session.id)] = session
    return session

@router.put("/study-sessions/{session_id}")
async def end_study_session(
    session_id: UUID,
    score: float,
    feedback: Optional[str] = None,
    current_user: User = Depends(registered_user),
) -> StudySession:
    session = STUDY_SESSIONS.get(str(session_id))
    if not session:
        raise HTTPException(status_code=404, detail="Study session not found")
    current_user_id = UUID(int=current_user.id) if current_user.id else None
    if session.user_id != current_user_id:
        raise HTTPException(status_code=403, detail="Not authorized to end this session")
    session.end_time = datetime.now(timezone.utc)
    session.score = score
    session.feedback = feedback
    return session

@router.get("/progress/{course_id}")
async def get_student_progress(
    course_id: str,
    current_user: User = Depends(registered_user)
) -> List[StudentProgress]:
    current_user_id = UUID(int=current_user.id) if current_user.id else None
    return [
        p for p in STUDENT_PROGRESS
        if p.course_id == UUID(course_id) and p.user_id == current_user_id
    ]

# --- Instructor Summary feature ---

class InstructorReportRequest(BaseModel):
    course_id: str

class InstructorReportResponse(BaseModel):
    report: str

# Mock struggles keyed by actual Course UUIDs
MOCK_INSTRUCTOR_DATA: Dict[str, Dict[str, int]] = {
    str(MOCK_COURSES["COMP401"].id): {
        "Data Structures": 5,
        "Algorithms": 3,
        "Object-Oriented Programming": 2
    },
    str(MOCK_COURSES["COMP402"].id): {
        "Sorting Algorithms": 4,
        "Graph Theory": 6,
        "Dynamic Programming": 5
    },
}

@router.post(
    "/instructor/report",
    response_model=InstructorReportResponse
)
async def generate_instructor_report(
    report_req: InstructorReportRequest = Body(...),
    service: StudyBuddyService = Depends()
) -> InstructorReportResponse:
    course_id = report_req.course_id
    struggles = MOCK_INSTRUCTOR_DATA.get(course_id)
    if struggles is None:
        raise HTTPException(status_code=404, detail="No data for this course")
    ai_summary = await service.generate_instructor_report(struggles)
    return InstructorReportResponse(report=ai_summary)
