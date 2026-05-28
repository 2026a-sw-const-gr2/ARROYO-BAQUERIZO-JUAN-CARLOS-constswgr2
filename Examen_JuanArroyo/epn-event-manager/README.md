# EPN Event Manager

API NestJS para registrar y consultar eventos de dominio (creación, actualización, eliminación y consulta) desde distintos sistemas (por ejemplo, control de gastos personales).

## Arquitectura

```
src/
├── main.ts                 # Bootstrap + ValidationPipe global
├── app.module.ts
├── database/
│   ├── database.module.ts  # TypeORM + variables de entorno
│   ├── data-source.ts      # CLI de migraciones
│   ├── entities/event.entity.ts
│   └── migrations/
└── modules/
    ├── events/             # Registro y consulta de eventos
    ├── stats/              # Estadísticas (desacoplado de Events)
    ├── health/             # Health check con verificación de BD
    └── dashboard/          # Vista estática en /dashboard
public/dashboard/           # HTML, CSS y JS (separados del backend)
```

Los eventos se almacenan en una única tabla `events` con columna `action` (`CREATE`, `UPDATE`, `DELETE`, `QUERY`) y fecha `created_at` en UTC.

## Requisitos

- Node.js 18+
- npm

## Configuración

1. Instalar dependencias:

```bash
npm install
```

2. Copiar variables de entorno:

```bash
cp .env.example .env
```

| Variable | Descripción | Valor por defecto |
|----------|-------------|-------------------|
| `PORT` | Puerto HTTP | `3000` |
| `DB_DATABASE` | Ruta del archivo SQLite | `db/events.sqlite` |
| `DB_SYNCHRONIZE` | Sincronizar esquema automáticamente (solo dev) | `false` |
| `DB_RUN_MIGRATIONS` | Ejecutar migraciones al iniciar | `true` |

3. Crear carpeta de base de datos (si no existe):

```bash
mkdir -p db
```

## Ejecución

```bash
# Desarrollo con recarga
npm run start:dev

# Producción
npm run build
npm run start:prod
```

Migraciones manuales (opcional):

```bash
npm run migration:run
npm run migration:revert
```

## Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| `POST` | `/events` | Registrar un evento |
| `GET` | `/events` | Listar eventos (ordenados por `created_at` DESC) |
| `GET` | `/events/:id` | Obtener evento por ID (numérico) |
| `GET` | `/events/source/:source` | Filtrar por origen |
| `GET` | `/events/entity/:entity` | Filtrar por entidad |
| `GET` | `/stats` | Contadores por acción y total |
| `GET` | `/health` | Estado de la API y conexión a BD |
| `GET` | `/dashboard` | Panel web estático |

### Ejemplo: registrar evento DELETE

```bash
curl -X POST http://localhost:3000/events \
  -H "Content-Type: application/json" \
  -d '{
    "source": "control-gastos",
    "entity": "expense",
    "action": "DELETE",
    "title": "Gasto eliminado",
    "payload": { "id": "42" }
  }'
```

### Ejemplo: estadísticas

```bash
curl http://localhost:3000/stats
```

Respuesta:

```json
{
  "create": 10,
  "update": 5,
  "delete": 2,
  "query": 3,
  "total": 20
}
```

## Calidad de código

```bash
npm run lint        # Solo revisión (sin modificar archivos)
npm run lint:fix    # Revisión y corrección automática
npm run test
```

## Integración

Otros servicios pueden enviar eventos HTTP a esta API. Configure `EVENT_MANAGER_URL` (o equivalente) en el cliente apuntando a la URL base de este servicio.
