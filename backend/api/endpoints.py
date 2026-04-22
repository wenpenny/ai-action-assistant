import json
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from pathlib import Path
from typing import List

from ..models import get_db, History, Action
from ..models.schemas import HistoryResponse, ActionResponse, StructuredData
from ..services.ocr import get_ocr_service
from ..services.llm import get_llm_service
from ..config import UPLOAD_DIR

router = APIRouter()

@router.post("/upload", response_model=StructuredData)
async def upload_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """上传图片并处理"""
    # 保存上传的文件
    file_extension = Path(file.filename).suffix
    file_path = UPLOAD_DIR / f"{file.filename}"
    
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    
    # 调用 OCR 服务提取文本
    ocr_service = get_ocr_service()
    ocr_text = ocr_service.extract_text(file_path)
    
    # 调用 LLM 服务分析文本
    llm_service = get_llm_service()
    structured_data = llm_service.analyze_text(ocr_text)
    
    # 保存到数据库
    history = History(
        image_path=str(file_path),
        ocr_text=ocr_text,
        scene_type=structured_data.get("scene_type", "unknown"),
        structured_data=json.dumps(structured_data)
    )
    db.add(history)
    db.commit()
    db.refresh(history)
    
    return structured_data

@router.post("/action")
async def execute_action(
    history_id: int,
    action_type: str,
    action_data: dict,
    db: Session = Depends(get_db)
):
    """执行动作"""
    # 验证历史记录是否存在
    history = db.query(History).filter(History.id == history_id).first()
    if not history:
        raise HTTPException(status_code=404, detail="History not found")
    
    # 验证动作类型是否有效
    valid_action_types = ["create_todo", "set_reminder", "open_map", "export_calendar"]
    if action_type not in valid_action_types:
        raise HTTPException(status_code=400, detail="Invalid action type")
    
    # 保存动作记录
    action = Action(
        history_id=history_id,
        action_type=action_type,
        action_data=json.dumps(action_data),
        executed=1  # 标记为已执行
    )
    db.add(action)
    db.commit()
    
    # 这里可以添加具体的动作执行逻辑
    # 例如，创建待办事项、设置提醒、打开地图或导出日历
    
    return {"message": f"Action {action_type} executed successfully"}

@router.get("/history", response_model=List[HistoryResponse])
async def get_history(db: Session = Depends(get_db)):
    """获取历史记录"""
    histories = db.query(History).all()
    result = []
    for history in histories:
        # 解析结构化数据 JSON 字符串
        structured_data = json.loads(history.structured_data)
        result.append(HistoryResponse(
            id=history.id,
            image_path=history.image_path,
            ocr_text=history.ocr_text,
            scene_type=history.scene_type,
            structured_data=structured_data,
            created_at=history.created_at
        ))
    return result

@router.get("/actions", response_model=List[ActionResponse])
async def get_actions(db: Session = Depends(get_db)):
    """获取动作记录"""
    actions = db.query(Action).all()
    result = []
    for action in actions:
        # 解析动作数据 JSON 字符串
        action_data = json.loads(action.action_data)
        result.append(ActionResponse(
            id=action.id,
            history_id=action.history_id,
            action_type=action.action_type,
            action_data=action_data,
            executed=action.executed,
            created_at=action.created_at
        ))
    return result
