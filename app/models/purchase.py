from sqlalchemy import Column, Integer, ForeignKey, TIMESTAMP, func
from app.db.database import Base
from sqlalchemy.orm import relationship

class Purchase(Base):
    __tablename__ = 'purchases'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    merch_id = Column(Integer, ForeignKey('merchandise.id'))
    quantity = Column(Integer, default=1)
    purchase_date = Column(TIMESTAMP, default=func.now())

    user = relationship("User", back_populates="purchases")
    merchandise = relationship("Merchandise", back_populates="purchases")
