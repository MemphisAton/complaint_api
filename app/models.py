from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, DateTime

from .database import Base


class Complaint(Base):
    __tablename__ = "complaints"  # Название таблицы

    id = Column(Integer, primary_key=True, index=True)  # Уникальный ID
    text = Column(String, nullable=False)  # Текст жалобы
    status = Column(String, default="open")  # Статус (open/closed)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))  # Время создания
    sentiment = Column(String, default="unknown")  # Тональность (positive/neutral/negative)
    category = Column(String, default="другое")  # Категория (определяется ИИ)
