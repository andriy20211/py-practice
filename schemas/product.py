from typing import Optional
from pydantic import BaseModel, Field

# Базова схема з правилами валідації
class ProductBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description="Назва одягу (напр., Сорочка Oxford)")
    brand: str = Field(..., min_length=1, max_length=100, description="Бренд одягу (напр., Nike, Zara)") # ДОДАЛИ ОБОВ'ЯЗКОВИЙ БРЕНД
    description: Optional[str] = Field(None, description="Опис товару")
    price: float = Field(..., gt=0, description="Ціна повинна бути більшою за 0")

# 1. Схема для створення (CREATE)
class ProductCreate(ProductBase):
    category_id: Optional[int] = Field(None, description="ID категорії")

# 2. Схема для оновлення (UPDATE)
class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    brand: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)

# 3. Схема для відповіді клієнту (READ)
class ProductRead(ProductBase):
    id: int
    category_id: int

    class Config:
        from_attributes = True