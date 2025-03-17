from contextlib import asynccontextmanager

from fastapi import FastAPI

from config import AppSettings
from utils.client.redis import init_redis_pool
from utils.client.mongoApi import MongoConn

dev = AppSettings.dev
dev_mongo = dev['mongo']


# 关于生命周期事件详见：https://fastapi.tiangolo.com/advanced/events/#lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    session = await init_redis_pool()  #
    app.state.redis = session
    app.state.mongo = MongoConn(dev_mongo)
    yield
    await session.close()
    app.state.mongo.close()
