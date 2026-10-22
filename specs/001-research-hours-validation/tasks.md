---
description: "Lista de tareas para la implementación de la feature"
---

# Tareas: Validación de Horas de Investigación mediante Proyectos Aprobados

**Input**: Documentos de diseño en `specs/001-research-hours-validation/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/openapi.yaml, quickstart.md

**Tests**: Incluidos — solicitados explícitamente y exigidos por el Principio V de la constitución.

**Organización**: Se conservan las **6 fases** solicitadas. Cada tarea lleva, cuando aplica, la
etiqueta de historia de usuario (`[US1]`, `[US2]`, `[US3]`) y las referencias a requisitos (RF) para
mantener la trazabilidad (Principio II). Mapeo de historias: **US1** = registrar/validar asignación
(P1); **US2** = consultar asignaciones (P2); **US3** = catálogo y estado de proyectos (P3).

## Formato: `[ID] [P?] [Story?] Descripción (RF) → ruta`

- **[P]**: paralelizable (archivo distinto, sin dependencias con tareas incompletas).
- **[US?]**: historia de usuario asociada (solo en fases de historia).
- Toda tarea indica su archivo y un **resultado verificable**.

> ⚠️ Regla operativa: **no marcar una tarea como completada `[x]` sin ejecutarla** (Principio IX /
> condición del taller). No agregar funcionalidades fuera de alcance.

---

## FASE 1: Preparación (Setup — infraestructura compartida)

**Propósito**: inicializar el proyecto y su estructura. Sin dependencias previas.

- [X] T001 Crear la estructura de carpetas (`app/`, `app/services/`, `app/routers/`,
  `app/templates/`, `app/static/css/`, `app/static/js/`, `tests/`) según plan.md →
  árbol de carpetas. **Verificable**: las carpetas existen con sus `__init__.py` donde aplica.
- [X] T002 Declarar dependencias en `requirements.txt` (fastapi, uvicorn, sqlalchemy, jinja2,
  pydantic, pytest, httpx) → `requirements.txt`. **Verificable**:
  `pip install -r requirements.txt` instala sin errores en el `.venv`.
- [X] T003 [P] Crear `.gitignore` excluyendo `.venv/`, `__pycache__/`, `*.db` → `.gitignore`.
  **Verificable**: los artefactos listados no aparecen como seguibles.
- [X] T004 [P] Crear configuración del entorno: ruta de BD vía variable de entorno
  (`CARGOREX_DB_URL`, por defecto `sqlite:///./cargorex.db`), sin secretos en código (Principio VI)
  → `app/config.py`. **Verificable**: `config` expone la URL y respeta la variable de entorno.
- [X] T005 Crear capa de base de datos: `engine`, `SessionLocal`, `Base` de SQLAlchemy a partir de
  `config` → `app/database.py`. **Verificable**: importar el módulo no lanza error y crea el engine.
- [X] T006 Configurar el servidor FastAPI inicial: instancia `app`, montaje de `static/`,
  configuración de `Jinja2Templates`, inclusión de routers (vacíos aún) y gancho de arranque que
  invoca la siembra → `app/main.py`. **Verificable**: `uvicorn app.main:app` levanta y responde en
  `/docs`.

**Checkpoint**: proyecto ejecutable con servidor vacío.

---

## FASE 2: Modelo de datos (Foundational — bloquea todas las historias)

**Propósito**: entidades, persistencia SQLite y datos de prueba. **⚠️ Ninguna historia puede
completarse antes de terminar esta fase.**

- [X] T007 [P] Definir el modelo `Teacher` (`id` Integer PK autoincremental; `name` String(120) NOT
  NULL) (RF-01) → `app/models.py`. **Verificable**: la tabla `teacher` se crea con esas columnas.
