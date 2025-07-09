from datetime import datetime
from typing import List, Optional

from fastapi import FastAPI, Depends
from fastapi import HTTPException, status
from fastapi import Path
from fastapi import Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import and_

from . import categorizer
from . import models, schemas
from . import profanity_check
from . import sentiment
from .database import engine, SessionLocal

app = FastAPI()


@app.on_event("startup")
async def startup():
    """Создаёт таблицы в БД при запуске приложения."""
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)


async def get_db():
    """Предоставляет сессию подключения к базе данных."""
    async with SessionLocal() as session:
        yield session


@app.post("/complaints", response_model=schemas.ComplaintResponse)
async def create_complaint(data: schemas.ComplaintCreate, db: AsyncSession = Depends(get_db)):
    """Создаёт жалобу, очищает от мата, определяет тональность и категорию."""

    try:
        # Очистка от мата
        cleaned_text = profanity_check.clean_profanity(data.text)

        # Анализ тональности
        try:
            sentiment_result = await sentiment.get_sentiment(cleaned_text)
        except Exception:
            sentiment_result = "unknown"

        # Создание жалобы
        complaint = models.Complaint(text=cleaned_text, sentiment=sentiment_result)
        db.add(complaint)
        await db.commit()
        await db.refresh(complaint)

        # Классификация
        try:
            category_result = await categorizer.classify_text(cleaned_text)
            complaint.category = category_result
            await db.commit()
            await db.refresh(complaint)
        except Exception:
            pass

        return complaint

    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@app.get("/complaints", response_model=List[schemas.ComplaintResponse])
async def get_complaints(
        status: Optional[str] = Query(None, description="Статус жалобы (например, open)"),
        from_timestamp: Optional[datetime] = Query(None, alias="from", description="Дата и время начала (ISO 8601)"),
        db: AsyncSession = Depends(get_db),
):
    """Возвращает список жалоб, отфильтрованных по статусу и/или дате создания."""

    query = select(models.Complaint)

    filters = []
    if status:
        filters.append(models.Complaint.status == status)
    if from_timestamp:
        filters.append(models.Complaint.timestamp >= from_timestamp)

    if filters:
        query = query.where(and_(*filters))

    result = await db.execute(query)
    complaints = result.scalars().all()

    return complaints


@app.put("/complaints/{complaint_id}", response_model=schemas.ComplaintResponse)
async def update_complaint_status(
        complaint_id: int = Path(..., description="ID жалобы"),
        status: str = Query(..., description="Новый статус: open или closed"),
        db: AsyncSession = Depends(get_db),
):
    """Обновляет статус жалобы по ID (например, закрывает её)."""

    query = select(models.Complaint).where(models.Complaint.id == complaint_id)
    result = await db.execute(query)
    complaint = result.scalar_one_or_none()

    if not complaint:
        raise HTTPException(status_code=404, detail="Жалоба не найдена")

    complaint.status = status
    await db.commit()
    await db.refresh(complaint)

    return complaint
