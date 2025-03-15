from typing import Dict, List, Optional
from uuid import UUID

from be_task_ca.domain.user.entities import User, CartItem
from be_task_ca.domain.user.repositories import UserRepository


class InMemoryUserRepository(UserRepository):
    def __init__(self):
        self.users: Dict[UUID, User] = {}
        self.cart_items: Dict[UUID, List[CartItem]] = {}

    def save_user(self, user: User) -> User:
        stored_user = User(
            id=user.id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            hashed_password=user.hashed_password,
            shipping_address=user.shipping_address
        )

        self.users[user.id] = stored_user

        # Store cart items separately
        if user.cart_items:
            self.cart_items[user.id] = [
                CartItem(
                    user_id=item.user_id,
                    item_id=item.item_id,
                    quantity=item.quantity
                )
                for item in user.cart_items
            ]

        return user

    def find_user_by_email(self, email: str) -> Optional[User]:
        for user in self.users.values():
            if user.email == email:
                return self._get_user_with_cart_items(user)
        return None

    def find_user_by_id(self, user_id: UUID) -> Optional[User]:
        user = self.users.get(user_id)
        if not user:
            return None
        return self._get_user_with_cart_items(user)

    def find_cart_items_for_user_id(self, user_id: UUID) -> List[CartItem]:
        return self.cart_items.get(user_id, [])

    def _get_user_with_cart_items(self, user: User) -> User:
        result = User(
            id=user.id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            hashed_password=user.hashed_password,
            shipping_address=user.shipping_address
        )

        result.cart_items = self.cart_items.get(user.id, [])

        return result