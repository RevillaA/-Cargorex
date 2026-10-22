# Auditoría de Cobertura (Speckit-coverage) — Cargorex, Iteración 1

## 1. Información General

| Campo | Detalle |
|-------|---------|
| **Proyecto** | Cargorex-SDD — Módulo de Distribución de Carga Horaria Docente (UFA ESPE) |
| **Iteración** | Primera iteración — Prototipo de validación de horas de investigación |
| **Feature** | `001-research-hours-validation` |
| **Fecha de auditoría** | 2026-10-21 |
| **Objetivo** | Verificar, con evidencia comprobable, la cobertura entre requisitos, tareas, implementación y pruebas de la primera iteración, diferenciando lo *implementado*, lo *probado* y lo *pendiente*. |
| **Alcance** | Exclusivamente el prototipo de validación de horas de investigación contra proyectos aprobados, con datos ficticios. No incluye la totalidad de Cargorex ni integraciones institucionales. |

## 2. Documentos y Artefactos Analizados

| Artefacto | Ruta real |
|-----------|-----------|
| Constitución | `.specify/memory/constitution.md` (v1.0.1) |
| Especificación | `specs/001-research-hours-validation/spec.md` |
| Plan técnico | `specs/001-research-hours-validation/plan.md` |
| Investigación (Fase 0) | `specs/001-research-hours-validation/research.md` |
| Modelo de datos | `specs/001-research-hours-validation/data-model.md` |
| Contrato de API | `specs/001-research-hours-validation/contracts/openapi.yaml` |
| Guía de inicio | `specs/001-research-hours-validation/quickstart.md` |
| Tareas | `specs/001-research-hours-validation/tasks.md` |
| Checklist de calidad | `specs/001-research-hours-validation/checklists/requirements.md` |
| Evidencia de pruebas | `specs/001-research-hours-validation/evidence/test-results.md` |
| Evidencia de ejecución | `specs/001-research-hours-validation/evidence/run-evidence.md` |
| Código fuente | `app/` (13 módulos) |
| Pruebas automatizadas | `tests/` (conftest + 2 suites, 20 pruebas) |

> **Nota sobre el punto 8 del encargo (reportes de speckit-analyze y speckit-converge):**
> `/speckit-analyze` se ejecutó previamente y su resultado (3 inconsistencias LOW/MEDIUM, ya
> corregidas) consta en el historial de la sesión; no genera archivo propio. La ejecución de
> `/speckit-converge` arrojó resultado **`converged`** (sin brechas), por lo que no añadió tareas a
> `tasks.md`. Esta auditoría es su documento de salida.

## 3. Matriz de Trazabilidad

Leyenda de estado: **Implementado** = existe código que lo satisface · **Probado** = verificado por
prueba automatizada que pasa · **Pendiente** = no construido.

| Req. | Descripción (resumen) | Tareas | Archivos de implementación | Pruebas asociadas | Estado | Verificación | Observaciones |
|------|------------------------|--------|-----------------------------|-------------------|--------|--------------|---------------|
| RF-01 | Seleccionar docente ficticio del catálogo | T007, T014, T021, T024 | `app/models.py`, `app/seed.py`, `app/routers/api.py`, `app/static/js/app.js` | `test_list_teachers`, `test_nonexistent_teacher_returns_400`, `test_nonexistent_teacher_is_rejected` | Implementado | ✅ Probado | — |
| RF-02 | Consultar y seleccionar proyectos | T008, T021, T024 | `app/models.py`, `app/seed.py`, `app/routers/api.py`, `app/static/js/app.js` | `test_list_projects_with_status` | Implementado | ✅ Probado | — |
| RF-03 | Mostrar estado del proyecto | T008, T021, T025 | `app/models.py` (enum `ProjectStatus`), `app/routers/api.py`, `app/static/js/app.js` | `test_list_projects_with_status` | Implementado | ✅ Probado | Render en UI verificado además manualmente (evidence/run-evidence.md) |
| RF-04 | Ingresar horas enteras positivas | T009, T012, T013, T026 | `app/schemas.py` (`gt=0`), `app/services/assignment_service.py`, `app/templates/index.html` | `test_create_valid_assignment`, `test_zero_hours_*`, `test_negative_hours_*` | Implementado | ✅ Probado | — |
| RF-05 | Verificar que el proyecto exista | T015, T018 | `app/services/assignment_service.py`, `app/routers/api.py` | `test_nonexistent_project_returns_400`, `test_nonexistent_project_is_rejected` | Implementado | ✅ Probado | — |
| RF-06 | Permitir solo si proyecto APPROVED | T016, T017 | `app/services/assignment_service.py` | `test_pending_project_*`, `test_rejected_project_*` | Implementado | ✅ Probado | — |
| RF-07 | Mensaje explicativo si no aprobado | T016, T019, T027 | `app/services/assignment_service.py`, `app/routers/api.py`, `app/static/js/app.js` | `test_pending_project_returns_400` (verifica contenido "aprobado") | Implementado | ✅ Probado | Mensaje de backend probado automáticamente; presentación en UI verificada manualmente |
| RF-08 | Rechazar horas ≤ 0, no enteras, no numéricas | T012, T013, T018 | `app/schemas.py`, `app/services/assignment_service.py`, `app/routers/api.py` | `test_zero/negative/non_integer/non_numeric_hours_returns_422` | Implementado | ✅ Probado | — |
| RF-09 | Almacenar asignaciones válidas | T009, T017, T018 | `app/models.py`, `app/services/assignment_service.py`, `app/routers/api.py` | `test_create_valid_assignment`, `test_valid_assignment_is_persisted` | Implementado | ✅ Probado | — |
| RF-10 | Consultar asignaciones registradas | T020, T028 | `app/routers/api.py`, `app/static/js/app.js` | `test_assignments_query_empty_then_populated` | Implementado | ✅ Probado | — |
| RF-11 | Validación en servidor, incluso por API directa | T016–T019 | `app/services/assignment_service.py`, `app/routers/api.py` | `test_rejected_requests_are_not_persisted` | Implementado | ✅ Probado | Probado mediante llamadas directas a la API (sin formulario) |