- [X] T008 [P] Definir la enumeración `ProjectStatus` (`APPROVED`, `PENDING`, `REJECTED`) y el modelo
  `ResearchProject` (`id` PK; `code` String(30) NOT NULL UNIQUE; `name` String(150) NOT NULL;
  `status` Enum(ProjectStatus) NOT NULL) (RF-02, RF-03) → `app/models.py`. **Verificable**: la tabla
  `research_project` se crea; `code` es único.
- [X] T009 [P] Definir el modelo `ResearchAssignment` (`id` PK; `teacher_id` FK→`teacher.id` NOT
  NULL; `project_id` FK→`research_project.id` NOT NULL; `hours` Integer NOT NULL con restricción
  `> 0`; `created_at` DateTime NOT NULL default ahora UTC) (RF-09) → `app/models.py`.
  **Verificable**: la tabla `research_assignment` se crea con FKs y restricción de horas.
- [X] T010 Configurar SQLite y la creación de tablas (`Base.metadata.create_all`) invocada al
  arranque → `app/database.py` + gancho en `app/main.py`. **Verificable**: al iniciar se genera
  `cargorex.db` con las tres tablas.
- [X] T011 Crear la siembra **idempotente** de datos ficticios: ≥2 docentes de prueba y ≥3 proyectos
  (uno `APPROVED`, uno `PENDING`, uno `REJECTED`), marcados como datos de prueba; no duplica si ya
  existen → `app/seed.py`. **Verificable**: tras dos arranques, los catálogos no se duplican y
  cubren los tres estados.
- [X] T012 [P] Definir los esquemas Pydantic: `TeacherOut`, `ResearchProjectOut`, `AssignmentCreate`
  (`teacher_id`, `project_id`, `hours` entero con `gt=0`) y `ResearchAssignmentOut` (RF-04, RF-08)
  → `app/schemas.py`. **Verificable**: `AssignmentCreate` rechaza `hours<=0` y no enteros a nivel de
  esquema (HTTP 422 en FastAPI).

**Checkpoint**: modelo y datos listos; las historias pueden comenzar.

---

## FASE 3: Backend (validaciones, registro, consulta, manejo de errores)

**Propósito**: implementar la lógica de negocio en una capa de servicio reutilizable (Principio IV)
y exponerla por la API. La regla principal pertenece a **US1**; la consulta a **US2**; los catálogos
a **US3**.

> Las tareas T013–T017 editan el mismo archivo `app/services/assignment_service.py`, por lo que son
> **secuenciales** entre sí (no `[P]`).

- [X] T013 [US1] Implementar validación de horas en el servicio (entero y `> 0`; rechazo → error de
  entrada que la ruta traducirá a 422) (RF-04, RF-08, CA-04) → `app/services/assignment_service.py`.
  **Verificable**: `hours=0`, `-3` o no entero producen rechazo sin persistir.
- [X] T014 [US1] Implementar validación de docente existente en el catálogo (rechazo → regla de
  negocio, 400) (RF-01) → `app/services/assignment_service.py`. **Verificable**: `teacher_id`
  inexistente se rechaza.
- [X] T015 [US1] Implementar validación de proyecto existente (rechazo → 400) (RF-05, CA-05) →
  `app/services/assignment_service.py`. **Verificable**: `project_id` inexistente se rechaza.
- [X] T016 [US1] Implementar verificación de proyecto en estado `APPROVED`; estados `PENDING`,
  `REJECTED` o desconocido se rechazan con mensaje explicativo (400) (RF-06, RF-07, CA-02, CA-03) →
  `app/services/assignment_service.py`. **Verificable**: proyecto no aprobado se rechaza con motivo.
- [X] T017 [US1] Implementar el registro de la asignación válida: persistir `ResearchAssignment` solo
  tras pasar T013–T016; devolver la entidad creada (RF-09, CA-01, CA-07) →
  `app/services/assignment_service.py`. **Verificable**: con proyecto aprobado y horas válidas, se
  crea un registro.
