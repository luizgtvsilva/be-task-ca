import pytest
import uuid
from be_task_ca.domain.item.entities import Item
from be_task_ca.infrastructure.factory import get_item_repository
from be_task_ca.infrastructure.database.repositories.item_repository import SQLItemRepository
from be_task_ca.infrastructure.in_memory.item_repository import InMemoryItemRepository


def test_parameters():
    """Generate test parameters for both repository types."""
    return [
        {"repo_fixture": "sql_item_repo", "use_fixture": "use_sql_db", "name": "SQL"},
        {"repo_fixture": "memory_item_repo", "use_fixture": "use_memory_db", "name": "InMemory"}
    ]


@pytest.fixture
def sql_item_repo(db_session):
    """Fixture for SQL item repository."""
    return SQLItemRepository(db_session)


@pytest.fixture
def memory_item_repo():
    """Fixture for in-memory item repository."""
    return InMemoryItemRepository()


@pytest.mark.parametrize("params", test_parameters())
def test_save_and_find_item(request, params):
    """Test saving and finding an item with both repository implementations."""
    repo = request.getfixturevalue(params["repo_fixture"])
    request.getfixturevalue(params["use_fixture"])

    item = Item(
        name=f"Test Item {uuid.uuid4()}",  # Ensure uniqueness
        description="This is a test item",
        price=29.99,
        quantity=10
    )

    saved_item = repo.save_item(item)
    found_item = repo.find_item_by_id(item.id)

    assert saved_item.id == item.id
    assert found_item is not None
    assert found_item.name == item.name
    assert found_item.price == 29.99


@pytest.mark.parametrize("params", test_parameters())
def test_find_item_by_name(request, params):
    """Test finding an item by name with both repository implementations."""
    repo = request.getfixturevalue(params["repo_fixture"])
    request.getfixturevalue(params["use_fixture"])

    unique_name = f"Unique Item {uuid.uuid4()}"
    item = Item(
        name=unique_name,
        description="This is a unique item",
        price=19.99,
        quantity=5
    )
    repo.save_item(item)

    found_item = repo.find_item_by_name(unique_name)
    not_found_item = repo.find_item_by_name("Nonexistent Item")

    assert found_item is not None
    assert found_item.name == unique_name
    assert not_found_item is None


@pytest.mark.parametrize("params", test_parameters())
def test_get_all_items(request, params):
    """Test getting all items with both repository implementations."""
    repo = request.getfixturevalue(params["repo_fixture"])
    request.getfixturevalue(params["use_fixture"])

    prefix = str(uuid.uuid4())[:8]
    item1 = Item(name=f"{prefix} Item 1", price=10.0, quantity=5)
    item2 = Item(name=f"{prefix} Item 2", price=20.0, quantity=10)

    repo.save_item(item1)
    repo.save_item(item2)

    all_items = repo.get_all_items()
    relevant_items = [item for item in all_items if item.name.startswith(prefix)]

    assert len(relevant_items) == 2
    names = [item.name for item in relevant_items]
    assert f"{prefix} Item 1" in names
    assert f"{prefix} Item 2" in names