import pytest
from app.schemas.transaction import TransactionRequest


def test_transaction(client):
    response1 = client.post('/api/auth', data={'username': 'testUser_transaction_e2e', 'password': 'qwerty'})
    assert response1.status_code == 200
    token1 = response1.json().get("access_token")

    response2 = client.post('/api/auth', data={'username': 'testUser2_transaction_e2e', 'password': 'qwerty'})
    assert response2.status_code == 200

    response = client.post(
        "/api/sendCoin",
        json={"toUser": "testUser2_transaction_e2e", "amount": 1},
        headers={"Authorization": f"Bearer {token1}", "Content-Type": "application/json", "Accept": "application/json"}
    )
    assert response.status_code == 200


def test_send_coin_insufficient_balance(client):
    response = client.post('/api/auth', data={'username': 'testUser_no_money', 'password': 'qwerty'})
    assert response.status_code == 200
    token = response.json().get("access_token")

    response = client.post(
        "/api/sendCoin",
        json={"toUser": "testUser2_transaction_e2e", "amount": 999999},
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json", "Accept": "application/json"}
    )
    assert response.status_code == 400
    assert response.json().get("detail") == "Not enough coins."


def test_send_coin_to_nonexistent_user(client):
    response = client.post('/api/auth', data={'username': 'testUser_send_fail', 'password': 'qwerty'})
    assert response.status_code == 200
    token = response.json().get("access_token")

    response = client.post(
        "/api/sendCoin",
        json={"toUser": "nonexistentUser", "amount": 1},
        headers={"Authorization": f"Bearer {token}", "Accept": "application/json"}
    )
    assert response.status_code == 400
    assert response.json().get("detail") == "Recipient not found."


def test_send_coin_to_yourself(client):
    response = client.post('/api/auth', data={'username': 'testUser_send_fail', 'password': 'qwerty'})
    assert response.status_code == 200
    token = response.json().get("access_token")

    response = client.post(
        "/api/sendCoin",
        json={"toUser": "testUser_send_fail", "amount": 10},
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json", "Accept": "application/json"}
    )
    assert response.status_code == 400
    assert response.json().get("detail") == "Cannot send coins to yourself."
