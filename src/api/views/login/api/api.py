from datetime import datetime, timezone, timedelta

from fastapi.responses import ORJSONResponse, JSONResponse
from fastapi.routing import APIRouter
from fastapi import *
from fastapi.responses import HTMLResponse

from utils.request.login import LoginClient

client = LoginClient()
router = APIRouter(
    prefix="/api",
    tags=["登录"],
    default_response_class=ORJSONResponse
)


@router.post("/captcha")
async def captcha(item: dict, request: Request):
    phone = item.get("phone") or ""
    async with client as c:
        data = await c.get_captcha(phone=phone)
    msg = data.get("msg")
    if msg == "操作成功":
        response = JSONResponse(status_code=200, content={"status": True, "msg": msg, "code": 200})
        return response
    else:
        return JSONResponse(status_code=200, content={"status": False, "msg": msg, "code": 300})


@router.post("/login")
async def login(item: dict, request: Request):
    captcha = item.get("captcha")
    phone = item.get("phone")
    async with client as c:
        data = await c.verify_captcha(phone=phone, captcha=captcha)
    msg = data.get("msg") or ""
    token = data.get("token") or ""
    if msg == "操作成功":
        response = JSONResponse(status_code=200, content={"status": True, "msg": msg, "code": 200})
        expires = datetime.now(timezone.utc) + timedelta(days=30)  # 设置过期时间
        response.set_cookie(key="t", value=token, expires=expires, secure=False, httponly=True)
        return response
    else:
        return JSONResponse(status_code=200, content={"status": False, "msg": msg, "code": 300})
