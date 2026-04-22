from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from ..core.database import get_db
from ..models import Image, ParseResult, ActionRecord
from ..schemas import ImageResponse, ParseResultResponse, Entities
from ..utils.json_utils import safe_json_deserialize

router = APIRouter()

@router.get("/history")
async def get_history(
    db: Session = Depends(get_db)
) -> List[Dict[str, Any]]:
    """获取所有历史记录"""
    # 获取所有图片
    images = db.query(Image).all()
    result = []
    
    for image in images:
        # 构建图片响应
        image_response = {
            "id": image.id,
            "file_name": image.file_name,
            "file_path": image.file_path,
            "created_at": image.created_at,
            "parse_status": image.parse_status.value if image.parse_status else None
        }
        
        # 获取解析结果
        parse_result = db.query(ParseResult).filter(ParseResult.image_id == image.id).first()
        parse_result_response = None
        if parse_result:
            # 解析 entities_json 和 suggested_actions_json
            entities_dict = safe_json_deserialize(parse_result.entities_json)
            suggested_actions = safe_json_deserialize(parse_result.suggested_actions_json)
            
            parse_result_response = {
                "id": parse_result.id,
                "image_id": parse_result.image_id,
                "scene_type": parse_result.scene_type,
                "summary": parse_result.summary,
                "entities": entities_dict,
                "suggested_actions": suggested_actions,
                "created_at": parse_result.created_at,
                "updated_at": parse_result.updated_at
            }
        
        # 获取动作记录
        action_records = db.query(ActionRecord).filter(ActionRecord.image_id == image.id).all()
        action_records_list = []
        for action in action_records:
            action_records_list.append({
                "id": action.id,
                "action_type": action.action_type,
                "action_payload": safe_json_deserialize(action.action_payload_json),
                "execute_status": action.execute_status.value if action.execute_status else None,
                "execute_result": safe_json_deserialize(action.execute_result_json),
                "created_at": action.created_at
            })
        
        # 构建历史记录项
        history_item = {
            "image": image_response,
            "parse_result": parse_result_response,
            "action_records": action_records_list
        }
        
        result.append(history_item)
    
    return result

@router.get("/history/{image_id}")
async def get_history_by_image_id(
    image_id: int,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """获取指定图片的历史记录"""
    # 查找图片
    image = db.query(Image).filter(Image.id == image_id).first()
    if not image:
        raise HTTPException(status_code=404, detail=f"Image with id {image_id} not found")
    
    # 构建图片响应
    image_response = {
        "id": image.id,
        "file_name": image.file_name,
        "file_path": image.file_path,
        "created_at": image.created_at,
        "parse_status": image.parse_status.value if image.parse_status else None
    }
    
    # 获取解析结果
    parse_result = db.query(ParseResult).filter(ParseResult.image_id == image_id).first()
    parse_result_response = None
    if parse_result:
        # 解析 entities_json 和 suggested_actions_json
        entities_dict = safe_json_deserialize(parse_result.entities_json)
        suggested_actions = safe_json_deserialize(parse_result.suggested_actions_json)
        
        parse_result_response = {
            "id": parse_result.id,
            "image_id": parse_result.image_id,
            "scene_type": parse_result.scene_type,
            "summary": parse_result.summary,
            "entities": entities_dict,
            "suggested_actions": suggested_actions,
            "created_at": parse_result.created_at,
            "updated_at": parse_result.updated_at
        }
    
    # 获取动作记录
    action_records = db.query(ActionRecord).filter(ActionRecord.image_id == image_id).all()
    action_records_list = []
    for action in action_records:
        action_records_list.append({
            "id": action.id,
            "action_type": action.action_type,
            "action_payload": safe_json_deserialize(action.action_payload_json),
            "execute_status": action.execute_status.value if action.execute_status else None,
            "execute_result": safe_json_deserialize(action.execute_result_json),
            "created_at": action.created_at
        })
    
    # 构建历史记录响应
    history_response = {
        "image": image_response,
        "parse_result": parse_result_response,
        "action_records": action_records_list
    }
    
    return history_response
