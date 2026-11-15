import asyncio
from core.db import AsyncSessionLocal, engine, Base
from core.models import Post
from sqlalchemy import select

async def seed_db():
    # 1. Primero nos aseguramos de que las tablas existan
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        print("✅ Tablas creadas/verificadas en PostgreSQL.")

    # 2. Ahora sí, interactuamos con la tabla
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Post).where(Post.slug == "home"))
        if result.scalar_one_or_none():
            print("El post 'home' ya existe.")
            return

        nuevo_post = Post(
            slug="home",
            title="Bienvenido a PyCMS",
            content="¡El motor asíncrono está funcionando a la perfección!",
            post_type="page",
            status="publish",
            meta={"autor": "Gema", "version": "1.0"}
        )
        session.add(nuevo_post)
        await session.commit()
        print("✅ Post de prueba 'home' insertado correctamente.")

if __name__ == "__main__":
    asyncio.run(seed_db())
