"""API routes for To-Do items."""
from typing import List, Optional

from fastapi import APIRouter, HTTPException

from app.logger import logger
from app.models.todo import Priority, Todo, TodoCreate, TodoStatus, TodoUpdate
from app.services.storage import JSONStorageService
from pathlib import Path


# Initialize storage service with data directory
storage = JSONStorageService(Path("data/todos.json"))

router = APIRouter(prefix="/todos", tags=["todos"])


@router.get("", response_model=List[Todo])
def get_all_todos() -> List[Todo]:
    """
    Retrieve all To-Do items.

    Returns:
        List of all To-Do items sorted by priority and creation date
    """
    try:
        todos = storage.get_all()
        logger.minor(f"Retrieved {len(todos)} todos")
        return todos
    except Exception as e:
        logger.bug(f"Error retrieving all todos: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve todos")


@router.get("/{todo_id}", response_model=Todo)
def get_todo(todo_id: str) -> Todo:
    """
    Retrieve a specific To-Do item by ID.

    Args:
        todo_id: The unique identifier of the To-Do item

    Returns:
        The To-Do item

    Raises:
        HTTPException: If To-Do item not found
    """
    try:
        todo = storage.get_by_id(todo_id)
        if todo is None:
            logger.warning(f"Todo with ID {todo_id} not found")
            raise HTTPException(status_code=404, detail="Todo not found")
        return todo
    except HTTPException:
        raise
    except Exception as e:
        logger.bug(f"Error retrieving todo {todo_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve todo")


@router.post("", response_model=Todo, status_code=201)
def create_todo(todo_data: TodoCreate) -> Todo:
    """
    Create a new To-Do item.

    Args:
        todo_data: Data for the new To-Do item

    Returns:
        The created To-Do item
    """
    try:
        todo = storage.create(todo_data)
        logger.minor(f"Created todo: {todo.id}")
        return todo
    except Exception as e:
        logger.bug(f"Error creating todo: {e}")
        raise HTTPException(status_code=500, detail="Failed to create todo")


@router.put("/{todo_id}", response_model=Todo)
def update_todo(todo_id: str, update_data: TodoUpdate) -> Todo:
    """
    Update an existing To-Do item.

    Args:
        todo_id: The unique identifier of the To-Do item to update
        update_data: Fields to update

    Returns:
        The updated To-Do item

    Raises:
        HTTPException: If To-Do item not found
    """
    try:
        todo = storage.update(todo_id, update_data)
        if todo is None:
            logger.warning(f"Todo with ID {todo_id} not found for update")
            raise HTTPException(status_code=404, detail="Todo not found")
        logger.minor(f"Updated todo: {todo_id}")
        return todo
    except HTTPException:
        raise
    except Exception as e:
        logger.bug(f"Error updating todo {todo_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to update todo")


@router.delete("/{todo_id}", status_code=204)
def delete_todo(todo_id: str) -> None:
    """
    Delete a To-Do item.

    Args:
        todo_id: The unique identifier of the To-Do item to delete

    Raises:
        HTTPException: If To-Do item not found
    """
    try:
        deleted = storage.delete(todo_id)
        if not deleted:
            logger.warning(f"Todo with ID {todo_id} not found for deletion")
            raise HTTPException(status_code=404, detail="Todo not found")
        logger.minor(f"Deleted todo: {todo_id}")
    except HTTPException:
        raise
    except Exception as e:
        logger.bug(f"Error deleting todo {todo_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete todo")


@router.post("/{todo_id}/complete", response_model=Todo)
def mark_completed(todo_id: str) -> Todo:
    """
    Mark a To-Do item as completed.

    Args:
        todo_id: The unique identifier of the To-Do item

    Returns:
        The updated To-Do item

    Raises:
        HTTPException: If To-Do item not found
    """
    try:
        todo = storage.mark_completed(todo_id)
        if todo is None:
            logger.warning(f"Todo with ID {todo_id} not found for completion")
            raise HTTPException(status_code=404, detail="Todo not found")
        logger.minor(f"Marked todo as completed: {todo_id}")
        return todo
    except HTTPException:
        raise
    except Exception as e:
        logger.bug(f"Error marking todo {todo_id} as completed: {e}")
        raise HTTPException(status_code=500, detail="Failed to mark as completed")


@router.post("/{todo_id}/fail", response_model=Todo)
def mark_failed(todo_id: str) -> Todo:
    """
    Mark a To-Do item as failed.

    Args:
        todo_id: The unique identifier of the To-Do item

    Returns:
        The updated To-Do item

    Raises:
        HTTPException: If To-Do item not found
    """
    try:
        todo = storage.mark_failed(todo_id)
        if todo is None:
            logger.warning(f"Todo with ID {todo_id} not found for failure marking")
            raise HTTPException(status_code=404, detail="Todo not found")
        logger.minor(f"Marked todo as failed: {todo_id}")
        return todo
    except HTTPException:
        raise
    except Exception as e:
        logger.bug(f"Error marking todo {todo_id} as failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to mark as failed")


@router.put("/{todo_id}/priority", response_model=Todo)
def set_priority(todo_id: str, priority: Priority) -> Todo:
    """
    Set the priority of a To-Do item.

    Args:
        todo_id: The unique identifier of the To-Do item
        priority: The new priority level

    Returns:
        The updated To-Do item

    Raises:
        HTTPException: If To-Do item not found
    """
    try:
        todo = storage.set_priority(todo_id, priority)
        if todo is None:
            logger.warning(f"Todo with ID {todo_id} not found for priority update")
            raise HTTPException(status_code=404, detail="Todo not found")
        logger.minor(f"Set priority for todo {todo_id} to {priority.value}")
        return todo
    except HTTPException:
        raise
    except Exception as e:
        logger.bug(f"Error setting priority for todo {todo_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to set priority")
