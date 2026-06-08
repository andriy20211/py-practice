from sqlalchemy import String, Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base

class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    quantity: Mapped[int] = mapped_column(default=1, nullable=False)
    size: Mapped[str] = mapped_column(String(10), nullable=False)  # S, M, L, XL
    price_at_sale: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)

    # Зв'язки
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id", ondelete="RESTRICT"), nullable=False)