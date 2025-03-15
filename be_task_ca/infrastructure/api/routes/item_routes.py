from fastapi import APIRouter, Depends, Request

from be_task_ca.domain.item.repositories import ItemRepository
from be_task_ca.application.item.usecases import create_item, get_all
from be_task_ca.application.dto.item_dto import CreateItemRequest, CreateItemResponse
from be_task_ca.infrastructure.database.repositories.item_repository import SQLItemRepository

item_router = APIRouter(
    prefix="/items",
    tags=["item"],
)

def get_item_repository(request: Request) -> ItemRepository:
    db = request.state.db
    return SQLItemRepository(db)

@item_router.post("/")
async def post_item(
    item: CreateItemRequest,
    repository: ItemRepository = Depends(get_item_repository)
) -> CreateItemResponse:
    return create_item(item, repository)

@item_router.get("/")
async def get_items(
    repository: ItemRepository = Depends(get_item_repository)
):
    return get_all(repository)