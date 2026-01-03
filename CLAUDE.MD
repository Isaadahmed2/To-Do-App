# CLAUDE.MD

This file provides project-specific instructions for Claude Code when working on this codebase.

## General Guidelines

1. **Always write type hints** for all Python functions, methods, and variables.
2. **Use `uv`** as the package manager for Python projects. Create virtual environments using `uv venv`.
3. **Always implement proper exception handling** with meaningful error messages.
4. **Add proper comments** to explain complex logic, business rules, and non-obvious code.
5. **Create a logger system** with three log levels:
   - `minor`: For minor issues that don't affect functionality
   - `warning`: For warnings about potential problems
   - `bug`: For actual bugs and errors
6. **Use ReactJs** for frontend development.
7. **Use FastApi** for Python backend development.
8. **Make code modular** and use OOP concepts where appropriate.

## Project Structure

```
project-root/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # FastAPI application entry point
│   │   ├── config.py               # Configuration settings
│   │   ├── logger.py               # Logger setup
│   │   ├── models/                 # Data models (Pydantic/SQLAlchemy)
│   │   │   ├── __init__.py
│   │   │   └── ...
│   │   ├── routes/                 # API routes/endpoints
│   │   │   ├── __init__.py
│   │   │   └── ...
│   │   ├── services/               # Business logic services
│   │   │   ├── __init__.py
│   │   │   └── ...
│   │   ├── repositories/           # Data access layer
│   │   │   ├── __init__.py
│   │   │   └── ...
│   │   └── utils/                  # Utility functions
│   │       ├── __init__.py
│   │       └── ...
│   ├── pyproject.toml
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/             # React components
│   │   │   ├── __init__.py
│   │   │   └── ...
│   │   ├── pages/                  # Page components
│   │   │   ├── __init__.py
│   │   │   └── ...
│   │   ├── services/               # API service layer
│   │   │   ├── __init__.py
│   │   │   └── ...
│   │   ├── hooks/                  # Custom React hooks
│   │   │   ├── __init__.py
│   │   │   └── ...
│   │   ├── utils/                  # Utility functions
│   │   │   ├── __init__.py
│   │   │   └── ...
│   │   ├── types/                  # TypeScript types
│   │   │   ├── index.ts
│   │   │   └── ...
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   └── vite.config.ts
├── CLAUDE.MD
└── README.md
```

## Python Coding Standards

### Type Hints
Always use type hints for:
- Function parameters and return types
- Class attributes
- Variable declarations

```python
from typing import List, Optional, Dict, Any

def process_items(items: List[str], threshold: int = 10) -> Dict[str, Any]:
    """Process a list of items and return results."""
    result: Dict[str, Any] = {}
    return result

class UserService:
    def __init__(self, user_id: int, name: str) -> None:
        self.user_id: int = user_id
        self.name: str = name

    def get_user(self) -> Optional[Dict[str, Any]]:
        """Get user data from database."""
        pass
```

### Exception Handling
Always use try-except blocks with specific exception types and meaningful messages.

```python
import logging
from typing import Any, Dict
from requests import RequestException

logger = logging.getLogger(__name__)

def fetch_user_data(user_id: int) -> Dict[str, Any]:
    """Fetch user data from external API."""
    try:
        response = requests.get(f"/api/users/{user_id}")
        response.raise_for_status()
        return response.json()
    except RequestException as e:
        logger.error(f"Failed to fetch user data for ID {user_id}: {e}")
        raise ValueError(f"Unable to fetch user {user_id}") from e
    except (KeyError, ValueError) as e:
        logger.warning(f"Invalid data format for user {user_id}: {e}")
        raise
```

### Commenting
- Use docstrings for all public classes, functions, and methods
- Add inline comments for complex logic
- Comment business rules and non-obvious decisions

```python
class OrderProcessor:
    """
    Processes customer orders and applies discounts.

    This class handles order validation, discount application,
    and order persistence following business rules defined in
    the company policy document (Section 3.2).
    """

    def apply_discount(self, order: Order, discount_code: str) -> float:
        """
        Apply a discount code to the order.

        Args:
            order: The order to apply discount to
            discount_code: Valid discount code string

        Returns:
            The discounted total amount

        Raises:
            InvalidDiscountCode: If the discount code is invalid or expired
        """
        # Apply 10% discount for first-time customers
        # This business rule is documented in: PRD-2024-001
        if order.is_first_customer:
            discount_rate = 0.10
        else:
            discount_rate = 0.05
```

