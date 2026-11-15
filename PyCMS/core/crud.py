# core/crud.py
import json
import asyncio
from datetime import datetime
from typing import Any
from sqlalchemy import select
from core.db import AsyncSessionLocal
from core.models import Post
from core.cache import CacheManager, redis_client

# Alias de tipos modernos (Python 3.12+)
type PostData = dict[str, Any]

async def _serialize_post(post: Post) -> PostData:
    """
    Helper para convertir el modelo SQLAlchemy a diccionario seguro.
    Esencial para que Redis y Jinja2 manejen los datos sin errores de sesión (DetachedInstanceError).
    """
    p_dict = post.__dict__.copy()
    p_dict.pop('_sa_instance_state', None)  # Removemos metadatos internos de SQLAlchemy

    # Formateamos las fechas a texto ISO 8601
    for k, v in p_dict.items():
        if isinstance(v, datetime):
            p_dict[k] = v.isoformat()

    return p_dict

async def get_post_by_slug(slug: str) -> PostData | None:
    """Obtiene un post verificando primero en Redis, y si falla, en PostgreSQL."""
    cache_key = f"cms:post:{slug}"

    async def fetch_from_pg() -> PostData | None:
        async with AsyncSessionLocal() as session:
            stmt = select(Post).where(Post.slug == slug, Post.status == 'publish')
            result = await session.execute(stmt)
            post = result.scalar_one_or_none()

            # Devolvemos el diccionario serializado para que Redis pueda guardarlo en JSON
            if post:
                return await _serialize_post(post)
            return None

    # Delegamos al CacheManager (el cual asume que lo que recibe es serializable)
    return await CacheManager.get_or_fetch(
        key=cache_key,
        fetcher=fetch_from_pg,
        ttl_seconds=3600
    )

async def get_post_by_id(post_id: int) -> Post | None:
    """Obtiene un objeto Post puro de SQLAlchemy por su ID. (Usado internamente por el admin)"""
    async with AsyncSessionLocal() as session:
        return await session.get(Post, post_id)

async def get_all_posts() -> list[PostData]:
    """Obtiene todos los posts para el panel de administración (en tiempo real, sin caché)."""
    async with AsyncSessionLocal() as session:
        stmt = select(Post).order_by(Post.created_at.desc())
        result = await session.execute(stmt)
        posts = result.scalars().all()

        # Usamos list comprehension para serializar todo rápidamente
        return [await _serialize_post(p) for p in posts]

async def create_post(title: str, slug: str, content: str, post_type: str = "post", blocks_json: str = "{}") -> bool:
    async with AsyncSessionLocal() as session:
        try:
            blocks_data = json.loads(blocks_json) if blocks_json else {}
        except json.JSONDecodeError:
            blocks_data = {}

        new_post = Post(
            slug=slug, title=title, content=content, post_type=post_type, status="publish",
            meta={"autor": "Admin", "version": "1.0", "blocks": blocks_data}
        )
        session.add(new_post)
        await session.commit()

    # 🚀 OPTIMIZACIÓN: Borramos las claves de caché de forma concurrente usando TaskGroup
    async with asyncio.TaskGroup() as tg:
        tg.create_task(redis_client.delete(f"cms:post:{slug}"))
        tg.create_task(redis_client.delete("cms:posts:recent:10"))

    return True

async def update_post(post_id: int, title: str, slug: str, content: str, post_type: str, blocks_json: str = "{}") -> bool:
    async with AsyncSessionLocal() as session:
        post = await session.get(Post, post_id)
        if not post: return False

        old_slug = post.slug
        post.title, post.slug, post.content, post.post_type = title, slug, content, post_type

        try:
            blocks_data = json.loads(blocks_json) if blocks_json else {}
        except json.JSONDecodeError:
            blocks_data = {}

        meta_copy = dict(post.meta) if post.meta else {}
        meta_copy["blocks"] = blocks_data
        post.meta = meta_copy 

        await session.commit()

    # 🚀 OPTIMIZACIÓN: Limpieza concurrente en Redis
    async with asyncio.TaskGroup() as tg:
        tg.create_task(redis_client.delete(f"cms:post:{old_slug}"))
        if old_slug != slug: 
            tg.create_task(redis_client.delete(f"cms:post:{slug}"))
        tg.create_task(redis_client.delete("cms:posts:recent:10"))

    return True

async def delete_post(post_id: int) -> bool:
    """Elimina un post de la BD usando su ID y purga las cachés relacionadas."""
    async with AsyncSessionLocal() as session:
        post = await session.get(Post, post_id)
        if not post: return False

        slug = post.slug
        await session.delete(post)
        await session.commit()

    # 🚀 OPTIMIZACIÓN: Limpieza concurrente en Redis
    async with asyncio.TaskGroup() as tg:
        tg.create_task(redis_client.delete(f"cms:post:{slug}"))
        tg.create_task(redis_client.delete("cms:posts:recent:10"))

    return True
