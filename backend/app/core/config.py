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
OCR_SERVICE_TYPE = "http"  # http
OCR_API_URL = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"
OCR_API_KEY = "TbdhuEoaBc4WJbdvz9dndRBJ"
OCR_SECRET_KEY = "ohrNnBPGJu5Cw5Iv0lk9YiwsrcN4QkRD"

# LLM 服务配置
LLM_SERVICE_TYPE = "deepseek"  # bluelm, deepseek, mock

# BlueLM 配置
BLUELM_API_URL = "https://api.vivo.com.cn/v1/chat/completions"
BLUELM_API_KEY = "your-bluelm-api-key"
BLUELM_MODEL = "BlueLM-7B-Chat"

# DeepSeek 配置
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
DEEPSEEK_API_KEY = "sk-eb8582d84cb84457b796c1ac92dc2026"
DEEPSEEK_MODEL = "deepseek-chat"

# 应用配置
APP_NAME = "AI Action Assistant"
APP_VERSION = "1.0.0"
DEBUG = True