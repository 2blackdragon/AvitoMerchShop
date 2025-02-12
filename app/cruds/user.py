from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate


def create_user(db: Session, user: UserCreate):
    db_user = User(username=user.username, hashed_password=user.hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def add_coins(db: Session, user: User, amount: int):
    user.coins_balance += amount
    db.commit()
    db.refresh(user)


def reduce_coins(db: Session, user: User, amount: int):
    user.coins_balance -= amount
    db.commit()
    db.refresh(user)


