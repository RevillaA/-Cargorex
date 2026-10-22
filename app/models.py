"""ORM entities (MODEL): Teacher, ResearchProject, ResearchAssignment.

All teachers and projects are FICTIONAL test data (constitution, Principle VIII).
"""
import enum
from datetime import datetime, timezone

from sqlalchemy import (
    CheckConstraint,
    Column,
    DateTime,
    Enum as SAEnum,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from app.database import Base


class ProjectStatus(str, enum.Enum):
    """Project lifecycle status. Only APPROVED enables an assignment (RF-06).

    The official catalogue of statuses remains PENDING VALIDATION with the
    functional area; these three values are a prototype assumption.
    """

    APPROVED = "APPROVED"
    PENDING = "PENDING"
    REJECTED = "REJECTED"


class Teacher(Base):
    """Fictional teacher from the test catalogue (RF-01)."""

    __tablename__ = "teacher"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(120), nullable=False)

    assignments = relationship("ResearchAssignment", back_populates="teacher")


class ResearchProject(Base):
    """Fictional research project with a status (RF-02, RF-03)."""

    __tablename__ = "research_project"

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(30), nullable=False, unique=True)
    name = Column(String(150), nullable=False)
    status = Column(SAEnum(ProjectStatus), nullable=False)

    assignments = relationship("ResearchAssignment", back_populates="project")


class ResearchAssignment(Base):
    """A valid research-hours assignment. Persisted only after all checks pass (RF-09)."""

    __tablename__ = "research_assignment"
    __table_args__ = (CheckConstraint("hours > 0", name="ck_hours_positive"),)

    id = Column(Integer, primary_key=True, autoincrement=True)
    teacher_id = Column(Integer, ForeignKey("teacher.id"), nullable=False)
    project_id = Column(Integer, ForeignKey("research_project.id"), nullable=False)
    hours = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    teacher = relationship("Teacher", back_populates="assignments")
    project = relationship("ResearchProject", back_populates="assignments")
