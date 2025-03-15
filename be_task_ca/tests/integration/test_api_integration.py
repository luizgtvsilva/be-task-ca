import pytest
from fastapi.testclient import TestClient
import uuid

from be_task_ca.main import app
from be_task_ca.application.dto.user_dto import CreateUserRequest, AddToCartRequest
from be_task_ca.application.dto.item_dto import CreateItemRequest


@pytest.fixture
def client():
    """Create a test client for the FastAPI application."""
    return TestClient(app)


@pytest.mark.parametrize("use_fixture", ["use_memory_db", "use_sql_db"])
def test_create_and_get_item(client, request, use_fixture):
    """Test creating and getting items through the API."""
    request.getfixturevalue(use_fixture)

    unique_name = f"API Test Item {uuid.uuid4()}"

    item_data = {
        "name": unique_name,
        "description": "This is a test item from API",
        "price": 25.99,
        "quantity": 15
    }

    create_response = client.post("/items/", json=item_data)

    assert create_response.status_code == 200
    created_item = create_response.json()
    assert created_item["name"] == unique_name
    assert created_item["price"] == 25.99

    get_response = client.get("/items/")

    assert get_response.status_code == 200
    items = get_response.json()["items"]
    created_item_in_list = next((item for item in items if item["name"] == unique_name), None)
    assert created_item_in_list is not None


@pytest.mark.parametrize("use_fixture", ["use_memory_db", "use_sql_db"])
def test_create_user_and_add_to_cart(client, request, use_fixture, db_session):
    """Test creating a user and adding items to their cart through the API."""
    request.getfixturevalue(use_fixture)

    unique_email = f"api_user_{uuid.uuid4()}@example.com"

    user_data = {
        "first_name": "API",
        "last_name": "User",
        "email": unique_email,
        "password": "api_password",
        "shipping_address": "API Street"
    }

    item_data = {
        "name": f"Cart Item {uuid.uuid4()}",
        "description": "This is an item for the cart test",
        "price": 15.99,
        "quantity": 20
    }

    create_item_response = client.post("/items/", json=item_data)
    assert create_item_response.status_code == 200
    item = create_item_response.json()

    create_user_response = client.post("/users/", json=user_data)

    assert create_user_response.status_code == 200
    user = create_user_response.json()
    assert user["email"] == unique_email

    cart_data = {
        "item_id": item["id"],
        "quantity": 2
    }

    add_to_cart_response = client.post(f"/users/{user['id']}/cart", json=cart_data)

    assert add_to_cart_response.status_code == 200
    cart = add_to_cart_response.json()
    assert len(cart["items"]) == 1
    assert cart["items"][0]["item_id"] == item["id"]
    assert cart["items"][0]["quantity"] == 2

    get_cart_response = client.get(f"/users/{user['id']}/cart")

    assert get_cart_response.status_code == 200
    cart = get_cart_response.json()
    assert len(cart["items"]) == 1