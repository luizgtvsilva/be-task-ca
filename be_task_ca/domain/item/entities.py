from dataclasses import dataclass
from uuid import UUID, uuid4
from typing import Optional
from dataclasses import field

@dataclass
class Item:
    id: UUID = field(default_factory=uuid4)
    name: str = None
    description: Optional[str] = None
    price: float = 0.0
    quantity: int = 0