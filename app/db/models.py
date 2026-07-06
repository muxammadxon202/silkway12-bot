from datetime import datetime

from sqlalchemy import BigInteger, Boolean, DateTime, Integer, String, Text, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    service: Mapped[str] = mapped_column(String(32))
    service_name: Mapped[str] = mapped_column(String(64))
    options: Mapped[str] = mapped_column(Text, default="")   # имена опций через ", "
    urgent: Mapped[bool] = mapped_column(Boolean, default=False)
    price: Mapped[int] = mapped_column(Integer)
    days: Mapped[int] = mapped_column(Integer)
    contact: Mapped[str | None] = mapped_column(String(120), nullable=True)
    status: Mapped[str] = mapped_column(String(16), default="new")  # new | in_work | done
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class BotState(Base):
    """Одна строка (id=1) с настройками рантайма — сейчас только admin_chat_id."""

    __tablename__ = "bot_state"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, default=1)
    admin_chat_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
