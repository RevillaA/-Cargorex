# Plan de Implementación: Validación de Horas de Investigación mediante Proyectos Aprobados

**Branch / Feature**: `001-research-hours-validation` | **Date**: 2026-10-21 | **Spec**: [spec.md](./spec.md)

**Input**: Especificación funcional en `specs/001-research-hours-validation/spec.md`

## Summary

Prototipo web independiente que valida la asignación de horas de investigación de un docente contra
un proyecto de investigación, permitiendo persistir el registro **únicamente** cuando el proyecto
tiene estado `APPROVED` y las horas son un entero positivo. La validación se realiza **en el
servidor** (independiente del cliente) y las solicitudes inválidas se rechazan sin persistir
(HTTP 422 para entrada inválida, HTTP 400 para regla de negocio). Enfoque técnico: FastAPI + SQLite
+ SQLAlchemy con una **arquitectura MVC adaptada** que aísla la lógica de negocio en una capa de
servicio reutilizable; frontend servido con Jinja2 + JS; pruebas con pytest sobre la capa de
servicio y sobre la API vía `TestClient`. Datos de docentes y proyectos **ficticios**, sembrados al
iniciar.

## Technical Context

**Language/Version**: Python 3.11 (intérprete `python` del sistema)

**Primary Dependencies**: FastAPI, Uvicorn (ASGI server), SQLAlchemy 2.x (ORM), Jinja2 (vistas),
Pydantic v2 (validación de entrada), httpx (cliente de pruebas vía `TestClient`)

> Nota: el formulario envía JSON mediante `fetch` a la API (el contrato solo define JSON), por lo que
> no se requiere `python-multipart` (dependencia de formularios `Form()`) en esta iteración.

**Storage**: SQLite local (archivo `cargorex.db`); acceso mediante SQLAlchemy con sesiones y
consultas parametrizadas por el ORM (sin SQL por concatenación)

**Testing**: pytest + FastAPI `TestClient`; base de datos SQLite en memoria o archivo temporal por
sesión de pruebas (aislada de la de ejecución)

**Target Platform**: Aplicación web local ejecutada en Windows 11 con PowerShell; navegador moderno
para el frontend

**Project Type**: Web service con frontend servido por el mismo backend (single project, no SPA)

**Performance Goals**: No crítico (prototipo demostrable). Objetivo cualitativo: respuestas
percibidas como instantáneas en uso local de un solo usuario

**Constraints**: Sin autenticación, sin integraciones externas, sin límite máximo de horas
(PENDIENTE DE VALIDACIÓN), datos exclusivamente ficticios, ejecución offline local

**Scale/Scope**: Un usuario a la vez, catálogos pequeños (unidades/decenas de docentes y proyectos),
volumen de asignaciones bajo; alcance de una sola iteración

## Constitution Check

*GATE: Debe pasar antes de la Fase 0. Re-evaluado tras la Fase 1.*

| # | Principio | Cumplimiento en el plan | Estado |
|---|-----------|--------------------------|--------|
| I | Desarrollo Guiado por Especificaciones | Plan derivado de spec.md ya aprobada; implementación posterior partirá de tasks.md | ✅ |
| II | Trazabilidad Completa | data-model y contracts referencian RF-01…RF-11; tareas (fase siguiente) ligarán RF ↔ T ↔ test | ✅ |
| III | Arquitectura Modular | Separación explícita models / services / api (controllers) / views (templates) | ✅ |
| IV | Validación en el Servidor (NO NEGOCIABLE) | La capa `services` valida toda regla antes de persistir; el frontend solo asiste. Pruebas de API directa (RF-11) | ✅ |
| V | Calidad y Pruebas | pytest con casos positivo/negativo/límite por cada regla; cobertura por RF | ✅ |
| VI | Seguridad Básica | Pydantic valida/sanea entradas; SQLAlchemy parametriza; sin credenciales en código; ruta de BD vía configuración | ✅ |
| VII | Simplicidad | Single project, sin capas superfluas; solo lo que exige la spec (YAGNI) | ✅ |
| VIII | Requisitos Verificables | Sin inventar normativa; límite de horas y estados oficiales permanecen PENDIENTE DE VALIDACIÓN | ✅ |
| IX | Gestión de Cambios | Cualquier cambio volverá a spec→plan→tasks→tests | ✅ |
| X | Documentación | Artefactos en español; código e identificadores en inglés | ✅ |