- [X] T018 [US1] Implementar el endpoint `POST /api/assignments` que delega en el servicio y mapea:
  entrada inválida → **422**, regla de negocio → **400**, éxito → **201** (RF-09, RF-11, CA-01–CA-05,
  CA-07) → `app/routers/api.py`. **Verificable**: contrato de `contracts/openapi.yaml` respetado.
- [X] T019 [US1] Implementar el manejo de errores de negocio como respuesta JSON `{"detail": "..."}`
  (excepción de dominio → handler/HTTPException 400) (RF-07, RF-11) → `app/routers/api.py` (+ main si
  requiere handler). **Verificable**: los rechazos devuelven JSON con motivo legible.
- [X] T020 [US2] Implementar el endpoint `GET /api/assignments` para consultar asignaciones
  registradas (lista, posiblemente vacía) (RF-10, CA-06) → `app/routers/api.py`. **Verificable**:
  devuelve 200 con las asignaciones existentes.
- [X] T021 [P] [US3] Implementar los endpoints `GET /api/teachers` y `GET /api/projects` (este último
  incluye `status`) (RF-01, RF-02, RF-03) → `app/routers/api.py`. **Verificable**: devuelven los
  catálogos ficticios con su estado.

**Checkpoint**: backend funcional y verificable vía `/docs` o `curl`/`Invoke-WebRequest`.

---

## FASE 4: Frontend (vista)

**Propósito**: interfaz web sencilla servida con Jinja2 + JS. Consume la API; las validaciones del
cliente son solo asistencia (la autoridad es el servidor).

- [X] T022 [US1] Crear la plantilla `index.html`: encabezado del prototipo Cargorex, **aviso visible
  de datos ficticios** y contenedor del formulario (RF) → `app/templates/index.html`.
  **Verificable**: `GET /` muestra encabezado y aviso.
- [X] T023 [US1] Implementar la ruta de la página (`GET /`) que renderiza `index.html` →
  `app/routers/pages.py` (+ inclusión en `app/main.py`). **Verificable**: la página carga sin error.
- [X] T024 [P] [US3] Poblar los selectores de docente y proyecto consumiendo `/api/teachers` y
  `/api/projects` (RF-01, RF-02) → `app/static/js/app.js`. **Verificable**: los `<select>` se llenan
  con datos de prueba.
- [X] T025 [P] [US3] Mostrar el estado del proyecto seleccionado (aprobado/pendiente/rechazado)
  (RF-03) → `app/static/js/app.js` + `app/templates/index.html`. **Verificable**: al elegir un
  proyecto se ve su estado.
- [X] T026 [US1] Añadir el campo de horas y el botón de registrar; enviar `POST /api/assignments`
  (RF-04) → `app/templates/index.html` + `app/static/js/app.js`. **Verificable**: el formulario
  envía la solicitud.
- [X] T027 [US1] Mostrar mensajes de resultado/validación según la respuesta (éxito, 400 con motivo,
  422 entrada inválida) (RF-07, RF-08) → `app/static/js/app.js`. **Verificable**: cada tipo de
  respuesta muestra su mensaje.
- [X] T028 [US2] Renderizar la tabla de asignaciones registradas consumiendo `/api/assignments`
  (RF-10) → `app/templates/index.html` + `app/static/js/app.js`. **Verificable**: la tabla refleja
  los registros tras una alta válida.
- [X] T029 [P] Crear los estilos base (incluye resaltado del aviso de datos ficticios) →
  `app/static/css/styles.css`. **Verificable**: la página se muestra con estilos aplicados.

**Checkpoint**: flujo web completo operativo de principio a fin.

---

## FASE 5: Pruebas (pytest)

**Propósito**: verificar automáticamente cada regla. Base de datos **aislada** de la de ejecución.
Cobertura por requisito (SC-007). *Recomendado escribir/ejecutar antes de cerrar las tareas de
implementación relacionadas (enfoque test-first del Principio III/V).*

