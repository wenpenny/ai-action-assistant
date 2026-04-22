import os
import uuid
from pathlib import Path
from typing import Optional

# 允许的图片文件类型
ALLOWED_IMAGE_TYPES = {
    ".jpg", ".jpeg", ".png", ".gif", ".webp"
}

def generate_unique_filename(original_filename: str) -> str:
    """生成唯一的文件名"""
    ext = Path(original_filename).suffix.lower()
    unique_id = str(uuid.uuid4())
    return f"{unique_id}{ext}"

def is_valid_image_file(filename: str) -> bool:
    """检查文件是否为有效的图片文件"""
    ext = Path(filename).suffix.lower()
    return ext in ALLOWED_IMAGE_TYPES

def ensure_directory_exists(directory: Path) -> None:
    """确保目录存在，如果不存在则创建"""
    directory.mkdir(parents=True, exist_ok=True)
