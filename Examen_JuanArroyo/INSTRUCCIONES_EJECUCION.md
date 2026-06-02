# Instrucciones de Ejecución

Este repositorio contiene dos proyectos base:
1. **Control Gastos Personales**: API y aplicación en Python (Flask).
2. **EPN Event Manager**: API y frontend desarrollados en TypeScript (NestJS) / Node.js.

*(Nota: En lugar de React puro, el frontend está integrado en el proyecto de NestJS como un dashboard estático incluido dentro de la misma aplicación Node.js).*

A continuación, los pasos para la instalación y ejecución de cada entorno:

---

## 1. Proyecto en Python: Control Gastos Personales (Flask)

Este proyecto maneja la API para los gastos y está en el directorio `control_gastos_personales`.

### Prerrequisitos
- **Python 3.8+**
- **pip** (Manejador de paquetes de Python)

### Pasos de Ejecución

1. Entra al directorio del proyecto:
   ```bash
   cd control_gastos_personales
   ```

2. (Recomendado) Crea un entorno virtual para instalar las dependencias de manera aislada:
   **En Windows:**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```
   **En macOS/Linux:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

3. Instala los requerimientos:
   ```bash
   pip install -r requirements.txt
   ```

4. Ejecuta la aplicación de Flask:
   ```bash
   flask --app app run --debug
   ```
   *La aplicación generalmente estará disponible en `http://127.0.0.1:5000`.*

---

## 2. Proyecto en Node.js/TypeScript: EPN Event Manager (NestJS)

Esta aplicación incluye tanto la API para los eventos y estadísticas como el código del "Dashboard" (frontend). El frontend se sirve desde la carpeta estática `public/dashboard`.

### Prerrequisitos
- **Node.js** (Versión 18+ recomendada)
- **npm** (Viene integrado con Node.js)

### Pasos de Ejecución

1. Entra al directorio del proyecto:
   ```bash
   cd epn-event-manager
   ```

2. Instala todas las dependencias del proyecto:
   ```bash
   npm install
   ```

3. Para que la base de datos se inicialice correctamente (SQLite), debes ejecutar la migración inicial:
   ```bash
   npm run migration:run
   ```

4. Ejecuta el servidor en modo de desarrollo interactivo:
   ```bash
   npm run start:dev
   ```

5. Opciones para el frontend y la API:
   - **Frontend (Dashboard):** Visita tu navegador e ingresa a `http://localhost:3000/dashboard/`.
   - **API (salud de la app):** `http://localhost:3000/health`.

---
