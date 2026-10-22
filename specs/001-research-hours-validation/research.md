# Investigación Técnica (Fase 0): Cargorex – Validación de Horas de Investigación

**Feature**: `001-research-hours-validation` | **Date**: 2026-10-21

Este documento consolida las decisiones técnicas que resuelven el contexto del plan. No había
marcadores `NEEDS CLARIFICATION` abiertos: el stack y la arquitectura fueron definidos por el
solicitante y por la constitución. Se documentan decisiones, justificación y alternativas
evaluadas.

---

## D1 — Patrón arquitectónico: MVC adaptado a FastAPI con capa de servicio

- **Decision**: Separar en Modelo (`models`/`database`/`schemas`), Vista (`templates`/`static`),
  Controlador (`routers`) y una capa de **Servicio de negocio** (`services`) reutilizable.
- **Rationale**: FastAPI no es un framework MVC estricto, pero admite una separación equivalente. La
  capa de servicio aísla la regla de negocio y permite probarla de forma unitaria (Principio V) y
  reutilizarla desde la API y la vista. Satisface directamente el Principio III (modularidad) y el
  Principio IV (validación en el servidor).
- **Alternatives considered**:
  - *Lógica dentro de las rutas* — rechazada: acopla negocio y transporte, dificulta las pruebas y
    viola el Principio III.
  - *Patrón Repository completo* — rechazada por el Principio VII (simplicidad): para un prototipo
    de 3 entidades, las sesiones de SQLAlchemy en el servicio son suficientes.

## D2 — Validación en dos niveles: Pydantic (forma) + Servicio (negocio)

- **Decision**: Pydantic v2 valida la **forma** de la entrada (horas = entero, requeridos
  presentes) devolviendo **HTTP 422**; la capa de servicio valida las **reglas de negocio**
  (existencia de docente/proyecto, estado `APPROVED`) devolviendo **HTTP 400** con JSON de motivo.
- **Rationale**: Coincide con la Clarificación del 2026-10-21. Separa claramente "entrada mal
  formada" de "regla de negocio incumplida", lo que hace las pruebas inequívocas (RF-08 → 422;
  RF-05/RF-06 → 400). 422 es el comportamiento nativo de FastAPI ante fallos de validación.
- **Alternatives considered**:
  - *Un único 400 para todo* — rechazada: pierde la distinción útil para pruebas y diagnóstico.
  - *200 con bandera de error* — rechazada: contraviene convenciones HTTP y complica las pruebas.

## D3 — Tipo de dato de `hours`: entero positivo

- **Decision**: `hours` es un entero (`int`) con restricción `> 0`, validado por Pydantic
  (`conint(gt=0)` o equivalente) **y** reforzado en el servicio.
- **Rationale**: Clarificación del 2026-10-21. No se impone límite máximo porque es normativo y
  permanece **[PENDIENTE DE VALIDACIÓN]** (Unidad de Docencia / UTIC). Validar también en el
  servicio cumple el Principio IV (no confiar solo en el borde/Pydantic).
- **Alternatives considered**:
  - *Decimal* — descartada por decisión del solicitante en la fase de clarificación.
  - *Solo validación en Pydantic* — insuficiente frente al Principio IV; por eso se duplica en el
    servicio para solicitudes que no pasen por el esquema del endpoint principal.

## D4 — Estado del proyecto: enumeración `APPROVED` / `PENDING` / `REJECTED`

- **Decision**: Modelar `status` como una enumeración controlada con tres valores. Solo `APPROVED`
  habilita el registro; cualquier otro valor (incluido uno desconocido) se trata como no aprobado.
- **Rationale**: Refleja RF-03/RF-06 y el caso límite "estado desconocido → rechazar". El catálogo
  oficial de estados queda **[PENDIENTE DE VALIDACIÓN]**; esta enumeración es un supuesto de
  prototipo, no una regla institucional (Principio VIII).
- **Alternatives considered**:
  - *Booleano `is_approved`* — rechazada: perdería la distinción pendiente/rechazado exigida por
    RF-03 y los mensajes explicativos (RF-07).

