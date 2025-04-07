from datetime import datetime, timezone
from typing import Optional, List
from pydantic import BaseModel, Field
from uuid import UUID, uuid4

class PracticeProblem(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    course_id: UUID
    topic: str
    difficulty: str  # easy, medium, hard
    question_type: str  # multiple_choice, free_response, coding
    question_text: str
    answer: str
    explanation: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class StudySession(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    user_id: UUID
    course_id: UUID
    start_time: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    end_time: Optional[datetime] = None
    topics_covered: List[str] = []
    problems_attempted: List[UUID] = []  # List of PracticeProblem IDs
    score: Optional[float] = None
    feedback: Optional[str] = None

class StudentProgress(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    user_id: UUID
    course_id: UUID
    topic: str
    proficiency_score: float = 0.0  # 0-1 scale
    problems_attempted: int = 0
    problems_correct: int = 0
    last_updated: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class StudyGuide(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    course_id: UUID
    topic: str
    content: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc)) 