"""Unit tests for the business-logic layer (service)."""
import pytest

from app.models import ResearchAssignment
from app.services import assignment_service
from app.services.assignment_service import BusinessRuleError, InvalidInputError

# Seeded ids: teachers 1..3; projects 1=APPROVED, 2=PENDING, 3=REJECTED.
APPROVED_PROJECT = 1
PENDING_PROJECT = 2
REJECTED_PROJECT = 3
VALID_TEACHER = 1


def _count(db):
    return db.query(ResearchAssignment).count()


def test_valid_assignment_is_persisted(db_session):
    """CA-01 / RF-09: approved project + positive hours -> stored."""
    result = assignment_service.create_assignment(
        db_session, teacher_id=VALID_TEACHER, project_id=APPROVED_PROJECT, hours=8
    )
    assert result.id is not None
    assert result.hours == 8
    assert _count(db_session) == 1


def test_pending_project_is_rejected(db_session):
    """CA-02: pending project -> BusinessRuleError, nothing persisted."""
    with pytest.raises(BusinessRuleError):
        assignment_service.create_assignment(
            db_session, teacher_id=VALID_TEACHER, project_id=PENDING_PROJECT, hours=5
        )
    assert _count(db_session) == 0


def test_rejected_project_is_rejected(db_session):
    """CA-03: rejected project -> BusinessRuleError."""
    with pytest.raises(BusinessRuleError):
        assignment_service.create_assignment(
            db_session, teacher_id=VALID_TEACHER, project_id=REJECTED_PROJECT, hours=5
        )
    assert _count(db_session) == 0


def test_nonexistent_project_is_rejected(db_session):
    """CA-05: unknown project id -> BusinessRuleError."""
    with pytest.raises(BusinessRuleError):
        assignment_service.create_assignment(
            db_session, teacher_id=VALID_TEACHER, project_id=9999, hours=5
        )
    assert _count(db_session) == 0


def test_nonexistent_teacher_is_rejected(db_session):
    """RF-01: unknown teacher id -> BusinessRuleError."""
    with pytest.raises(BusinessRuleError):
        assignment_service.create_assignment(
            db_session, teacher_id=9999, project_id=APPROVED_PROJECT, hours=5
        )
    assert _count(db_session) == 0


def test_zero_hours_is_rejected(db_session):
    """CA-04: hours = 0 -> InvalidInputError."""
    with pytest.raises(InvalidInputError):
        assignment_service.create_assignment(
            db_session, teacher_id=VALID_TEACHER, project_id=APPROVED_PROJECT, hours=0
        )
    assert _count(db_session) == 0


def test_negative_hours_is_rejected(db_session):
    """CA-04: negative hours -> InvalidInputError."""
    with pytest.raises(InvalidInputError):
        assignment_service.create_assignment(
            db_session, teacher_id=VALID_TEACHER, project_id=APPROVED_PROJECT, hours=-3
        )
    assert _count(db_session) == 0
