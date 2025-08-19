# Todo API - FastAPI + SQLite

Este proyecto es una API REST para gestionar tareas (todos), construida con FastAPI y SQLite. Se puede levantar fácilmente usando Docker.

## Características
- CRUD completo de tareas (crear, leer, actualizar, eliminar)
- Base de datos SQLite embebida
- CORS habilitado (útil para frontends)
- Dockerfile listo para producción

## Requisitos
- Docker

## Levantar el servicio

1. **Construir la imagen Docker:**
   ```bash
   docker build -t todos_app .
   ```

2. **Ejecutar el contenedor:**
   ```bash
   docker run -d -p 8000:8000 --name todos_app todos_app:latest
   ```

3. **Acceder a la API:**
   - Documentación interactiva: [http://localhost:8000/docs](http://localhost:8000/docs)
   - Endpoints disponibles:
     - `GET /todos/` - Listar tareas
     - `POST /todos/` - Crear tarea
     - `GET /todos/{id}` - Obtener tarea
     - `PUT /todos/{id}` - Actualizar tarea
     - `PATCH /todos/{id}` - Actualización parcial
     - `DELETE /todos/{id}` - Eliminar tarea

## Estructura del proyecto
- `main.py`: Código principal de la API
- `requirements.txt`: Dependencias Python
- `Dockerfile`: Imagen Docker
- `todos.db`: Base de datos SQLite (se crea automáticamente)

## Personalización
- Puedes modificar los modelos y endpoints en `main.py` según tus necesidades.
- Para desarrollo local sin Docker:
  ```bash
  pip install -r requirements.txt
  uvicorn main:app --reload
  ```

## Licencia
MIT
