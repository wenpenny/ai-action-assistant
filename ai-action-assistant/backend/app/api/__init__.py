from fastapi import APIRouter
from .upload import router as upload_router
from .parse import router as parse_router
from .action import router as action_router
from .history import router as history_router

# 创建主路由器
api_router = APIRouter()

# 注册子路由器
api_router.include_router(upload_router, tags=["upload"])
api_router.include_router(parse_router, tags=["parse"])
api_router.include_router(action_router, tags=["action"])
api_router.include_router(history_router, tags=["history"])

__all__ = ["api_router"]
