from typing import Dict, Any, List
from sqlalchemy.orm import Session
from ..models import ActionRecord, ExecuteStatus, Todo, TodoStatus, TodoPriority, Reminder, ReminderStatus

class ActionService:
    def execute_action(self, action_type: str, payload: Dict[str, Any], item_id: str, db: Session) -> Dict[str, Any]:
        """执行动作并返回结果"""
        try:
            # 记录动作执行
            action_record = ActionRecord(
                action_type=action_type,
                payload=str(payload),
                item_id=item_id,
                status=ExecuteStatus.PENDING
            )
            db.add(action_record)
            db.flush()  # 获取 action_record.id
            
            # 根据动作类型执行不同的操作
            if action_type == "create_todo":
                result = self._create_todo(payload, db)
            elif action_type == "set_reminder":
                result = self._set_reminder(payload, db)
            elif action_type == "open_map":
                result = self._open_map(payload)
            elif action_type == "export_calendar":
                result = self._export_calendar(payload)
            else:
                raise ValueError(f"Invalid action type: {action_type}")
            
            # 更新动作执行状态
            action_record.status = ExecuteStatus.COMPLETED
            action_record.result = str(result)
            
            db.commit()
            
            return {
                "success": True,
                "result": result,
                "action_id": action_record.id
            }
        except Exception as e:
            # 更新动作执行状态为失败
            if 'action_record' in locals():
                action_record.status = ExecuteStatus.FAILED
                action_record.result = str(e)
                db.commit()
            
            return {
                "success": False,
                "error": str(e)
            }
    
    def _create_todo(self, payload: Dict[str, Any], db: Session) -> Dict[str, Any]:
        """创建待办事项"""
        # 创建待办事项
        todo = Todo(
            title=payload.get("title", "未命名任务"),
            description=payload.get("description", ""),
            deadline=payload.get("deadline"),
            status=TodoStatus.PENDING,
            priority=TodoPriority.MEDIUM
        )
        db.add(todo)
        db.commit()
        db.refresh(todo)
        
        return {
            "todo_id": todo.id,
            "title": todo.title,
            "status": todo.status.value
        }
    
    def _set_reminder(self, payload: Dict[str, Any], db: Session) -> Dict[str, Any]:
        """设置提醒"""
        # 创建提醒
        reminder = Reminder(
            title=payload.get("title", "未命名提醒"),
            remind_at=payload.get("remind_at"),
            status=ReminderStatus.PENDING
        )
        db.add(reminder)
        db.commit()
        db.refresh(reminder)
        
        return {
            "reminder_id": reminder.id,
            "title": reminder.title,
            "remind_at": reminder.remind_at
        }
    
    def _open_map(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """打开地图"""
        # 这里只是返回地图链接，实际打开地图的操作需要在前端执行
        from .map_service import MapService
        
        map_service = MapService()
        map_url = map_service.generate_map_url(payload)
        
        return {
            "map_url": map_url,
            "location": payload.get("location"),
            "address": payload.get("address")
        }
    
    def _export_calendar(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """导出日历"""
        # 生成 .ics 文件
        from .calendar_service import CalendarService
        
        calendar_service = CalendarService()
        ics_file_path = calendar_service.generate_ics(payload)
        
        # 构建日历事件数据
        calendar_event = {
            "title": payload.get("title", "未命名事件"),
            "date": payload.get("date"),
            "start_time": payload.get("start_time"),
            "end_time": payload.get("end_time"),
            "location": payload.get("location"),
            "ics_file_path": ics_file_path
        }
        
        return {
            "calendar_event": calendar_event
        }
    
    def build_action_plan(self, item: Dict[str, Any]) -> List[Dict[str, Any]]:
        """为事项生成 action plan"""
        action_plan = []
        entities = item.get("entities", {})
        
        # 根据 suggested_actions 生成 action plan
        for action in item.get("suggested_actions", []):
            if action == "create_todo":
                # 生成创建待办事项的 action plan
                title = entities.get("title", entities.get("task_name", "未命名任务"))
                deadline = entities.get("deadline")
                
                action_plan.append({
                    "action_type": "create_todo",
                    "label": "创建待办",
                    "payload": {
                        "title": title,
                        "deadline": deadline
                    }
                })
            
            elif action == "set_reminder":
                # 生成设置提醒的 action plan
                title = entities.get("title", entities.get("task_name", "未命名任务"))
                
                # 优先使用 deadline，然后使用 date + start_time
                remind_at = entities.get("deadline")
                if not remind_at and entities.get("date") and entities.get("start_time"):
                    remind_at = f"{entities['date']} {entities['start_time']}"
                
                action_plan.append({
                    "action_type": "set_reminder",
                    "label": "设置提醒",
                    "payload": {
                        "title": title,
                        "remind_at": remind_at
                    }
                })
            
            elif action == "open_map":
                # 生成打开地图的 action plan
                location = entities.get("location")
                address = entities.get("address")
                
                action_plan.append({
                    "action_type": "open_map",
                    "label": "打开地图",
                    "payload": {
                        "location": location,
                        "address": address
                    }
                })
            
            elif action == "export_calendar":
                # 生成导出日历的 action plan
                title = entities.get("title", "未命名事件")
                date = entities.get("date")
                start_time = entities.get("start_time")
                end_time = entities.get("end_time")
                location = entities.get("location")
                
                action_plan.append({
                    "action_type": "export_calendar",
                    "label": "导出日历",
                    "payload": {
                        "title": title,
                        "date": date,
                        "start_time": start_time,
                        "end_time": end_time,
                        "location": location
                    }
                })
        
        return action_plan

def get_action_service() -> ActionService:
    """获取动作服务实例"""
    return ActionService()