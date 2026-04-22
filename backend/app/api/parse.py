from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any

from ..core.database import get_db
from ..schemas import ParseResultUpdate
from ..services.parse_service import ParseService

router = APIRouter()
parse_service = ParseService()

@router.post("/parse/{image_id}")
async def parse_image(
    image_id: int,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """解析图片"""
    try:
        result = parse_service.parse_image(image_id, db)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.put("/parse/{image_id}")
async def update_parse_result(
    image_id: int,
    update_data: ParseResultUpdate,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """更新解析结果"""
    try:
        # 将 Pydantic 模型转换为字典
        update_dict = update_data.dict(exclude_unset=True)
        # 处理 entities 字段
        if "entities" in update_dict:
            update_dict["entities"] = update_dict["entities"].dict()
        result = parse_service.update_parse_result(image_id, update_dict, db)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
