
from fastapi import Request
from fastapi.responses import JSONResponse

async def unhandled_exception_handler(request: Request, exc: Exception):
    # 生产建议：记录到日志/监控
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"},
    )
