# Control de Gastos Personales

CRUD Flask para el examen práctico de **Mantenimiento de Software** (FIS EPN). Integra eventos con [epn-event-manager](../epn-event-manager).

## Requisitos del examen implementados

| Tipo | Implementación |
|------|----------------|
| **Correctivo** | Validación de entrada, corrección de `PUT` con JSON nulo, IDs duplicados, códigos HTTP del Event Manager |
| **Adaptativo** | Header obligatorio `X-FIS-EPN-KEY`, configuración en `.env_config` / variables de entorno |
| **Perfectivo** | Pruebas unitarias (`pytest`), documentación OpenAPI en `docs/openapi.yaml` |
| **Preventivo** | Sanitización de campos, límites de longitud, `try/except` por endpoint, logs de auditoría |

## Dónde se guarda cada cosa

| Dato | Ubicación |
|------|-----------|
| **Gastos del CRUD** | `db/gastos.sqlite` (tabla `gastos`) |
| **Logs de la aplicación** | `logs/audit.log` |
| **Eventos de auditoría** | `epn-event-manager/db/events.sqlite` |

## Variables de entorno

Copie `.env.example` a `.env_config`:

```bash
APP_PORT=5000
FIS_API_KEY=su-clave-secreta
EVENT_MANAGER_URL=http://localhost:3000/events
LOG_LEVEL=INFO
LOG_FILE=logs/audit.log
DB_DATABASE=db/gastos.sqlite
```

## Ejecución

```bash
pip install -r requirements.txt
python app.py
```

Interfaz: http://localhost:5000/

## API

Todas las rutas `/gastos*` requieren el header:

```
X-FIS-EPN-KEY: <valor de FIS_API_KEY>
```

Ejemplo con curl:

```bash
curl -H "X-FIS-EPN-KEY: su-clave-secreta" http://localhost:5000/gastos
```

## Pruebas

```bash
pytest tests/ -v
```

## Logs

Logs estructurados JSON con niveles INFO, WARNING y ERROR en consola y en `logs/audit.log` (timestamp ISO 8601).
