import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from fastapi import Depends
from typing import Annotated

# 1. Беремо рядок з .env, а якщо його немає (про всяк випадок) — використовуємо дефолтний SQLite
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./fastapi_db.db")

# 2. Створюємо асинхронний двигун для SQLite
engine = create_async_engine(
    DATABASE_URL, 
    echo=True,
    # Цей параметр потрібен тільки для SQLite, щоб підтримувати роботу з потоками FastAPI
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

# 3. Фабрика сесій
AsyncSessionLocal = async_sessionmaker(
    bind=engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

# 4. Функція-генератор сесій для ін'єкції залежностей
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

# Переконайтеся, що назва типу співпадає з тією, яку ви імпортуєте в роутерах (SessionDepend)
SessionDepend = Annotated[AsyncSession, Depends(get_db)]

# Якщо у вашому main.py імпортується функція ping, додамо її просту заглушку
async def ping():
    return True