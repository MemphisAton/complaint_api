from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, DateTime

from .database import Base


class Complaint(Base):
    __tablename__ = "complaints"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    status = Column(String, default="open")
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    sentiment = Column(String, default="unknown")
    category = Column(String, default="другое")
