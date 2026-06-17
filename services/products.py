from typing import Sequence

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

# Імпортуємо конкретну модель продукту з вашої папки models
from models.product import Product
from schemas.product import ProductCreate, ProductUpdate
from settings.db import get_db

class ProductService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> Sequence[Product]:
        result = await self.db.execute(select(Product))
        return result.scalars().all()

    async def get_by_id(self, product_id: int) -> Product | None:
        result = await self.db.execute(select(Product).where(Product.id == product_id))
        return result.scalars().first()

    async def create(self, data: ProductCreate) -> Product:
        new_product = Product(**data.model_dump())
        self.db.add(new_product)
        await self.db.commit()
        await self.db.refresh(new_product)
        return new_product

    async def update(self, product_id: int, data: ProductUpdate) -> Product | None:
        product = await self.get_by_id(product_id)
        if not product:
            return None

        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(product, field, value)

        self.db.add(product)
        await self.db.commit()
        await self.db.refresh(product)
        return product

    async def delete(self, product_id: int) -> bool:
        product = await self.get_by_id(product_id)
        if not product:
            return False

        await self.db.delete(product)
        await self.db.commit()
        return True


# Функція-провайдер, яку ми будемо викликати через Depends в роутері
async def get_product_service(db: AsyncSession = Depends(get_db)) -> ProductService:
    return ProductService(db)