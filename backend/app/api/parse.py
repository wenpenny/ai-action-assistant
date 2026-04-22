from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any
import json

from ..core.database import get_db
from ..schemas import ParseResultUpdate
from ..services.parse_service import ParseService
from ..models import ParseResult

router = APIRouter()
parse_service = ParseService()

@router.post("/{image_id}")
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

@router.get("/{image_id}")
async def get_parse_result(
    image_id: int,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """获取解析结果"""
    try:
        # 查找解析结果
        parse_result = db.query(ParseResult).filter(ParseResult.image_id == image_id).first()
        if not parse_result:
            raise ValueError(f"Parse result for image {image_id} not found")
        
        # 构建返回结果
        return {
            "scene_type": parse_result.scene_type,
            "summary": parse_result.summary,
            "entities": json.loads(parse_result.entities_json),
            "suggested_actions": json.loads(parse_result.suggested_actions_json)
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.put("/{image_id}")
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