import asyncio
from loguru import logger
import aioredis

# Redis 连接配置
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 8

# 最大并发任务数
max_work = 100
key = "tasks:fwd"

redis_client = aioredis.Redis.from_url(f"redis://{REDIS_HOST}", port=REDIS_PORT, db=REDIS_DB)


async def control():
    while len(asyncio.all_tasks()) - 2 >= max_work:
        await asyncio.sleep(1)


async def state():
    while True:
        tasks = (len(asyncio.all_tasks()) - 2) // 3
        tasks = tasks if tasks > 0 else 0
        logger.info(f"running({tasks})")
        await asyncio.sleep(5)


async def poll_data():
    tasks = await redis_client.zrangebyscore(key, -1, -1, start=0, num=10)
    if tasks:
        for task_id in tasks:
            await redis_client.zadd(key, {task_id: 0})
    return tasks

