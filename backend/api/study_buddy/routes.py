# backend/api/study_buddy/routes.py

from fastapi import APIRouter, Depends, HTTPException, Body
from typing import List, Optional
from pydantic import BaseModel

from ...models.study_buddy.study_buddy_models import (
    PracticeProblem,
    StudyGuide,
)
from ...models.user import User
from ...services.study_buddy.study_buddy_service import StudyBuddyService
from ...api.authentication import registered_user

router = APIRouter(prefix="/api/study-buddy", tags=["study-buddy"])

# --- Standard Study‑Buddy endpoints ---


@router.get("/courses/{course_id}/practice-problems")
async def get_practice_problems(
    course_id: str,
    difficulty: Optional[str] = None,
    question_type: Optional[str] = None,
    study_buddy_service: StudyBuddyService = Depends(),
) -> List[PracticeProblem]:
    """
    Generate practice problems for a course
    """
    try:
        return await study_buddy_service.generate_practice_problems(
            course_id=course_id,
            difficulty=difficulty,
            question_type=question_type,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/courses/{course_id}/study-guide")
async def generate_study_guide(
    course_id: str, study_buddy_service: StudyBuddyService = Depends()
) -> StudyGuide:
    """
    Generate a study guide for a course
    """
    try:
        return await study_buddy_service.generate_study_guide(
            course_id=course_id,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- Instructor Summary feature ---


class InstructorReportResponse(BaseModel):
    report: str


@router.get(
    "/courses/{course_id}/instructor-report", response_model=InstructorReportResponse
)
async def generate_instructor_report(
    course_id: str, service: StudyBuddyService = Depends()
) -> InstructorReportResponse:
    """
    Generate an instructor report for a course
    """
    try:
        report = await service.generate_instructor_report(course_id)
        return InstructorReportResponse(report=report)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
