import pytest
from fastapi.testclient import TestClient
import uuid

from be_task_ca.main import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.mark.parametrize("use_fixture", ["use_memory_db", "use_sql_db"])
def test_full_shopping_scenario(client, request, use_fixture):
    """Test a complete shopping scenario: create items, create user, add to cart."""
    request.getfixturevalue(use_fixture)

    test_id = str(uuid.uuid4())[:8]
    user_email = f"shopper_{test_id}@example.com"

    items = []
    for i in range(3):
        item_data = {
            "name": f"Product {test_id}-{i}",
            "description": f"Description for product {i}",
            "price": 10.0 + i * 5.0,
            "quantity": 10 + i
        }
        response = client.post("/items/", json=item_data)
        assert response.status_code == 200
        items.append(response.json())

    user_data = {
        "first_name": "Test",
        "last_name": "Shopper",
        "email": user_email,
        "password": "secure_password",
        "shipping_address": "123 Shopping St"
    }
    user_response = client.post("/users/", json=user_data)
    assert user_response.status_code == 200
    user = user_response.json()

    added_items = 0
    for i, item in enumerate(items):
        cart_data = {
            "item_id": item["id"],
            "quantity": i + 1  # Different quantity for each item
        }
        response = client.post(f"/users/{user['id']}/cart", json=cart_data)

        if added_items == 0:
            assert response.status_code == 200
            cart = response.json()
            assert len(cart["items"]) == 1
            added_items += 1
        else:
            # Check if this is implementing single item cart logic
            # or multi-item cart logic
            if response.status_code == 200:
                # Multi-item cart is supported
                cart = response.json()
                added_items += 1
                assert len(cart["items"]) == added_items
            elif response.status_code == 409:
                # Single-item cart is enforced
                assert "Item already in cart" in response.text
                # Break the loop as we can't add more items
                break

    cart_response = client.get(f"/users/{user['id']}/cart")
    assert cart_response.status_code == 200
    final_cart = cart_response.json()

    assert len(final_cart["items"]) == added_items

    cart_item = final_cart["items"][0]
    assert cart_item["item_id"] == items[0]["id"]