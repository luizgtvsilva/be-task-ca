from fastapi import HTTPException
from uuid import UUID

from be_task_ca.domain.item.entities import Item
from be_task_ca.domain.item.repositories import ItemRepository

from ..dto.item_dto import (
    AllItemsResponse,
    CreateItemRequest,
    CreateItemResponse
)

def create_item(item: CreateItemRequest, item_repository: ItemRepository) -> CreateItemResponse:
    search_result = item_repository.find_item_by_name(item.name)
    if search_result is not None:
        raise HTTPException(
            status_code=409, detail="An item with this name already exists"
        )

    new_item = Item(
        name=item.name,
        description=item.description,
        price=item.price,
        quantity=item.quantity,
    )

    item_repository.save_item(new_item)
    return model_to_schema(new_item)

def get_all(item_repository: ItemRepository) -> AllItemsResponse:
    item_list = item_repository.get_all_items()
    return AllItemsResponse(items=list(map(model_to_schema, item_list)))

def model_to_schema(item: Item) -> CreateItemResponse:
    return CreateItemResponse(
        id=item.id,
        name=item.name,
        description=item.description,
        price=item.price,
        quantity=item.quantity,
    )