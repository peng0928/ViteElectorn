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
        accept = 'application/json, text/javascript, */*; q=0.01'
        ua = "Dart/3.5 (dart:io)"
        self.headers = {
            "Accept": "*/*",
            "User-Agent": ua,
        }
        self.headers_form = {
            'Accept': accept,
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'User-Agent': ua,
        }
        self.headers_json = {
            'Accept': accept,
            'content-type': "application/json; charset=utf-8",
            'User-Agent': ua,
        }
        self.cookie = kwargs.get('cookie')

    async def __aenter__(self):
        self.conn = aiohttp.TCPConnector(ssl=False)
        self.request = aiohttp.ClientSession(headers=self.headers, cookies=self.cookie, connector=self.conn)
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.request.close()
        await self.conn.close()


    def get_token(self, request: object):
        cookie = request.cookies or {}
        token = cookie.get("t") or ""
        return token


def loop_run(func):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(func())
