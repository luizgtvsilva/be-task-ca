from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from .entities import User, CartItem


class UserRepository(ABC):
    @abstractmethod
    def save_user(self, user: User) -> User:
        pass

    @abstractmethod
    def find_user_by_email(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    def find_user_by_id(self, user_id: UUID) -> Optional[User]:
        pass

    @abstractmethod
    def find_cart_items_for_user_id(self, user_id: UUID) -> List[CartItem]:
        pass