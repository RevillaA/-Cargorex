# Evidencias de Funcionamiento — Cargorex (Iteración 1)

**Fecha**: 2026-10-21 · **Entorno**: Windows 11 · PowerShell · `.venv` · uvicorn

La aplicación se levantó con `uvicorn app.main:app` y se ejercitaron los escenarios de
`quickstart.md` mediante `Invoke-WebRequest` (llamadas directas a la API, sin usar el formulario →
demuestra la validación del servidor, RF-11).

## Salida observada

```text
GET /             -> 200 (aviso datos ficticios: True)
GET /api/teachers -> count=3
GET /api/projects -> estados=APPROVED,PENDING,REJECTED
POST valida       -> 201 (esperado 201)     # proyecto aprobado + horas=8  (E1 / CA-01)
POST pendiente    -> 400 (esperado 400)      # proyecto PENDING            (E2 / CA-02)
POST horas=0      -> 422 (esperado 422)      # entrada inválida            (E5 / CA-04)
GET /api/assignments -> count=1 (esperado 1: solo la valida)  # (E9 / CA-06, CA-07)
```

## Mapeo a escenarios de quickstart.md

| Escenario | Verificación | Dónde |
|-----------|--------------|-------|
| E1 — registro válido (201) | ✅ smoke test (POST valida → 201; count=1) | arriba + `test_create_valid_assignment` |
| E2 — proyecto pendiente (400) | ✅ smoke test (POST pendiente → 400) | arriba + `test_pending_project_returns_400` |
| E3 — proyecto rechazado (400) | ✅ pytest | `test_rejected_project_returns_400` |
| E4 — proyecto inexistente (400) | ✅ pytest | `test_nonexistent_project_returns_400` |
| E5 — horas 0 / negativas (422) | ✅ smoke test + pytest | arriba + `test_zero/negative_hours_returns_422` |
| E6 — horas no enteras/no numéricas (422) | ✅ pytest | `test_non_integer/non_numeric_hours_returns_422` |
| E7 — docente inexistente (400) | ✅ pytest | `test_nonexistent_teacher_returns_400` |
| E8 — validación por API directa (RF-11) | ✅ smoke test (llamadas directas) + pytest | arriba + `test_rejected_requests_are_not_persisted` |
| E9 — consulta de asignaciones (200) | ✅ smoke test (count=1) + pytest | arriba + `test_assignments_query_empty_then_populated` |

**Conclusión**: la regla de negocio (solo proyectos `APPROVED`, horas enteras > 0) se valida en el
servidor; las solicitudes inválidas se rechazan con el código correcto (400 / 422) y **ninguna**
queda persistida; solo la asignación válida se almacena y es consultable.
