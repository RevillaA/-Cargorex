"""Pydantic schemas (input validation + output contracts).

Input validation of ``hours`` (integer > 0) happens here and yields HTTP 422
natively in FastAPI (RF-04, RF-08). Business rules live in the service layer.
"""
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models import ProjectStatus


class TeacherOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class ResearchProjectOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    code: str
    name: str
    status: ProjectStatus


class AssignmentCreate(BaseModel):
    """Payload to register an assignment. ``hours`` must be an integer > 0."""

    teacher_id: int = Field(..., ge=1)
    project_id: int = Field(..., ge=1)
    hours: int = Field(..., gt=0, description="Entero estrictamente positivo (sin límite máximo).")


class ResearchAssignmentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    teacher_id: int
    project_id: int
    hours: int
    created_at: datetime
