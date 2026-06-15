import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from settings.db import get_db
from models import Product  # Перевірте, як саме імпортується ваша модель Product
from schemas.product import ProductCreate, ProductRead, ProductUpdate

# Налаштування логування для цього роутера
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/products", tags=["Products"])

# Сучасне оголошення залежності сесії БД через Annotated
SessionDepend = Annotated[AsyncSession, Depends(get_db)]


# 1. Отримання списку всього одягу (READ - GET)
@router.get("/", response_model=list[ProductRead])
async def get_products(session: SessionDepend):
    try:
        result = await session.execute(select(Product))
        return result.scalars().all()
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Failed to get products")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get products",
        ) from exc


# 2. Отримання однієї одиниці одягу за ID (READ - GET)
@router.get("/{product_id}", response_model=ProductRead)
async def get_product(product_id: int, session: SessionDepend):
    try:
        result = await session.execute(select(Product).where(Product.id == product_id))
        product = result.scalars().first()
        
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Product not found"
            )
        return product
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Failed to get product with id %d", product_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get product",
        ) from exc


# 3. Додавання нового одягу в магазин (CREATE - POST)
@router.post("/", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
async def create_product(product_data: ProductCreate, session: SessionDepend):
    try:
        new_product = Product(**product_data.model_dump())
        session.add(new_product)
        await session.commit()
        await session.refresh(new_product)
        return new_product
    except HTTPException:
        raise
    except Exception as exc:
        await session.rollback()
        logger.exception("Failed to create product")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create product",
        ) from exc


# 4. Часткове оновлення інформації про товар (UPDATE - PATCH)
@router.patch("/{product_id}", response_model=ProductRead)
async def update_product(product_id: int, product_update: ProductUpdate, session: SessionDepend):
    try:
        result = await session.execute(select(Product).where(Product.id == product_id))
        existing_product = result.scalars().first()
        
        if not existing_product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Product not found"
            )
            
        # Оновлюємо лише ті поля, які користувач передав у запиті
        for field, value in product_update.model_dump(exclude_unset=True).items():
            setattr(existing_product, field, value)
            
        session.add(existing_product)
        await session.commit()
        await session.refresh(existing_product)
        return existing_product
    except HTTPException:
        raise
    except Exception as exc:
        await session.rollback()
        logger.exception("Failed to update product with id %s", product_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update product",
        ) from exc


# 5. Видалення товару з магазину (DELETE)
@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: int, session: SessionDepend):
    try:
        result = await session.execute(select(Product).where(Product.id == product_id))
        existing_product = result.scalars().first()
        
        if not existing_product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Product not found"
            )
            
        await session.delete(existing_product)
        await session.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except HTTPException:
        raise
    except Exception as exc:
        await session.rollback()
        logger.exception("Failed to delete product with id %s", product_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete product",
        ) from exc