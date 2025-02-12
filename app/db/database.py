from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings


engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    from app.models.merch import Merchandise
    from app.models.user import User
    from app.models.purchase import Purchase
    from app.models.transaction import CoinTransaction

    Base.metadata.create_all(bind=engine)

    session = SessionLocal()

    try:
        if session.query(Merchandise).count() == 0:
            merchandise_data = [
                {'name': 't-shirt', 'price': 80},
                {'name': 'cup', 'price': 20},
                {'name': 'book', 'price': 50},
                {'name': 'pen', 'price': 10},
                {'name': 'powerbank', 'price': 200},
                {'name': 'hoody', 'price': 300},
                {'name': 'umbrella', 'price': 200},
                {'name': 'socks', 'price': 10},
                {'name': 'wallet', 'price': 50},
                {'name': 'pink-hoody', 'price': 500},
            ]

            for item in merchandise_data:
                new_item = Merchandise(name=item['name'], price=item['price'])
                session.add(new_item)

            session.commit()
            print("Товары добавлены")
        else:
            print("Товары уже добавлены в базу данных.")

    except IntegrityError as e:
        print(f"Ошибка при вставке данных: {e}")
    finally:
        session.close()
