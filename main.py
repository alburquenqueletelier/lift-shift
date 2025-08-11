from typing import Optional, List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Field, SQLModel, create_engine, Session, select

# ---------------------------
# Modelos / DB
# ---------------------------
class Todo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = None
    done: bool = Field(default=False)


DATABASE_URL = "sqlite:///./todos.db"
# check_same_thread False permite uso desde distintos hilos (uvicorn workers)
engine = create_engine(DATABASE_URL, echo=False, connect_args={"check_same_thread": False})

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# ---------------------------
# App
# ---------------------------
app = FastAPI(title="Todo API - FastAPI + SQLite")

# CORS (opcional, útil si tienes un frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # en producción ajusta esto
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# ---------------------------
# Endpoints CRUD
# ---------------------------

# Create
@app.post("/todos/", response_model=Todo, status_code=201)
def create_todo(todo: Todo):
    with Session(engine) as session:
        session.add(todo)
        session.commit()
        session.refresh(todo)
        return todo

# Read all
@app.get("/todos/", response_model=List[Todo])
def read_todos(skip: int = 0, limit: int = 100):
    with Session(engine) as session:
        statement = select(Todo).offset(skip).limit(limit)
        results = session.exec(statement).all()
        return results

# Read one
@app.get("/todos/{todo_id}", response_model=Todo)
def read_todo(todo_id: int):
    with Session(engine) as session:
        todo = session.get(Todo, todo_id)
        if not todo:
            raise HTTPException(status_code=404, detail="Todo not found")
        return todo

# Update (reemplazo total)
@app.put("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, updated: Todo):
    with Session(engine) as session:
        todo = session.get(Todo, todo_id)
        if not todo:
            raise HTTPException(status_code=404, detail="Todo not found")
        # actualizar campos
        todo.title = updated.title
        todo.description = updated.description
        todo.done = updated.done
        session.add(todo)
        session.commit()
        session.refresh(todo)
        return todo

# Patch parcial (solo campos enviados)
@app.patch("/todos/{todo_id}", response_model=Todo)
def patch_todo(todo_id: int, title: Optional[str] = None, description: Optional[str] = None, done: Optional[bool] = None):
    with Session(engine) as session:
        todo = session.get(Todo, todo_id)
        if not todo:
            raise HTTPException(status_code=404, detail="Todo not found")
        if title is not None:
            todo.title = title
        if description is not None:
            todo.description = description
        if done is not None:
            todo.done = done
        session.add(todo)
        session.commit()
        session.refresh(todo)
        return todo

# Delete
@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: int):
    with Session(engine) as session:
        todo = session.get(Todo, todo_id)
        if not todo:
            raise HTTPException(status_code=404, detail="Todo not found")
        session.delete(todo)
        session.commit()
        return None
