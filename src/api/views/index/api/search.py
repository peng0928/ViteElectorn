from datetime import datetime, timezone, timedelta

from fastapi.responses import ORJSONResponse, JSONResponse
from fastapi.routing import APIRouter
from fastapi import *
from fastapi.responses import HTMLResponse

from utils.request.login import RequestClient

client = RequestClient()
router = APIRouter(
    prefix="/api",
    tags=["登录"],
    default_response_class=ORJSONResponse
)


@router.post("/search")
async def search(item: dict, request: Request):
    search_text = item.get("text") or ""
    async with client as c:
        data = await c.search(text=search_text)
    msg = data.get("msg")
    result = data.get("data")
    if msg == "操作成功":
        response = JSONResponse(status_code=200, content={"status": True, "msg": msg, "code": 200, "data": result})
        return response
    else:
        return JSONResponse(status_code=200, content={"status": False, "msg": msg, "code": 300, "data": result})
