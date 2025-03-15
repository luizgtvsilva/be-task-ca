import hashlib
from fastapi import HTTPException
from uuid import UUID

from be_task_ca.domain.user.entities import User, CartItem
from be_task_ca.domain.user.repositories import UserRepository
from be_task_ca.domain.item.repositories import ItemRepository

from ..dto.user_dto import (
    AddToCartRequest,
    AddToCartResponse,
    CreateUserRequest,
    CreateUserResponse,
)

def create_user(create_user: CreateUserRequest, user_repository: UserRepository) -> CreateUserResponse:
    search_result = user_repository.find_user_by_email(create_user.email)
    if search_result is not None:
        raise HTTPException(
            status_code=409, detail="An user with this email adress already exists"
        )

    new_user = User(
        first_name=create_user.first_name,
        last_name=create_user.last_name,
        email=create_user.email,
        hashed_password=hashlib.sha512(
            create_user.password.encode("UTF-8")
        ).hexdigest(),
        shipping_address=create_user.shipping_address,
    )

    user_repository.save_user(new_user)

    return CreateUserResponse(
        id=new_user.id,
        first_name=new_user.first_name,
        last_name=new_user.last_name,
        email=new_user.email,
        shipping_address=new_user.shipping_address,
    )

def add_item_to_cart(
    user_id: UUID,
    cart_item: AddToCartRequest,
    user_repository: UserRepository,
    item_repository: ItemRepository
) -> AddToCartResponse:
    user = user_repository.find_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User does not exist")

    item = item_repository.find_item_by_id(cart_item.item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item does not exist")
    if item.quantity < cart_item.quantity:
        raise HTTPException(status_code=409, detail="Not enough items in stock")

    item_ids = [o.item_id for o in user.cart_items]
    if cart_item.item_id in item_ids:
        raise HTTPException(status_code=409, detail="Item already in cart")

    new_cart_item = CartItem(
        user_id=user.id,
        item_id=cart_item.item_id,
        quantity=cart_item.quantity
    )

    user.cart_items.append(new_cart_item)
    user_repository.save_user(user)

    return list_items_in_cart(user.id, user_repository)

def list_items_in_cart(user_id: UUID, user_repository: UserRepository):
    cart_items = user_repository.find_cart_items_for_user_id(user_id)
    return AddToCartResponse(items=list(map(cart_item_model_to_schema, cart_items)))

def cart_item_model_to_schema(model: CartItem):
    return AddToCartRequest(item_id=model.item_id, quantity=model.quantity)