from sqlalchemy import UUID, ForeignKey, Column, String, Integer
from sqlalchemy.orm import relationship
import uuid

from be_task_ca.infrastructure.database.config import Base

class CartItemModel(Base):
    __tablename__ = "cart_items"

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        primary_key=True,
        index=True
    )
    item_id = Column(
        UUID(as_uuid=True),
        ForeignKey("items.id"),
        primary_key=True
    )
    quantity = Column(Integer)

class UserModel(Base):
    __tablename__ = "users"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )
    email = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    shipping_address = Column(String, nullable=True)
    cart_items = relationship("CartItemModel", cascade="all, delete-orphan")