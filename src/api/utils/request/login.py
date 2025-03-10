import asyncio

from .modal.aio import *


class LoginClient(AioHttpClient):

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


async def main():
    phone = "17732639704"
    client = LoginClient()
    data = await client.verify_captcha(phone=phone, captcha="697644")
    await client.close()
    print(data)


if __name__ == '__main__':
    # asyncio.run(main())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
