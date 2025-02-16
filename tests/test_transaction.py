import pytest

from app.cruds.user import reduce_coins, add_coins

def test_create_transaction(db):
    from app.models.user import User
    from app.models.transaction import CoinTransaction

    user1 = User(username="testuser_transaction", hashed_password="hashedpassword123")
    user2 = User(username="testuser2_transaction", hashed_password="hashedpassword123")
    db.add(user1)
    db.add(user2)
    db.commit()

    db.refresh(user1)
    db.refresh(user2)
    initial_balance_user1 = user1.coins_balance
    initial_balance_user2 = user2.coins_balance

    amount = 100

    reduce_coins(db, user1, amount)
    add_coins(db, user2, amount)

    db.refresh(user1)
    db.refresh(user2)

    assert user1.coins_balance == initial_balance_user1 - amount
    assert user2.coins_balance == initial_balance_user2 + amount

    transaction = CoinTransaction(sender_id=user1.id, recipient_id=user2.id, amount=amount)
    db.add(transaction)
    db.commit()

    transaction = db.query(CoinTransaction).filter(CoinTransaction.sender_id == user1.id).first()
    assert transaction is not None
    assert transaction.amount == amount
