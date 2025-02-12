from sqlalchemy.orm import Session

from app.models.merch import Merchandise

def get_merch(db: Session, name: str):
    return db.query(Merchandise).filter(Merchandise.name == name).first()
