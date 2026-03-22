from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uuid

app = FastAPI(title="Todo API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

todos: dict[str, dict] = {}


class TodoCreate(BaseModel):
    title: str


class TodoUpdate(BaseModel):
    title: Optional[str] = None
    completed: Optional[bool] = None


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/todos")
def list_todos():
    return list(todos.values())


@app.post("/api/todos", status_code=201)
def create_todo(body: TodoCreate):
    todo_id = str(uuid.uuid4())
    todo = {"id": todo_id, "title": body.title, "completed": False}
    todos[todo_id] = todo
    return todo


@app.put("/api/todos/{todo_id}")
def update_todo(todo_id: str, body: TodoUpdate):
    if todo_id not in todos:
        raise HTTPException(status_code=404, detail="Todo not found")
    if body.title is not None:
        todos[todo_id]["title"] = body.title
    if body.completed is not None:
        todos[todo_id]["completed"] = body.completed
    return todos[todo_id]


@app.delete("/api/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: str):
    if todo_id not in todos:
        raise HTTPException(status_code=404, detail="Todo not found")
    del todos[todo_id]
