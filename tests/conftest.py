import pytest
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.main import app
from app.db.database import get_db, Base
from app.core.config import settings

TEST_DATABASE_URL = settings.TEST_DATABASE_URL

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    from app.models.user import User
    from app.models.purchase import Purchase
    from app.models.transaction import CoinTransaction
    from app.models.merch import Merchandise

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()

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


    session = TestingSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()
