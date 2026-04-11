import sqlite3
import threading
from pathlib import Path
from .models import Task


class TaskRepository:
    def __init__(self, db_path: str | Path = "database.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()
        self._create_table()

    def _get_connection(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.db_path, check_same_thread=False)
        connection.row_factory = sqlite3.Row
        return connection

    def _create_table(self) -> None:
        connection = self._get_connection()
        try:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL,
                    completed INTEGER NOT NULL DEFAULT 0,
                    created_at TEXT NOT NULL
                )
                """
            )
            connection.commit()
        finally:
            connection.close()

    def create_task(self, title: str, description: str) -> Task:
        connection = self._get_connection()
        try:
            with self._lock:
                cursor = connection.execute(
                    "INSERT INTO tasks (title, description, completed, created_at) VALUES (?, ?, ?, datetime('now'))",
                    (title.strip(), description.strip(), 0),
                )
                task_id = cursor.lastrowid
                connection.commit()
                row = connection.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
                return Task.from_row(tuple(row))
        finally:
            connection.close()

    def get_task(self, task_id: int) -> Task | None:
        connection = self._get_connection()
        try:
            row = connection.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
            return Task.from_row(tuple(row)) if row else None
        finally:
            connection.close()

    def list_tasks(self) -> list[Task]:
        connection = self._get_connection()
        try:
            rows = connection.execute("SELECT * FROM tasks ORDER BY created_at DESC").fetchall()
            return [Task.from_row(tuple(row)) for row in rows]
        finally:
            connection.close()

    def update_task(self, task_id: int, data: dict) -> Task | None:
        existing = self.get_task(task_id)
        if existing is None:
            return None

        title = data.get("title", existing.title)
        if title is None:
            title = existing.title

        description = data.get("description", existing.description)
        if description is None:
            description = existing.description

        completed = data.get("completed", existing.completed)

        updated_values = {
            "title": title.strip(),
            "description": description.strip(),
            "completed": 1 if completed else 0,
        }
        connection = self._get_connection()
        try:
            with self._lock:
                connection.execute(
                    "UPDATE tasks SET title = ?, description = ?, completed = ? WHERE id = ?",
                    (updated_values["title"], updated_values["description"], updated_values["completed"], task_id),
                )
                connection.commit()
                row = connection.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
                return Task.from_row(tuple(row))
        finally:
            connection.close()

    def delete_task(self, task_id: int) -> bool:
        connection = self._get_connection()
        try:
            with self._lock:
                cursor = connection.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
                connection.commit()
                return cursor.rowcount > 0
        finally:
            connection.close()
