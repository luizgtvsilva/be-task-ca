from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel

class CreateItemRequest(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    quantity: int

class CreateItemResponse(CreateItemRequest):
    id: UUID

class AllItemsResponse(BaseModel):
    items: List[CreateItemResponse]