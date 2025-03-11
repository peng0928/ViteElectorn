import asyncio
from .modal.aio import *


class RequestClient(AioHttpClient):

    @catch_exceptions_async
    async def get_captcha(self, phone: str):
        url = "https://api.livelab.com.cn/thirdParty/sms/app/captcha"
        data = f"phone={phone}&type=1"
        response = await self.request.post(url, data=data, headers=self.headers_form)
        json_data = await response.json()
        return json_data

    @catch_exceptions_async
    async def verify_captcha(self, phone: str, captcha: str):
        url = "https://api.livelab.com.cn/auth/app/login/phoneCaptcha"
        data = f"phone={phone}&captcha={captcha}&sekyCaptcha=&deviceId=&deviceType=2&blackBox="
        response = await self.request.post(url, data=data, headers=self.headers_form)
        json_data = await response.json()
        json_dict = json_data.get("data") or {}
        query = {
            "msg": json_data.get("msg"),
            "token": json_dict.get("token", ""),
        }
        return query

    @catch_exceptions_async
    async def search(self, text: str):
        url = "https://api.livelab.com.cn/search/app/search/text"
        payload = {"keyword": text, "channel": 1}
        response = await self.request.post(url, json=payload, headers=self.headers_json, ssl=False)
        json_data = await response.json()
        json_dict = json_data.get("data") or []
        query = {
            "msg": json_data.get("msg"),
            "data": json_dict,
        }
        return query

    @catch_exceptions_async
    async def app_info(self, request: object):
        cookie = self.get_token(request)
        url = "https://api.livelab.com.cn/member/member/app/info"
        headers = self.headers.copy()
        headers.update({
            'authorization': f"Bearer {cookie}",
        })
        response = await self.request.get(url, headers=headers)
        json_data = await response.json()
        json_dict = json_data.get("data") or []
        query = {
            "msg": json_data.get("msg"),
            "data": json_dict,
        }
        return query


async def main():
    phone = "17732639704"
    client = RequestClient()
    async with client as c:
        data = await c.app_info("五月天")
    print(data)


if __name__ == '__main__':
    # asyncio.run(main())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
