"""Idempotent seeding of FICTIONAL test data.

Loads at least 3 teachers and projects covering the three statuses so the demo
and the tests are reproducible. Does nothing if data already exists.
"""
from sqlalchemy.orm import Session

from app.models import ProjectStatus, ResearchProject, Teacher

# Fictional data — NOT an official catalogue (constitution, Principle VIII).
_TEACHERS = [
    "Docente de Prueba 1 (ficticio)",
    "Docente de Prueba 2 (ficticio)",
    "Docente de Prueba 3 (ficticio)",
]

_PROJECTS = [
    ("PI-001", "Proyecto de Investigacion de Prueba (Aprobado)", ProjectStatus.APPROVED),
    ("PI-002", "Proyecto de Investigacion de Prueba (Pendiente)", ProjectStatus.PENDING),
    ("PI-003", "Proyecto de Investigacion de Prueba (Rechazado)", ProjectStatus.REJECTED),
]


def seed(db: Session) -> None:
    """Populate teachers and projects if their tables are empty (idempotent)."""
    if db.query(Teacher).count() == 0:
        db.add_all(Teacher(name=name) for name in _TEACHERS)

    if db.query(ResearchProject).count() == 0:
        db.add_all(
            ResearchProject(code=code, name=name, status=status)
            for code, name, status in _PROJECTS
        )

    db.commit()
