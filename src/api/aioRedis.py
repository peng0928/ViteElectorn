import json
from hashlib import md5

from task.core import *
from utils.request.api import RequestClient
import asyncio
import random
import aioredis
from loguru import logger
from typing import List


class RedisTaskQueue:
    def __init__(
            self,
            redis_host: str = 'localhost',
            redis_port: int = 6379,
            redis_db: int = 0,
            queue_key: str = "task_queue",
            max_concurrent_tasks: int = 100
    ):
        """
        Redis 异步任务队列处理器
        :param redis_host: Redis 主机地址
        :param redis_port: Redis 端口
        :param redis_db: Redis 数据库编号
        :param queue_key: 任务队列的 Redis key
        :param max_concurrent_tasks: 最大并发任务数
        """
        self.redis_client = aioredis.from_url(url=f"redis://{redis_host}", port=redis_port, db=redis_db)
        self.queue_key = queue_key
        self.max_concurrent = max_concurrent_tasks

        # 预注册 Lua 脚本
        self._poll_script = self.redis_client.register_script("""
        local min_score = ARGV[1]
        local max_score = ARGV[2]
        local set_score = ARGV[3]
        local count = ARGV[4]

        local real_datas = {}
        if count ~= '' then
            for i = 1, count do
                local data_with_score = redis.call('zrangebyscore', 
                    KEYS[1], min_score, max_score, 'withscores', 'limit', 0, 1)
                if #data_with_score > 0 then
                    local data = data_with_score[1]
                    table.insert(real_datas, data)
                    redis.call('zincrby', KEYS[1], set_score - data_with_score[2], data)
                end
            end
        else
            local datas = redis.call('zrangebyscore', 
                KEYS[1], min_score, max_score, 'withscores')
            for i=1, #datas, 2 do
                table.insert(real_datas, datas[i])
                redis.call('zincrby', KEYS[1], set_score - datas[i+1], datas[i])
            end
        end
        return real_datas
        """)

    async def execute_task(self, task_id: str) -> None:
        """执行单个任务"""
        logger.info(f"[Task Start] {task_id}")
        try:
            await self.main(task_id)
            logger.success(f"[Task Complete] {task_id}")
        except Exception as e:
            logger.error(f"[Task Failed] {task_id}: {str(e)}")
        finally:
            self.redis_client.zadd(self.queue_key, {task_id: 1})

    async def _control_concurrency(self) -> None:
        """并发控制"""
        while len(asyncio.all_tasks()) - 2 >= self.max_concurrent:
            await asyncio.sleep(1)

    @staticmethod
    def get_all_tasks():
        return len(asyncio.all_tasks()) - 2

    async def listing(self):
        active_tasks = self.get_all_tasks()
        logger.info(f"Active Tasks: {active_tasks}/{self.max_concurrent}")
        await asyncio.sleep(5)

    async def _monitor_status(self) -> None:
        """系统状态监控"""
        while True:
            await self.listing()

    async def _fetch_tasks(self, batch_size: int = 10) -> List[str]:
        """获取待处理任务"""
        return await self._poll_script(
            keys=[self.queue_key],
            args=[-1, -1, 0, batch_size]
        )

    async def start(self) -> None:
        """启动任务处理系统"""
        logger.info("System Starting...")
        asyncio.create_task(self._monitor_status())

        while True:
            tasks = await self._fetch_tasks()
            print(tasks)
            for task_id in tasks:
                await self._control_concurrency()
                asyncio.create_task(self.execute_task(task_id))
            await asyncio.sleep(0.314)

    async def main(self, task_id):
        await asyncio.sleep(random.randint(10, 30))


class Task(RedisTaskQueue):

    async def main(self, task_id):
        print(task_id)

    async def listing(self):
        logger.info(f"Active Tasks: {self.get_all_tasks()}/{self.max_concurrent}")
        await asyncio.sleep(60)


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
            async with RequestClient() as c:
                response = await c.order_create(cookie, item=data)
                print(response)
            await asyncio.sleep(5)
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


if __name__ == "__main__":
    asyncio.run(main())
    # task_queue = Task()
    # asyncio.run(task_queue.start())
