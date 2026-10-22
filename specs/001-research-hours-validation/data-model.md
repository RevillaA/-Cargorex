# Modelo de Datos (Fase 1): Cargorex – Validación de Horas de Investigación

**Feature**: `001-research-hours-validation` | **Date**: 2026-10-21

Modelo de datos del prototipo. Todos los registros de docentes y proyectos son **ficticios** (datos
de prueba). Nombres técnicos en inglés (Principio X).

---

## Entidad: `Teacher` (Docente)

Representa a un docente ficticio del catálogo de prueba. (RF-01)

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---------------|-------------|
| `id` | Integer | PK, autoincremental | Identificador interno |
| `name` | String(120) | NOT NULL | Nombre del docente (ficticio) |

- **Relaciones**: 1 `Teacher` → N `ResearchAssignment`.

## Entidad: `ResearchProject` (Proyecto de Investigación)

Representa un proyecto ficticio contra el cual se asignan horas. (RF-02, RF-03)

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---------------|-------------|
| `id` | Integer | PK, autoincremental | Identificador interno |
| `code` | String(30) | NOT NULL, UNIQUE | Código del proyecto (ficticio, legible) |
| `name` | String(150) | NOT NULL | Título del proyecto (ficticio) |
| `status` | Enum(`ProjectStatus`) | NOT NULL | Estado: `APPROVED`, `PENDING`, `REJECTED` |

- **Relaciones**: 1 `ResearchProject` → N `ResearchAssignment`.

### Enumeración `ProjectStatus`

| Valor | Significado | ¿Habilita registro? |
|-------|-------------|---------------------|
| `APPROVED` | Proyecto aprobado | **Sí** (RF-06) |
| `PENDING` | Proyecto pendiente | No (CA-02) |
| `REJECTED` | Proyecto rechazado | No (CA-03) |

> Cualquier valor no reconocido se trata como **no aprobado** (caso límite de la spec). El catálogo
> oficial de estados permanece **[PENDIENTE DE VALIDACIÓN]** (supuesto de prototipo, Principio VIII).

## Entidad: `ResearchAssignment` (Asignación de Horas)

Representa el registro **válido** de horas de investigación. Solo se persiste tras pasar todas las
validaciones. (RF-09)

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---------------|-------------|
| `id` | Integer | PK, autoincremental | Identificador interno |
| `teacher_id` | Integer | FK → `Teacher.id`, NOT NULL | Docente asignado |
| `project_id` | Integer | FK → `ResearchProject.id`, NOT NULL | Proyecto asociado (debe estar `APPROVED`) |
| `hours` | Integer | NOT NULL, `> 0` | Horas de investigación (entero positivo) |
| `created_at` | DateTime | NOT NULL, default = ahora (UTC) | Marca temporal del registro |

- **Relaciones**: N `ResearchAssignment` → 1 `Teacher`; N `ResearchAssignment` → 1 `ResearchProject`.

---

## Reglas de validación (capa de servicio)

Orden de evaluación y resultado. La validación ocurre **en el servidor** antes de persistir
(Principio IV). Mapeo a requisitos y código HTTP según la Clarificación 2026-10-21.

| # | Regla | Si falla | HTTP | Requisito |
|---|-------|----------|------|-----------|
| 1 | `hours` presente y es entero | Rechazo entrada inválida | 422 | RF-08 |
| 2 | `hours > 0` | Rechazo entrada inválida | 422 | RF-04, RF-08, CA-04 |
| 3 | `teacher_id` existe en catálogo | Rechazo regla de negocio | 400 | RF-01 (supuesto docente) |
| 4 | `project_id` existe en catálogo | Rechazo regla de negocio | 400 | RF-05, CA-05 |
| 5 | `project.status == APPROVED` | Rechazo regla de negocio (mensaje explicativo) | 400 | RF-06, RF-07, CA-02, CA-03 |
| ✔ | Todas las reglas pasan | Persistir `ResearchAssignment` | 201 | RF-09, CA-01 |

> **Invariante (CA-07 / RF-11)**: si cualquier regla falla, **no** se crea ningún
> `ResearchAssignment`. La validación se aplica aunque la solicitud llegue directamente a la API sin
> pasar por el formulario web.

## Reglas de dominio NO aplicadas en esta iteración

- **Límite máximo de horas**: no se impone (PENDIENTE DE VALIDACIÓN – normativo).
- **Acumulación / unicidad de (teacher, project)**: no se restringe; se permiten múltiples registros
  (PENDIENTE DE VALIDACIÓN).

## Datos de siembra (ficticios)

El módulo de siembra cargará, de forma idempotente, un conjunto mínimo que cubra los tres estados
para hacer la demo y las pruebas reproducibles:

- Docentes: al menos 2 (p. ej. "Docente de Prueba 1", "Docente de Prueba 2").
- Proyectos: al menos 3, uno por estado (`APPROVED`, `PENDING`, `REJECTED`).

> Las cantidades y nombres exactos se concretarán en `tasks.md`; aquí solo se fija la cobertura
> mínima requerida por las pruebas.
