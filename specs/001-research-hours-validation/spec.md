# Especificación Funcional: Validación de Horas de Investigación mediante Proyectos Aprobados

**Feature Directory**: `specs/001-research-hours-validation`

**Created**: 2026-10-21

**Status**: Draft

**Input**: Validación de la asignación de horas de investigación de docentes contra
proyectos de investigación en estado aprobado (prototipo independiente con datos ficticios,
sin conexión a sistemas reales de la ESPE).

> **Nota de contexto**: Cargorex es un módulo institucional de distribución de carga horaria
> docente. Esta es la **primera iteración** y se limita a un prototipo demostrable de una única
> regla de negocio. Los estados y datos ficticios son un mecanismo de demostración y **no**
> representan un catálogo oficial. Los límites, políticas y reglas normativas definitivas
> permanecen **pendientes de levantamiento** con el área funcional y los documentos normativos.

## Clarifications

### Session 2026-10-21

- Q: ¿Qué tipo de valor numérico debe aceptar el backend para las horas de investigación? → A: Entero positivo (> 0); la unidad y el límite máximo permanecen PENDIENTE DE VALIDACIÓN (Unidad de Docencia / normativa).
- Q: ¿Cómo debe responder el backend cuando rechaza una solicitud inválida? → A: HTTP 422 para entrada inválida (horas ≤ 0, no entera o no numérica) y HTTP 400 para regla de negocio incumplida (proyecto no aprobado o inexistente), siempre con cuerpo JSON que incluya el motivo del rechazo.

> **Nota**: Estas aclaraciones son decisiones **técnicas** del prototipo, adoptadas para poder
> implementarlo y diseñar las pruebas. **No** constituyen reglas institucionales oficiales. Las
> cuestiones normativas (unidad/límite de horas, catálogo oficial de estados, acumulación de
> horas/duplicados) continúan **pendientes de validación** con la Unidad de Docencia, UTIC y los
> documentos normativos de la ESPE.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Registrar horas de investigación contra un proyecto aprobado (Priority: P1)

Como **docente**, quiero registrar una cantidad de horas de investigación asociada a un proyecto
seleccionado, para que el sistema valide —antes de guardar— que el proyecto está aprobado y que las
horas son válidas, y solo entonces persista mi asignación.

**Why this priority**: Es el núcleo del prototipo y la razón de ser de la iteración. Sin esta
historia no hay valor demostrable; concentra la regla de negocio principal (solo proyectos
aprobados) y la validación en el servidor. Entregada de forma aislada ya constituye un MVP.

**Independent Test**: Puede probarse de extremo a extremo seleccionando un docente y un proyecto del
catálogo ficticio, ingresando horas y verificando que el registro se acepta solo con proyecto
aprobado y horas positivas, y se rechaza en cualquier otro caso, sin requerir las demás historias.

**Acceptance Scenarios**:

1. **CA-01** — **Dado** un proyecto en estado *aprobado* y una cantidad positiva de horas, **cuando**
   el docente registra la asignación, **entonces** el sistema la guarda y confirma el registro.
2. **CA-02** — **Dado** un proyecto en estado *pendiente*, **cuando** el docente intenta registrar
   horas, **entonces** el sistema rechaza la asignación y muestra un mensaje explicativo.
3. **CA-03** — **Dado** un proyecto en estado *rechazado*, **cuando** el docente intenta registrar
   horas, **entonces** el sistema impide el registro y muestra un mensaje explicativo.
4. **CA-04** — **Dadas** horas iguales a cero o negativas, **cuando** el docente envía la solicitud,
   **entonces** el sistema la rechaza indicando que las horas deben ser positivas.
5. **CA-05** — **Dado** un identificador de proyecto inexistente en el catálogo, **cuando** se envía
   la solicitud, **entonces** el sistema la rechaza indicando que el proyecto no existe.
6. **CA-07** — **Dado** cualquier caso en que el sistema rechaza la operación, **cuando** finaliza la
   solicitud, **entonces** **no** queda persistida ninguna asignación inválida.

---

### User Story 2 - Consultar las asignaciones registradas (Priority: P2)

Como **usuario evaluador** (y como docente), quiero consultar la lista de asignaciones de horas
válidas ya registradas, para verificar el funcionamiento del prototipo y los resultados de las
pruebas.

**Why this priority**: Aporta la evidencia de que los registros válidos se persistieron
correctamente y cierra el ciclo de demostración. Depende de que exista al menos un registro, por lo
que es posterior a US1, pero es independientemente testable con datos sembrados.

**Independent Test**: Tras existir al menos una asignación válida (sembrada o creada), consultar el
listado y verificar que la asignación aparece con docente, proyecto y horas correctos.

**Acceptance Scenarios**:

1. **CA-06** — **Dado** un registro válido previamente almacenado, **cuando** el usuario consulta las
   asignaciones, **entonces** el sistema muestra dicho registro con sus datos.
