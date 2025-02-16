import pytest


def test_buy_merch(client):
    response = client.post("/api/auth", data={"username": "testuser_purchase_e2e", "password": "password"})
    assert response.status_code == 200
    auth_token = response.json().get("access_token")
    assert auth_token is not None

    merch_name = 'umbrella'
    response = client.get(
        f"/api/buy/{merch_name}?quantity={1}",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    assert response.json().get("merch_id") == 7


def test_buy_not_auth_user(client):
    merch_name = 'umbrella'
    response = client.get(
        f"/api/buy/{merch_name}?quantity={1}",
        headers={"Authorization": f"Bearer "}
    )
    assert response.status_code == 401


def test_buy_not_exist_merch(client):
    response = client.post("/api/auth", data={"username": "testuser_purchase_e2e", "password": "password"})
    assert response.status_code == 200
    auth_token = response.json().get("access_token")
    assert auth_token is not None

    merch_name = 'umbrella2'
    response = client.get(
        f"/api/buy/{merch_name}?quantity={1}",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 400
    assert response.json().get("detail") == "Item not found."


def test_buy_invalid_quantity(client):
    response = client.post("/api/auth", data={"username": "testuser_purchase_e2e", "password": "password"})
    assert response.status_code == 200
    auth_token = response.json().get("access_token")
    assert auth_token is not None

    merch_name = 'umbrella'
    response = client.get(
        f"/api/buy/{merch_name}?quantity={0}",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 400
    assert response.json().get("detail") == "Quantity must be positive."


def test_buy_not_enough_coins(client):
    response = client.post("/api/auth", data={"username": "testuser_purchase_e2e", "password": "password"})
    assert response.status_code == 200
    auth_token = response.json().get("access_token")
    assert auth_token is not None

    merch_name = 'umbrella'
    response = client.get(
        f"/api/buy/{merch_name}?quantity={10}",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 400
    assert response.json().get("detail") == "Not enough coins."
