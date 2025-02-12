from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.merch import Merchandise
from app.models.purchase import Purchase
from app.schemas.purchase import PurchaseCreate


def create_purchase(db: Session, purchase: PurchaseCreate):
    db_purchase = Purchase(merch_id=purchase.merch_id,
                              user_id=purchase.user_id,
                              quantity=purchase.quantity)
    db.add(db_purchase)
    db.commit()
    db.refresh(db_purchase)
    return db_purchase


def get_user_purchases(db: Session, user_id: int):
    return (
        db.query(Merchandise.name, func.sum(Purchase.quantity).label("total_quantity"))
        .join(Merchandise, Merchandise.id == Purchase.merch_id)
        .filter(Purchase.user_id == user_id)
        .group_by(Merchandise.name)
        .all()
    )