2. **Dado** que no existen asignaciones, **cuando** el usuario consulta el listado, **entonces** el
   sistema muestra una lista vacía sin error.

---

### User Story 3 - Visualizar el catálogo de proyectos y su estado (Priority: P3)

Como **docente**, quiero consultar los proyectos de investigación de prueba y ver su estado
(aprobado, pendiente o rechazado), para elegir con conocimiento antes de registrar horas.

**Why this priority**: Mejora la usabilidad y guía la selección, pero la regla de negocio se valida
igualmente en el servidor aunque el docente no consulte primero el catálogo; por eso es la de menor
prioridad.

**Independent Test**: Consultar el catálogo y verificar que cada proyecto ficticio muestra su estado
correctamente, independientemente del flujo de registro.

**Acceptance Scenarios**:

1. **Dado** el catálogo ficticio de proyectos, **cuando** el docente lo consulta, **entonces** cada
   proyecto muestra su identificador, nombre y estado (aprobado / pendiente / rechazado).
2. **Dado** un proyecto no aprobado, **cuando** el docente lo selecciona e intenta registrar horas,
   **entonces** el sistema muestra un mensaje explicativo del motivo del rechazo (RF-07).

---

### Edge Cases

- **Horas no numéricas, no enteras o vacías**: una entrada que no sea un número entero (texto,
  símbolos, decimales como `1.5`, campo vacío) debe rechazarse como entrada inválida con HTTP 422
  (RF-08).
- **Horas en el límite inferior**: el valor `0` se rechaza; el menor valor aceptable es `1` (entero
  estrictamente positivo). *(El límite máximo y la unidad de horas quedan [PENDIENTE DE
  VALIDACIÓN].)*
- **Proyecto inexistente enviado directamente al servidor**: una solicitud construida fuera del
  formulario (p. ej. llamada directa al backend) con un proyecto inexistente o datos inválidos debe
  rechazarse igualmente (RF-11, CA-07).
- **Estado del proyecto distinto de los tres contemplados**: cualquier estado no reconocido se trata
  como *no aprobado* y se rechaza el registro.
- **Docente inexistente**: una solicitud que referencie un docente fuera del catálogo ficticio debe
  rechazarse. *(Ver [SUPUESTO PROVISIONAL].)*
- **Duplicados**: el tratamiento de una misma combinación docente+proyecto repetida queda como
  [PENDIENTE DE VALIDACIÓN] (ver Assumptions).

## Requirements *(mandatory)*

### Functional Requirements

- **RF-01**: El sistema DEBE permitir seleccionar un docente ficticio desde un catálogo de prueba.
- **RF-02**: El sistema DEBE permitir consultar y seleccionar proyectos de investigación de prueba.
- **RF-03**: El sistema DEBE mostrar el estado de cada proyecto: *aprobado*, *pendiente* o
  *rechazado*.
- **RF-04**: El sistema DEBE permitir ingresar una cantidad positiva de horas de investigación,
  entendida como un número **entero estrictamente mayor que cero**. *(La unidad y el límite máximo
  de horas quedan [PENDIENTE DE VALIDACIÓN].)*
- **RF-05**: El sistema DEBE verificar que el proyecto seleccionado exista en el catálogo de prueba.
- **RF-06**: El sistema DEBE permitir el registro únicamente cuando el proyecto tenga estado
  *aprobado*.
- **RF-07**: El sistema DEBE mostrar un mensaje explicativo cuando el proyecto no esté aprobado.
- **RF-08**: El sistema DEBE rechazar horas iguales o menores que cero, valores no enteros, valores
  no numéricos y entradas inválidas, respondiendo con **HTTP 422** y un cuerpo JSON que indique el
  motivo.
- **RF-09**: El sistema DEBE almacenar las asignaciones válidas.
- **RF-10**: El sistema DEBE permitir consultar las asignaciones registradas.
- **RF-11**: El sistema DEBE impedir que una solicitud inválida sea almacenada, aunque se envíe
  directamente al servidor sin utilizar el formulario web (validación en el servidor,
  independiente del cliente). El rechazo por regla de negocio (proyecto no aprobado o inexistente)
  DEBE responder con **HTTP 400** y un cuerpo JSON que indique el motivo.

**Trazabilidad requisito → criterio de aceptación**:

| Requisito | Historia | Criterios de aceptación |
|-----------|----------|--------------------------|
| RF-01 | US1 | CA-01 |
| RF-02 | US1, US3 | CA-01 |
| RF-03 | US3 | US3.1 |
| RF-04 | US1 | CA-01, CA-04 |
| RF-05 | US1 | CA-05 |
| RF-06 | US1 | CA-01, CA-02, CA-03 |
| RF-07 | US1, US3 | CA-02, CA-03, US3.2 |
| RF-08 | US1 | CA-04 |
| RF-09 | US1 | CA-01 |
| RF-10 | US2 | CA-06 |
| RF-11 | US1 | CA-07 |

