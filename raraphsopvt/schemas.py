from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = Field(default="", max_length=500)

    model_config = {"extra": "forbid"}


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=3, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    completed: Optional[bool] = None

    model_config = {"extra": "forbid"}


class TaskResponse(TaskCreate):
    id: int
    completed: bool
    created_at: datetime

    model_config = {"from_attributes": True}
