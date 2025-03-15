import pytest
import uuid
from be_task_ca.domain.user.entities import User, CartItem
from be_task_ca.domain.item.entities import Item
from be_task_ca.infrastructure.factory import get_user_repository, get_item_repository
from be_task_ca.infrastructure.database.repositories.user_repository import SQLUserRepository
from be_task_ca.infrastructure.database.repositories.item_repository import SQLItemRepository
from be_task_ca.infrastructure.in_memory.user_repository import InMemoryUserRepository
from be_task_ca.infrastructure.in_memory.item_repository import InMemoryItemRepository


def test_parameters():
    """Generate test parameters for both repository types."""
    return [
        {"repo_fixture": "sql_user_repo", "use_fixture": "use_sql_db", "name": "SQL"},
        {"repo_fixture": "memory_user_repo", "use_fixture": "use_memory_db", "name": "InMemory"}
    ]


@pytest.fixture
def sql_user_repo(db_session):
    """Fixture for SQL user repository."""
    return SQLUserRepository(db_session)


@pytest.fixture
def memory_user_repo():
    """Fixture for in-memory user repository."""
    return InMemoryUserRepository()


@pytest.mark.parametrize("params", test_parameters())
def test_save_and_find_user(request, params):
    """Test saving and finding a user with both repository implementations."""
    repo = request.getfixturevalue(params["repo_fixture"])
    request.getfixturevalue(params["use_fixture"])

    unique_email = f"user_{uuid.uuid4()}@example.com"

    user = User(
        first_name="Test",
        last_name="User",
        email=unique_email,
        hashed_password="hashed_password_123",
        shipping_address="123 Test St"
    )

    saved_user = repo.save_user(user)
    found_user_by_id = repo.find_user_by_id(user.id)
    found_user_by_email = repo.find_user_by_email(unique_email)

    assert saved_user.id == user.id
    assert found_user_by_id is not None
    assert found_user_by_id.email == unique_email
    assert found_user_by_email is not None
    assert found_user_by_email.id == user.id


@pytest.fixture
def sql_item_repo(db_session):
    """Fixture for SQL item repository."""
    return SQLItemRepository(db_session)


@pytest.fixture
def memory_item_repo():
    """Fixture for in-memory item repository."""
    return InMemoryItemRepository()


@pytest.mark.parametrize("params", test_parameters())
def test_save_user_with_cart_items(request, params):
    """Test saving a user with cart items with both repository implementations."""
    user_repo = request.getfixturevalue(params["repo_fixture"])
    request.getfixturevalue(params["use_fixture"])

    if params["name"] == "SQL":
        item_repo = request.getfixturevalue("sql_item_repo")
    else:
        item_repo = request.getfixturevalue("memory_item_repo")

    unique_email = f"user_{uuid.uuid4()}@example.com"

    user = User(
        first_name="Cart",
        last_name="User",
        email=unique_email,
        hashed_password="hashed_password_123"
    )

    item1 = Item(
        name=f"Test Item 1 {uuid.uuid4()}",
        description="Description 1",
        price=10.0,
        quantity=10
    )
    item2 = Item(
        name=f"Test Item 2 {uuid.uuid4()}",
        description="Description 2",
        price=20.0,
        quantity=20
    )

    item_repo.save_item(item1)
    item_repo.save_item(item2)

    cart_item1 = CartItem(user_id=user.id, item_id=item1.id, quantity=2)
    cart_item2 = CartItem(user_id=user.id, item_id=item2.id, quantity=3)

    user.cart_items = [cart_item1, cart_item2]

    user_repo.save_user(user)
    found_user = user_repo.find_user_by_id(user.id)
    cart_items = user_repo.find_cart_items_for_user_id(user.id)

    assert found_user is not None
    assert len(cart_items) == 2

    item_ids = [item.item_id for item in cart_items]
    assert item1.id in item_ids
    assert item2.id in item_ids


@pytest.mark.parametrize("params", test_parameters())
def test_update_user(request, params):
    """Test updating user information with both repository implementations."""
    repo = request.getfixturevalue(params["repo_fixture"])
    request.getfixturevalue(params["use_fixture"])

    unique_email = f"user_{uuid.uuid4()}@example.com"

    user = User(
        first_name="Original",
        last_name="Name",
        email=unique_email,
        hashed_password="original_password",
        shipping_address="Original Address"
    )

    repo.save_user(user)

    user.first_name = "Updated"
    user.shipping_address = "Updated Address"

    repo.save_user(user)
    updated_user = repo.find_user_by_id(user.id)

    assert updated_user.first_name == "Updated"
    assert updated_user.shipping_address == "Updated Address"
    assert updated_user.email == unique_email