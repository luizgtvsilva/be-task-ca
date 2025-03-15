# tests/infrastructure/in_memory/test_item_repository.py
import pytest
import uuid

from be_task_ca.domain.item.entities import Item
from be_task_ca.infrastructure.in_memory.item_repository import InMemoryItemRepository


@pytest.fixture
def repository():
    return InMemoryItemRepository()


def test_save_item(repository):
    # Arrange
    item = Item(
        name="Test Item",
        description="Test Description",
        price=29.99,
        quantity=10
    )

    # Act
    saved_item = repository.save_item(item)

    # Assert
    assert saved_item.id == item.id
    assert saved_item.name == "Test Item"

    # Verify item was stored
    items = repository.get_all_items()
    assert len(items) == 1
    assert items[0].name == "Test Item"


def test_get_all_items_empty(repository):
    # Act
    items = repository.get_all_items()

    # Assert
    assert len(items) == 0


def test_get_all_items(repository):
    # Arrange
    item1 = Item(name="Item 1", price=10.0, quantity=5)
    item2 = Item(name="Item 2", price=20.0, quantity=10)
    repository.save_item(item1)
    repository.save_item(item2)

    # Act
    items = repository.get_all_items()

    # Assert
    print('\n \n Items: ', items, "\n \n ")
    assert len(items) == 2
    names = {item.name for item in items}
    assert "Item 1" in names
    assert "Item 2" in names


def test_find_item_by_name_existing(repository):
    # Arrange
    item = Item(name="Test Item", price=15.0, quantity=3)
    repository.save_item(item)

    # Act
    found_item = repository.find_item_by_name("Test Item")

    # Assert
    assert found_item is not None
    assert found_item.name == "Test Item"
    assert found_item.price == 15.0


def test_find_item_by_name_nonexistent(repository):
    # Act
    found_item = repository.find_item_by_name("Nonexistent Item")

    # Assert
    assert found_item is None


def test_find_item_by_id_existing(repository):
    # Arrange
    item = Item(name="Test Item", price=15.0, quantity=3)
    repository.save_item(item)

    # Act
    found_item = repository.find_item_by_id(item.id)

    # Assert
    assert found_item is not None
    assert found_item.id == item.id
    assert found_item.name == "Test Item"


def test_find_item_by_id_nonexistent(repository):
    # Arrange
    random_id = uuid.uuid4()

    # Act
    found_item = repository.find_item_by_id(random_id)

    # Assert
    assert found_item is None