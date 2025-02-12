from sqlalchemy.orm import Session

from app.models.transaction import CoinTransaction
from app.models.user import User
from app.schemas.transaction import TransactionCreate


def create_transaction(db: Session, transaction: TransactionCreate):
    db_transaction = CoinTransaction(sender_id=transaction.sender_id,
                                       recipient_id=transaction.recipient_id,
                                       amount=transaction.amount)
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


def get_received_transactions(db: Session, user_id: int):
    return db.query(
        CoinTransaction.amount,
        User.username.label("fromUser")
    ).join(
        User, User.id == CoinTransaction.sender_id
    ).filter(
        CoinTransaction.recipient_id == user_id
    ).all()


def get_sent_transactions(db: Session, user_id: int):
    return db.query(
        CoinTransaction.amount,
        User.username.label("toUser")
    ).join(
        User, User.id == CoinTransaction.recipient_id
    ).filter(
        CoinTransaction.sender_id == user_id
    ).all()
