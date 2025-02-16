import pytest


def test_create_user(db):
    from app.models.user import User

    new_user = User(username="testuser", hashed_password="hashedpassword123")
    db.add(new_user)
    db.commit()

    user = db.query(User).filter(User.username == "testuser").first()
    assert user is not None
    assert user.username == "testuser"
    assert user.coins_balance == 1000
