# core/models.py
from datetime import datetime
from typing import Any
from sqlalchemy import String, Text, DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from .db import Base

class Post(Base):
    """
    Modelo principal para el contenido de PyCMS.
    Maneja Entradas, Páginas y Custom Post Types.
    """
    __tablename__ = "posts"

    # Tipado estricto con Mapped y mapped_column (SQLAlchemy 2.0+)
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    slug: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)

    # page, post, portfolio, etc.
    post_type: Mapped[str] = mapped_column(String(50), default="post", index=True)

    # publish, draft, trash, etc.
    status: Mapped[str] = mapped_column(String(50), default="draft", index=True)

    # Campo JSONB nativo para flexibilidad total de metadatos (como en WordPress)
    meta: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)

    # Fechas automáticas manejadas por el motor de BD
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
