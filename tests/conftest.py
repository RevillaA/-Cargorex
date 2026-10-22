"""Pytest fixtures with an ISOLATED in-memory database.

The test database never touches the demonstration file ``cargorex.db`` (RF-11
test support; constitution Principle V).
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app
from app.seed import seed


@pytest.fixture()
def db_session():
    """A fresh in-memory SQLite session, seeded with fictional data."""
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    seed(db)
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client(db_session):
    """TestClient whose get_db dependency uses the isolated seeded session."""

    def _override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _override_get_db
    # Note: TestClient is NOT used as a context manager on purpose, so the app
    # startup event (which would create/seed the real cargorex.db) does not run.
    # The isolated in-memory session is injected via the get_db override instead.
    test_client = TestClient(app)
    try:
        yield test_client
    finally:
        app.dependency_overrides.clear()
