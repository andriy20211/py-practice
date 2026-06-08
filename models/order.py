import datetime
from sqlalchemy import String, Numeric, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base

class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    order_number: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    status: Mapped[str] = mapped_column(String(50), default="New")  # New, Paid, Delivered
    total_amount: Mapped[float] = mapped_column(Numeric(10, 2), default=0.00)

    # Зв'язок з клієнтом
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id", ondelete="RESTRICT"), nullable=False)