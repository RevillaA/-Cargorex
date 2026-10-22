# Guía de Inicio (Quickstart): Cargorex – Prototipo de Validación de Horas de Investigación

**Feature**: `001-research-hours-validation` | **Date**: 2026-10-21

Guía reproducible para instalar, ejecutar y **validar** el prototipo en **Windows PowerShell**. No
contiene el código de implementación (eso corresponde a `tasks.md` y a la fase de implementación);
describe cómo poner en marcha el sistema y qué escenarios demuestran que funciona.

> ⚠️ **Datos ficticios**: el prototipo usa docentes y proyectos de prueba. No se conecta a sistemas
> reales de la ESPE.

## Prerrequisitos

- Windows 11 con **PowerShell**.
- **Python 3.11** disponible como `python` (verificado en el entorno: `python --version`).
- Dependencias declaradas en `requirements.txt` (se generan en la implementación):
  FastAPI, Uvicorn, SQLAlchemy, Jinja2, Pydantic, pytest, httpx.

## 1. Preparar el entorno (PowerShell)

```powershell
# Desde la raíz del repositorio
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

> Si PowerShell bloquea la activación del entorno, permitir scripts en la sesión actual:
> `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`

## 2. Ejecutar la aplicación

```powershell
uvicorn app.main:app --reload
```

- Abrir en el navegador: `http://127.0.0.1:8000`
- Al iniciar, la app **siembra** datos ficticios (si la BD está vacía): docentes de prueba y
  proyectos con estados `APPROVED`, `PENDING` y `REJECTED`.

## 3. Ejecutar las pruebas

```powershell
pytest -v
```

Las pruebas usan una base de datos aislada (no afectan a `cargorex.db`).

---

## Escenarios de validación end-to-end

Cada escenario mapea a criterios de aceptación de [spec.md](./spec.md) y al contrato
[contracts/openapi.yaml](./contracts/openapi.yaml). Pueden ejecutarse desde la interfaz web o
directamente contra la API.

### E1 — Registro válido (proyecto aprobado) · CA-01, RF-09

1. Seleccionar un docente y un proyecto con estado `APPROVED`.
2. Ingresar horas = `8` y registrar.
3. **Esperado**: HTTP **201**; la asignación aparece en la tabla de registros.

### E2 — Proyecto pendiente · CA-02, RF-07

1. Seleccionar un proyecto `PENDING`, horas = `5`.
2. **Esperado**: HTTP **400** con mensaje explicativo; **no** se persiste.

### E3 — Proyecto rechazado · CA-03, RF-07

1. Seleccionar un proyecto `REJECTED`, horas = `5`.
2. **Esperado**: HTTP **400** con mensaje explicativo; **no** se persiste.

### E4 — Proyecto inexistente · CA-05, RF-05

1. Enviar `project_id` que no existe en el catálogo.
2. **Esperado**: HTTP **400**; **no** se persiste.

### E5 — Horas = 0 y horas negativas · CA-04, RF-08

1. Enviar horas = `0`, luego horas = `-3`.
2. **Esperado**: HTTP **422** en ambos casos; **no** se persiste.

### E6 — Horas no enteras / no numéricas · RF-08

1. Enviar horas = `1.5` o `"abc"`.
2. **Esperado**: HTTP **422**; **no** se persiste.

### E7 — Docente inexistente · supuesto de prototipo

1. Enviar `teacher_id` que no existe en el catálogo.
2. **Esperado**: HTTP **400**; **no** se persiste.

### E8 — Validación por API directa (sin formulario) · RF-11, CA-07

Comprobar que la validación del servidor no depende del cliente. Ejemplo en PowerShell contra un
proyecto no aprobado:

```powershell
# Rechazo esperado (regla de negocio): HTTP 400
$body = '{"teacher_id":1,"project_id":2,"hours":5}'
Invoke-WebRequest -Uri http://127.0.0.1:8000/api/assignments -Method POST `
  -ContentType "application/json" -Body $body
```

- **Esperado**: respuesta **400** (proyecto no aprobado) sin crear registro. Un `hours` inválido por
  esta misma vía debe devolver **422**.

### E9 — Consulta de asignaciones · CA-06, RF-10

```powershell
Invoke-WebRequest -Uri http://127.0.0.1:8000/api/assignments -Method GET
```

- **Esperado**: HTTP **200** con la lista de asignaciones válidas (incluye la de E1); lista vacía si
  no hay registros, sin error.

---

## Criterio de éxito de la demostración

El prototipo se considera validado cuando: E1 persiste y se consulta (E9); E2–E7 se rechazan con el
código correcto (400 o 422) sin persistir; E8 confirma la validación del servidor; y `pytest -v`
pasa en verde cubriendo cada requisito (SC-007). Tiempo estimado del recorrido: < 5 minutos (SC-006).
