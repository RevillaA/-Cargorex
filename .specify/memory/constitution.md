<!--
SYNC IMPACT REPORT (scratch — eliminar antes de versionar el archivo final)
=========================================================================
Cambio de versión: (ninguna) → 1.0.0 → 1.0.1
Motivo del bump: 1.0.0 = ratificación inicial (MAJOR desde plantilla vacía).
  1.0.1 = PATCH (2026-10-21, vía /speckit-analyze): aclaración de notación en el
  Principio II — el formato de ID de tarea es `T###` (p. ej. `T001`, plantilla
  Spec Kit), no `T-XXX`. Sin cambios de principio ni de alcance.

Principios definidos (10, según entrada del usuario; la plantilla núcleo trae 5
slots y se amplió respetando el número solicitado):
  I.    Desarrollo Guiado por Especificaciones (SDD)
  II.   Trazabilidad Completa
  III.  Arquitectura Modular
  IV.   Validación en el Servidor (NO NEGOCIABLE)
  V.    Calidad y Pruebas
  VI.   Seguridad Básica
  VII.  Simplicidad
  VIII. Requisitos Verificables
  IX.   Gestión de Cambios
  X.    Documentación

Secciones añadidas:
  - Restricciones y Stack Técnico (SECTION_2)
  - Flujo de Desarrollo y Puertas de Calidad (SECTION_3)
  - Governance (procedimiento de enmienda, política de versionado, cumplimiento
    y gestión de excepciones)

Secciones eliminadas: ninguna.

Plantillas dependientes a revisar en fases posteriores:
  - .specify/templates/spec-template.md       → debe exigir IDs de requisito (RF-XXX)
  - .specify/templates/plan-template.md        → debe reflejar MVC/validación backend
  - .specify/templates/tasks-template.md       → debe ligar tareas ↔ requisitos ↔ pruebas

TODOs diferidos: ninguno (RATIFICATION_DATE conocida = fecha de adopción hoy).
=========================================================================
-->

# Cargorex-SDD Constitution

Constitución del proyecto **Cargorex-SDD**, primera iteración del prototipo de
validación de horas de investigación para el Módulo de Distribución de Carga
Horaria Docente de la Universidad de las Fuerzas Armadas ESPE. Este documento
establece los principios técnicos y metodológicos de obligado cumplimiento
durante el desarrollo del prototipo.

## Core Principles

### I. Desarrollo Guiado por Especificaciones (SDD)

Toda funcionalidad DEBE nacer de una especificación antes de escribir código.
Ninguna línea de implementación puede comenzar sin que exista, en este orden:
(1) requisitos funcionales, (2) criterios de aceptación verificables,
(3) un plan técnico y (4) tareas derivadas. El orden de las fases SDD
—`constitution` → `specify` → `plan` → `tasks` → `implement` → `analyze`— es
obligatorio y no puede saltarse.

**Rationale**: El valor académico del taller reside en demostrar el método SDD;
implementar sin especificación previa invalida el ejercicio y rompe la
trazabilidad.

### II. Trazabilidad Completa

Cada requisito funcional DEBE tener un identificador único (formato `RF-XXX`).
Cada requisito DEBE estar enlazado con una o más tareas (formato `T###`, p. ej.
`T001`, conforme a la plantilla Spec Kit) y con al menos una prueba que verifique
su cumplimiento. La cadena
`requisito → tarea → implementación → prueba` DEBE poder recorrerse en ambos
sentidos y mantenerse consistente en todos los artefactos.

**Rationale**: Sin identificadores y enlaces explícitos no es posible auditar la
cobertura ni demostrar que lo construido corresponde a lo especificado.

### III. Arquitectura Modular

El prototipo DEBE separar responsabilidades de presentación, lógica de negocio y
acceso a datos. Se adoptará un enfoque MVC o una adaptación documentada para
FastAPI (por ejemplo: `routes`/`views` para presentación, `services` para la
lógica de negocio y `repositories`/`models` para el acceso a datos). La capa de
presentación NO DEBE contener reglas de negocio ni consultas SQL directas.

