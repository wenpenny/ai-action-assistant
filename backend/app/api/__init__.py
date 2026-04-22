from fastapi import APIRouter
from .upload import router as upload_router
from .parse import router as parse_router
from .action import router as action_router
from .history import router as history_router

api_router = APIRouter()

api_router.include_router(upload_router, prefix="/upload", tags=["upload"])
api_router.include_router(parse_router, prefix="/parse", tags=["parse"])
api_router.include_router(action_router, prefix="/action", tags=["action"])
api_router.include_router(history_router, prefix="/history", tags=["history"])