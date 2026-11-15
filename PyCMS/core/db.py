# core/db.py
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

DATABASE_URL = "postgresql+asyncpg://user:password@localhost/pycms"

engine = create_async_engine(DATABASE_URL, pool_size=20, max_overflow=0, echo=False)
AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)

class Base(AsyncAttrs, DeclarativeBase):
    """Clase base para todos los modelos SQLAlchemy"""
    pass
