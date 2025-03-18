import asyncio
import aioredis


async def subscribe_to_channel(topic):
    redis = aioredis.Redis.from_url("redis://localhost")
    pubsub = redis.pubsub()
    await pubsub.subscribe(topic)

    stop_event = asyncio.Event()

    async def listen_for_messages():
        async for message in pubsub.listen():
            if message['type'] == 'message':
                data = message['data'].decode('utf-8')
                print(f"Received: {data}")
                if data == 'stop':  # 如果收到停止信号
                    stop_event.set()  # 设置停止事件
                    break  # 退出消息监听循环
        await pubsub.unsubscribe(topic)

    async def run_task():
        while not stop_event.is_set():  # 检查是否收到停止信号
            # 执行任务逻辑
            print(f"{topic} is running...")
            await asyncio.sleep(1)
        print(f"{topic} stopped.")

    try:
        # 并发运行消息监听和任务逻辑
        await asyncio.gather(listen_for_messages(), run_task())
    finally:
        await redis.close()


async def main():
    task = []
    for topic in ['topic1', 'topic2']:
        task.append(asyncio.create_task(subscribe_to_channel(topic)))
    await asyncio.gather(*task)


if __name__ == '__main__':
    # 运行主函数
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
