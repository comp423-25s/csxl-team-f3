import pytest
from unittest.mock import MagicMock, call
from typing import List, Optional
import uuid


from ....models.study_buddy.study_buddy_models import (
    PracticeProblem,
    StudyGuide,
)
from ....models.academics import Course

from ....services.study_buddy.study_buddy_service import (
    PracticeProblemListResponse,
    PracticeProblemResponse,
    StudyGuideResponse,
)


from ....services.study_buddy import StudyBuddyService



COURSE_ID = "COMP110"

DUMMY_COURSE = Course(
    id=COURSE_ID,
    subject_code="COMP",
    number="110",
    title="Intro to Programming",
    description="Fundamental programming concepts.",
    credit_hours=3,
)



@pytest.mark.asyncio
async def test_generate_practice_problems_success(
    study_buddy_svc: StudyBuddyService,  
    openai_svc_mock: MagicMock,  
    course_svc_mock: MagicMock,  
):
    """Tests successful generation of practice problems."""
    
    course_svc_mock.reset_mock()
    openai_svc_mock.reset_mock()

    course_svc_mock.get_by_id.return_value = DUMMY_COURSE

    difficulty = "Easy"
    question_type = "Multiple Choice"
    num_problems = 2


    expected_ai_response = PracticeProblemListResponse(
        problems=[
            PracticeProblemResponse(
                question_text="Q1 Text", answer="A1", explanation="E1"
            ),
            PracticeProblemResponse(
                question_text="Q2 Text", answer="A2", explanation="E2"
            ),
        ]
    )
    openai_svc_mock.prompt.side_effect = None 
    openai_svc_mock.prompt.return_value = expected_ai_response

    result = await study_buddy_svc.generate_practice_problems(
        course_id=COURSE_ID,
        difficulty=difficulty,
        question_type=question_type,
        num_problems=num_problems,
    )

    assert isinstance(result, list)
    assert len(result) == len(expected_ai_response.problems)
    assert all(isinstance(p, PracticeProblem) for p in result)
    assert result[0].question_text == "Q1 Text"
    assert result[0].answer == "A1"
    assert result[0].explanation == "E1"
    assert result[0].course_id == COURSE_ID
    assert result[0].difficulty == difficulty
    assert result[0].question_type == question_type

    course_svc_mock.get_by_id.assert_called_once_with(COURSE_ID)
    openai_svc_mock.prompt.assert_called_once()
    args, kwargs = openai_svc_mock.prompt.call_args
    assert "system_prompt" in kwargs
    assert "user_prompt" in kwargs
    assert DUMMY_COURSE.description in kwargs["user_prompt"]
    assert f"Difficulty: {difficulty}" in kwargs["user_prompt"]
    assert f"Question Type: {question_type}" in kwargs["user_prompt"]
    assert f"Create {num_problems} practice problems" in kwargs["user_prompt"]
    assert kwargs["response_model"] == PracticeProblemListResponse


@pytest.mark.asyncio
async def test_generate_practice_problems_defaults(
    study_buddy_svc: StudyBuddyService, 
    openai_svc_mock: MagicMock,
    course_svc_mock: MagicMock,
):
    """Tests generation with default difficulty and question type."""
    course_svc_mock.reset_mock()
    openai_svc_mock.reset_mock()
    course_svc_mock.get_by_id.return_value = DUMMY_COURSE
    num_problems = 5 

    mock_problem_response = PracticeProblemListResponse(
        problems=[
            PracticeProblemResponse(
                question_text="Q Default", answer="A Default", explanation="E Default"
            )
        ]
        * num_problems
    )
    openai_svc_mock.prompt.side_effect = None
    openai_svc_mock.prompt.return_value = mock_problem_response

    result = await study_buddy_svc.generate_practice_problems(course_id=COURSE_ID)

    assert len(result) == num_problems
    assert result[0].question_text == "Q Default"
    assert result[0].difficulty is None
    assert result[0].question_type is None

    course_svc_mock.get_by_id.assert_called_once_with(COURSE_ID)
    openai_svc_mock.prompt.assert_called_once()
    args, kwargs = openai_svc_mock.prompt.call_args
    assert "Difficulty: Any difficulty" in kwargs["user_prompt"]
    assert "Question Type: Any type" in kwargs["user_prompt"]
    assert f"Create {num_problems} practice problems" in kwargs["user_prompt"]
    assert kwargs["response_model"] == PracticeProblemListResponse


