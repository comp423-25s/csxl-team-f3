# backend/api/study_buddy/routes.py

from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from pydantic import BaseModel

from ...models.study_buddy.study_buddy_models import PracticeProblem, StudyGuide
from ...models.user import User
from ...services.study_buddy.study_buddy_service import StudyBuddyService
from ...api.authentication import registered_user
from ...services.permission import PermissionService
from ...services.exceptions import UserPermissionException

router = APIRouter(prefix="/api/study-buddy", tags=["study-buddy"])


@router.get(
    "/courses/{course_id}/practice-problems",
    response_model=List[PracticeProblem],
)
async def get_practice_problems(
    course_id: str,
    difficulty: Optional[str] = None,
    question_type: Optional[str] = None,
    study_buddy_service: StudyBuddyService = Depends(),
) -> List[PracticeProblem]:
    try:
        return await study_buddy_service.generate_practice_problems(
            course_id=course_id,
            difficulty=difficulty,
            question_type=question_type,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/courses/{course_id}/study-guide",
    response_model=StudyGuide,
)
async def generate_study_guide(
    course_id: str,
    study_buddy_service: StudyBuddyService = Depends(),
) -> StudyGuide:
    try:
        return await study_buddy_service.generate_study_guide(course_id=course_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class InstructorReportResponse(BaseModel):
    report: str


@router.get(
    "/courses/{course_id}/instructor-report",
    response_model=InstructorReportResponse,
)
async def generate_instructor_report(
    course_id: str,
    service: StudyBuddyService    = Depends(),
    current_user: User            = Depends(registered_user),
    permission: PermissionService = Depends(),
) -> InstructorReportResponse:
    """
    Generate an instructor report for a course — only if you're an instructor *or* an admin.
    """
    try:
        try:
            permission.enforce(
                current_user,
                "course.instructor_report",
                f"course/{course_id}"
            )
        except UserPermissionException:
            permission.enforce(
                current_user,
                "role.list",
                "role/"
            )

        report = await service.generate_instructor_report(course_id)
        return InstructorReportResponse(report=report)

    except UserPermissionException as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
