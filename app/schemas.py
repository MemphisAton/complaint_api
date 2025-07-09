from pydantic import BaseModel
from datetime import datetime


class ComplaintCreate(BaseModel):
    """Схема для входящего запроса (создание жалобы)."""
    text: str


class ComplaintResponse(BaseModel):
    """Схема для ответа клиенту (возвращаемая жалоба)."""
    id: int
    text: str
    status: str
    timestamp: datetime
    sentiment: str
    category: str

    class Config:
        orm_mode = True  # Важно для работы с ORM-моделью SQLAlchemy
