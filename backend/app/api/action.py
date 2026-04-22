from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..schemas import ActionRequest, ActionResponse
from ..services.action_service import ActionService

router = APIRouter()
action_service = ActionService()

@router.post("/execute", response_model=ActionResponse)
async def execute_action(
    action_request: ActionRequest,
    db: Session = Depends(get_db)
) -> ActionResponse:
    """执行动作"""
    try:
        result = action_service.execute_action(
            image_id=action_request.image_id,
            action_type=action_request.action_type,
            payload=action_request.payload,
            db=db
        )
        
        # 根据动作类型生成响应消息
        messages = {
            "create_todo": "待办已创建",
            "set_reminder": "提醒已设置",
            "open_map": "地图链接已生成",
            "export_calendar": "日历已导出"
        }
        
        message = messages.get(action_request.action_type, "动作已执行")
        
        return ActionResponse(
            success=True,
            message=message,
            data=result
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")