### Key Entities *(include if feature involves data)*

- **Docente (Teacher)**: representa a un profesor ficticio que registra horas. Atributos clave:
  identificador, nombre. Pertenece al catálogo de prueba.
- **Proyecto de Investigación (ResearchProject)**: representa un proyecto ficticio contra el cual se
  asignan horas. Atributos clave: identificador, nombre/título, estado (*aprobado*, *pendiente*,
  *rechazado*).
- **Asignación de Horas (HoursAssignment)**: representa el registro válido de horas de investigación.
  Atributos clave: identificador, docente asociado, proyecto asociado, cantidad de horas
  (entero positivo), marca temporal de registro.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: El 100% de los intentos de registro contra un proyecto no aprobado (pendiente o
  rechazado) son rechazados con HTTP 400 y ninguno queda persistido.
- **SC-002**: El 100% de los intentos con horas ≤ 0, no enteras, no numéricas o inválidas son
  rechazados con HTTP 422.
- **SC-003**: El 100% de los intentos contra un proyecto inexistente son rechazados con HTTP 400.
- **SC-004**: Un registro con proyecto aprobado y horas positivas se guarda y puede recuperarse
  íntegramente en la consulta posterior (coincidencia de docente, proyecto y horas).
- **SC-005**: Las reglas de rechazo se cumplen también cuando la solicitud se envía directamente al
  servidor sin pasar por el formulario web (ninguna solicitud inválida se persiste por esa vía).
- **SC-006**: Un usuario evaluador puede completar el ciclo demostrativo (registrar un caso válido,
  provocar al menos un rechazo y consultar el resultado) en menos de 5 minutos siguiendo la
  documentación reproducible.
- **SC-007**: Cada requisito funcional (RF-01…RF-11) cuenta con al menos una prueba automatizada que
  verifica su cumplimiento.

## Assumptions

Supuestos adoptados ante detalles no especificados. Los marcados como provisionales deben
confirmarse con el área funcional o la normativa (Principio VIII de la constitución).

- **Datos ficticios**: el catálogo de docentes y proyectos es de prueba, precargado/sembrado para la
  demostración, y no proviene de ningún sistema real de la ESPE.
- **Formato de horas (decisión técnica, Clarificación 2026-10-21)**: las horas se representan como un
  número **entero estrictamente mayor que cero**. El valor **máximo** y la **unidad**
  (semanales/por periodo) quedan **[PENDIENTE DE VALIDACIÓN]** con la Unidad de Docencia y la
  normativa; esta iteración **no** aplica límites normativos de horas (fuera de alcance).
- **[SUPUESTO PROVISIONAL] Estados del proyecto**: se asumen exactamente tres estados —*aprobado*,
  *pendiente*, *rechazado*— y solo *aprobado* habilita el registro. El catálogo oficial de estados
  queda pendiente de levantamiento.
- **[SUPUESTO PROVISIONAL] Validación de docente**: se asume que el docente debe existir en el
  catálogo de prueba; el comportamiento ante docentes no catalogados se rechaza por defecto.
- **[PENDIENTE DE VALIDACIÓN] Duplicados**: no se define en esta iteración si una misma combinación
  docente+proyecto puede registrarse más de una vez ni si las horas se acumulan; por defecto se
  permiten múltiples registros sin acumulación automática.
- **Persistencia local**: la persistencia es local y orientada únicamente a la demostración; no hay
  requisitos de alta disponibilidad, respaldo ni concurrencia masiva.
- **Sin autenticación**: no hay autenticación ni autorización institucional; cualquier usuario del
  prototipo puede operar el formulario (fuera de alcance).
- **Idioma**: los mensajes al usuario del prototipo se presentan en español.

## Dependencies

- **Datos de prueba sembrados**: el prototipo depende de disponer de catálogos ficticios de docentes
  y proyectos (con los tres estados) para ser demostrable y testeable.
- **Documentación reproducible**: la demostración depende de instrucciones que permitan ejecutar el
  prototipo y las pruebas de forma repetible.
- **Sin dependencias externas institucionales**: explícitamente **no** depende de APIs, credenciales,
  bases de datos ni módulos reales de la ESPE (no disponibles ni confirmados).

## Out of Scope

Quedan explícitamente **fuera de alcance** de esta iteración:

- Autenticación y autorización institucional real.
- Integración con APIs o sistemas reales de la ESPE.
- Aplicación de límites normativos de horas.
- Aprobaciones departamentales o flujos de autorización.
- Distribución completa de la carga horaria docente (docencia, vinculación, gestión).
- Reporterías institucionales.
- Seguimiento de cumplimiento por parciales o periodos.
- Conexiones con módulos de investigación reales.
