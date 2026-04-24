import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from ..core.database import get_db
from ..models import Image, ParseResult, ParseItem, ActionRecord
from ..schemas import HistoryResponse, HistoryDetailResponse, HistoryItem

router = APIRouter()

@router.get("")
async def get_history(
    db: Session = Depends(get_db)
) -> List[Dict[str, Any]]:
    """获取历史记录"""
    try:
        # 查询所有图片记录
        images = db.query(Image).order_by(Image.created_at.desc()).all()
        
        history = []
        for image in images:
            # 查询对应的解析结果
            parse_result = db.query(ParseResult).filter(ParseResult.image_id == image.id).first()
            
            if parse_result:
                # 查询解析出的事项数量
                items = db.query(ParseItem).filter(ParseItem.parse_result_id == parse_result.id).all()
                item_count = len(items)
                
                # 收集所有事项的 item_id
                item_ids = [item.item_id for item in items]
                
                # 查询执行的动作数量
                action_count = 0
                if item_ids:
                    action_count = db.query(ActionRecord).filter(ActionRecord.item_id.in_(item_ids)).count()
                
                history.append({
                    "image_id": image.id,
                    "file_name": image.file_name,
                    "created_at": image.created_at,
                    "parse_status": image.parse_status.value,
                    "item_count": item_count,
                    "action_count": action_count
                })
        
        return history
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/{image_id}")
async def get_history_detail(
    image_id: int,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """获取历史详情"""
    try:
        # 查询图片记录
        image = db.query(Image).filter(Image.id == image_id).first()
        if not image:
            raise ValueError(f"Image with id {image_id} not found")
        
        # 查询对应的解析结果
        parse_result = db.query(ParseResult).filter(ParseResult.image_id == image_id).first()
        
        if not parse_result:
            return {
                "image_id": image.id,
                "file_name": image.file_name,
                "created_at": image.created_at,
                "parse_status": image.parse_status.value,
                "ocr_text": "",
                "items": []
            }
        
        # 查询所有事项
        parse_items = db.query(ParseItem).filter(ParseItem.parse_result_id == parse_result.id).all()
        
        # 构建事项列表
        items = []
        for item in parse_items:
            # 查询该事项的动作记录
            actions = db.query(ActionRecord).filter(ActionRecord.item_id == item.item_id).all()
            
            # 构建动作记录列表
            action_records = []
            for action in actions:
                action_records.append({
                    "action_id": action.id,
                    "action_type": action.action_type,
                    "status": action.status.value,
                    "created_at": action.created_at
                })
            
            # 解析 JSON 字段
            try:
                entities = json.loads(item.entities_json) if item.entities_json else {}
                suggested_actions = json.loads(item.suggested_actions_json) if item.suggested_actions_json else []
                action_plan = json.loads(item.action_plan_json) if item.action_plan_json else []
            except json.JSONDecodeError:
                entities = {}
                suggested_actions = []
                action_plan = []
            
            items.append({
                "item_id": item.item_id,
                "scene_type": item.scene_type,
                "summary": item.summary,
                "entities": entities,
                "suggested_actions": suggested_actions,
                "action_plan": action_plan,
                "actions": action_records
            })
        
        # 尝试获取 ocr_text，如果不存在则使用空字符串
        ocr_text = getattr(parse_result, 'ocr_text', '')
        
        return {
            "image_id": image.id,
            "file_name": image.file_name,
            "created_at": image.created_at,
            "parse_status": image.parse_status.value,
            "ocr_text": ocr_text,
            "items": items
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")