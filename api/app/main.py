import os
import time
from datetime import datetime
from typing import Generator

import psycopg
from psycopg.rows import dict_row
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://taskuser:taskpass@database:5432/tasksdb",
)

app = FastAPI(title="Task Manager API", version="1.0.0")


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(default="", max_length=2000)
    completed: bool = False


class Task(TaskCreate):
    id: int
    created_at: datetime
    updated_at: datetime


def get_connection(retries: int = 20) -> psycopg.Connection:
    last_error = None
    for _ in range(retries):
        try:
            return psycopg.connect(DATABASE_URL, row_factory=dict_row)
        except psycopg.OperationalError as exc:
            last_error = exc
            time.sleep(1)
    raise last_error


def init_db() -> None:
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id SERIAL PRIMARY KEY,
                title VARCHAR(200) NOT NULL,
                description VARCHAR(2000) NOT NULL DEFAULT '',
                completed BOOLEAN NOT NULL DEFAULT FALSE,
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
            )
            """
        )
        conn.commit()


@app.on_event("startup")
def startup() -> None:
    init_db()


@app.get("/health")
def health() -> dict[str, str]:
    with get_connection() as conn:
        conn.execute("SELECT 1")
    return {"status": "ok"}


@app.get("/api/tasks", response_model=list[Task])
def list_tasks() -> list[Task]:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT id, title, description, completed, created_at, updated_at "
            "FROM tasks ORDER BY id"
        ).fetchall()
    return [Task(**dict(row)) for row in rows]


@app.get("/api/tasks/{task_id}", response_model=Task)
def get_task(task_id: int) -> Task:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT id, title, description, completed, created_at, updated_at "
            "FROM tasks WHERE id = %s",
            (task_id,),
        ).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return Task(**dict(row))


@app.post("/api/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate) -> Task:
    with get_connection() as conn:
        row = conn.execute(
            "INSERT INTO tasks (title, description, completed) VALUES (%s, %s, %s) "
            "RETURNING id, title, description, completed, created_at, updated_at",
            (payload.title, payload.description, payload.completed),
        ).fetchone()
        conn.commit()
    return Task(**dict(row))


@app.put("/api/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, payload: TaskCreate) -> Task:
    with get_connection() as conn:
        row = conn.execute(
            "UPDATE tasks SET title=%s, description=%s, completed=%s, updated_at=NOW() "
            "WHERE id=%s RETURNING id, title, description, completed, created_at, updated_at",
            (payload.title, payload.description, payload.completed, task_id),
        ).fetchone()
        conn.commit()
    if row is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return Task(**dict(row))


@app.delete("/api/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int) -> None:
    with get_connection() as conn:
        result = conn.execute("DELETE FROM tasks WHERE id=%s", (task_id,))
        conn.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Task not found")
