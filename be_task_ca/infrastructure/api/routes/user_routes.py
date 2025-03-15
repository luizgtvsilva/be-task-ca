from fastapi import APIRouter, Depends, Request
from uuid import UUID

from be_task_ca.domain.user.repositories import UserRepository
from be_task_ca.domain.item.repositories import ItemRepository
from be_task_ca.application.user.usecases import add_item_to_cart, create_user, list_items_in_cart
from be_task_ca.application.dto.user_dto import AddToCartRequest, CreateUserRequest
from be_task_ca.infrastructure.factory import get_user_repository, get_item_repository
from be_task_ca.config import REPOSITORY_TYPE

user_router = APIRouter(
    prefix="/users",
    tags=["user"],
)

def get_user_repo(request: Request) -> UserRepository:
    if REPOSITORY_TYPE == "sql":
        return get_user_repository("sql", request.state.db)
    return get_user_repository("memory")

def get_item_repo(request: Request) -> ItemRepository:
    if REPOSITORY_TYPE == "sql":
        return get_item_repository("sql", request.state.db)
    return get_item_repository("memory")

@user_router.post("/")
async def post_customer(
    user: CreateUserRequest,
    user_repository: UserRepository = Depends(get_user_repo)
):
    return create_user(user, user_repository)

@user_router.post("/{user_id}/cart")
async def post_cart(
    user_id: UUID,
    cart_item: AddToCartRequest,
    user_repository: UserRepository = Depends(get_user_repo),
    item_repository: ItemRepository = Depends(get_item_repo)
):
    return add_item_to_cart(user_id, cart_item, user_repository, item_repository)

@user_router.get("/{user_id}/cart")
async def get_cart(
    user_id: UUID,
    user_repository: UserRepository = Depends(get_user_repo)
):
    return list_items_in_cart(user_id, user_repository)