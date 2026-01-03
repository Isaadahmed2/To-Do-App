"""Storage service for persisting To-Do items to JSON file."""
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from app.logger import logger
from app.models.todo import Priority, Todo, TodoCreate, TodoStatus, TodoUpdate


class JSONStorageService:
    """
    Service for managing To-Do data persistence using JSON file storage.

    This service handles all CRUD operations for To-Do items,
    persisting data to a local JSON file for session persistence.
    """

    def __init__(self, storage_path: Path) -> None:
        """
        Initialize the JSON storage service.

        Args:
            storage_path: Path to the JSON file for data persistence
        """
        self.storage_path = storage_path
        self._ensure_storage_file()

    def _ensure_storage_file(self) -> None:
        """Create the storage file if it doesn't exist."""
        try:
            if not self.storage_path.exists():
                self.storage_path.parent.mkdir(parents=True, exist_ok=True)
                self._save_to_file([])
                logger.minor(f"Created new storage file at {self.storage_path}")
            else:
                logger.minor(f"Using existing storage file at {self.storage_path}")
        except Exception as e:
            logger.bug(f"Failed to ensure storage file exists: {e}")
            raise

    def _load_from_file(self) -> List[Dict[str, Any]]:
        """
        Load To-Do items from the JSON storage file.

        Returns:
            List of To-Do item dictionaries

        Raises:
            RuntimeError: If file cannot be read
        """
        try:
            with open(self.storage_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            logger.minor(f"Loaded {len(data)} items from storage")
            return data
        except FileNotFoundError:
            logger.warning("Storage file not found, returning empty list")
            return []
        except json.JSONDecodeError as e:
            logger.bug(f"Failed to decode JSON from storage file: {e}")
            raise RuntimeError(f"Invalid JSON in storage file: {e}") from e
        except Exception as e:
            logger.bug(f"Unexpected error reading storage file: {e}")
            raise

    def _save_to_file(self, items: List[Dict[str, Any]]) -> None:
        """
        Save To-Do items to the JSON storage file.

        Args:
            items: List of To-Do item dictionaries to save

        Raises:
            RuntimeError: If file cannot be written
        """
        try:
            with open(self.storage_path, "w", encoding="utf-8") as f:
                json.dump(items, f, indent=2, ensure_ascii=False)
            logger.minor(f"Saved {len(items)} items to storage")
        except Exception as e:
            logger.bug(f"Failed to save to storage file: {e}")
            raise RuntimeError(f"Failed to save data: {e}") from e

    def _generate_id(self) -> str:
        """
        Generate a unique ID for a new To-Do item.

        Returns:
            Unique string ID
        """
        return datetime.now().strftime("%Y%m%d%H%M%S%f")

    def _dict_to_todo(self, data: Dict[str, Any]) -> Todo:
        """
        Convert a dictionary to a Todo object.

        Args:
            data: Dictionary containing todo data

        Returns:
            Todo model instance
        """
        return Todo(
            id=data["id"],
            title=data["title"],
            description=data.get("description"),
            priority=Priority(data["priority"]),
            status=TodoStatus(data["status"]),
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]),
        )

    def get_all(self) -> List[Todo]:
        """
        Retrieve all To-Do items from storage.

        Returns:
            List of all To-Do items, ordered by priority (high to low) then by creation date
        """
        try:
            items = self._load_from_file()
            todos = [self._dict_to_todo(item) for item in items]
            # Sort by priority (high first) then by creation date (newest first)
            priority_order = {Priority.HIGH: 0, Priority.MEDIUM: 1, Priority.LOW: 2}
            todos.sort(key=lambda x: (priority_order[x.priority], -x.created_at.timestamp()))
            return todos
        except Exception as e:
            logger.bug(f"Error getting all todos: {e}")
            raise

    def get_by_id(self, todo_id: str) -> Optional[Todo]:
        """
        Retrieve a specific To-Do item by ID.

        Args:
            todo_id: The unique identifier of the To-Do item

        Returns:
            Todo if found, None otherwise
        """
        try:
            items = self._load_from_file()
            for item in items:
                if item["id"] == todo_id:
                    return self._dict_to_todo(item)
            return None
        except Exception as e:
            logger.bug(f"Error getting todo by ID {todo_id}: {e}")
            raise

    def create(self, todo_data: TodoCreate) -> Todo:
        """
        Create a new To-Do item.

        Args:
            todo_data: Data for the new To-Do item

        Returns:
            The created Todo object
        """
        try:
            now = datetime.now()
            new_todo = {
                "id": self._generate_id(),
                "title": todo_data.title,
                "description": todo_data.description,
                "priority": todo_data.priority.value,
                "status": TodoStatus.PENDING.value,
                "created_at": now.isoformat(),
                "updated_at": now.isoformat(),
            }

            items = self._load_from_file()
            items.append(new_todo)
            self._save_to_file(items)

            logger.minor(f"Created new todo with ID: {new_todo['id']}")
            return self._dict_to_todo(new_todo)
        except Exception as e:
            logger.bug(f"Error creating todo: {e}")
            raise

    def update(self, todo_id: str, update_data: TodoUpdate) -> Optional[Todo]:
        """
        Update an existing To-Do item.

        Args:
            todo_id: The unique identifier of the To-Do item to update
            update_data: Fields to update

        Returns:
            The updated Todo object, or None if not found
        """
        try:
            items = self._load_from_file()
            updated = False

            for item in items:
                if item["id"] == todo_id:
                    # Update fields if provided
                    if update_data.title is not None:
                        item["title"] = update_data.title
                    if update_data.description is not None:
                        item["description"] = update_data.description
                    if update_data.priority is not None:
                        item["priority"] = update_data.priority.value
                    if update_data.status is not None:
                        item["status"] = update_data.status.value

                    item["updated_at"] = datetime.now().isoformat()
                    self._save_to_file(items)
                    updated = True

                    logger.minor(f"Updated todo with ID: {todo_id}")
                    return self._dict_to_todo(item)

            if not updated:
                logger.warning(f"Todo with ID {todo_id} not found for update")
                return None
        except Exception as e:
            logger.bug(f"Error updating todo {todo_id}: {e}")
            raise

    def delete(self, todo_id: str) -> bool:
        """
        Delete a To-Do item.

        Args:
            todo_id: The unique identifier of the To-Do item to delete

        Returns:
            True if deleted, False if not found
        """
        try:
            items = self._load_from_file()
            original_count = len(items)

            items = [item for item in items if item["id"] != todo_id]

            if len(items) < original_count:
                self._save_to_file(items)
                logger.minor(f"Deleted todo with ID: {todo_id}")
                return True
            else:
                logger.warning(f"Todo with ID {todo_id} not found for deletion")
                return False
        except Exception as e:
            logger.bug(f"Error deleting todo {todo_id}: {e}")
            raise

    def mark_completed(self, todo_id: str) -> Optional[Todo]:
        """
        Mark a To-Do item as completed.

        Args:
            todo_id: The unique identifier of the To-Do item

        Returns:
            The updated Todo object, or None if not found
        """
        return self.update(todo_id, TodoUpdate(status=TodoStatus.COMPLETED))

    def mark_failed(self, todo_id: str) -> Optional[Todo]:
        """
        Mark a To-Do item as failed.

        Args:
            todo_id: The unique identifier of the To-Do item

        Returns:
            The updated Todo object, or None if not found
        """
        return self.update(todo_id, TodoUpdate(status=TodoStatus.FAILED))

    def set_priority(self, todo_id: str, priority: Priority) -> Optional[Todo]:
        """
        Set the priority of a To-Do item.

        Args:
            todo_id: The unique identifier of the To-Do item
            priority: The new priority level

        Returns:
            The updated Todo object, or None if not found
        """
        return self.update(todo_id, TodoUpdate(priority=priority))
