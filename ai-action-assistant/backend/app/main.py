from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from .api import api_router
from .core.config import APP_NAME, APP_VERSION, DEBUG, UPLOAD_DIR
from .core.database import engine, Base

# 导入所有模型，确保它们被注册
from .models import Image, ParseResult, Todo, Reminder, ActionRecord

# 创建数据库表
Base.metadata.create_all(bind=engine)

# 创建 FastAPI 应用
app = FastAPI(
    title=APP_NAME,
    description="基于截图与系统上下文理解的 AI 行动助手 API",
    version=APP_VERSION,
    debug=DEBUG
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置具体的前端域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载静态文件目录
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# 注册路由
app.include_router(api_router, prefix="/api")

# 根路径
@app.get("/")
async def root():
    return {"message": f"{APP_NAME} API is running"}

# 健康检查
@app.get("/health")
async def health_check():
    return {"status": "healthy"}
