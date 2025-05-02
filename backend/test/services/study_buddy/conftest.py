import pytest
from unittest.mock import create_autospec


from ....services.study_buddy import StudyBuddyService
from ....services.openai import OpenAIService
from ....services.academics import CourseService


@pytest.fixture()
def openai_svc_mock():
    """Provides a MagicMock mimicking OpenAIService."""
    return create_autospec(OpenAIService)


@pytest.fixture()
def course_svc_mock():
    """Provides a MagicMock mimicking CourseService."""
    return create_autospec(CourseService)


@pytest.fixture()
def study_buddy_svc(openai_svc_mock: OpenAIService, course_svc_mock: CourseService):
    """Provides an instance of StudyBuddyService with mocked dependencies."""
    return StudyBuddyService(openai=openai_svc_mock, course_service=course_svc_mock)
