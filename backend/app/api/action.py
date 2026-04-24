from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any
from ..core.database import get_db
from ..services.action_service import ActionService

router = APIRouter()
action_service = ActionService()

@router.post("/execute")
async def execute_action(
    action_data: Dict[str, Any],
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """执行动作"""
    try:
        action_type = action_data.get("action_type")
        payload = action_data.get("payload", {})
        item_id = action_data.get("item_id", "")
        
        if not action_type:
            return {
                "success": False,
                "message": "Action type is required",
                "data": None
            }
        
        result = action_service.execute_action(action_type, payload, item_id, db)
        
        if result.get("success"):
            return {
                "success": True,
                "message": "Action executed successfully",
                "data": result
            }
        else:
            return {
                "success": False,
                "message": result.get("error", "Failed to execute action"),
                "data": None
            }
    except Exception as e:
        return {
            "success": False,
            "message": f"Internal server error: {str(e)}",
            "data": None
        }

@router.post("/execute-item")
async def execute_item_action(
    action_data: Dict[str, Any],
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """执行事项级动作"""
    try:
        action_type = action_data.get("action_type")
        payload = action_data.get("payload", {})
        item_id = action_data.get("item_id")
        
        if not action_type:
            return {
                "success": False,
                "message": "Action type is required",
                "data": None
            }
        
        if not item_id:
            return {
                "success": False,
                "message": "Item ID is required",
                "data": None
            }
        
        result = action_service.execute_action(action_type, payload, item_id, db)
        
        if result.get("success"):
            return {
                "success": True,
                "message": "Action executed successfully",
                "data": result
            }
        else:
            return {
                "success": False,
                "message": result.get("error", "Failed to execute action"),
                "data": None
            }
    except Exception as e:
        return {
            "success": False,
            "message": f"Internal server error: {str(e)}",
            "data": None
        }