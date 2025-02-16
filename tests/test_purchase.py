import pytest

from app.cruds.user import reduce_coins


def test_buy_merchandise(db):
    from app.models.user import User
    from app.models.merch import Merchandise
    from app.models.purchase import Purchase

    new_user = User(username="testuser_purchase", hashed_password="hashedpassword123")
    db.add(new_user)
    db.commit()

    item = "umbrella"
    merch = db.query(Merchandise).filter_by(name=item).first()

    assert merch is not None, "Merchandise not found in the database"
    assert merch.name == item

    initial_balance = new_user.coins_balance

    purchase = Purchase(user_id=new_user.id, merch_id=merch.id)
    db.add(purchase)
    db.commit()

    reduce_coins(db, new_user, amount=merch.price)
    db.refresh(new_user)

    assert new_user.coins_balance == initial_balance - merch.price

    purchased_merch = db.query(Purchase).filter(Purchase.user_id == new_user.id).first()
    assert purchased_merch is not None
    assert purchased_merch.merch_id == merch.id


def test_get_not_exist_merchandise(db):
    from app.models.user import User
    from app.models.merch import Merchandise

    new_user = User(username="testuserpurchase", hashed_password="hashedpassword123")
    db.add(new_user)
    db.commit()

    item = "umbrella1"
    merch = db.query(Merchandise).filter_by(name=item).first()

    assert merch is None
