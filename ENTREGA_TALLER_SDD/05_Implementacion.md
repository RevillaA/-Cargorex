# Evidencia de Implementación (Speckit-implement) — Cargorex, Iteración 1

**Feature:** `001-research-hours-validation` · **Fecha:** 2026-10-21

## 1. Introducción

El objetivo de esta primera iteración del proyecto **Cargorex-SDD** es construir un prototipo web
independiente que valide la asignación de **horas de investigación** de un docente contra un
**proyecto de investigación**, permitiendo la persistencia únicamente cuando el proyecto esté
**aprobado** y las horas sean un **entero positivo**. El desarrollo se realizó bajo la metodología
*Spec-Driven Development* (SDD) con GitHub Spec Kit, partiendo de la constitución, la especificación,
el plan y las tareas previamente aprobados. Todos los datos son ficticios y no existe conexión con
sistemas reales de la ESPE.

## 2. Alcance Implementado

Se desarrollaron exclusivamente las funcionalidades contempladas en `spec.md`:

- Catálogo de **docentes** ficticios de prueba (RF-01).
- Catálogo de **proyectos** ficticios con su **estado** aprobado/pendiente/rechazado (RF-02, RF-03).
- Registro de **horas de investigación** como entero positivo (RF-04).
- **Validación en el servidor**: existencia de docente y proyecto, estado aprobado y horas válidas
  (RF-05, RF-06, RF-08, RF-11).
- **Mensajes explicativos** ante rechazos (RF-07).
- **Persistencia** de asignaciones válidas en SQLite (RF-09).
- **Consulta** de asignaciones registradas (RF-10).
- Interfaz web sencilla con formulario y tabla de resultados.
- Suite de **pruebas automatizadas** con pytest sobre base de datos aislada.

No se implementó —por estar fuera de alcance— ninguna integración institucional, autenticación,
límites normativos de horas ni reportería (ver sección 10).

## 3. Arquitectura

Se aplicó una separación **MVC adaptada a FastAPI**, con una **capa de servicio** que concentra la
lógica de negocio y garantiza la validación en el servidor (Principio IV de la constitución):

- **Modelo (datos y persistencia):** entidades ORM (`app/models.py`), configuración y sesión de base
  de datos (`app/database.py`, `app/config.py`) y esquemas de validación de entrada/salida
  (`app/schemas.py`).
- **Vista (presentación):** plantilla Jinja2 (`app/templates/index.html`), estilos
  (`app/static/css/styles.css`) y lógica de cliente (`app/static/js/app.js`).
- **Controlador (coordinación HTTP):** rutas de página (`app/routers/pages.py`) y de API
  (`app/routers/api.py`).
- **Servicio de negocio (reglas reutilizables):** `app/services/assignment_service.py`, donde reside
  la regla "solo proyectos `APPROVED`, horas enteras > 0", invocable tanto por la API como por las
  pruebas, independiente del cliente.

El punto de entrada (`app/main.py`) ensambla las capas: monta los archivos estáticos, incluye los
routers y, en el arranque (evento `lifespan`), crea las tablas y siembra los datos ficticios.

## 4. Estructura del Proyecto

Árbol real de los archivos principales (se omiten `__pycache__`, `.venv` y la base de datos local):

```text
cargorex-sdd/
├── app/
│   ├── __init__.py
│   ├── config.py                     # Configuración (URL de BD vía variable de entorno)
│   ├── database.py                   # Engine, SessionLocal, Base, dependencia get_db
│   ├── main.py                       # Entrada FastAPI; estáticos, routers, creación/siembra
│   ├── models.py                     # Teacher, ResearchProject, ResearchAssignment, ProjectStatus
│   ├── schemas.py                    # Esquemas Pydantic (validación de forma)
│   ├── seed.py                       # Datos ficticios idempotentes
│   ├── services/
│   │   └── assignment_service.py     # Reglas de negocio (validación en servidor)
│   ├── routers/
│   │   ├── pages.py                  # Vista HTML (GET /)
│   │   └── api.py                    # API JSON (teachers, projects, assignments)
│   ├── templates/
│   │   └── index.html                # Vista principal
│   └── static/
│       ├── css/styles.css
│       └── js/app.js
├── tests/
│   ├── conftest.py                   # Fixtures con BD en memoria aislada + TestClient
│   ├── test_assignment_service.py    # Pruebas unitarias del servicio
│   └── test_api.py                   # Pruebas de integración de la API
├── requirements.txt
├── .gitignore
└── README.md
```

## 5. Funcionalidades Desarrolladas

### F1 — Listado de docentes de prueba
- **Requisito:** RF-01.
- **Descripción:** expone el catálogo de docentes ficticios sembrados al iniciar.
- **Archivos:** `app/models.py` (`Teacher`), `app/seed.py`, `app/routers/api.py` (`GET /api/teachers`),
  `app/static/js/app.js`.
