from fastapi import APIRouter, Depends, Request

from be_task_ca.domain.item.repositories import ItemRepository
from be_task_ca.application.item.usecases import create_item, get_all
from be_task_ca.application.dto.item_dto import CreateItemRequest, CreateItemResponse
from be_task_ca.infrastructure.factory import get_item_repository
from be_task_ca.config import get_repository_type

item_router = APIRouter(
    prefix="/items",
    tags=["item"],
)

def get_item_repo(request: Request) -> ItemRepository:
    repo_type = get_repository_type()
    if repo_type == "sql":
        return get_item_repository("sql", request.state.db)
    return get_item_repository("memory")

@item_router.post("/")
async def post_item(
    item: CreateItemRequest,
    repository: ItemRepository = Depends(get_item_repo)
) -> CreateItemResponse:
    return create_item(item, repository)

@item_router.get("/")
async def get_items(
    repository: ItemRepository = Depends(get_item_repo)
):
    return get_all(repository)