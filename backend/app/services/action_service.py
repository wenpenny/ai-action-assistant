import json
from typing import Dict, Any
from sqlalchemy.orm import Session
from datetime import datetime
from ..models import ActionRecord, Todo, Reminder, ExecuteStatus, TodoStatus, TodoPriority, ReminderStatus
from .map_service import MapService
from .calendar_service import CalendarService

class ActionService:
    def __init__(self):
        self.map_service = MapService()
        self.calendar_service = CalendarService()
    
    def execute_action(self, image_id: int, action_type: str, payload: Dict[str, Any], db: Session) -> Dict[str, Any]:
        """执行动作"""
        # 验证动作类型
        valid_action_types = ["create_todo", "set_reminder", "open_map", "export_calendar"]
        if action_type not in valid_action_types:
            raise ValueError(f"Invalid action type: {action_type}")
        
        # 创建动作记录
        action_record = ActionRecord(
            image_id=image_id,
            action_type=action_type,
            action_payload_json=json.dumps(payload),
            execute_status=ExecuteStatus.PENDING
        )
        db.add(action_record)
        
        try:
            # 执行动作
            if action_type == "create_todo":
                result = self._create_todo(image_id, payload, db)
            elif action_type == "set_reminder":
                result = self._set_reminder(image_id, payload, db)
            elif action_type == "open_map":
                result = self._open_map(payload)
            elif action_type == "export_calendar":
                result = self._export_calendar(payload)
            else:
                result = {}
            
            # 更新动作记录状态为成功
            action_record.execute_status = ExecuteStatus.SUCCESS
            action_record.execute_result_json = json.dumps(result)
            db.commit()
            
            return result
        except Exception as e:
            # 更新动作记录状态为失败
            action_record.execute_status = ExecuteStatus.FAILED
            action_record.execute_result_json = json.dumps({"error": str(e)})
            db.commit()
            # 重新抛出异常，让调用者知道执行失败
            raise
    
    def _create_todo(self, image_id: int, payload: Dict[str, Any], db: Session) -> Dict[str, Any]:
        """创建待办事项"""
        title = payload.get("title", "")
        if not title:
            raise ValueError("Todo title is required")
        
        # 解析截止日期
        deadline_str = payload.get("deadline")
        deadline = None
        if deadline_str:
            try:
                deadline = datetime.strptime(deadline_str, "%Y-%m-%d %H:%M")
            except ValueError:
                pass
        
        # 解析优先级
        priority_str = payload.get("priority", "medium")
        priority = TodoPriority.MEDIUM
        if priority_str in ["low", "medium", "high"]:
            priority = TodoPriority(priority_str)
        
        # 创建待办事项
        todo = Todo(
            title=title,
            deadline=deadline,
            priority=priority,
            source_image_id=image_id,
            status=TodoStatus.PENDING
        )
        db.add(todo)
        db.commit()
        db.refresh(todo)
        
        return {"todo_id": todo.id}
    
    def _set_reminder(self, image_id: int, payload: Dict[str, Any], db: Session) -> Dict[str, Any]:
        """设置提醒"""
        title = payload.get("title", "")
        remind_at_str = payload.get("remind_at")
        
        if not title or not remind_at_str:
            raise ValueError("Reminder title and time are required")
        
        # 解析提醒时间
        try:
            remind_at = datetime.strptime(remind_at_str, "%Y-%m-%d %H:%M")
        except ValueError:
            raise ValueError("Invalid reminder time format, use YYYY-MM-DD HH:MM")
        
        # 创建提醒
        reminder = Reminder(
            title=title,
            remind_at=remind_at,
            source_image_id=image_id,
            status=ReminderStatus.PENDING
        )
        db.add(reminder)
        db.commit()
        db.refresh(reminder)
        
        return {"reminder_id": reminder.id}
    
    def _open_map(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """打开地图"""
        address = payload.get("address")
        location = payload.get("location")
        
        map_url = self.map_service.get_map_url(address, location)
        return {"map_url": map_url}
    
    def _export_calendar(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """导出日历"""
        title = payload.get("title", "")
        start_time = payload.get("start_time")
        
        if not title or not start_time:
            raise ValueError("Event title and start time are required")
        
        calendar_url = self.calendar_service.generate_ics_file(
            title=title,
            start_time=start_time,
            end_time=payload.get("end_time"),
            location=payload.get("location"),
            description=payload.get("description")
        )
        
        return {"calendar_url": calendar_url}
