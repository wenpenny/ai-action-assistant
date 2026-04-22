from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..core.database import get_db
from ..models import Image, ParseResult, ActionRecord, Todo, Reminder
from ..schemas import HistoryResponse, HistoryDetailResponse, ImageResponse, ParseResultResponse, Entities
from datetime import datetime

router = APIRouter()

@router.get("", response_model=List[HistoryResponse])
async def get_history(db: Session = Depends(get_db)):
    """获取所有历史记录"""
    images = db.query(Image).order_by(Image.created_at.desc()).all()
    
    history = []
    for image in images:
        parse_result = db.query(ParseResult).filter(ParseResult.image_id == image.id).first()
        
        history_item = HistoryResponse(
            image_id=image.id,
            file_name=image.file_name,
            file_path=image.file_path,
            created_at=image.created_at,
            parse_status=image.parse_status.value,
            scene_type=parse_result.scene_type if parse_result else None,
            summary=parse_result.summary if parse_result else None
        )
        history.append(history_item)
    
    return history

@router.get("/{image_id}", response_model=HistoryDetailResponse)
async def get_history_detail(image_id: int, db: Session = Depends(get_db)):
    """获取单条历史详情"""
    # 获取图片信息
    image = db.query(Image).filter(Image.id == image_id).first()
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    
    # 获取解析结果
    parse_result = db.query(ParseResult).filter(ParseResult.image_id == image_id).first()
    
    # 获取动作记录
    action_records = db.query(ActionRecord).filter(ActionRecord.image_id == image_id).order_by(ActionRecord.created_at.desc()).all()
    
    # 构建响应
    image_response = ImageResponse(
        image_id=image.id,
        file_name=image.file_name,
        file_path=image.file_path,
        created_at=image.created_at
    )
    
    parse_response = None
    if parse_result:
        entities = Entities(
            title=parse_result.entities_json.get("title"),
            date=parse_result.entities_json.get("date"),
            start_time=parse_result.entities_json.get("start_time"),
            end_time=parse_result.entities_json.get("end_time"),
            deadline=parse_result.entities_json.get("deadline"),
            location=parse_result.entities_json.get("location"),
            address=parse_result.entities_json.get("address"),
            link=parse_result.entities_json.get("link")
        )
        
        parse_response = ParseResultResponse(
            scene_type=parse_result.scene_type,
            summary=parse_result.summary,
            entities=entities,
            suggested_actions=parse_result.suggested_actions_json
        )
    
    # 构建动作记录列表
    action_records_list = []
    for record in action_records:
        action_records_list.append({
            "id": record.id,
            "action_type": record.action_type,
            "action_payload": record.action_payload_json,
            "execute_status": record.execute_status.value,
            "execute_result": record.execute_result_json,
            "created_at": record.created_at
        })
    
    return HistoryDetailResponse(
        image=image_response,
        parse_result=parse_response,
        action_records=action_records_list
    )