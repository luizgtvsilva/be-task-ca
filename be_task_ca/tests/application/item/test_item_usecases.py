import pytest
import uuid
from fastapi import HTTPException

from be_task_ca.application.item.usecases import create_item, get_all, model_to_schema
from be_task_ca.application.dto.item_dto import CreateItemRequest
from be_task_ca.domain.item.entities import Item
from be_task_ca.infrastructure.in_memory.item_repository import InMemoryItemRepository


@pytest.fixture
def item_repository():
    """Fixture that provides a clean in-memory item repository for each test"""
    return InMemoryItemRepository()


def test_create_item_success(item_repository):
    # Arrange
    item_request = CreateItemRequest(
        name="Test Item",
        description="This is a test item",
        price=10.99,
        quantity=5
    )

    response = create_item(item_request, item_repository)

    assert response.id is not None
    assert response.name == "Test Item"
    assert response.description == "This is a test item"
    assert response.price == 10.99
    assert response.quantity == 5

    saved_item = item_repository.find_item_by_name("Test Item")
    assert saved_item is not None
    assert saved_item.price == 10.99


def test_create_item_duplicate_name(item_repository):
    item_request = CreateItemRequest(
        name="Test Item",
        description="This is a test item",
        price=10.99,
        quantity=5
    )
    create_item(item_request, item_repository)  # Create first item

    duplicate_request = CreateItemRequest(
        name="Test Item",  # Same name as first item
        description="This is another item",
        price=15.99,
        quantity=10
    )

    with pytest.raises(HTTPException) as excinfo:
        create_item(duplicate_request, item_repository)

    assert excinfo.value.status_code == 409
    assert "already exists" in excinfo.value.detail


def test_get_all_items_empty(item_repository):
    response = get_all(item_repository)

    assert len(response.items) == 0


def test_get_all_items_with_items(item_repository):
    items = [
        CreateItemRequest(name="Item 1", description="Description 1", price=10.0, quantity=5),
        CreateItemRequest(name="Item 2", description="Description 2", price=20.0, quantity=10),
        CreateItemRequest(name="Item 3", description="Description 3", price=30.0, quantity=15)
    ]

    for item_request in items:
        create_item(item_request, item_repository)

    response = get_all(item_repository)

    # Assert
    assert len(response.items) == 3
    assert {item.name for item in response.items} == {"Item 1", "Item 2", "Item 3"}
    assert {item.price for item in response.items} == {10.0, 20.0, 30.0}


def test_model_to_schema_conversion():
    item_id = uuid.uuid4()
    item = Item(
        id=item_id,
        name="Test Item",
        description="Test Description",
        price=15.99,
        quantity=7
    )

    schema = model_to_schema(item)

    assert schema.id == item_id
    assert schema.name == "Test Item"
    assert schema.description == "Test Description"
    assert schema.price == 15.99
    assert schema.quantity == 7