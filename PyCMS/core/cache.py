# core/cache.py
import json
from collections.abc import Callable, Awaitable
from redis.asyncio import Redis, ConnectionPool
from datetime import datetime

redis_pool = ConnectionPool.from_url("redis://localhost:6379/0", decode_responses=True)
redis_client = Redis(connection_pool=redis_pool)

class CacheManager:
    @staticmethod
    async def get_or_fetch[T](key: str, fetcher: Callable[[], Awaitable[T]], ttl_seconds: int = 3600) -> T | None:
        cached_data = await redis_client.get(key)

        if cached_data:
            return json.loads(cached_data)

        data = await fetcher()

        if data is not None:
            data_to_store = data if isinstance(data, dict) else data.__dict__.copy()
            data_to_store.pop('_sa_instance_state', None)

            for k, v in data_to_store.items():
                if isinstance(v, datetime):
                    data_to_store[k] = v.isoformat()

            await redis_client.setex(key, ttl_seconds, json.dumps(data_to_store))
            return data_to_store

        return None
