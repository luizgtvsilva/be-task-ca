from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from .entities import Item


class ItemRepository(ABC):
    @abstractmethod
    def save_item(self, item: Item) -> Item:
        pass

    @abstractmethod
    def get_all_items(self) -> List[Item]:
        pass

    @abstractmethod
    def find_item_by_name(self, name: str) -> Optional[Item]:
        pass

    @abstractmethod
    def find_item_by_id(self, id: UUID) -> Optional[Item]:
        pass