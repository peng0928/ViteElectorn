import functools
from flask import Request
from fastapi.responses import JSONResponse


def token_required(func):
    @functools.wraps(func)
    async def wrapper(request: Request, *args, **kwargs):
        cookie = request.cookies or {}
        token = cookie.get("t") or ""
        if not token:
            return JSONResponse(
                status_code=200,
                content={"status": False, "msg": "登录超时", "code": 300}
            )
        return await func(request, *args, **kwargs)

    return wrapper
