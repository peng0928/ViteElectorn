from datetime import datetime, timezone, timedelta

from fastapi.responses import ORJSONResponse, JSONResponse
from fastapi.routing import APIRouter
from fastapi import *
from fastapi.responses import HTMLResponse

from utils.request.api import RequestClient
from utils.wapper.index import token_required

router = APIRouter(
    prefix="/api",
    tags=["user"],
    default_response_class=ORJSONResponse
)

@router.post("/user/info")
@token_required
async def app_info(request: Request):
    async with RequestClient() as c:
        data = await c.app_info(request)
    msg = data.get("msg")
    result = data.get("data")
    if msg == "操作成功":
        response = JSONResponse(status_code=200, content={"status": True, "msg": msg, "code": 200, "data": result})
        return response
    else:
        return JSONResponse(status_code=200, content={"status": False, "msg": msg, "code": 300, "data": None})
