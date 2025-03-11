import asyncio
import datetime
import json

import aiohttp
from PrSpider import Xpath
import requests

from loguru import logger

from functools import wraps


def catch_exceptions_async(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            logger.error(f"[catch_exceptions_async] {e}")
            return {"status": False, "msg": "服务暂不可用"}

    return wrapper


class AioHttpClient:

    def __init__(self, **kwargs):
        self.headers = {
            "Accept": "*/*",
            "User-Agent": "Dart/3.5 (dart:io)",
        }
        self.headers_form = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'User-Agent': 'Dart/3.5 (dart:io)',
        }
        self.cookie = kwargs.get('cookie')

    async def __aenter__(self):
        self.request = aiohttp.ClientSession(headers=self.headers, cookies=self.cookie)
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.request.close()

    async def close(self):
        await self.request.close()


def loop_run(func):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(func())