**Rationale**: La separación de capas facilita las pruebas unitarias, la
trazabilidad y la extensión futura sin acoplar la interfaz a la persistencia.

### IV. Validación en el Servidor (NO NEGOCIABLE)

Toda asignación DEBE validarse en el backend antes de persistirse. Las
validaciones del frontend son únicamente ayudas de usabilidad y NUNCA sustituyen
a la validación del servidor. En particular, la regla de negocio del prototipo
—asignar horas de investigación solo contra un proyecto en estado aprobado— DEBE
aplicarse en el servidor, y las horas DEBEN ser positivas. Una solicitud que
incumpla una regla DEBE rechazarse con un mensaje explícito y sin persistir datos.

**Rationale**: Confiar en el cliente es una vulnerabilidad; la integridad de los
datos solo puede garantizarse en el backend.

### V. Calidad y Pruebas

Se DEBE usar `pytest` para verificar el comportamiento del prototipo. Cada regla
de validación DEBE cubrir, como mínimo, un escenario positivo (aprobado), uno
negativo (no aprobado o inválido) y los casos límite identificados (por ejemplo,
horas en cero o negativas, proyecto inexistente). Ningún requisito funcional se
considera completo sin su prueba asociada que pase.

**Rationale**: Las pruebas son la evidencia objetiva del cumplimiento de los
requisitos y el mecanismo de regresión ante cambios.

### VI. Seguridad Básica

El prototipo DEBE validar y sanear todas las entradas. El acceso a datos DEBE
usar consultas parametrizadas; se PROHÍBE construir SQL por concatenación de
cadenas. NO DEBEN almacenarse credenciales, secretos ni rutas sensibles en el
código fuente ni en el control de versiones; cualquier valor configurable DEBE
leerse de variables de entorno o de un archivo de configuración excluido del
versionado.

**Rationale**: Aun siendo un prototipo con datos ficticios, las prácticas
inseguras no deben normalizarse y serían observadas en la auditoría de calidad.

### VII. Simplicidad

La implementación DEBE limitarse a una primera iteración funcional y demostrable.
Se aplica el principio YAGNI: no se añadirán capas, dependencias, abstracciones ni
funcionalidades que no exija un requisito vigente. Cualquier complejidad adicional
DEBE justificarse explícitamente frente a este principio.

**Rationale**: El alcance acotado evita sobre-ingeniería y mantiene el prototipo
comprensible y entregable dentro del taller.

### VIII. Requisitos Verificables

NO se DEBEN inventar normativas institucionales, APIs, credenciales ni límites de
horas. Todo dato es ficticio. Las reglas, umbrales o comportamientos no
confirmados por documentos normativos o por el levantamiento con el área funcional
DEBEN marcarse explícitamente como `[SUPUESTO PROVISIONAL]` o
`[PENDIENTE DE VALIDACIÓN]` en el artefacto correspondiente, nunca presentarse
como hechos.

**Rationale**: La honestidad sobre lo que es supuesto y lo que es confirmado
protege la validez del prototipo y evita decisiones basadas en reglas inexistentes.

### IX. Gestión de Cambios

Todo cambio en un requisito DEBE propagarse de forma consistente a la
especificación, a las tareas y a las pruebas afectadas. No se admite modificar la
implementación sin actualizar primero el artefacto de especificación que la
origina. Cada cambio DEBE preservar la trazabilidad definida en el Principio II.

**Rationale**: Un cambio aplicado solo en el código degrada la especificación y
rompe la trazabilidad, que es el eje del método SDD.

### X. Documentación

