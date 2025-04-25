from datetime import datetime, timezone
from typing import Optional, List
from pydantic import BaseModel, Field
from uuid import UUID, uuid4


class PracticeProblem(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    course_id: str
    difficulty: Optional[str] = None  # easy, medium, hard
    question_type: Optional[str] = None  # multiple_choice, free_response, coding
    question_text: str
    answer: str
    explanation: str


class StudyGuide(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    course_id: str
    content: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