@pytest.mark.asyncio
async def test_generate_practice_problems_openai_error(
    study_buddy_svc: StudyBuddyService, 
    openai_svc_mock: MagicMock,
    course_svc_mock: MagicMock,
):
    """Tests handling of OpenAI API errors during problem generation."""
    course_svc_mock.reset_mock()
    openai_svc_mock.reset_mock()
    course_svc_mock.get_by_id.return_value = DUMMY_COURSE
    openai_svc_mock.prompt.side_effect = Exception("OpenAI API Error")

    with pytest.raises(
        Exception, match="Failed to generate practice problems: OpenAI API Error"
    ):
        await study_buddy_svc.generate_practice_problems(course_id=COURSE_ID)

    course_svc_mock.get_by_id.assert_called_once_with(COURSE_ID)
    openai_svc_mock.prompt.assert_called_once()




@pytest.mark.asyncio
async def test_generate_study_guide_success(
    study_buddy_svc: StudyBuddyService, 
    openai_svc_mock: MagicMock,
    course_svc_mock: MagicMock,
):
    """Tests successful generation of a study guide."""
    course_svc_mock.reset_mock()
    openai_svc_mock.reset_mock()
    course_svc_mock.get_by_id.return_value = DUMMY_COURSE
    expected_content = "# Guide Content\nDetails..."
    expected_ai_response = StudyGuideResponse(content=expected_content)

    openai_svc_mock.prompt.side_effect = None
    openai_svc_mock.prompt.return_value = expected_ai_response

    result = await study_buddy_svc.generate_study_guide(course_id=COURSE_ID)

    assert isinstance(result, StudyGuide)
    assert result.course_id == COURSE_ID
    assert result.content == expected_content

    course_svc_mock.get_by_id.assert_called_once_with(COURSE_ID)
    openai_svc_mock.prompt.assert_called_once()
    args, kwargs = openai_svc_mock.prompt.call_args
    assert "system_prompt" in kwargs
    assert "user_prompt" in kwargs
    assert DUMMY_COURSE.description in kwargs["user_prompt"]
    assert "Create a comprehensive study guide" in kwargs["user_prompt"]
    assert kwargs["response_model"] == StudyGuideResponse


@pytest.mark.asyncio
async def test_generate_study_guide_openai_error(
    study_buddy_svc: StudyBuddyService, 
    openai_svc_mock: MagicMock,
    course_svc_mock: MagicMock,
):
    """Tests handling of OpenAI API errors during study guide generation."""
    course_svc_mock.reset_mock()
    openai_svc_mock.reset_mock()
    course_svc_mock.get_by_id.return_value = DUMMY_COURSE
    openai_svc_mock.prompt.side_effect = Exception("OpenAI API Error")

    with pytest.raises(
        Exception, match="Failed to generate study guide: OpenAI API Error"
    ):
        await study_buddy_svc.generate_study_guide(course_id=COURSE_ID)

    course_svc_mock.get_by_id.assert_called_once_with(COURSE_ID)
    openai_svc_mock.prompt.assert_called_once()





@pytest.mark.asyncio
async def test_generate_instructor_report_success(
    study_buddy_svc: StudyBuddyService,  
    openai_svc_mock: MagicMock,
    course_svc_mock: MagicMock,
):
    """Tests successful generation of an instructor report."""
    course_svc_mock.reset_mock()
    openai_svc_mock.reset_mock()
    course_svc_mock.get_by_id.return_value = DUMMY_COURSE
    expected_report_content = "## Instructor Guide\nFocus on..."
    expected_ai_response = StudyGuideResponse(content=expected_report_content)

    openai_svc_mock.prompt.side_effect = None
    openai_svc_mock.prompt.return_value = expected_ai_response

    result = await study_buddy_svc.generate_instructor_report(course_id=COURSE_ID)

    assert isinstance(result, str)
    assert result == expected_report_content

    course_svc_mock.get_by_id.assert_called_once_with(COURSE_ID)
    openai_svc_mock.prompt.assert_called_once()
    args, kwargs = openai_svc_mock.prompt.call_args
    assert "system_prompt" in kwargs
    assert "user_prompt" in kwargs
    assert DUMMY_COURSE.description in kwargs["user_prompt"]
    assert "Create a teaching guide" in kwargs["user_prompt"]
    assert kwargs["response_model"] == StudyGuideResponse


@pytest.mark.asyncio
async def test_generate_instructor_report_openai_error(
    study_buddy_svc: StudyBuddyService, 
    openai_svc_mock: MagicMock,
    course_svc_mock: MagicMock,
):
    """Tests handling of OpenAI API errors during instructor report generation."""
    course_svc_mock.reset_mock()
    openai_svc_mock.reset_mock()
    course_svc_mock.get_by_id.return_value = DUMMY_COURSE
    openai_svc_mock.prompt.side_effect = Exception("OpenAI API Error")

    with pytest.raises(Exception, match="OpenAI API Error"):
        await study_buddy_svc.generate_instructor_report(course_id=COURSE_ID)

    course_svc_mock.get_by_id.assert_called_once_with(COURSE_ID)
    openai_svc_mock.prompt.assert_called_once()
