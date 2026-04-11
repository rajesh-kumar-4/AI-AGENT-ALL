from dataclasses import dataclass
from datetime import datetime


@dataclass
class Task:
    id: int
    title: str
    description: str
    completed: bool
    created_at: datetime

    @classmethod
    def from_row(cls, row: tuple) -> "Task":
        return cls(
            id=row[0],
            title=row[1],
            description=row[2],
            completed=bool(row[3]),
            created_at=datetime.fromisoformat(row[4]),
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed,
            "created_at": self.created_at.isoformat(),
        }
