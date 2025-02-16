# AvitoMerchShop
__AvitoMerchShop__ - тестовое задание для 
отбора на стажировку в Авито.

## Содержание
- [Технологии](#технологии)
- [Установка](#установка)
- [Использование](#использование)
- [Тестирование](#тестирование)

## Технологии
В проекте используются следующие технологии:

- Python 3.9
- FastAPI
- SQLAlchemy
- PostgreSQL
- Docker
- Docker Compose

## Установка

Для локального запуска проекта выполните следующие шаги:

1. Клонируйте репозиторий:

```
git clone https://github.com/2blackdragon/AvitoMerchShop.git
cd AvitoMerchShop 
```

2. Создайте и активируйте виртуальное окружение:

```
python3 -m venv venv
source venv/bin/activate  # Для Windows используйте `venv\Scripts\activate`
```
3. Установите зависимости:

```
pip install -r requirements.txt
```

4. Настройте переменные окружения:

Создайте файл .env в корневой директории проекта и добавьте необходимые переменные окружения. Пример:

```
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=avito_merch_shop
POSTGRES_HOST=db
POSTGRES_PORT=5432

DATABASE_URL=postgresql://user:password@db:5432/avito_merch_shop
TEST_DATABASE_URL=postgresql://user:password@localhost:5432/avito_merch_shop_test_db

EXPIRE_TOKEN_MINUTES=20
SECRET_KEY=some_secret_key
ALGORITHM=HS256
```

5. Соберите и запустите контейнеры

```
docker-compose up --build
```

Приложение будет доступно по адресу http://localhost:8000.

## Использование

После запуска приложения вы можете:

- Покупать товары.
- Проводить транзакции между пользователями.
- Просматривать историю покупок и переводов.

Подробная документация API доступна по адресу http://127.0.0.1:8000/docs.

## Тестирование

Для запуска тестов выполните:

```
python -m pytest -v
```

Убедитесь, что перед запуском тестов настроена тестовая база данных и необходимые переменные окружения.

