import asyncio
from loguru import logger
import aioredis
from typing import List
from loguru import logger
from datetime import datetime

# Redis 连接配置
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 8

# 最大并发任务数
max_work = 100
key = "tasks:fwd"

redis_client = aioredis.Redis.from_url(f"redis://{REDIS_HOST}", port=REDIS_PORT, db=REDIS_DB)


class RedisTaskQueue:
    queue_key = key
    redis_host = REDIS_HOST
    redis_port = REDIS_PORT
    redis_db = REDIS_DB
    max_concurrent = max_work

    def __init__(self):
        """
        Redis 异步任务队列处理器
        :param redis_host: Redis 主机地址
        :param redis_port: Redis 端口
        :param redis_db: Redis 数据库编号
        :param queue_key: 任务队列的 Redis key
        :param max_concurrent_tasks: 最大并发任务数
        """
        self.log_init()
        self.redis_client = aioredis.from_url(url=f"redis://{self.redis_host}", port=self.redis_port, db=self.redis_db)
        self.queue_key = self.queue_key
        self.max_concurrent = self.max_concurrent
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

    def log_init(self):
        logger.info("=" * 60)
        logger.info(f"Service Initialization".center(60))
        logger.info(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}".center(60))
        logger.info(f"[Redis Key] {self.queue_key}".center(60))
        logger.info("=" * 60)
        logger.info("Initializing components...")

    async def execute_task(self, task_id: str) -> None:
        """执行单个任务"""
        logger.info(f"[Task Start] {task_id}")
        try:
            await self.main(task_id)
            logger.success(f"[Task Complete] {task_id}")
        except Exception as e:
            logger.error(f"[Task Failed] {task_id}: {str(e)}")
        finally:
            await self.redis_client.zadd(self.queue_key, {task_id: 1})

    async def _control_concurrency(self) -> None:
        """并发控制"""
        while len(asyncio.all_tasks()) - 2 >= self.max_concurrent:
            await asyncio.sleep(1)

    @staticmethod
    def get_all_tasks():
        return len(asyncio.all_tasks()) - 2

    async def listing(self):
        active_tasks = self.get_all_tasks()
        if active_tasks >= self.max_concurrent:
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
            for task_id in tasks:
                await self._control_concurrency()
                asyncio.create_task(self.execute_task(task_id))
            await asyncio.sleep(0.314)

    async def main(self, task):
        await asyncio.sleep(random.randint(10, 30))
