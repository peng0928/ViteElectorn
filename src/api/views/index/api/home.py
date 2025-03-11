from datetime import datetime, timezone, timedelta

from fastapi.responses import ORJSONResponse, JSONResponse
from fastapi.routing import APIRouter
from fastapi import *
from fastapi.responses import HTMLResponse

from utils.request.login import RequestClient

router = APIRouter(
    prefix="/api",
    tags=["主页"],
    default_response_class=ORJSONResponse
)


@router.post("/hotShop")
async def hotShop(item: dict, request: Request):
    async with RequestClient() as c:
        data = await c.hotShop()
    msg = data.get("msg")
    result = data.get("data")
    if msg == "操作成功":
        response = JSONResponse(status_code=200, content={"status": True, "msg": msg, "code": 200, "data": result})
        return response
    else:
        return JSONResponse(status_code=200, content={"status": False, "msg": msg, "code": 300, "data": result})

@router.post("/headShop")
async def headShop(item: dict, request: Request):
    async with RequestClient() as c:
        data = await c.headShop()
    msg = data.get("msg")
    result = data.get("data")
    if msg == "操作成功":
        response = JSONResponse(status_code=200, content={"status": True, "msg": msg, "code": 200, "data": result})
        return response
    else:
        return JSONResponse(status_code=200, content={"status": False, "msg": msg, "code": 300, "data": result})
