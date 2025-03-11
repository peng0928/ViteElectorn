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
