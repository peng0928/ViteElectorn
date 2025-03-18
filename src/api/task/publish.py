import asyncio
import aioredis


async def publish_message():
    redis = aioredis.Redis.from_url("redis://localhost")

    # 发布停止信号
    await redis.publish('topic2', 'stop')
    print("Published: stop signal")

    await redis.close()


async def main():
    await asyncio.gather(
        publish_message()
    )


if __name__ == '__main__':
    # 运行主函数
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

