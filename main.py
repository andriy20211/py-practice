from fastapi import FastAPI, HTTPException, status
from contextlib import asynccontextmanager

from models import Base  # Імпортуємо наш Base, де лежать метадані моделей
from settings.db import ping, engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    # При старті додатку автоматично створюємо всі таблиці в PostgreSQL
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # При зупинці додатку закриваємо з'єднання з БД
    await engine.dispose()

app = FastAPI(title="Магазин чоловічого одягу", lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "Welcome to Men's Clothing Store API"}

@app.get("/healthcheck", status_code=status.HTTP_200_OK)
async def db_healthcheck():
    is_alive = await ping()
    if not is_alive:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection failed",
        )
    return {"status": "healthy", "database": "connected"}