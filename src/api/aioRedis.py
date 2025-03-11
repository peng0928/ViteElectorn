import asyncio
import random

import redis
import time
from loguru import logger

# Redis 连接配置
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0

# 最大并发任务数
max_work = 100
key = "task_queue"

redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)


async def execute_task(task_id):
    """
    模拟任务执行
    """
    logger.info(f"开始执行任务: {task_id}")

    # 模拟任务执行时间
    time_sleep = random.randint(10, 30)
    await asyncio.sleep(time_sleep)

    logger.info(f"任务 {task_id} 执行完成")


async def control():
    while len(asyncio.all_tasks()) - 2 >= max_work:
        await asyncio.sleep(1)


async def state():
    while True:
        tasks = len(asyncio.all_tasks()) - 2
        logger.info(f"running({tasks})")
        await asyncio.sleep(5)


async def poll_data():
    tasks = redis_client.zrangebyscore(key, -1, -1, start=0, num=10)
    if tasks:
        for task_id in tasks:
            redis_client.zadd(key, {task_id: 0})
    return tasks


async def main():
    """
    轮询 Redis，获取未开始的任务并下发执行
    """
    logger.info("START")
    asyncio.create_task(state())
    while True:
        tasks = await poll_data()
        for task_id in tasks:
            await control()
            asyncio.create_task(execute_task(task_id))
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())
