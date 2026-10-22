"""Integration tests for the API (includes direct API calls, RF-11)."""

# Seeded ids: teachers 1..3; projects 1=APPROVED, 2=PENDING, 3=REJECTED.
APPROVED_PROJECT = 1
PENDING_PROJECT = 2
REJECTED_PROJECT = 3
VALID_TEACHER = 1


def _payload(teacher_id=VALID_TEACHER, project_id=APPROVED_PROJECT, hours=8):
    return {"teacher_id": teacher_id, "project_id": project_id, "hours": hours}


# --- Catalogues (US3) -------------------------------------------------------

def test_list_teachers(client):
    """RF-01: catalogue of fictional teachers (at least 3)."""
    res = client.get("/api/teachers")
    assert res.status_code == 200
    assert len(res.json()) >= 3


def test_list_projects_with_status(client):
    """RF-02, RF-03: projects expose their status; three statuses present."""
    res = client.get("/api/projects")
    assert res.status_code == 200
    statuses = {p["status"] for p in res.json()}
    assert {"APPROVED", "PENDING", "REJECTED"}.issubset(statuses)


# --- Valid registration (US1) ----------------------------------------------

def test_create_valid_assignment(client):
    """CA-01 / RF-09: approved project + positive hours -> 201."""
    res = client.post("/api/assignments", json=_payload(hours=10))
    assert res.status_code == 201
    body = res.json()
    assert body["hours"] == 10
    assert body["id"] is not None


# --- Business-rule rejections -> 400 (US1) ---------------------------------

def test_pending_project_returns_400(client):
    """CA-02: pending project -> 400 with explanatory detail."""
    res = client.post("/api/assignments", json=_payload(project_id=PENDING_PROJECT))
    assert res.status_code == 400
    assert "aprobado" in res.json()["detail"].lower()


def test_rejected_project_returns_400(client):
    """CA-03: rejected project -> 400."""
    res = client.post("/api/assignments", json=_payload(project_id=REJECTED_PROJECT))
    assert res.status_code == 400


def test_nonexistent_project_returns_400(client):
    """CA-05: unknown project -> 400."""
    res = client.post("/api/assignments", json=_payload(project_id=9999))
    assert res.status_code == 400


def test_nonexistent_teacher_returns_400(client):
    """RF-01: unknown teacher -> 400."""
    res = client.post("/api/assignments", json=_payload(teacher_id=9999))
    assert res.status_code == 400


# --- Invalid input -> 422 (US1, RF-08) -------------------------------------

def test_zero_hours_returns_422(client):
    """CA-04: hours = 0 -> 422."""
    res = client.post("/api/assignments", json=_payload(hours=0))
    assert res.status_code == 422


def test_negative_hours_returns_422(client):
    """CA-04: negative hours -> 422."""
    res = client.post("/api/assignments", json=_payload(hours=-3))
    assert res.status_code == 422


def test_non_integer_hours_returns_422(client):
    """RF-08: non-integer hours -> 422."""
    res = client.post("/api/assignments", json=_payload(hours=1.5))
    assert res.status_code == 422


def test_non_numeric_hours_returns_422(client):
    """RF-08: non-numeric hours -> 422."""
    res = client.post("/api/assignments", json=_payload(hours="abc"))
    assert res.status_code == 422


# --- Persistence invariants (RF-10, RF-11, CA-06, CA-07, SC-004) -----------

def test_rejected_requests_are_not_persisted(client):
    """RF-11 / CA-07: direct API calls that fail never persist anything."""
    client.post("/api/assignments", json=_payload(project_id=PENDING_PROJECT))
    client.post("/api/assignments", json=_payload(project_id=REJECTED_PROJECT))
    client.post("/api/assignments", json=_payload(project_id=9999))
    client.post("/api/assignments", json=_payload(hours=0))
    res = client.get("/api/assignments")
    assert res.status_code == 200
    assert res.json() == []


def test_assignments_query_empty_then_populated(client):
    """CA-06 / RF-10 / SC-004: empty list, then the valid record is retrievable."""
    assert client.get("/api/assignments").json() == []

    created = client.post("/api/assignments", json=_payload(hours=6)).json()

    listed = client.get("/api/assignments").json()
    assert len(listed) == 1
    assert listed[0]["id"] == created["id"]
    assert listed[0]["hours"] == 6
    assert listed[0]["teacher_id"] == VALID_TEACHER
    assert listed[0]["project_id"] == APPROVED_PROJECT
