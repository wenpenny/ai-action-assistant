from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from pathlib import Path

from ..core.config import UPLOAD_DIR
from ..core.database import get_db
from ..models import Image
from ..schemas import UploadResponse
from ..utils.file_utils import generate_unique_filename, is_valid_image_file, ensure_directory_exists

router = APIRouter()

@router.post("/upload", response_model=UploadResponse)
async def upload_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """上传图片"""
    # 检查文件类型
    if not is_valid_image_file(file.filename):
        raise HTTPException(status_code=400, detail="Invalid file type, only images are allowed")
    
    # 确保上传目录存在
    ensure_directory_exists(UPLOAD_DIR)
    
    # 生成唯一文件名
    filename = generate_unique_filename(file.filename)
    file_path = UPLOAD_DIR / filename
    
    # 保存文件
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    
    # 生成图片 URL
    image_url = f"/uploads/{filename}"
    
    # 保存到数据库
    image = Image(
        file_name=filename,
        file_path=str(file_path),
    )
    db.add(image)
    db.commit()
    db.refresh(image)
    
    return UploadResponse(
        image_id=image.id,
        image_url=image_url
    )