## Logger System

Use the following log levels in the specified scenarios:

### Minor Issues
Log at `INFO` level for minor issues that don't affect functionality but should be tracked.

```python
logger.info(f"Minor: User {user_id} performed action: {action}")
```

### Warnings
Log at `WARNING` level for situations that could lead to problems.

```python
logger.warning(f"Warning: Rate limit approaching for user {user_id}")
logger.warning(f"Warning: Deprecated API version used by client: {client_version}")
```

### Bugs/Errors
Log at `ERROR` level for actual bugs and errors.

```python
logger.error(f"Bug: Unexpected error processing order {order_id}: {error}")
logger.exception(f"Bug: Database connection failed after 3 retries")
```

### Logger Setup Example

```python
# backend/app/logger.py
import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional

class CustomLogger:
    """Custom logger with file and console output."""

    def __init__(self, name: str, log_dir: Optional[Path] = None) -> None:
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(
            logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        )
        self.logger.addHandler(console_handler)

        # File handler (if log directory provided)
        if log_dir:
            log_dir.mkdir(parents=True, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_handler = logging.FileHandler(
                log_dir / f"{name}_{timestamp}.log"
            )
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(
                logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
            )
            self.logger.addHandler(file_handler)

    def minor(self, message: str) -> None:
        """Log minor issues."""
        self.logger.info(f"MINOR: {message}")

    def warning(self, message: str) -> None:
        """Log warnings."""
        self.logger.warning(f"WARNING: {message}")

    def bug(self, message: str) -> None:
        """Log bugs and errors."""
        self.logger.error(f"BUG: {message}")


# Usage
logger = CustomLogger("app", Path("logs"))
logger.minor("Service started successfully")
logger.warning("Cache memory usage above 80%")
logger.bug("Failed to process user request")
```

## Frontend (ReactJs) Guidelines

### TypeScript Usage
- Use TypeScript for all React components
- Define proper interfaces for props and state
- Use generic types where applicable

```typescript
// types/index.ts
interface User {
  id: number;
  name: string;
  email: string;
}

interface UserListProps {
  users: User[];
  onUserSelect: (user: User) => void;
  isLoading: boolean;
}

// components/UserList.tsx
import React from 'react';
import { UserListProps } from '../types';

export const UserList: React.FC<UserListProps> = ({
  users,
  onUserSelect,
  isLoading,
}) => {
  if (isLoading) {
    return <div>Loading...</div>;
  }

  return (
    <ul>
      {users.map((user) => (
        <li key={user.id} onClick={() => onUserSelect(user)}>
          {user.name}
        </li>
      ))}
    </ul>
  );
};
```

## Backend (FastApi) Guidelines

### Project Structure
- Use FastApi for API development
- Create modular routers with proper separation of concerns
- Use dependency injection for services and repositories

```python
# backend/app/main.py
from fastapi import FastAPI
from app.routes import users, orders

app = FastAPI(title="My API")

app.include_router(users.router, prefix="/api/users")
app.include_router(orders.router, prefix="/api/orders")
```

## OOP Principles

Use classes for:
- Service layer (business logic)
- Repository layer (data access)
- Configuration management
- Custom utilities

Keep functions pure where possible and use composition over inheritance.

```python
from abc import ABC, abstractmethod
from typing import Protocol

class Repository(Protocol):
    """Protocol for repository pattern."""

    def get(self, id: int) -> Optional[Any]:
        ...

    def create(self, entity: Any) -> Any:
        ...

class UserRepository:
    """Concrete implementation of user repository."""

    def __init__(self, db_session: Session) -> None:
        self.db = db_session

    def get(self, user_id: int) -> Optional[User]:
        """Fetch user by ID."""
        return self.db.query(User).filter(User.id == user_id).first()

    def create(self, user: User) -> User:
        """Create a new user."""
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
```

## Package Management

Always use `uv` for Python package management:

```bash
# Create virtual environment
uv venv

# Activate virtual environment (Windows)
.venv\Scripts\activate

# Install dependencies
uv pip install -r requirements.txt

# Add new dependency
uv pip add package_name

# Sync dependencies
uv pip sync requirements.txt
```
