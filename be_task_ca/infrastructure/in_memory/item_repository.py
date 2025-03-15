from typing import Dict, List, Optional
from uuid import UUID

from be_task_ca.domain.item.entities import Item
from be_task_ca.domain.item.repositories import ItemRepository


class InMemoryItemRepository(ItemRepository):
    def __init__(self):
        self.items: Dict[UUID, Item] = {}

    def save_item(self, item: Item) -> Item:
        stored_item = Item(
            id=item.id,
            name=item.name,
            description=item.description,
            price=item.price,
            quantity=item.quantity
        )

        self.items[item.id] = stored_item
        return item

    def get_all_items(self) -> List[Item]:
        return list(self.items.values())

    def find_item_by_name(self, name: str) -> Optional[Item]:
        for item in self.items.values():
            if item.name == name:
                return item
        return None

    def find_item_by_id(self, id: UUID) -> Optional[Item]:
        return self.items.get(id)