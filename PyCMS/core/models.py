# core/models.py
from datetime import datetime, UTC
from typing import Any
from sqlalchemy import String, Text, DateTime, Index
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from core.db import Base # Importamos la base

class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(String(200), unique=True, index=True)
    title: Mapped[str] = mapped_column(String(255))
    content: Mapped[str] = mapped_column(Text)
    post_type: Mapped[str] = mapped_column(String(50), default="post", index=True) 
    status: Mapped[str] = mapped_column(String(20), default="publish", index=True)

    # Campo JSONB para metadatos sin límite de estructura
    meta: Mapped[dict[str, Any]] = mapped_column(JSONB, server_default='{}')

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))

    __table_args__ = (
        Index('idx_post_type_status', 'post_type', 'status'),
        Index('idx_post_meta_gin', 'meta', postgresql_using='gin'),
    )
