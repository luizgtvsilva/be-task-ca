from dataclasses import dataclass, field
from typing import List, Optional
import uuid
from datetime import datetime


@dataclass
class CartItem:
    user_id: uuid.UUID
    item_id: uuid.UUID
    quantity: int


@dataclass
class User:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    email: str = None
    first_name: str = None
    last_name: str = None
    hashed_password: str = None
    shipping_address: Optional[str] = None
    cart_items: List[CartItem] = None

    def __post_init__(self):
        if self.cart_items is None:
            self.cart_items = []