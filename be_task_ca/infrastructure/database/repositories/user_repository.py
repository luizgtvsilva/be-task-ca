from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session

from be_task_ca.domain.user.entities import User, CartItem
from be_task_ca.domain.user.repositories import UserRepository
from be_task_ca.infrastructure.database.models.user_model import UserModel, CartItemModel


class SQLUserRepository(UserRepository):
    def __init__(self, db: Session):
        self.db = db

    def save_user(self, user: User) -> User:
        db_user = self.db.query(UserModel).filter(UserModel.id == user.id).first()

        if not db_user:
            db_user = UserModel(
                id=user.id,
                email=user.email,
                first_name=user.first_name,
                last_name=user.last_name,
                hashed_password=user.hashed_password,
                shipping_address=user.shipping_address
            )
            self.db.add(db_user)
        else:
            db_user.email = user.email
            db_user.first_name = user.first_name
            db_user.last_name = user.last_name
            db_user.hashed_password = user.hashed_password
            db_user.shipping_address = user.shipping_address

        if user.cart_items:
            self.db.query(CartItemModel).filter(
                CartItemModel.user_id == user.id
            ).delete()

            for item in user.cart_items:
                db_cart_item = CartItemModel(
                    user_id=item.user_id,
                    item_id=item.item_id,
                    quantity=item.quantity
                )
                self.db.add(db_cart_item)

        self.db.commit()
        return user

    def find_user_by_email(self, email: str) -> Optional[User]:
        db_user = self.db.query(UserModel).filter(UserModel.email == email).first()
        if not db_user:
            return None

        return self._map_to_domain(db_user)

    def find_user_by_id(self, user_id: UUID) -> Optional[User]:
        db_user = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        if not db_user:
            return None

        return self._map_to_domain(db_user)

    def find_cart_items_for_user_id(self, user_id: UUID) -> List[CartItem]:
        db_cart_items = self.db.query(CartItemModel).filter(
            CartItemModel.user_id == user_id
        ).all()

        return [
            CartItem(
                user_id=item.user_id,
                item_id=item.item_id,
                quantity=item.quantity
            )
            for item in db_cart_items
        ]

    def _map_to_domain(self, db_user: UserModel) -> User:
        cart_items = [
            CartItem(
                user_id=item.user_id,
                item_id=item.item_id,
                quantity=item.quantity
            )
            for item in db_user.cart_items
        ]

        return User(
            id=db_user.id,
            email=db_user.email,
            first_name=db_user.first_name,
            last_name=db_user.last_name,
            hashed_password=db_user.hashed_password,
            shipping_address=db_user.shipping_address,
            cart_items=cart_items
        )