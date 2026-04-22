from sqlalchemy.orm import Session
from ..models import ActionRecord, Todo, Reminder, ExecuteStatus, TodoStatus, TodoPriority, ReminderStatus
from ..services.calendar_service import CalendarService
from ..services.map_service import MapService
import json
from datetime import datetime

class ActionService:
    def __init__(self):
        self.calendar_service = CalendarService()
        self.map_service = MapService()
    
    def execute_action(self, db: Session, image_id: int, action_type: str, payload: dict) -> dict:
        """执行动作"""
        # 创建动作记录
        action_record = ActionRecord(
            image_id=image_id,
            action_type=action_type,
            action_payload_json=payload,
            execute_status=ExecuteStatus.PENDING
        )
        db.add(action_record)
        db.commit()
        
        try:
            result = {}
            
            if action_type == "create_todo":
                result = self._create_todo(db, image_id, payload)
            elif action_type == "set_reminder":
                result = self._set_reminder(db, image_id, payload)
            elif action_type == "open_map":
                result = self._open_map(payload)
            elif action_type == "export_calendar":
                result = self._export_calendar(payload)
            else:
                raise ValueError(f"Unknown action type: {action_type}")
            
            # 更新动作记录为成功
            action_record.execute_status = ExecuteStatus.COMPLETED
            action_record.execute_result_json = result
            db.commit()
            
            return {
                "success": True,
                "message": self._get_success_message(action_type),
                "data": result
            }
        except Exception as e:
            # 更新动作记录为失败
            action_record.execute_status = ExecuteStatus.FAILED
            action_record.execute_result_json = {"error": str(e)}
            db.commit()
            
            return {
                "success": False,
                "message": f"执行失败: {str(e)}",
                "data": {}
            }
    
    def _create_todo(self, db: Session, image_id: int, payload: dict) -> dict:
        """创建待办事项"""
        todo = Todo(
            title=payload.get("title"),
            deadline=payload.get("deadline"),
            priority=TodoPriority.MEDIUM,
            source_image_id=image_id,
            status=TodoStatus.PENDING
        )
        db.add(todo)
        db.commit()
        db.refresh(todo)
        
        return {
            "todo_id": todo.id,
            "title": todo.title,
            "deadline": todo.deadline,
            "status": todo.status.value
        }
    
    def _set_reminder(self, db: Session, image_id: int, payload: dict) -> dict:
        """设置提醒"""
        reminder = Reminder(
            title=payload.get("title"),
            remind_at=payload.get("remind_at"),
            source_image_id=image_id,
            status=ReminderStatus.PENDING
        )
        db.add(reminder)
        db.commit()
        db.refresh(reminder)
        
        return {
            "reminder_id": reminder.id,
            "title": reminder.title,
            "remind_at": reminder.remind_at,
            "status": reminder.status.value
        }
    
    def _open_map(self, payload: dict) -> dict:
        """打开地图"""
        location = payload.get("location") or payload.get("address")
        if not location:
            raise ValueError("Location or address is required")
        
        map_url = self.map_service.generate_map_url(location)
        
        return {
            "map_url": map_url
        }
    
    def _export_calendar(self, payload: dict) -> dict:
        """导出日历"""
        ics_path = self.calendar_service.generate_ics(payload)
        
        return {
            "ics_path": ics_path
        }
    
    def _get_success_message(self, action_type: str) -> str:
        """获取成功消息"""
        messages = {
            "create_todo": "待办已创建",
            "set_reminder": "提醒已设置",
            "open_map": "地图已打开",
            "export_calendar": "日历已导出"
        }
        return messages.get(action_type, "动作执行成功")