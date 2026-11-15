# core/crud.py
import json
from typing import Any
from datetime import datetime
from sqlalchemy import select, delete
from core.db import AsyncSessionLocal
from core.models import Post
from core.cache import CacheManager, redis_client

async def get_post_by_slug(slug: str) -> dict[str, Any] | None:
    """Obtiene un post verificando primero en Redis, y si falla, en PostgreSQL."""
    cache_key = f"cms:post:{slug}"

    async def fetch_from_pg() -> Post | None:
        # Abrimos conexión a DB de forma segura
        async with AsyncSessionLocal() as session:
            stmt = select(Post).where(Post.slug == slug, Post.status == 'publish')
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    # Delegamos al CacheManager
    post_data = await CacheManager.get_or_fetch(
        key=cache_key,
        fetcher=fetch_from_pg,
        ttl_seconds=3600
    )

    return post_data

async def get_post_by_id(post_id: int) -> Post | None:
    """Obtiene un objeto Post puro de SQLAlchemy por su ID."""
    async with AsyncSessionLocal() as session:
        stmt = select(Post).where(Post.id == post_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

async def get_all_posts() -> list[dict[str, Any]]:
    """Obtiene todos los posts para el panel de administración (en tiempo real, sin caché)."""

    async with AsyncSessionLocal() as session:
        # Traemos todo ordenado por fecha de creación descendente
        stmt = select(Post).order_by(Post.created_at.desc())
        result = await session.execute(stmt)
        posts = result.scalars().all()
        posts_list = []

        for p in posts:
            p_dict = p.__dict__.copy()
            p_dict.pop('_sa_instance_state', None)
            for k, v in p_dict.items():
                if isinstance(v, datetime):
                    p_dict[k] = v.isoformat()
            posts_list.append(p_dict)

        return posts_list

async def create_post(title: str, slug: str, content: str, post_type: str = "post", blocks_json: str = "{}") -> bool:
    async with AsyncSessionLocal() as session:
        blocks_data = json.loads(blocks_json) if blocks_json else {}

        new_post = Post(
            slug=slug, title=title, content=content, post_type=post_type, status="publish",
            # Guardamos el JSON de Editor.js en nuestro campo JSONB
            meta={"autor": "Gema (Admin)", "version": "1.0", "blocks": blocks_data}
        )
        session.add(new_post)
        await session.commit()
        await redis_client.delete(f"cms:post:{slug}")
        await redis_client.delete("cms:posts:recent:10")
        return True

async def update_post(post_id: int, title: str, slug: str, content: str, post_type: str, blocks_json: str = "{}") -> bool:
    async with AsyncSessionLocal() as session:
        post = await session.get(Post, post_id)

        if not post: return False
        old_slug = post.slug
        post.title, post.slug, post.content, post.post_type = title, slug, content, post_type

        # Actualizamos el JSONB
        blocks_data = json.loads(blocks_json) if blocks_json else {}
        meta_copy = dict(post.meta) if post.meta else {}
        meta_copy["blocks"] = blocks_data
        post.meta = meta_copy # Reasignamos para que SQLAlchemy detecte el cambio

        await session.commit()

        await redis_client.delete(f"cms:post:{old_slug}")
        if old_slug != slug: await redis_client.delete(f"cms:post:{slug}")
        await redis_client.delete("cms:posts:recent:10")
        return True

async def delete_post(post_id: int) -> bool:
    """Elimina un post de la BD usando su ID y purga las cachés relacionadas."""
    async with AsyncSessionLocal() as session:
        stmt = select(Post).where(Post.id == post_id)
        result = await session.execute(stmt)
        post = result.scalar_one_or_none()

        if post:
            slug = post.slug
            await session.delete(post)
            await session.commit()

            # 🧹 Limpieza crucial de caché en Redis
            await redis_client.delete(f"cms:post:{slug}")
            await redis_client.delete("cms:posts:recent:10")
            return True

    return False
