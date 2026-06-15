import logging
from fastapi import FastAPI, HTTPException, status
from contextlib import asynccontextmanager

from settings.db import ping, engine

# ІМПОРТ: Підключаємо ваш роутер товарів
from routers.products import router as products_router

# НАЛАШТУВАННЯ ЛОГУВАННЯ
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

# Очищений lifespan: тепер він ТІЛЬКИ закриває з'єднання при зупинці сервера.
# Створення таблиць (Base.metadata.create_all) звідси ВИДАЛЕНО.
@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    # При зупинці додатку закриваємо з'єднання з БД
    await engine.dispose()

app = FastAPI(title="Магазин чоловічого одягу", lifespan=lifespan)

# ПІДКЛЮЧЕННЯ РОУТЕРА
app.include_router(products_router)

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