from fastapi import APIRouter, Depends, HTTPException, Query, Path
from typing import List, Optional
from backend.models.academics.study_buddy import (
    PracticeProblem,
    StudySession,
    StudentProgress,
    StudyGuide,
    StudyQuestion,
    StudyPlan,
    ChatResponse,
    DifficultyLevel,  # enum with EASY, MEDIUM, HARD
    QuestionType      # enum with SHORT_ANSWER, MULTIPLE_CHOICE
)
from backend.models.user import User
from backend.auth import get_current_user
from backend.services.study_buddy import StudyBuddyService

router = APIRouter(prefix="/api/study-buddy", tags=["study-buddy"])

study_buddy_service = StudyBuddyService()

@router.get("/courses/{course_id}/practice-problems", response_model=List[PracticeProblem])
async def get_practice_problems(
    course_id: int = Path(..., ge=100, le=999, description="3-digit course ID"),
    topic: Optional[int] = Query(None, description="Unit number of the class"),
    difficulty: Optional[DifficultyLevel] = Query(None, description="Difficulty level: easy, medium, or hard"),
    question_type: Optional[QuestionType] = Query(None, description="Question type: short_answer or multiple_choice"),
    current_user: User = Depends(get_current_user)
) -> List[PracticeProblem]:
    """
    Get practice problems for a specific course with optional filters.
    """
    # TODO: Implement database query with filters
    pass

@router.post("/courses/{course_id}/practice-problems", response_model=PracticeProblem)
async def create_practice_problem(
    course_id: int = Path(..., ge=000, le=999, description="3-digit course ID"),
    current_user: User = Depends(get_current_user)
) -> PracticeProblem:
    """
    Create a new practice problem (for instructors/TAs).
    """
    # TODO: Implement problem creation
    pass

@router.post("/study-sessions", response_model=StudySession)
async def start_study_session(
    course_id: int = Query(..., ge=000, le=999, description="3-digit course ID"),
    topics: List[int] = Query(..., description="List of unit numbers"),
    current_user: User = Depends(get_current_user)
) -> StudySession:
    """
    Start a new study session.
    """
    # TODO: Implement study session creation
    pass

@router.put("/study-sessions/{session_id}", response_model=StudySession)
async def end_study_session(
    session_id: int,  # adjust type if needed (could be UUID)
    score: float,
    feedback: Optional[str] = None,
    current_user: User = Depends(get_current_user)
) -> StudySession:
    """
    End a study session and record results.
    """
    # TODO: Implement study session completion
    pass

@router.get("/progress/{course_id}", response_model=List[StudentProgress])
async def get_student_progress(
    course_id: int = Path(..., ge=000, le=999, description="3-digit course ID"),
    current_user: User = Depends(get_current_user)
) -> List[StudentProgress]:
    """
    Get student's progress for all topics in a course.
    """
    # TODO: Implement progress retrieval
    pass

@router.post("/study-guides", response_model=StudyGuide)
async def generate_study_guide(
    course_id: int = Query(..., ge=000, le=999, description="3-digit course ID"),
    topics: List[int] = Query(..., description="List of unit numbers"),
    current_user: User = Depends(get_current_user)
) -> StudyGuide:
    """
    Generate a personalized study guide based on student's weak areas.
    """
    # TODO: Get student progress from database
    student_progress = []  # Placeholder
    return await study_buddy_service.generate_study_guide(
        course_id, topics, student_progress
    )

@router.get("/courses/{course_id}/topics", response_model=List[int])
async def get_course_topics(
    course_id: int = Path(..., ge=000, le=999, description="3-digit course ID"),
    current_user: User = Depends(get_current_user)
) -> List[int]:
    """
    Get all available topics (unit numbers) for a course.
    """
    # TODO: Implement topic retrieval
    pass
