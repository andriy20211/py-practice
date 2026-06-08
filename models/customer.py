from typing import Optional
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base

class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    delivery_address: Mapped[Optional[str]] = mapped_column(Text, nullable=True)