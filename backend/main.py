from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import router
from models import init_db

# 创建 FastAPI 应用
app = FastAPI(
    title="AI Action Assistant API",
    description="基于截图与系统上下文理解的 AI 行动助手 API",
    version="1.0.0"
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置具体的前端域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(router, prefix="/api")

# 初始化数据库
init_db()

# 根路径
@app.get("/")
async def root():
    return {"message": "AI Action Assistant API is running"}

# 健康检查
@app.get("/health")
async def health_check():
    return {"status": "healthy"}
