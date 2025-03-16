import asyncio
from .modal.aio import *
from .modal.msg import *


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

    @catch_exceptions_async
    async def app_ticket(self, request: object):
        cookie = self.get_token(request)
        url = "https://api.livelab.com.cn/performance/app/ticket/list/v2?pageNum=1&pageSize=5"
        headers = self.headers.copy()
        headers.update({
            'authorization': f"Bearer {cookie}",
        })
        response = await self.request.get(url, headers=headers)
        json_data = await response.json()
        json_dict = json_data.get("data") or {}
        json_dict = json_dict.get("list") or []
        query = {
            "msg": json_data.get("msg"),
            "data": json_dict,
        }
        return query

    @catch_exceptions_async
    async def hotShop(self):
        url = "https://api.livelab.com.cn/appShow/app/homepage/projects?projectModuleId=81&pageNum=1&pageSize=15&v="
        response = await self.request.get(url, headers=self.headers)
        json_data = await response.json()
        json_dict = json_data.get("data") or {}
        json_dict = json_dict.get("list") or []
        query = {
            "msg": json_data.get("msg"),
            "data": json_dict,
        }
        return query

    @catch_exceptions_async
    async def get_project(self, project_id):
        url = f"https://api.livelab.com.cn/performance/app/project/get_project_info?project_id={project_id}"
        response = await self.request.get(url, headers=self.headers)
        json_data = await response.json()
        json_dict = json_data.get("data") or {}
        query = {
            "msg": json_data.get("msg"),
            "data": json_dict,
        }
        return query

    @catch_exceptions_async
    async def headShop(self):
        url = "https://api.livelab.com.cn/appShow/app/homepage/banners?bannerModuleId=52"
        response = await self.request.get(url, headers=self.headers)
        json_data = await response.json()
        json_dict = json_data.get("data") or []
        query = {
            "msg": json_data.get("msg"),
            "data": json_dict,
        }
        return query

    @catch_exceptions_async
    async def get_performs(self, request: object, _id):
        cookie = self.get_token(request)
        headers = self.headers.copy()
        headers.update({
            'authorization': f"Bearer {cookie}",
        })
        url = f"https://api.livelab.com.cn/performance/app/project/get_performs?project_id={_id}&standbyChannel=1"
        response = await self.request.get(url, headers=headers)
        json_data = await response.json()
        json_dict = json_data.get("data") or []
        query = {
            "msg": json_data.get("msg"),
            "data": json_dict,
        }
        return query

    @catch_exceptions_async
    async def get_member(self, request: object):
        cookie = self.get_token(request)
        headers = self.headers.copy()
        headers.update({
            'authorization': f"Bearer {cookie}",
        })
        url = "https://api.livelab.com.cn/member/member/bearer/app/list"
        response = await self.request.get(url, headers=headers)
        json_data = await response.json()
        json_dict = json_data.get("data") or []
        query = {
            "msg": json_data.get("msg"),
            "data": json_dict,
        }
        return query

    @catch_exceptions_async
    async def get_orders(self, request: object, pageNum=1, pageSize=5, type=0):
        """
        :param request:
        :param pageNum:
        :param pageSize:
        :param type: 0 全部 1 待支付 2 取消
        :return:
        """
        cookie = self.get_token(request)
        headers = self.headers.copy()
        headers.update({
            'authorization': f"Bearer {cookie}",
        })
        url = f"https://api.livelab.com.cn/performance/app/order/list?type={type}&pageNum={pageNum}&pageSize={pageSize}"
        response = await self.request.get(url, headers=headers)
        json_data = await response.json()
        json_dict = json_data.get("data") or []
        query = {
            "msg": json_data.get("msg"),
            "data": json_dict,
        }
        return query

    @catch_exceptions_async
    async def order_create(self, request: object, item: dict = {}):
        name = item.get("name") or ""
        phnoe = item.get("phnoe") or ""
        deliveryType = item.get("deliveryType") or ""
        projectId = item.get("projectId") or ""
        performId = item.get("performId") or ""
        audienceCount = item.get("audienceCount") or ""
        frequentIds = item.get("frequentIds") or ""
        seatPlanIds = item.get("seatPlanIds") or ""
        cookie = self.get_token(request)
        headers = self.headers_json.copy()
        headers.update({
            'authorization': f"Bearer {cookie}",
        })
        url = "https://api.livelab.com.cn/order/app/center/v3/create"
        payload = {"contactName": name, "contactPhone": phnoe, "deliveryName": name,
                   "deliveryPhone": phnoe, "expressFee": 0.0, "deliveryAddress": "", "addressId": None,
                   "deliveryType": deliveryType, "projectId": projectId, "performId": performId, "totalPrice": "0.00",
                   "payment": "0.00", "ordinaryTicketVos": None, "combineTicketVos": None, "blackBox": ":1",
                   "buyerId": None, "audienceCount": audienceCount, "frequentIds": frequentIds,
                   "seatPlanIds": seatPlanIds}
        response = await self.request.post(url, headers=headers, json=payload)
        json_data = await response.json()
        msg = json_data.get("msg")
        json_dict = json_data.get("data") or []
        code = json_data.get("code") or 10000
        if code != 10000:
            msg = code_msg.get(code) or msg
        query = {
            "msg": msg,
            "data": json_dict,
        }
        return query


async def main():
    phone = "17732639704"
    client = RequestClient()
    async with client as c:
        data = await c.hotShop()
    print(data)


if __name__ == '__main__':
    # asyncio.run(main())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
