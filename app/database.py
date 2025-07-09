from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

# URL для подключения к SQLite
DATABASE_URL = "sqlite+aiosqlite:///./complaints.db"

# Создаём движок с асинхронной поддержкой
engine = create_async_engine(DATABASE_URL, echo=True)

# Создаём фабрику сессий (будем использовать в запросах к БД)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# Базовый класс для моделей SQLAlchemy
Base = declarative_base()
