import pytest
import uuid

from be_task_ca.domain.user.entities import User, CartItem
from be_task_ca.infrastructure.in_memory.user_repository import InMemoryUserRepository


@pytest.fixture
def repository():
    return InMemoryUserRepository()


def test_save_user(repository):
    user = User(
        first_name="John",
        last_name="Doe",
        email="john@example.com",
        hashed_password="hashed_password",
        shipping_address="123 Main St"
    )

    saved_user = repository.save_user(user)

    assert saved_user.id == user.id
    assert saved_user.email == "john@example.com"

    found_user = repository.find_user_by_email("john@example.com")
    assert found_user is not None
    assert found_user.first_name == "John"


def test_save_user_with_cart_items(repository):
    user = User(
        first_name="John",
        last_name="Doe",
        email="john@example.com",
    )

    item_id = uuid.uuid4()
    cart_item = CartItem(user_id=user.id, item_id=item_id, quantity=3)
    user.cart_items = [cart_item]

    repository.save_user(user)

    found_user = repository.find_user_by_id(user.id)
    assert len(found_user.cart_items) == 1
    assert found_user.cart_items[0].item_id == item_id
    assert found_user.cart_items[0].quantity == 3


def test_find_user_by_email_existing(repository):
    user = User(email="test@example.com", first_name="Test", last_name="User")
    repository.save_user(user)

    found_user = repository.find_user_by_email("test@example.com")

    assert found_user is not None
    assert found_user.email == "test@example.com"
    assert found_user.first_name == "Test"


def test_find_user_by_email_nonexistent(repository):
    found_user = repository.find_user_by_email("nonexistent@example.com")

    assert found_user is None


def test_find_user_by_id_existing(repository):
    user = User(email="test@example.com", first_name="Test", last_name="User")
    repository.save_user(user)

    found_user = repository.find_user_by_id(user.id)

    assert found_user is not None
    assert found_user.id == user.id
    assert found_user.email == "test@example.com"


def test_find_user_by_id_nonexistent(repository):
    random_id = uuid.uuid4()

    found_user = repository.find_user_by_id(random_id)

    assert found_user is None


def test_find_cart_items_for_user_id(repository):
    user = User(email="test@example.com")
    item_id1 = uuid.uuid4()
    item_id2 = uuid.uuid4()

    cart_item1 = CartItem(user_id=user.id, item_id=item_id1, quantity=2)
    cart_item2 = CartItem(user_id=user.id, item_id=item_id2, quantity=3)
    user.cart_items = [cart_item1, cart_item2]

    repository.save_user(user)

    cart_items = repository.find_cart_items_for_user_id(user.id)

    assert len(cart_items) == 2

    item_ids = {item.item_id for item in cart_items}
    assert item_id1 in item_ids
    assert item_id2 in item_ids

    quantities = {item.quantity for item in cart_items}
    assert 2 in quantities
    assert 3 in quantities


def test_find_cart_items_for_user_id_no_items(repository):
    user = User(email="test@example.com")
    repository.save_user(user)

    cart_items = repository.find_cart_items_for_user_id(user.id)

    assert len(cart_items) == 0


def test_find_cart_items_for_user_id_nonexistent_user(repository):
    random_id = uuid.uuid4()

    cart_items = repository.find_cart_items_for_user_id(random_id)

    assert len(cart_items) == 0