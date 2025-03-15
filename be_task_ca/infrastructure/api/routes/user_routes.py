from uuid import UUID
from fastapi import APIRouter, Depends, Request

from be_task_ca.domain.user.repositories import UserRepository
from be_task_ca.domain.item.repositories import ItemRepository
from be_task_ca.application.user.usecases import add_item_to_cart, create_user, list_items_in_cart
from be_task_ca.application.dto.user_dto import AddToCartRequest, CreateUserRequest
from be_task_ca.infrastructure.database.repositories.user_repository import SQLUserRepository
from be_task_ca.infrastructure.database.repositories.item_repository import SQLItemRepository
from be_task_ca.infrastructure.database.config import get_db_session

user_router = APIRouter(
    prefix="/users",
    tags=["user"],
)

def get_user_repository(request: Request) -> UserRepository:
    db = request.state.db
    return SQLUserRepository(db)

def get_item_repository(request: Request) -> ItemRepository:
    db = request.state.db
    return SQLItemRepository(db)

@user_router.post("/")
async def post_customer(
    user: CreateUserRequest,
    user_repository: UserRepository = Depends(get_user_repository)
):
    return create_user(user, user_repository)

@user_router.post("/{user_id}/cart")
async def post_cart(
    user_id: UUID,
    cart_item: AddToCartRequest,
    user_repository: UserRepository = Depends(get_user_repository),
    item_repository: ItemRepository = Depends(get_item_repository)
):
    return add_item_to_cart(user_id, cart_item, user_repository, item_repository)

@user_router.get("/{user_id}/cart")
async def get_cart(
    user_id: UUID,
    user_repository: UserRepository = Depends(get_user_repository)
):
    return list_items_in_cart(user_id, user_repository)