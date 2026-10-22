# Registro de Resultados de Pruebas — Cargorex (Iteración 1)

**Fecha de ejecución**: 2026-10-21
**Entorno**: Windows 11 · Python 3.11.9 · `.venv` · pytest 9.1.1

## Comando

```powershell
pytest -q
```

## Resultado

**20 passed, 1 warning in 0.23s**

> El único warning es interno de la librería (`starlette.testclient` usa `httpx`), no proviene del
> código del prototipo.

### Detalle (pytest -v)

```text
tests/test_api.py::test_list_teachers PASSED
tests/test_api.py::test_list_projects_with_status PASSED
tests/test_api.py::test_create_valid_assignment PASSED
tests/test_api.py::test_pending_project_returns_400 PASSED
tests/test_api.py::test_rejected_project_returns_400 PASSED
tests/test_api.py::test_nonexistent_project_returns_400 PASSED
tests/test_api.py::test_nonexistent_teacher_returns_400 PASSED
tests/test_api.py::test_zero_hours_returns_422 PASSED
tests/test_api.py::test_negative_hours_returns_422 PASSED
tests/test_api.py::test_non_integer_hours_returns_422 PASSED
tests/test_api.py::test_non_numeric_hours_returns_422 PASSED
tests/test_api.py::test_rejected_requests_are_not_persisted PASSED
tests/test_api.py::test_assignments_query_empty_then_populated PASSED
tests/test_assignment_service.py::test_valid_assignment_is_persisted PASSED
tests/test_assignment_service.py::test_pending_project_is_rejected PASSED
tests/test_assignment_service.py::test_rejected_project_is_rejected PASSED
tests/test_assignment_service.py::test_nonexistent_project_is_rejected PASSED
tests/test_assignment_service.py::test_nonexistent_teacher_is_rejected PASSED
tests/test_assignment_service.py::test_zero_hours_is_rejected PASSED
tests/test_assignment_service.py::test_negative_hours_is_rejected PASSED
```

## Cobertura por requisito (SC-007)

| Requisito | Prueba(s) que lo verifican |
|-----------|-----------------------------|
| RF-01 | test_list_teachers, test_nonexistent_teacher_* |
| RF-02 | test_list_projects_with_status |
| RF-03 | test_list_projects_with_status |
| RF-04 / RF-08 | test_zero/negative/non_integer/non_numeric_hours_returns_422, test_*_hours_is_rejected |
| RF-05 | test_nonexistent_project_* |
| RF-06 / RF-07 | test_pending/rejected_project_returns_400, test_*_project_is_rejected |
| RF-09 | test_create_valid_assignment, test_valid_assignment_is_persisted |
| RF-10 | test_assignments_query_empty_then_populated |
| RF-11 / CA-07 | test_rejected_requests_are_not_persisted |
