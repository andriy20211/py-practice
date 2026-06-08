from typing import Optional
from sqlalchemy import String, Numeric, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base

class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    brand: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)  # Використовуємо Numeric для грошей
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    material: Mapped[Optional[str]] = mapped_column(String(150), nullable=True)
    
    # Зв'язок з категорією (Один до Багатьох)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)