## 4. Cobertura de Requisitos

| Métrica | Valor |
|---------|-------|
| Total de requisitos funcionales | 11 |
| Requisitos implementados | 11 |
| Requisitos parcialmente implementados | 0 |
| Requisitos pendientes | 0 |
| **Porcentaje de cobertura (implementación)** | **(11 / 11) × 100 = 100 %** |
| Requisitos verificados por prueba automatizada | 11 |
| **Porcentaje de verificación (pruebas)** | **(11 / 11) × 100 = 100 %** |

**Diferenciación implementación vs. validación:** los 11 requisitos están implementados **y**
verificados por al menos una prueba automatizada que pasa. Observación de honestidad metodológica:
la **presentación visual** de los mensajes (RF-03 y RF-07 en la interfaz) se comprobó mediante el
*smoke test* manual registrado en `evidence/run-evidence.md`, no por una prueba automatizada de UI;
la lógica subyacente (estado y motivo devueltos por el backend) sí está cubierta automáticamente.

## 5. Cobertura de Tareas

| Métrica | Valor |
|---------|-------|
| Total de tareas (tasks.md) | 42 |
| Tareas completadas `[X]` | 42 |
| Tareas pendientes `[ ]` | 0 |
| **Porcentaje de avance** | **100 %** |

Distribución por fase: Preparación (T001–T006), Modelo de datos (T007–T012), Backend (T013–T021),
Frontend (T022–T029), Pruebas (T030–T036), Documentación (T037–T042). Los checkboxes se marcaron
tras ejecutar y verificar cada tarea.

## 6. Resultados de Pruebas

Ejecución real reproducida durante esta auditoría (no inventada):

| Campo | Valor |
|-------|-------|
| Comando utilizado | `pytest -v` (dentro de `.venv`, Python 3.11.9, pytest 9.1.1) |
| Total de pruebas ejecutadas | 20 |
| Pruebas aprobadas | 20 |
| Pruebas fallidas | 0 |
| Pruebas omitidas (skipped) | 0 |
| Advertencias | 1 (interna de `starlette.testclient`; ajena al código del prototipo) |

**Evidencia (línea final de pytest):**

```text
======================== 20 passed, 1 warning in 0.23s ========================
```

Desglose: 13 pruebas de API (`tests/test_api.py`) + 7 pruebas de servicio
(`tests/test_assignment_service.py`). Detalle completo en
`specs/001-research-hours-validation/evidence/test-results.md`. Las pruebas usan una base de datos
SQLite **en memoria aislada** (`tests/conftest.py`), sin alterar los datos de demostración.

## 7. Cumplimiento de la Constitución

Evaluación con evidencia (no por el mero hecho de estar documentado):

