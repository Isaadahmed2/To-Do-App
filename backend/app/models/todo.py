"""Pydantic models for To-Do items."""
from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class Priority(str, Enum):
    """Priority levels for To-Do items."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class TodoStatus(str, Enum):
    """Status of a To-Do item."""

    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"


class TodoCreate(BaseModel):
    """Model for creating a new To-Do item."""

    title: str = Field(..., min_length=1, max_length=200, description="Title of the todo item")
    description: Optional[str] = Field(default=None, description="Detailed description of the todo item")
    priority: Priority = Field(default=Priority.MEDIUM, description="Priority level of the todo item")


class TodoUpdate(BaseModel):
    """Model for updating an existing To-Do item."""

    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = None
    priority: Optional[Priority] = None
    status: Optional[TodoStatus] = None


class Todo(BaseModel):
    """Model representing a complete To-Do item."""

    id: str
    title: str
    description: Optional[str] = None
    priority: Priority
    status: TodoStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic configuration."""

        from_attributes = True
