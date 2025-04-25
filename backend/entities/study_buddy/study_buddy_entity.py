from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PGUUID
import json

from ..entity_base import EntityBase


class PracticeProblem(EntityBase):
    """SQLAlchemy entity for practice problems"""

    __tablename__ = "practice_problems"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    course_id = Column(String, nullable=False)
    difficulty = Column(String, nullable=True)  # easy, medium, hard
    question_type = Column(
        String, nullable=True
    )  # multiple_choice, free_response, coding
    question_text = Column(String, nullable=False)
    answer = Column(String, nullable=False)
    explanation = Column(String, nullable=False)


class StudyGuide(EntityBase):
    """SQLAlchemy entity for study guides"""

    __tablename__ = "study_guides"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    course_id = Column(String, nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)


class AIAuditLog(EntityBase):
    """SQLAlchemy entity for logging AI interactions"""

    __tablename__ = "ai_audit_logs"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(PGUUID(as_uuid=True), nullable=False)
    feature = Column(String, nullable=False)  # e.g., "practice_problems", "study_guide"
    prompt = Column(String, nullable=False)
    response = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, user_id: UUID, feature: str, prompt: str, response: str):
        super().__init__()
        self.user_id = user_id
        self.feature = feature
        self.prompt = prompt
        self.response = response