| Principio | Evaluación | Evidencia |
|-----------|------------|-----------|
| I. SDD | ✅ Cumple | Se siguió el flujo constitution→specify→clarify→plan→tasks→implement→analyze→converge; artefactos presentes |
| II. Trazabilidad | ✅ Cumple | IDs `RF-01..RF-11` y `T001..T042`; matriz RF→Tareas→Pruebas (sección 3) recorrible |
| III. Arquitectura modular | ✅ Cumple | Separación real: `models/schemas/database` (modelo), `templates/static` (vista), `routers` (controlador), `services` (negocio) |
| IV. Validación en servidor | ✅ Cumple | Reglas en `app/services/assignment_service.py`; `test_rejected_requests_are_not_persisted` prueba validación por API directa |
| V. Calidad y pruebas | ✅ Cumple | 20 pruebas (positivos, negativos, límite) en verde; cobertura por cada RF |
| VI. Seguridad básica | ✅ Cumple | Entradas validadas (Pydantic); acceso vía ORM parametrizado (sin SQL concatenado); sin credenciales en código; URL de BD vía variable de entorno (`app/config.py`) |
| VII. Simplicidad | ✅ Cumple | Un solo proyecto, sin capas superfluas; dependencia sin uso (`python-multipart`) eliminada en analyze |
| VIII. Requisitos verificables | ✅ Cumple | No se inventó normativa; pendientes institucionales marcados como `[PENDIENTE DE VALIDACIÓN]` |
| IX. Gestión de cambios | ✅ Cumple | Las clarificaciones y la corrección de notación (analyze) se propagaron a los artefactos |
| X. Documentación | ✅ Cumple | Artefactos académicos en español; código e identificadores en inglés; `README.md` presente |

**Conclusión del gate constitucional:** sin incumplimientos de principios MUST.

## 8. Hallazgos

- **Incumplimientos (constitución):** ninguno.
- **Defectos detectados y corregidos durante la implementación:**
  - La versión de Starlette (1.9.0) cambió la firma de `TemplateResponse`; `GET /` devolvía HTTP 500.
    Corregido en `app/routers/pages.py` a `TemplateResponse(request, "index.html")`; reverificado
    con *smoke test* (HTTP 200). Registrado en `evidence/run-evidence.md`.
- **Riesgos:**
  - Advertencia de dependencia interna de la librería (`starlette.testclient`/`httpx`): sin impacto
    funcional; a vigilar en futuras actualizaciones.
  - Cobertura de UI no automatizada: la presentación visual de mensajes/estado depende de
    verificación manual; riesgo bajo para un prototipo.
- **Requisitos no cubiertos:** ninguno (11/11 cubiertos y probados).
- **Dependencias institucionales pendientes** (no son defectos; esperan levantamiento):
  - Límite máximo y unidad de las horas de investigación — Unidad de Docencia / normativa.
  - Catálogo oficial de estados de proyecto — Unidad de Docencia / módulo de investigación.
  - Reglas de acumulación / duplicados de asignaciones — Unidad de Docencia / normativa.
  - Integración real con sistemas de la ESPE (APIs, autenticación) — UTIC (fuera de alcance).

## 9. Limitaciones

- La **integración institucional no se implementó**: el prototipo no se conecta a APIs, bases de
  datos ni credenciales reales de la ESPE.
- Los **docentes y proyectos son ficticios**; los estados (`APPROVED`/`PENDING`/`REJECTED`) son un
  supuesto de prototipo, no un catálogo oficial.
- La **normativa definitiva está pendiente**: no se aplican límites de horas ni reglas de
  acumulación por no estar confirmados.
- Esta prueba **no implica certificación ni validación institucional**; es un ejercicio académico
  demostrativo de la metodología SDD.
- La persistencia local (SQLite) es solo para demostración: sin concurrencia, respaldo ni alta
  disponibilidad.

## 10. Conclusiones y Recomendaciones

**Conclusión.** La primera iteración es **funcional, verificable y coherente con SDD**. Cobertura de
requisitos del **100 % (11/11)** implementada y verificada por **20/20** pruebas en verde; **42/42**
tareas completadas; cumplimiento íntegro de los diez principios de la constitución; y trazabilidad
recorrible de extremo a extremo (requisito → tarea → archivo → prueba). La convergencia
(`/speckit-converge`) devolvió **`converged`**: no quedan brechas de implementación respecto de los
artefactos.

**Recomendaciones.**
1. Realizar el **levantamiento normativo** con la Unidad de Docencia y UTIC para convertir los
   supuestos provisionales en requisitos confirmados (límites de horas, estados oficiales,
   duplicados) en una próxima iteración.
2. Añadir **pruebas automatizadas de interfaz** (o pruebas de extremo a extremo del navegador) para
   cubrir la presentación visual de mensajes y estado (actualmente verificada manualmente).
3. Preparar la **capa de integración** (adaptadores hacia APIs reales) como trabajo futuro, una vez
   disponibles accesos y contratos institucionales.
4. Mantener la disciplina SDD: todo cambio de regla debe propagarse a `spec.md`, `tasks.md` y
   pruebas antes de tocar el código (Principio IX).

---

*Documento generado como auditoría de cobertura (sexto entregable). Basado exclusivamente en
artefactos reales y en la ejecución comprobable de `pytest` del 2026-10-21.*