## D5 — Persistencia: SQLite + SQLAlchemy

- **Decision**: SQLite local con SQLAlchemy 2.x (ORM). La ruta del archivo se lee de configuración
  (`config.py` / variable de entorno), con valor por defecto `cargorex.db`.
- **Rationale**: Ligera, sin servidor, ideal para demo local en Windows. El ORM parametriza las
  consultas (Principio VI, sin SQL concatenado). No almacenar la ruta sensible ni credenciales en el
  código (no hay credenciales en SQLite local, pero la ruta es configurable).
- **Alternatives considered**:
  - *sqlite3 crudo* — rechazada: mayor riesgo de SQL manual y más código repetitivo.
  - *PostgreSQL* — rechazada por el Principio VII y porque añade dependencia de servidor innecesaria.

## D6 — Siembra de datos ficticios

- **Decision**: Un módulo `seed.py` inserta docentes y proyectos ficticios (con los tres estados) al
  iniciar la app si las tablas están vacías. Cada registro se marca claramente como dato de prueba.
- **Rationale**: Hace el prototipo demostrable y las pruebas reproducibles (Dependencia declarada en
  la spec). Idempotente: no duplica si ya hay datos.
- **Alternatives considered**:
  - *Datos incrustados en el frontend* — rechazada: la validación es del servidor; los catálogos
    deben vivir en el backend (RF-01, RF-02, RF-05).

## D7 — Frontend: Jinja2 + JavaScript mínimo

- **Decision**: Una página `index.html` renderizada con Jinja2; JavaScript (`app.js`) consume la API
  JSON para poblar selectores, enviar el formulario y mostrar mensajes y la tabla de registros.
- **Rationale**: Cumple el diseño de interfaz solicitado con el mínimo de complejidad. El aviso de
  "datos ficticios" se renderiza visible. Las validaciones del cliente son solo asistencia; la
  autoridad es el servidor (Principio IV).
- **Alternatives considered**:
  - *SPA (React/Vue)* — rechazada por el Principio VII (sobre-ingeniería para un prototipo).
  - *HTML 100% renderizado en servidor sin JS* — viable, pero el JS mejora la UX de mensajes y la
    actualización de la tabla sin recargar; se mantiene mínimo.

## D8 — Estrategia de pruebas (pytest)

- **Decision**: Dos niveles — (a) unitarias de `assignment_service` con una BD aislada; (b)
  integración de la API con `TestClient`, incluyendo **llamadas directas a la API** que saltan el
  formulario (RF-11). Fixtures crean una BD temporal/in-memory por sesión.
- **Rationale**: Garantiza cobertura por cada RF (Principio V y SC-007) y verifica explícitamente la
  validación del servidor independiente del cliente (Principio IV, RF-11, CA-07).
- **Casos mínimos** (mapeados a la spec): registro aprobado (CA-01), pendiente (CA-02), rechazado
  (CA-03), inexistente (CA-05), horas = 0 (CA-04), horas negativas (CA-04), horas no enteras (RF-08),
  docente inexistente (supuesto), persistencia correcta (SC-004), ausencia de persistencia en
  rechazo (CA-07), validación por API directa (RF-11).
- **Alternatives considered**:
  - *Solo pruebas de API* — rechazada: las unitarias del servicio son más rápidas y aíslan la regla.

## Dependencias pendientes de validación (no técnicas)

Se registran como dependencias institucionales, **no** se resuelven en esta fase (Principio VIII):

| Tema | Responsable sugerido | Estado |
|------|----------------------|--------|
| Límite máximo y unidad de horas de investigación | Unidad de Docencia / normativa | PENDIENTE DE VALIDACIÓN |
| Catálogo oficial de estados de proyecto | Unidad de Docencia / módulo de investigación | PENDIENTE DE VALIDACIÓN |
| Reglas de acumulación / duplicados de asignaciones | Unidad de Docencia / normativa | PENDIENTE DE VALIDACIÓN |
| Integración real con sistemas ESPE (APIs, auth) | UTIC | FUERA DE ALCANCE (esta iteración) |
