"""Business-logic layer (SERVICE).

Holds the reusable validation rules so they run on the server regardless of the
client (constitution, Principle IV; RF-11). Raises two typed errors:

* ``InvalidInputError``  -> malformed input  -> HTTP 422 at the API boundary.
* ``BusinessRuleError``  -> business rule     -> HTTP 400 at the API boundary.
"""
from sqlalchemy.orm import Session

from app.models import ProjectStatus, ResearchAssignment, ResearchProject, Teacher


class InvalidInputError(Exception):
    """Raised when the input itself is invalid (e.g. hours <= 0 or not an integer)."""


class BusinessRuleError(Exception):
    """Raised when a domain rule is violated (teacher/project/status)."""


def list_teachers(db: Session):
    return db.query(Teacher).order_by(Teacher.id).all()


def list_projects(db: Session):
    return db.query(ResearchProject).order_by(ResearchProject.id).all()


def list_assignments(db: Session):
    return db.query(ResearchAssignment).order_by(ResearchAssignment.id).all()


def create_assignment(db: Session, teacher_id: int, project_id: int, hours: int) -> ResearchAssignment:
    """Validate every rule in order and persist only if all pass.

    No ``ResearchAssignment`` is created when any rule fails (RF-11, CA-07).
    """
    # 1. Hours must be a finite positive integer (RF-04, RF-08, CA-04).
    #    (bool is a subclass of int, so it is rejected explicitly.)
    if isinstance(hours, bool) or not isinstance(hours, int) or hours <= 0:
        raise InvalidInputError("Las horas deben ser un numero entero mayor que cero.")

    # 2. Teacher must exist in the test catalogue (RF-01).
    teacher = db.get(Teacher, teacher_id)
    if teacher is None:
        raise BusinessRuleError("El docente indicado no existe en el catalogo de prueba.")

    # 3. Project must exist (RF-05, CA-05).
    project = db.get(ResearchProject, project_id)
    if project is None:
        raise BusinessRuleError("El proyecto indicado no existe en el catalogo de prueba.")

    # 4. Project must be APPROVED (RF-06, RF-07, CA-02, CA-03).
    if project.status != ProjectStatus.APPROVED:
        raise BusinessRuleError(
            f"El proyecto seleccionado no esta aprobado (estado: {project.status.value}). "
            "Solo se permiten horas de investigacion en proyectos aprobados."
        )

    # All checks passed -> persist the valid assignment (RF-09, CA-01).
    assignment = ResearchAssignment(
        teacher_id=teacher_id, project_id=project_id, hours=hours
    )
    db.add(assignment)
    db.commit()
    db.refresh(assignment)
    return assignment
