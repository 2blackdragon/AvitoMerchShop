import pytest
from app.models.user import User
from app.models.transaction import CoinTransaction
from app.models.purchase import Purchase
from app.utils.user import get_password_hash


@pytest.fixture
def create_user_and_data(db, client):
    user1 = User(username="test_user", hashed_password=get_password_hash("hashedpassword123"), coins_balance=1000)
    db.add(user1)
    db.commit()

    user2 = User(username="test_user2", hashed_password="hashedpassword123", coins_balance=500)
    db.add(user2)
    db.commit()

    transaction1 = CoinTransaction(sender_id=user1.id, recipient_id=user2.id, amount=100)
    db.add(transaction1)
    db.commit()

    transaction2 = CoinTransaction(sender_id=user2.id, recipient_id=user1.id, amount=50)
    db.add(transaction2)
    db.commit()

    purchase1 = Purchase(user_id=user1.id, merch_id=1, quantity=2)
    db.add(purchase1)
    db.commit()

    purchase1 = Purchase(user_id=user1.id, merch_id=1, quantity=3)
    db.add(purchase1)
    db.commit()

    purchase2 = Purchase(user_id=user1.id, merch_id=2, quantity=3)
    db.add(purchase2)
    db.commit()

    response_user1 = client.post('/api/auth', data={'username': 'test_user', 'password': 'hashedpassword123'})
    token1 = response_user1.json().get("access_token")

    return user1, user2, token1


def test_user_info(client, db, create_user_and_data):
    user1, user2, token1 = create_user_and_data

    response = client.get('/api/info', headers={"Authorization": f"Bearer {token1}"})

    assert response.status_code == 200

    info = response.json()

    print(info)

    assert info["coins"] == user1.coins_balance

    assert len(info["inventory"]) == 2
    assert info["inventory"][0]["name"] == "cup"
    assert info["inventory"][1]["name"] == "t-shirt"
    assert info["inventory"][0]["quantity"] == 3
    assert info["inventory"][1]["quantity"] == 5

    assert len(info["coinHistory"]["received"]) == 1
    assert len(info["coinHistory"]["sent"]) == 1
    assert info["coinHistory"]["received"][0]["fromUser"] == user2.username
    assert info["coinHistory"]["received"][0]["amount"] == 50
    assert info["coinHistory"]["sent"][0]["toUser"] == user2.username
    assert info["coinHistory"]["sent"][0]["amount"] == 100


def test_user_info_no_token(client):
    response = client.get('/api/info')

    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_user_info_invalid_token(client, db):
    response_user1 = client.post('/api/auth', json={'username': 'test_user', 'password': 'hashedpassword123'})
    token1 = response_user1.json().get("access_token")

    response = client.get('/api/info', headers={"Authorization": "Bearer invalidtoken"})

    assert response.status_code == 401
    assert response.json() == {"detail": "Token is invalid."}
