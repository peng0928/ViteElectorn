import json
from datetime import datetime, timezone, timedelta

from fastapi.responses import ORJSONResponse, JSONResponse
from fastapi.routing import APIRouter
from fastapi import *
from fastapi.responses import HTMLResponse
from config import *

from settions import app
from utils.request.api import RequestClient
from utils.tools.index import *
from utils.wapper.index import token_required

router = APIRouter(
    prefix="/api",
    tags=["ticket"],
    default_response_class=ORJSONResponse
)
dbConfig = DBConfig()


@router.post("/ticket")
@token_required
async def app_ticket(request: Request, item: dict):
    async with RequestClient() as c:
        data = await c.app_ticket(request)
    msg = data.get("msg")
    result = data.get("data")
    if msg == "操作成功":
        response = JSONResponse(status_code=200, content={"status": True, "msg": msg, "code": 200, "data": result})
        return response
    else:
        return JSONResponse(status_code=200, content={"status": False, "msg": msg, "code": 300, "data": result})


@router.post("/project")
async def app_ticket(request: Request, item: dict):
    pid = item.get("id") or ""
    async with RequestClient() as c:
        data = await c.get_project(pid)
    msg = data.get("msg")
    result = data.get("data")
    if msg == "操作成功":
        response = JSONResponse(status_code=200, content={"status": True, "msg": msg, "code": 200, "data": result})
        return response
    else:
        return JSONResponse(status_code=200, content={"status": False, "msg": msg, "code": 300, "data": result})


@router.post("/performs")
@token_required
async def get_performs(request: Request, item: dict):
    pid = item.get("id") or ""
    async with RequestClient() as c:
        data = await c.get_performs(request, pid)
    msg = data.get("msg")
    result = data.get("data")
    if msg == "操作成功":
        response = JSONResponse(status_code=200, content={"status": True, "msg": msg, "code": 200, "data": result})
        return response
    else:
        return JSONResponse(status_code=200, content={"status": False, "msg": msg, "code": 300, "data": result})


@router.post("/member")
@token_required
async def get_member(request: Request, item: dict):
    async with RequestClient() as c:
        data = await c.get_member(request)
    msg = data.get("msg")
    result = data.get("data")
    if msg == "操作成功":
        response = JSONResponse(status_code=200, content={"status": True, "msg": msg, "code": 200, "data": result})
        return response
    else:
        return JSONResponse(status_code=200, content={"status": False, "msg": msg, "code": 300, "data": result})


@router.post("/order/create")
@token_required
async def create_order(request: Request, item: dict):
    async with RequestClient() as c:
        data = await c.order_create(request, item)
    msg = data.get("msg")
    result = data.get("data")
    if msg == "操作成功":
        response = JSONResponse(status_code=200, content={"status": True, "msg": msg, "code": 200, "data": result})
        return response
    else:
        return JSONResponse(status_code=200, content={"status": False, "msg": msg, "code": 300, "data": result})


@router.post("/orders")
@token_required
async def orders(request: Request, item: dict):
    async with RequestClient() as c:
        data = await c.get_orders(request, **item)
    msg = data.get("msg")
    result = data.get("data")
    if msg == "操作成功":
        response = JSONResponse(status_code=200, content={"status": True, "msg": msg, "code": 200, "data": result})
        return response
    else:
        return JSONResponse(status_code=200, content={"status": False, "msg": msg, "code": 300, "data": result})


@router.post("/task")
@token_required
async def task(request: Request, item: dict):
    item.update({"cookie": request.cookies})
    finger = md5(f'{item.get("name")}-{item.get("startDate")}-{item.get("data").get("performId")}')
    item.update({
        "m5": finger
    })
    exists = app.state.mongo.find_query(dbConfig.mongo.fwd_task, {"m5": finger})
    if not exists:
        item.update({
            "spider_status": 0,
            "create_time": get_time()
        })
        item_string = json.dumps(item)
        await app.state.redis.zadd(dbConfig.redis.fwd_task, {item_string: -1})
        app.state.mongo.insert(dbConfig.mongo.fwd_task, item)
        return JSONResponse(status_code=200, content={"status": True, "msg": '成功', "code": 200, "data": []})
    else:
        return JSONResponse(status_code=200, content={"status": True, "msg": '任务已存在', "code": 100, "data": []})


@router.post("/task/find")
@token_required
async def task(request: Request, item: dict):
    page = item.get("page")
    _type = item.get("type")
    page_size = item.get("pageSize")
    find_data = item.get("data") or {}
    if _type != 200:
        find_data.update({"spider_status": _type})
    data = app.state.mongo.find_with_pagination(dbConfig.mongo.fwd_task, find_data, page=page, page_size=page_size)
    return JSONResponse(status_code=200, content={"status": True, "msg": '成功', "code": 200, "data": data})


@router.post("/task/m5/find")
@token_required
async def task_md(request: Request, item: dict):
    m5 = item.get("m5")
    find_data = {"m5": m5}
    data = app.state.mongo.find_query(dbConfig.mongo.fwd_task, find_data, filter={"_id": 0, "cookie": 0})[0]
    return JSONResponse(status_code=200, content={"status": True, "msg": '成功', "code": 200, "data": data})
