"""
@ File        : redis.py
@ Version     : V1.0.0
@ Description : redis
"""

from typing import AsyncIterator

from aioredis import from_url, Redis
from config import AppSettings

dev = AppSettings.dev.get('redis')
async def init_redis_pool() -> AsyncIterator[Redis]:
    session = await from_url(
        url=f"redis://{dev['host']}", port=dev['port'], password=dev['password'], db=dev['db'], encoding="utf-8", decode_responses=True)
    return session