- [X] T030 Configurar pytest y fixtures con **base de datos aislada** (SQLite in-memory o archivo
  temporal) y `TestClient`, con override de la dependencia de sesión → `tests/conftest.py`.
  **Verificable**: las pruebas no tocan `cargorex.db`.
- [X] T031 [P] [US1] Pruebas unitarias del servicio — **caso válido**: registro con proyecto
  aprobado y horas positivas persiste (CA-01, RF-09) → `tests/test_assignment_service.py`.
  **Verificable**: test pasa en verde.
- [X] T032 [P] [US1] Pruebas unitarias del servicio — **casos inválidos**: proyecto pendiente
  (CA-02), proyecto rechazado (CA-03), proyecto inexistente (CA-05), docente inexistente (RF-01),
  horas = 0 y negativas (CA-04), horas no enteras (RF-08) → `tests/test_assignment_service.py`.
  **Verificable**: cada caso se rechaza con el tipo de error esperado.
- [X] T033 [P] [US1] Pruebas de **API** sobre `POST /api/assignments`, incluyendo **llamadas directas
  a la API** (sin formulario) que confirman 400 (negocio) y 422 (entrada) (RF-11, CA-07) →
  `tests/test_api.py`. **Verificable**: los códigos HTTP coinciden con el contrato.
- [X] T034 [P] [US1] Pruebas de **persistencia**: verificar que un alta válida queda almacenada y que
  **ninguna** solicitud rechazada se persiste (SC-004, CA-07) → `tests/test_api.py`. **Verificable**:
  el conteo de filas refleja solo las altas válidas.
- [X] T035 [P] [US2] Pruebas de **consulta** `GET /api/assignments`: lista vacía sin error y listado
  tras un alta (CA-06, RF-10) → `tests/test_api.py`. **Verificable**: tests pasan.
- [X] T036 [P] [US3] Pruebas de **catálogos** `GET /api/teachers` y `GET /api/projects` con estados
  (RF-01, RF-02, RF-03) → `tests/test_api.py`. **Verificable**: devuelven datos ficticios y estados.

**Checkpoint**: `pytest -v` en verde cubriendo RF-01…RF-11.

---

## FASE 6: Documentación (Polish & cross-cutting)

**Propósito**: documentación reproducible y evidencias (en español; Principio X).

- [X] T037 Crear `README.md`: descripción del prototipo, aviso de datos ficticios y enlace a
  `specs/001-research-hours-validation/quickstart.md` → `README.md`. **Verificable**: el README
  describe el proyecto y su alcance.
- [X] T038 [P] Documentar las **instrucciones de instalación** en Windows PowerShell (venv +
  `pip install -r requirements.txt`) → `README.md`. **Verificable**: un tercero instala siguiendo los
  pasos.
- [X] T039 [P] Documentar las **instrucciones de ejecución** (`uvicorn app.main:app --reload`,
  `pytest -v`) → `README.md`. **Verificable**: los comandos ejecutan la app y las pruebas.
- [X] T040 Registrar **evidencias de funcionamiento** de los escenarios E1–E9 de quickstart.md
  (salidas/capturas) → `specs/001-research-hours-validation/evidence/` (o sección en README).
  **Verificable**: existe evidencia de al menos un caso válido y varios rechazos.
- [X] T041 Registrar los **resultados de las pruebas** (salida de `pytest -v`) →
  `specs/001-research-hours-validation/evidence/test-results.md`. **Verificable**: consta la salida
  de pytest.
- [X] T042 Ejecutar la **validación de quickstart.md** de extremo a extremo (E1–E9) →
  `specs/001-research-hours-validation/quickstart.md`. **Verificable**: todos los escenarios se
  comportan como se espera.

---

## Matriz de Trazabilidad (RF → Tareas → Pruebas)

