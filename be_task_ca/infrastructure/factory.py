from typing import Optional, Literal
from sqlalchemy.orm import Session

from be_task_ca.domain.user.repositories import UserRepository
from be_task_ca.domain.item.repositories import ItemRepository
from be_task_ca.infrastructure.database.repositories.user_repository import SQLUserRepository
from be_task_ca.infrastructure.database.repositories.item_repository import SQLItemRepository
from be_task_ca.infrastructure.in_memory.user_repository import InMemoryUserRepository
from be_task_ca.infrastructure.in_memory.item_repository import InMemoryItemRepository

_in_memory_user_repository = None
_in_memory_item_repository = None


def get_user_repository(repository_type: Literal["sql", "memory"] = "sql",
                        db_session: Optional[Session] = None) -> UserRepository:
    """
    Get a user repository implementation.

    Args:
        repository_type: "sql" or "memory"
        db_session: SQLAlchemy session (required for SQL repositories)

    Returns:
        Implementation of UserRepository
    """
    global _in_memory_user_repository

    if repository_type == "sql":
        if db_session is None:
            raise ValueError("Database session is required for SQL repositories")
        return SQLUserRepository(db_session)

    if _in_memory_user_repository is None:
        _in_memory_user_repository = InMemoryUserRepository()
    return _in_memory_user_repository


def get_item_repository(repository_type: Literal["sql", "memory"] = "sql",
                        db_session: Optional[Session] = None) -> ItemRepository:
    """
    Get an item repository implementation.

    Args:
        repository_type: "sql" or "memory"
        db_session: SQLAlchemy session (required for SQL repositories)

    Returns:
        Implementation of ItemRepository
    """
    global _in_memory_item_repository

    if repository_type == "sql":
        if db_session is None:
            raise ValueError("Database session is required for SQL repositories")
        return SQLItemRepository(db_session)

    if _in_memory_item_repository is None:
        _in_memory_item_repository = InMemoryItemRepository()
    return _in_memory_item_repository