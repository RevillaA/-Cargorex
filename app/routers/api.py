"""API controller: JSON endpoints for catalogues and assignments.

Maps service errors to HTTP codes: InvalidInputError -> 422, BusinessRuleError
-> 400 (Clarification 2026-10-21). Every rejection carries a JSON ``detail``.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import (
    AssignmentCreate,
    ResearchAssignmentOut,
    ResearchProjectOut,
    TeacherOut,
)
from app.services import assignment_service

router = APIRouter(prefix="/api", tags=["api"])


@router.get("/teachers", response_model=list[TeacherOut])
def get_teachers(db: Session = Depends(get_db)):
    """List fictional teachers (RF-01)."""
    return assignment_service.list_teachers(db)


@router.get("/projects", response_model=list[ResearchProjectOut])
def get_projects(db: Session = Depends(get_db)):
    """List fictional projects with their status (RF-02, RF-03)."""
    return assignment_service.list_projects(db)


@router.get("/assignments", response_model=list[ResearchAssignmentOut])
def get_assignments(db: Session = Depends(get_db)):
    """List stored assignments (RF-10, CA-06)."""
    return assignment_service.list_assignments(db)


@router.post(
    "/assignments",
    response_model=ResearchAssignmentOut,
    status_code=status.HTTP_201_CREATED,
)
def create_assignment(payload: AssignmentCreate, db: Session = Depends(get_db)):
    """Register an assignment after server-side validation (RF-04..RF-09, RF-11)."""
    try:
        return assignment_service.create_assignment(
            db,
            teacher_id=payload.teacher_id,
            project_id=payload.project_id,
            hours=payload.hours,
        )
    except assignment_service.InvalidInputError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc))
    except assignment_service.BusinessRuleError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