- **Resultado:** la API devuelve los docentes y el formulario los carga en su selector.

### F2 — Listado de proyectos y su estado
- **Requisito:** RF-02, RF-03.
- **Descripción:** expone proyectos ficticios con estado `APPROVED`, `PENDING` o `REJECTED`.
- **Archivos:** `app/models.py` (`ResearchProject`, `ProjectStatus`), `app/seed.py`,
  `app/routers/api.py` (`GET /api/projects`), `app/static/js/app.js`.
- **Resultado:** la API devuelve los proyectos con su estado; la interfaz muestra el estado del
  proyecto seleccionado.

### F3 — Registro validado de horas de investigación
- **Requisito:** RF-04, RF-05, RF-06, RF-08, RF-09, RF-11.
- **Descripción:** valida en el servidor (horas entero > 0, docente y proyecto existentes, proyecto
  aprobado) y persiste solo si todo es correcto.
- **Archivos:** `app/schemas.py` (`AssignmentCreate`), `app/services/assignment_service.py`
  (`create_assignment`), `app/routers/api.py` (`POST /api/assignments`), `app/models.py`
  (`ResearchAssignment`), `app/templates/index.html`, `app/static/js/app.js`.
- **Resultado:** proyecto aprobado + horas válidas → HTTP **201** y registro almacenado; cualquier
  incumplimiento → **400** (negocio) o **422** (entrada) sin persistir.

### F4 — Mensajes de rechazo comprensibles
- **Requisito:** RF-07.
- **Descripción:** ante un rechazo, el backend devuelve un motivo legible en JSON y la interfaz lo
  muestra.
- **Archivos:** `app/services/assignment_service.py` (mensajes de error), `app/routers/api.py`
  (mapeo a `HTTPException` con `detail`), `app/static/js/app.js`.
- **Resultado:** p. ej., "El proyecto seleccionado no esta aprobado (estado: PENDING)…".

### F5 — Consulta de asignaciones registradas
- **Requisito:** RF-10.
- **Descripción:** lista las asignaciones válidas almacenadas.
- **Archivos:** `app/routers/api.py` (`GET /api/assignments`), `app/static/js/app.js`,
  `app/templates/index.html` (tabla).
- **Resultado:** la tabla refleja los registros; lista vacía sin error cuando no hay datos.

> Toda afirmación anterior está respaldada por los archivos citados y por las pruebas de la sección 7.

## 6. Flujo de Funcionamiento

1. El docente abre la página (`GET /`), que se renderiza con el aviso visible de datos ficticios.
2. El cliente (`app.js`) consulta `GET /api/teachers` y `GET /api/projects` y puebla los selectores;
   al elegir un proyecto se muestra su estado.
3. El docente ingresa las horas y envía el formulario, que realiza `POST /api/assignments` con un
   cuerpo JSON (`teacher_id`, `project_id`, `hours`).
4. En el servidor, **Pydantic** valida la forma (horas entero > 0); si falla, responde **422**.
5. Si la forma es válida, el router delega en `assignment_service.create_assignment`, que verifica en
   orden: horas > 0, existencia de docente, existencia de proyecto y estado `APPROVED`. Cualquier
   regla incumplida lanza un error de negocio → **400**, sin persistir.
6. Si todas las reglas pasan, se crea el `ResearchAssignment`, se confirma la transacción y se
   devuelve **201** con el registro.
7. El cliente muestra el mensaje de resultado y recarga la tabla mediante `GET /api/assignments`.

Este flujo garantiza que la validación resida en el servidor y sea efectiva incluso si la solicitud
se envía directamente a la API sin usar el formulario (RF-11).

## 7. Casos de Prueba

Implementados en `tests/test_assignment_service.py` (unitarias) y `tests/test_api.py` (integración):

**Positivos**
- Registro con proyecto aprobado y horas positivas → aceptado (CA-01): `test_valid_assignment_is_persisted`, `test_create_valid_assignment`.
- Consulta de asignaciones (vacía y poblada) (CA-06, RF-10): `test_assignments_query_empty_then_populated`.
- Catálogos de docentes y proyectos con estados (RF-01, RF-02, RF-03): `test_list_teachers`, `test_list_projects_with_status`.

**Negativos / límite**
- Proyecto pendiente → rechazado 400 (CA-02): `test_pending_project_*`.
- Proyecto rechazado → rechazado 400 (CA-03): `test_rejected_project_*`.
- Proyecto inexistente → rechazado 400 (CA-05): `test_nonexistent_project_*`.
- Docente inexistente → rechazado 400 (RF-01): `test_nonexistent_teacher_*`.
- Horas = 0 y negativas → rechazado 422 (CA-04): `test_zero_hours_*`, `test_negative_hours_*`.
- Horas no enteras / no numéricas → rechazado 422 (RF-08): `test_non_integer_hours_returns_422`, `test_non_numeric_hours_returns_422`.
- Solicitudes inválidas por API directa → ninguna persistida (RF-11, CA-07): `test_rejected_requests_are_not_persisted`.