| Requisito | Tareas de implementación | Pruebas |
|-----------|--------------------------|---------|
| RF-01 (seleccionar docente) | T007, T014, T021, T024 | T032, T036 |
| RF-02 (seleccionar proyecto) | T008, T021, T024 | T036 |
| RF-03 (mostrar estado) | T008, T021, T025 | T036 |
| RF-04 (horas positivas) | T009, T012, T013, T026 | T031, T032 |
| RF-05 (proyecto existe) | T015, T018 | T032, T033 |
| RF-06 (solo aprobado) | T016, T017 | T031, T032 |
| RF-07 (mensaje si no aprobado) | T016, T019, T027 | T032, T033 |
| RF-08 (rechazar horas/entrada inválida) | T012, T013, T018 | T032, T033 |
| RF-09 (almacenar válidas) | T009, T017, T018 | T031, T034 |
| RF-10 (consultar registros) | T020, T028 | T035 |
| RF-11 (validación en servidor, API directa) | T016, T017, T018, T019 | T033, T034 |

---

## Dependencias y Orden de Ejecución

### Dependencias entre fases

- **FASE 1 (Setup)**: sin dependencias — inicia de inmediato.
- **FASE 2 (Modelo)**: depende de FASE 1 — **bloquea** FASES 3–6.
- **FASE 3 (Backend)**: depende de FASE 2.
- **FASE 4 (Frontend)**: depende de FASE 3 (consume la API).
- **FASE 5 (Pruebas)**: `conftest` (T030) depende de FASE 2; las pruebas por historia dependen de su
  implementación en FASE 3 (y T036/T035 de los endpoints respectivos). Recomendado escribirlas en
  paralelo a FASE 3 (test-first).
- **FASE 6 (Documentación)**: depende de FASES 3–5 (requiere app funcionando y pruebas ejecutadas).

### Dependencias entre historias

- **US1 (P1)** es el MVP; **US2 (P2)** y **US3 (P3)** dependen solo de la FASE 2 y son testeables de
  forma independiente. US2 (tabla) muestra valor pleno tras existir un alta de US1.

### Dentro de cada historia

- Modelos (FASE 2) → servicio (T013–T017) → endpoints (T018–T021) → vista (FASE 4).
- Las tareas sobre `assignment_service.py` (T013–T017) y sobre `api.py` (T018–T021) son secuenciales
  por compartir archivo.

### Oportunidades de paralelización `[P]`

- FASE 1: T003 y T004 en paralelo.
- FASE 2: T007, T008, T009 (modelos) y T012 (esquemas) en paralelo — archivos/porciones distintas.
- FASE 3: T021 en paralelo respecto a las tareas de `assignment_service.py`.
- FASE 4: T024, T025 y T029 en paralelo.
- FASE 5: T031–T036 en paralelo una vez disponible `conftest` (T030) y los endpoints implicados.
- FASE 6: T038 y T039 en paralelo.

---

## Estrategia de Implementación

### MVP primero (US1)

1. FASE 1 (Setup) → 2. FASE 2 (Modelo) → 3. FASE 3 tareas de US1 (T013–T019) → 4. FASE 4 tareas de
   US1 (T022, T023, T026, T027) → 5. FASE 5 pruebas de US1 (T030–T034). **Validar US1 de forma
   aislada** antes de continuar.

### Entrega incremental

- US1 (registro+validación) → US2 (consulta: T020, T028, T035) → US3 (catálogo/estado: T021,
  T024, T025, T036). Cada historia agrega valor sin romper la anterior.

---

## Notas

- `[P]` = archivos distintos, sin dependencias.
- La etiqueta `[US]` liga cada tarea a su historia para trazabilidad (Principio II).
- Verificar que las pruebas fallan antes de implementar (enfoque test-first recomendado).
- **No marcar `[x]` sin ejecutar la tarea** (condición del taller / Principio IX).
- No añadir funcionalidades fuera de alcance (ver sección *Out of Scope* de spec.md).
