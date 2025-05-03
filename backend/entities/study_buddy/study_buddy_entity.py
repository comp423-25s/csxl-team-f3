# backend/entities/study_buddy_entity.py

from datetime import datetime
from typing import List, Optional
from uuid import uuid4, UUID

from sqlalchemy import (
    Column,
    String,
    Float,
    DateTime,
    ForeignKey,
    JSON,
    Integer,
)
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import relationship, Session

from ..entity_base import EntityBase
from ...models.study_buddy.study_buddy_models import (
    PracticeProblem as PPModel,
    StudyGuide     as SGModel,
)


class Course(EntityBase):
    """SQLAlchemy entity for courses."""
    __tablename__ = "courses"

    id          = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    name        = Column(String,  nullable=False)
    description = Column(String,  nullable=False)
    topics      = Column(JSON,    nullable=False, default=list)
    created_at  = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at  = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    practice_problems = relationship("PracticeProblem", back_populates="course")
    study_sessions    = relationship("StudySession",    back_populates="course")
    student_progress  = relationship("StudentProgress", back_populates="course")
    study_guides      = relationship("StudyGuide",      back_populates="course")


class PracticeProblem(EntityBase):
    """SQLAlchemy entity for practice problems."""
    __tablename__ = "practice_problems"

    id            = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    course_id     = Column(PGUUID(as_uuid=True), ForeignKey("courses.id"), nullable=False)
    topic         = Column(String, nullable=True)
    difficulty    = Column(String, nullable=True)
    question_type = Column(String, nullable=True)
    question_text = Column(String, nullable=False)
    answer        = Column(String, nullable=False)
    explanation   = Column(String, nullable=False)

    course         = relationship("Course", back_populates="practice_problems")
    study_sessions = relationship(
        "StudySession",
        secondary="study_session_problems",
        overlaps="practice_problems",
    )

    @classmethod
    def create(cls, model: PPModel, db: Session) -> "PracticeProblem":
        """
        Instantiate from Pydantic PracticeProblem, persist, and return the entity.
        """
        entity = cls(
            course_id     = model.course_id,
            topic         = model.topic,
            difficulty    = model.difficulty,
            question_type = model.question_type,
            question_text = model.question_text,
            answer        = model.answer,
            explanation   = model.explanation,
        )
        db.add(entity)
        db.commit()
        return entity


class StudySession(EntityBase):
    """SQLAlchemy entity for study sessions."""
    __tablename__    = "study_sessions"

    id             = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id        = Column(PGUUID(as_uuid=True), nullable=False)
    course_id      = Column(PGUUID(as_uuid=True), ForeignKey("courses.id"), nullable=False)
    start_time     = Column(DateTime, nullable=False, default=datetime.utcnow)
    end_time       = Column(DateTime, nullable=True)
    topics_covered = Column(JSON, nullable=False, default=list)
    score          = Column(Float, nullable=True)
    feedback       = Column(String, nullable=True)

    course   = relationship("Course", back_populates="study_sessions")
    problems = relationship(
        "PracticeProblem",
        secondary="study_session_problems",
        overlaps="study_sessions",
    )


class StudySessionProblem(EntityBase):
    """Association table for study sessions ↔ practice problems."""
    __tablename__       = "study_session_problems"

    study_session_id = Column(
        PGUUID(as_uuid=True), ForeignKey("study_sessions.id"), primary_key=True
    )
    problem_id       = Column(
        PGUUID(as_uuid=True), ForeignKey("practice_problems.id"), primary_key=True
    )


class StudentProgress(EntityBase):
    """Tracks per-topic student progress."""
    __tablename__     = "student_progress"

    id                = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id           = Column(PGUUID(as_uuid=True), nullable=False)
    course_id         = Column(PGUUID(as_uuid=True), ForeignKey("courses.id"), nullable=False)
    topic             = Column(String, nullable=False)
    proficiency_score = Column(Float,  nullable=False, default=0.0)
    problems_attempted= Column(Integer, nullable=False, default=0)
    problems_correct  = Column(Integer, nullable=False, default=0)
    last_updated      = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    course = relationship("Course", back_populates="student_progress")


class StudyGuide(EntityBase):
    """SQLAlchemy entity for study guides."""
    __tablename__ = "study_guides"

    id          = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    course_id   = Column(PGUUID(as_uuid=True), ForeignKey("courses.id"), nullable=False)
    topic       = Column(String, nullable=True)
    content     = Column(String, nullable=False)
    created_at  = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at  = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    course = relationship("Course", back_populates="study_guides")

    @classmethod
    def create(cls, model: SGModel, db: Session) -> "StudyGuide":
        """
        Instantiate from Pydantic StudyGuide, persist, and return the entity.
        """
        entity = cls(
            course_id = model.course_id,
            topic     = model.topic,
            content   = model.content,
        )
        db.add(entity)
        db.commit()
        return entity


class AIAuditLog(EntityBase):
    """Logs every AI prompt/response pair."""
    __tablename__ = "ai_audit_logs"

    id         = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id    = Column(Integer, ForeignKey("user.id"), nullable=False)
    feature    = Column(String, nullable=False)
    prompt     = Column(String, nullable=False)
    response   = Column(JSON,   nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, user_id: int, feature: str, prompt: str, response: dict):
        super().__init__()
        self.user_id  = user_id
        self.feature  = feature
        self.prompt   = prompt
        self.response = response

    @classmethod
    def log(cls, user_id: int, feature: str, prompt: str, response: dict, db: Session) -> "AIAuditLog":
        """
        Create and persist an audit log entry.
        """
        entry = cls(user_id=user_id, feature=feature, prompt=prompt, response=response)
        db.add(entry)
        db.commit()
        return entry