Los artefactos académicos (especificación, plan, tareas, análisis y documentación
funcional) DEBEN redactarse en **español**. Los nombres técnicos, identificadores,
código fuente, nombres de funciones, variables y mensajes de commit DEBEN
mantenerse en **inglés**. Los mensajes dirigidos al usuario final del prototipo
pueden ser en español por tratarse de contexto institucional.

**Rationale**: El taller es académico y en español, pero el código debe seguir las
convenciones técnicas estándar en inglés para legibilidad y mantenibilidad.

## Restricciones y Stack Técnico

- **Stack autorizado**: Python, FastAPI, SQLite, HTML, CSS y JavaScript.
- **Pruebas**: `pytest` (y, cuando aplique, `httpx`/`TestClient` para endpoints).
- **Entorno de ejecución**: se usará el intérprete `python` 3.11 del sistema,
  preferentemente dentro de un entorno virtual (`venv`) aislado.
- **Persistencia**: SQLite con acceso mediante consultas parametrizadas.
- **Alcance**: SOLO el prototipo independiente de validación de horas de
  investigación. NO se desarrollará la totalidad de Cargorex ni se integrará con
  el código, APIs o credenciales institucionales (no disponibles ni confirmados).
- **Datos**: exclusivamente ficticios (docentes y proyectos de prueba con estado
  aprobado / no aprobado).
- **Funcionalidad mínima**: formulario web, selección de docente y proyecto
  ficticios, registro de horas positivas, validación en backend, mensajes de
  rechazo, almacenamiento en SQLite, consulta de registros y pruebas `pytest`.

## Flujo de Desarrollo y Puertas de Calidad

El desarrollo sigue el flujo Spec Kit en fases secuenciales. Cada fase es una
puerta de calidad (quality gate) que DEBE superarse antes de avanzar:

1. **Constitution** — principios aprobados (este documento).
2. **Specify** — requisitos con IDs `RF-XXX` y criterios de aceptación.
3. **Plan** — diseño técnico coherente con los Principios III, IV y VII.
4. **Tasks** — tareas `T-XXX` enlazadas a requisitos y a pruebas previstas.
5. **Implement** — código + pruebas `pytest`; ninguna tarea se cierra sin prueba
   que pase.
6. **Analyze** — auditoría de consistencia y trazabilidad entre artefactos.

**Puertas de verificación**:
- No se avanza de fase si la anterior deja requisitos sin ID o sin criterios de
  aceptación.
- No se marca una tarea como completa sin su prueba asociada en verde.
- Cualquier `[SUPUESTO PROVISIONAL]` abierto DEBE quedar listado en el análisis
  final.

## Governance

Esta constitución tiene precedencia sobre cualquier otra práctica del proyecto
durante la iteración. Su cumplimiento se verifica así:

- **Revisión de cumplimiento**: la fase `analyze` DEBE comprobar explícitamente
  cada principio y reportar incumplimientos. La auditoría de calidad DEBE revisar
  trazabilidad (II), validación en backend (IV) y cobertura de pruebas (V).
- **Procedimiento de enmienda**: toda modificación de esta constitución DEBE
  realizarse editando este archivo mediante el flujo `/speckit-constitution`,
  documentando el cambio en el Sync Impact Report y propagando el impacto a las
  plantillas y artefactos dependientes.
- **Política de versionado** (SemVer):
  - **MAJOR**: eliminación o redefinición incompatible de principios o gobernanza.
  - **MINOR**: adición de un principio/sección o ampliación material de una guía.
  - **PATCH**: aclaraciones, correcciones de redacción o ajustes no semánticos.
- **Gestión de excepciones**: cualquier desviación de un principio DEBE
  justificarse por escrito en el artefacto afectado, indicando el principio
  afectado, el motivo y la medida compensatoria. Las excepciones al Principio IV
  (Validación en el Servidor) NO están permitidas. Toda excepción abierta DEBE
  listarse en la fase `analyze`.

**Version**: 1.0.1 | **Ratified**: 2026-10-21 | **Last Amended**: 2026-10-21
