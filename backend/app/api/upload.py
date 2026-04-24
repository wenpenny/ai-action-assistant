import logging
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from pathlib import Path

from ..core.config import UPLOAD_DIR
from ..core.database import get_db
from ..models import Image
from ..schemas import UploadResponse
from ..utils.file_utils import generate_unique_filename, is_valid_image_file, ensure_directory_exists

# 配置日志
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

router = APIRouter()

@router.post("/", response_model=UploadResponse)
async def upload_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """上传图片"""
    try:
        logger.info(f"开始上传文件: {file.filename}")
        logger.info(f"文件类型: {file.content_type}")
        
        # 检查文件类型
        if not is_valid_image_file(file.filename):
            logger.warning(f"无效的文件类型: {file.filename}")
            raise HTTPException(status_code=400, detail="Invalid file type, only images are allowed")
        
        # 确保上传目录存在
        ensure_directory_exists(UPLOAD_DIR)
        logger.info(f"上传目录: {UPLOAD_DIR}")
        
        # 生成唯一文件名
        filename = generate_unique_filename(file.filename)
        file_path = UPLOAD_DIR / filename
        logger.info(f"保存路径: {file_path}")
        
        # 保存文件
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        logger.info(f"文件保存成功，大小: {len(content)} bytes")
        
        # 生成图片 URL
        image_url = f"/uploads/{filename}"
        logger.info(f"生成图片 URL: {image_url}")
        
        # 保存到数据库
        image = Image(
            file_name=filename,
            file_path=str(file_path),
        )
        db.add(image)
        db.commit()
        db.refresh(image)
        logger.info(f"数据库保存成功，图片 ID: {image.id}")
        
        return UploadResponse(
            image_id=image.id,
            image_url=image_url
        )
    except Exception as e:
        logger.error(f"上传失败: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="上传失败")