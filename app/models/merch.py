from sqlalchemy import Column, Integer, String
from app.db.database import Base
from sqlalchemy.orm import relationship

class Merchandise(Base):
    __tablename__ = 'merchandise'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    price = Column(Integer, nullable=False)

    purchases = relationship("Purchase", back_populates="merchandise")