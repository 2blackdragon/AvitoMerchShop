from sqlalchemy import Column, Integer, ForeignKey, TIMESTAMP, func
from app.db.database import Base
from sqlalchemy.orm import relationship

class CoinTransaction(Base):
    __tablename__ = 'coin_transactions'

    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey('users.id'))
    recipient_id = Column(Integer, ForeignKey('users.id'))
    amount = Column(Integer, nullable=False)
    transaction_date = Column(TIMESTAMP, default=func.now())

    sender = relationship("User", back_populates="sent_transactions", foreign_keys=[sender_id])
    recipient = relationship("User", back_populates="received_transactions", foreign_keys=[recipient_id])
