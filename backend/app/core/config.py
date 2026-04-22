import os
from pathlib import Path

# 项目根目录
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# 上传文件目录
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

# 数据库配置
DATABASE_URL = "sqlite:///" + str(BASE_DIR / "db.sqlite3")

# OCR 服务配置
OCR_SERVICE_TYPE = "mock"  # mock, http
OCR_API_URL = "https://api.example.com/ocr"
OCR_API_KEY = "your-api-key"

# LLM 服务配置
LLM_SERVICE_TYPE = "mock"  # mock, http
LLM_API_URL = "https://api.example.com/llm"
LLM_API_KEY = "your-api-key"

# 应用配置
APP_NAME = "AI Action Assistant"
APP_VERSION = "1.0.0"
DEBUG = True