## 8. Resultados de Pruebas

Ejecución real y verificable (no inventada):

- **Comando:** `pytest -v` (dentro de `.venv`, Python 3.11.9, pytest 9.1.1).
- **Total:** 20 · **Aprobadas:** 20 · **Fallidas:** 0 · **Omitidas:** 0 · **Advertencias:** 1
  (interna de `starlette.testclient`, ajena al código).

```text
======================== 20 passed, 1 warning in 0.23s ========================
```

Detalle completo en `specs/001-research-hours-validation/evidence/test-results.md`. Las pruebas usan
una base de datos SQLite **en memoria aislada** (`tests/conftest.py`), por lo que no alteran los
datos de demostración.

## 9. Evidencias

No existen capturas de imagen en el repositorio al momento de redactar este documento. A
continuación se indica **qué evidencia gráfica debe adjuntarse** y la evidencia **textual** ya
disponible. Las imágenes deberán guardarse en
`specs/001-research-hours-validation/evidence/` y enlazarse en los espacios señalados.

| # | Evidencia a adjuntar | Cómo obtenerla | Estado |
|---|----------------------|----------------|--------|
| 1 | **Formulario** (página principal) | Abrir `http://127.0.0.1:8000/` y capturar | ⏳ Pendiente de adjuntar — `evidence/01-formulario.png` |
| 2 | **Registro aceptado** | Enviar proyecto aprobado + horas válidas; capturar mensaje 201 y tabla | ⏳ Pendiente — `evidence/02-registro-aceptado.png` |
| 3 | **Registro rechazado** | Enviar proyecto pendiente/rechazado o horas inválidas; capturar mensaje de error | ⏳ Pendiente — `evidence/03-registro-rechazado.png` |
| 4 | **Consulta de asignaciones** | Capturar la tabla con registros | ⏳ Pendiente — `evidence/04-consulta.png` |
| 5 | **Ejecución de pruebas** | Captura de la terminal con la salida de `pytest -v` | ⏳ Pendiente — `evidence/05-pytest.png` |

**Evidencia textual ya disponible (verificable):**
- Salida de pytest: `specs/001-research-hours-validation/evidence/test-results.md`.
- Comprobación funcional por *smoke test* vía PowerShell (GET /, catálogos, 201/400/422, consulta):
  `specs/001-research-hours-validation/evidence/run-evidence.md`.

> Plantilla para insertar una imagen una vez capturada:
> `![Formulario](evidence/01-formulario.png)`

## 10. Limitaciones y Trabajo Futuro

**Desarrollado en esta iteración:** validación de horas de investigación contra proyectos aprobados,
con datos ficticios, persistencia local, interfaz sencilla y pruebas automatizadas.

**Pendiente (trabajo institucional / fuera de alcance):**
- Integración con APIs, bases de datos y autenticación reales de la ESPE (UTIC).
- Aplicación de **límites normativos** de horas (máximo, unidad) — pendiente de la Unidad de Docencia
  y la normativa.
- Definición del **catálogo oficial de estados** de proyecto.
- Reglas de **acumulación / duplicados** de asignaciones.
- Aprobaciones departamentales, reportería institucional y distribución completa de carga horaria.

Estas limitaciones están registradas de forma consistente en `spec.md`, `research.md` y `coverage.md`
como supuestos provisionales o dependencias pendientes de validación, sin inventar normativa.

## 11. Conclusiones

La primera iteración se completó de forma **funcional y verificable**: se implementaron los 11
requisitos funcionales (RF-01…RF-11), respaldados por 20 pruebas automatizadas que pasan, con una
arquitectura modular que sitúa la validación en el servidor conforme a la constitución del proyecto.
El prototipo demuestra, con datos ficticios, la regla de negocio núcleo (solo proyectos aprobados y
horas enteras positivas) y mantiene trazabilidad de extremo a extremo entre requisitos, tareas,
código y pruebas.

## 12. Recomendaciones

1. Realizar el **levantamiento funcional definitivo** con la Unidad de Docencia y UTIC para convertir
   los supuestos provisionales en requisitos confirmados (límites de horas, estados oficiales,
   duplicados).
2. Adjuntar las **capturas de evidencia** señaladas en la sección 9 para completar el soporte gráfico
   del entregable.
3. Incorporar **pruebas automatizadas de interfaz** (end-to-end de navegador) que cubran la
   presentación visual, hoy verificada manualmente.
4. Diseñar la **capa de integración** (adaptadores hacia servicios institucionales) una vez
   disponibles accesos y contratos reales.
5. Mantener la disciplina SDD: todo cambio de regla debe reflejarse primero en `spec.md`, `tasks.md`
   y las pruebas antes de modificar el código.
