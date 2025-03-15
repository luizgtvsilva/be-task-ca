from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session

from be_task_ca.domain.item.entities import Item
from be_task_ca.domain.item.repositories import ItemRepository
from be_task_ca.infrastructure.database.models.item_model import ItemModel


class SQLItemRepository(ItemRepository):
    def __init__(self, db: Session):
        self.db = db

    def save_item(self, item: Item) -> Item:
        db_item = self.db.query(ItemModel).filter(ItemModel.id == item.id).first()

        if not db_item:
            db_item = ItemModel(
                id=item.id,
                name=item.name,
                description=item.description,
                price=item.price,
                quantity=item.quantity
            )
            self.db.add(db_item)
        else:
            db_item.name = item.name
            db_item.description = item.description
            db_item.price = item.price
            db_item.quantity = item.quantity

        self.db.commit()
        return item

    def get_all_items(self) -> List[Item]:
        db_items = self.db.query(ItemModel).all()
        return [self._map_to_domain(item) for item in db_items]

    def find_item_by_name(self, name: str) -> Optional[Item]:
        db_item = self.db.query(ItemModel).filter(ItemModel.name == name).first()
        if not db_item:
            return None

        return self._map_to_domain(db_item)

    def find_item_by_id(self, id: UUID) -> Optional[Item]:
        db_item = self.db.query(ItemModel).filter(ItemModel.id == id).first()
        if not db_item:
            return None

        return self._map_to_domain(db_item)

    def _map_to_domain(self, db_item: ItemModel) -> Item:
        return Item(
            id=db_item.id,
            name=db_item.name,
            description=db_item.description,
            price=db_item.price,
            quantity=db_item.quantity
        )