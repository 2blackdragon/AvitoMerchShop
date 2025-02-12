from sqlalchemy import Column, Integer, String, func, TIMESTAMP

from app.db.database import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    coins_balance = Column(Integer, default=1000)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    purchases = relationship("Purchase", back_populates="user")
    sent_transactions = relationship("CoinTransaction", back_populates="sender",
                                     foreign_keys="[CoinTransaction.sender_id]")
    received_transactions = relationship("CoinTransaction", back_populates="recipient",
                                         foreign_keys="[CoinTransaction.recipient_id]")

