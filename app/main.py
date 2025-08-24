
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .db import init_db
from .middleware.errors import unhandled_exception_handler
from .routers import auth, protected, billing

def create_app() -> FastAPI:
    app = FastAPI(title="SaaS/API Starter", version="0.1.0")

    # CORS （生产请按需限制域名）
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 路由
    app.include_router(auth.router)
    app.include_router(protected.router)
    app.include_router(billing.router)

    # 健康检查
    @app.get("/health")
    def health():
        return {"status": "ok"}

    # 全局异常处理
    app.add_exception_handler(Exception, unhandled_exception_handler)

    return app

app = create_app()

# 首次启动建表
init_db()
