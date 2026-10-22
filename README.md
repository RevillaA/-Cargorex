# Cargorex — Prototipo de Validación de Horas de Investigación

Primera iteración del **Módulo de Distribución de Carga Horaria Docente** de la Universidad de las
Fuerzas Armadas ESPE, desarrollada con **Spec-Driven Development (SDD)** usando GitHub Spec Kit.

> ⚠️ **Datos ficticios de demostración.** Este prototipo no se conecta a sistemas, APIs ni
> credenciales reales de la ESPE. Los docentes, proyectos y estados son de prueba y **no**
> representan un catálogo oficial.

## Descripción del prototipo

Aplicación web independiente que permite a un docente registrar **horas de investigación** asociadas
a un **proyecto**, validando en el servidor que el proyecto esté **aprobado** y que las horas sean un
**entero positivo** antes de persistir el registro. Las solicitudes inválidas se rechazan sin
almacenarse.

## Objetivo de la iteración

Validar la asignación de horas de investigación contra proyectos de prueba con estado *aprobado* o
*no aprobado*, demostrando la regla de negocio núcleo con validación en el backend, persistencia
local y pruebas automatizadas, manteniendo trazabilidad entre requisitos, tareas, implementación y
pruebas.

## Tecnologías

- **Python 3.11**
- **FastAPI** (servidor y servicios HTTP) + **Uvicorn** (servidor ASGI)
- **SQLAlchemy 2.x** (ORM) sobre **SQLite** (persistencia local)
- **Jinja2** + **HTML/CSS/JavaScript** (interfaz)
- **Pydantic v2** (validación de entrada)
- **pytest** + **httpx/TestClient** (pruebas)

## Arquitectura (MVC adaptado a FastAPI)

```text
app/
├── main.py                      # Punto de entrada; monta estáticos, routers; crea tablas y siembra
├── config.py                    # Configuración (URL de BD vía variable de entorno)
├── database.py                  # Engine, SessionLocal, Base (MODELO: persistencia)
├── models.py                    # Entidades ORM: Teacher, ResearchProject, ResearchAssignment
├── schemas.py                   # Esquemas Pydantic (validación de forma de datos)
├── seed.py                      # Datos ficticios (idempotente)
├── services/
│   └── assignment_service.py    # SERVICIO DE NEGOCIO: reglas de validación reutilizables
├── routers/
│   ├── pages.py                 # CONTROLADOR (vista HTML)
│   └── api.py                   # CONTROLADOR (API JSON)
├── templates/index.html         # VISTA
└── static/ (css, js)            # VISTA

tests/                           # pytest con base de datos aislada (in-memory)
```

- **Modelo**: `models.py`, `database.py`, `schemas.py`.
- **Vista**: `templates/`, `static/`.
- **Controlador**: `routers/`.
- **Servicio de negocio**: `services/assignment_service.py` — la regla "solo proyectos `APPROVED`,
  horas enteras > 0" vive aquí y se ejecuta **en el servidor**, independiente del cliente.

## Instalación en Windows (PowerShell)

```powershell
# Desde la raíz del repositorio
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

> Si PowerShell bloquea la activación del entorno:
> `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`

## Ejecución

```powershell
uvicorn app.main:app --reload
```

Abrir en el navegador: **http://127.0.0.1:8000**

Al iniciar, la aplicación crea `cargorex.db` (si no existe) y siembra datos ficticios: 3 docentes y 3
proyectos (uno `APPROVED`, uno `PENDING`, uno `REJECTED`).

### Endpoints principales

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/` | Página del prototipo (formulario + tabla) |
| GET | `/api/teachers` | Catálogo de docentes ficticios |
| GET | `/api/projects` | Catálogo de proyectos con estado |
| GET | `/api/assignments` | Asignaciones registradas |
| POST | `/api/assignments` | Registrar asignación (201 / 400 / 422) |

- **201**: proyecto aprobado + horas válidas → persiste.
- **400**: regla de negocio (proyecto no aprobado, proyecto/docente inexistente) → no persiste.
- **422**: entrada inválida (horas ≤ 0, no enteras, no numéricas) → no persiste.

## Pruebas

```powershell
pytest -v
```

Las pruebas usan una **base de datos SQLite en memoria aislada**: no tocan `cargorex.db` ni los datos
de demostración. Cubren escenarios positivos, negativos, casos límite y llamadas directas a la API.

Evidencias de ejecución y resultados de pruebas en
[`specs/001-research-hours-validation/evidence/`](specs/001-research-hours-validation/evidence/).

## Limitaciones del prototipo

- Sin autenticación ni autorización institucional.
- Sin integración con APIs, bases de datos ni módulos reales de la ESPE.
- **No** aplica límites normativos de horas (el máximo y la unidad quedan *pendientes de validación*
  con la Unidad de Docencia / normativa).
- El catálogo de estados (`APPROVED`/`PENDING`/`REJECTED`) es un supuesto de prototipo; el catálogo
  oficial queda *pendiente de validación*.
- Reglas de acumulación / duplicados de asignaciones *pendientes de validación*.
- Persistencia local orientada solo a demostración (sin concurrencia, respaldo ni alta
  disponibilidad).
- Alcance acotado: solo la validación de horas de investigación, **no** la totalidad de Cargorex.

## Trazabilidad (SDD)

Los artefactos del proceso están en `specs/001-research-hours-validation/`:
`spec.md` (requisitos RF-01…RF-11), `plan.md`, `data-model.md`, `contracts/openapi.yaml`,
`research.md`, `quickstart.md` y `tasks.md`. La constitución del proyecto está en
`.specify/memory/constitution.md`.
