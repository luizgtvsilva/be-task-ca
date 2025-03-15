# tests/application/user/test_user_usecases.py
import pytest
import uuid
from fastapi import HTTPException

from be_task_ca.application.user.usecases import (
    create_user, add_item_to_cart, list_items_in_cart, cart_item_model_to_schema
)
from be_task_ca.application.dto.user_dto import CreateUserRequest, AddToCartRequest
from be_task_ca.domain.user.entities import User, CartItem
from be_task_ca.domain.item.entities import Item
from be_task_ca.infrastructure.in_memory.user_repository import InMemoryUserRepository
from be_task_ca.infrastructure.in_memory.item_repository import InMemoryItemRepository


@pytest.fixture
def user_repository():
    """Fixture that provides a clean in-memory user repository for each test"""
    return InMemoryUserRepository()


@pytest.fixture
def item_repository():
    """Fixture that provides a clean in-memory item repository for each test"""
    return InMemoryItemRepository()


@pytest.fixture
def sample_user_request():
    """Fixture that provides a sample user creation request"""
    return CreateUserRequest(
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
        password="password123",
        shipping_address="123 Main St"
    )


@pytest.fixture
def sample_item(item_repository):
    """Fixture that creates and returns a sample item for testing"""
    item = Item(
        name="Test Item",
        description="This is a test item",
        price=29.99,
        quantity=10
    )
    item_repository.save_item(item)
    return item


def test_create_user_success(user_repository, sample_user_request):
    # Act
    response = create_user(sample_user_request, user_repository)

    # Assert
    assert response.id is not None
    assert response.first_name == "John"
    assert response.last_name == "Doe"
    assert response.email == "john.doe@example.com"
    assert response.shipping_address == "123 Main St"

    # Verify user was saved to repository
    saved_user = user_repository.find_user_by_email("john.doe@example.com")
    assert saved_user is not None
    assert saved_user.first_name == "John"
    assert saved_user.hashed_password is not None  # Password should be hashed


def test_create_user_duplicate_email(user_repository, sample_user_request):
    # Arrange
    create_user(sample_user_request, user_repository)  # Create first user

    # Create another user with the same email
    duplicate_request = CreateUserRequest(
        first_name="Jane",
        last_name="Smith",
        email="john.doe@example.com",  # Same email as first user
        password="different123",
        shipping_address="456 Oak St"
    )

    # Act & Assert
    with pytest.raises(HTTPException) as excinfo:
        create_user(duplicate_request, user_repository)

    assert excinfo.value.status_code == 409
    assert "already exists" in excinfo.value.detail


def test_add_item_to_cart_success(user_repository, item_repository, sample_user_request, sample_item):
    # Arrange
    user_response = create_user(sample_user_request, user_repository)
    cart_request = AddToCartRequest(
        item_id=sample_item.id,
        quantity=2
    )

    # Act
    response = add_item_to_cart(user_response.id, cart_request, user_repository, item_repository)

    # Assert
    assert len(response.items) == 1
    assert response.items[0].item_id == sample_item.id
    assert response.items[0].quantity == 2

    # Verify cart item was saved to repository
    user = user_repository.find_user_by_id(user_response.id)
    assert len(user.cart_items) == 1
    assert user.cart_items[0].item_id == sample_item.id
    assert user.cart_items[0].quantity == 2


def test_add_item_to_cart_user_not_found(user_repository, item_repository, sample_item):
    # Arrange
    random_user_id = uuid.uuid4()
    cart_request = AddToCartRequest(
        item_id=sample_item.id,
        quantity=2
    )

    # Act & Assert
    with pytest.raises(HTTPException) as excinfo:
        add_item_to_cart(random_user_id, cart_request, user_repository, item_repository)

    assert excinfo.value.status_code == 404
    assert "User does not exist" in excinfo.value.detail


def test_add_item_to_cart_item_not_found(user_repository, item_repository, sample_user_request):
    # Arrange
    user_response = create_user(sample_user_request, user_repository)
    random_item_id = uuid.uuid4()
    cart_request = AddToCartRequest(
        item_id=random_item_id,
        quantity=2
    )

    # Act & Assert
    with pytest.raises(HTTPException) as excinfo:
        add_item_to_cart(user_response.id, cart_request, user_repository, item_repository)

    assert excinfo.value.status_code == 404
    assert "Item does not exist" in excinfo.value.detail


def test_add_item_to_cart_insufficient_quantity(user_repository, item_repository, sample_user_request, sample_item):
    # Arrange
    user_response = create_user(sample_user_request, user_repository)
    cart_request = AddToCartRequest(
        item_id=sample_item.id,
        quantity=sample_item.quantity + 1  # Request more than available
    )

    # Act & Assert
    with pytest.raises(HTTPException) as excinfo:
        add_item_to_cart(user_response.id, cart_request, user_repository, item_repository)

    assert excinfo.value.status_code == 409
    assert "Not enough items in stock" in excinfo.value.detail


def test_add_item_to_cart_already_in_cart(user_repository, item_repository, sample_user_request, sample_item):
    # Arrange
    user_response = create_user(sample_user_request, user_repository)
    cart_request = AddToCartRequest(
        item_id=sample_item.id,
        quantity=2
    )

    # Add item to cart first time
    add_item_to_cart(user_response.id, cart_request, user_repository, item_repository)

    # Try to add same item again
    # Act & Assert
    with pytest.raises(HTTPException) as excinfo:
        add_item_to_cart(user_response.id, cart_request, user_repository, item_repository)

    assert excinfo.value.status_code == 409
    assert "Item already in cart" in excinfo.value.detail


def test_list_items_in_cart_empty(user_repository, sample_user_request):
    # Arrange
    user_response = create_user(sample_user_request, user_repository)

    # Act
    response = list_items_in_cart(user_response.id, user_repository)

    # Assert
    assert len(response.items) == 0


def test_list_items_in_cart_with_items(user_repository, item_repository, sample_user_request, sample_item):
    # Arrange
    user_response = create_user(sample_user_request, user_repository)

    # Create another item
    second_item = Item(
        name="Second Item",
        description="This is another test item",
        price=19.99,
        quantity=5
    )
    item_repository.save_item(second_item)

    # Add items to cart
    add_item_to_cart(
        user_response.id,
        AddToCartRequest(item_id=sample_item.id, quantity=2),
        user_repository,
        item_repository
    )

    # Manually add second item (since add_item_to_cart won't allow adding a second item)
    user = user_repository.find_user_by_id(user_response.id)
    cart_item = CartItem(user_id=user.id, item_id=second_item.id, quantity=3)
    user.cart_items.append(cart_item)
    user_repository.save_user(user)

    # Act
    response = list_items_in_cart(user_response.id, user_repository)

    # Assert
    assert len(response.items) == 2
    item_ids = {item.item_id for item in response.items}
    assert sample_item.id in item_ids
    assert second_item.id in item_ids

    # Check quantities
    quantities = {item.quantity for item in response.items}
    assert 2 in quantities
    assert 3 in quantities


def test_cart_item_model_to_schema():
    # Arrange
    item_id = uuid.uuid4()
    user_id = uuid.uuid4()
    cart_item = CartItem(
        user_id=user_id,
        item_id=item_id,
        quantity=4
    )

    # Act
    schema = cart_item_model_to_schema(cart_item)

    # Assert
    assert schema.item_id == item_id
    assert schema.quantity == 4