**Resultado del gate**: ✅ PASA. Sin violaciones. La sección *Complexity Tracking* queda vacía.

## Project Structure

### Documentation (this feature)

```text
specs/001-research-hours-validation/
├── plan.md              # Este archivo (/speckit-plan)
├── research.md          # Fase 0 (/speckit-plan)
├── data-model.md        # Fase 1 (/speckit-plan)
├── quickstart.md        # Fase 1 (/speckit-plan)
├── contracts/           # Fase 1 (/speckit-plan)
│   └── openapi.yaml
├── checklists/
│   └── requirements.md  # Checklist de calidad de la spec
├── evidence/            # Evidencias de ejecución y resultados de pruebas (Fase 6 de tasks.md)
└── tasks.md             # Fase 2 (/speckit-tasks - NO creado aquí)
```

### Source Code (repository root)

```text
app/
├── __init__.py
├── main.py                 # Punto de entrada FastAPI; monta rutas, estáticos y templates; seed inicial
├── config.py               # Configuración (ruta de BD vía variable de entorno; sin secretos en código)
├── database.py             # Engine, SessionLocal y Base de SQLAlchemy (MODELO: persistencia)
├── models.py               # Entidades ORM: Teacher, ResearchProject, ResearchAssignment (MODELO)
├── schemas.py              # Esquemas Pydantic de entrada/salida (validación de contrato)
├── seed.py                 # Carga de datos FICTICIOS de prueba (docentes y proyectos)
├── services/
│   ├── __init__.py
│   └── assignment_service.py   # SERVICIO DE NEGOCIO: reglas de validación reutilizables
├── routers/
│   ├── __init__.py
│   ├── pages.py            # CONTROLADOR (vistas): formulario y tabla (HTML vía Jinja2)
│   └── api.py              # CONTROLADOR (API): endpoints JSON (teachers, projects, assignments)
├── templates/              # VISTA: plantillas Jinja2
│   └── index.html
└── static/                 # VISTA: estilos y scripts
    ├── css/styles.css
    └── js/app.js

tests/
├── __init__.py
├── conftest.py             # Fixtures: app + BD aislada (TestClient)
├── test_assignment_service.py   # Pruebas unitarias de la capa de negocio
└── test_api.py             # Pruebas de integración de la API (incluye llamadas directas, RF-11)

requirements.txt            # Dependencias
README.md                   # Guía de inicio (apunta a quickstart.md)
.gitignore                  # Excluye venv, __pycache__, *.db
```

**Structure Decision**: Se elige **Single project** (Option 1 del template) porque el frontend se
sirve desde el mismo backend FastAPI (Jinja2 + estáticos), no es una SPA separada. La separación MVC
adaptada a FastAPI se materializa así:

- **Modelo**: `models.py` (entidades + reglas de persistencia), `database.py`, `schemas.py`
  (validación de forma de datos con Pydantic).
- **Vista**: `templates/` y `static/` (HTML, CSS, JS).
- **Controlador**: `routers/` (rutas HTTP que coordinan casos de uso y delegan en el servicio).
- **Servicio de negocio**: `services/assignment_service.py`, capa reutilizable e independiente de
  las rutas donde reside la regla "solo proyectos `APPROVED`, horas enteras > 0" — garantizando el
  Principio IV (validación en el servidor) y su reutilización tanto desde la API como desde la vista.

## Complexity Tracking

> Sin violaciones de la constitución. Sección no aplicable (vacía).

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| — | — | — |
