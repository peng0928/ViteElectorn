import json
from hashlib import md5

from task.core import *
from utils.request.api import RequestClient
import asyncio
import random
import aioredis
from loguru import logger


async def make_order(cookie, data):
    async with RequestClient() as c:
        response = await c.order_create(cookie, item=data)
    await asyncio.sleep(5)
    return response


async def subscribe_to_channel(finger, data, cookie):
    redis = aioredis.Redis.from_url(f"redis://{REDIS_HOST}")
    pubsub = redis.pubsub()
    await pubsub.subscribe(finger)
    stop_event = asyncio.Event()

    async def listen_for_messages():
        async for message in pubsub.listen():
            if message['type'] == 'message':
                data = message['data'].decode('utf-8')
                logger.info(f"[Sub Rev]: {data}")
                if data == 'stop':  # 如果收到停止信号
                    stop_event.set()  # 设置停止事件
                    break  # 退出消息监听循环
        await pubsub.unsubscribe(finger)

    async def run_task():
        while not stop_event.is_set():  # 检查是否收到停止信号
            # 执行任务逻辑
            response = await make_order(cookie, data)
            print(response)
        logger.info(f"[Task] Completed => {finger}")

    try:
        # 并发运行消息监听和任务逻辑
        await asyncio.gather(listen_for_messages(), run_task())
    finally:
        await redis.close()


async def execute_task(task):
    """
    模拟任务执行
    """
    task = json.loads(task.decode('utf-8'))
    name = task.get("name")
    start_date = task.get("startDate")
    data = task.get("data")
    cookie = task.get("cookie")
    fingerprint = md5(f"{name}{start_date}".encode('utf-8')).hexdigest()
    logger.info(f"[Task] Starting => {fingerprint}")
    asyncio.create_task(subscribe_to_channel(fingerprint, data, cookie))


async def main():
    """
    轮询 Redis，获取未开始的任务并下发执行
    """
    logger.info("START")
    asyncio.create_task(state())
    while True:
        tasks = await poll_data()
        for task in tasks:
            await control()
            asyncio.create_task(execute_task(task))
        await asyncio.sleep(1)


class FwdTasks(RedisTaskQueue):

    async def main(self, task):
        asyncio.create_task(execute_task(task))
        await asyncio.sleep(1)
        print(task)


if __name__ == "__main__":
    task = FwdTasks()
    asyncio.run(task.start())
