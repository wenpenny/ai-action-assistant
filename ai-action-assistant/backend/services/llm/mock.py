from typing import Dict, Any
from .base import LLMService

class MockLLMService(LLMService):
    def analyze_text(self, text: str) -> Dict[str, Any]:
        """模拟分析文本并返回结构化数据"""
        text_lower = text.lower()
        
        # 检测场景类型
        if any(keyword in text_lower for keyword in ["会议", "面试", "课程", "活动", "时间"]):
            return {
                "scene_type": "schedule",
                "data": {
                    "title": "产品会议",
                    "date": "2026-04-25",
                    "time": "14:00-16:00",
                    "location": "A101会议室",
                    "participants": ["产品团队"]
                },
                "suggested_actions": ["create_todo", "set_reminder", "export_calendar"]
            }
        elif any(keyword in text_lower for keyword in ["作业", "通知", "提交", "截止"]):
            return {
                "scene_type": "task",
                "data": {
                    "title": "完成项目报告",
                    "deadline": "2026-04-30",
                    "description": "完成项目报告",
                    "submission_method": "邮箱"
                },
                "suggested_actions": ["create_todo", "set_reminder"]
            }
        elif any(keyword in text_lower for keyword in ["航班", "酒店", "车票", "地址"]):
            return {
                "scene_type": "travel",
                "data": {
                    "type": "flight",
                    "flight_number": "CA1234",
                    "departure_time": "2026-05-01 08:30",
                    "departure_city": "北京",
                    "arrival_city": "上海",
                    "hotel": "上海外滩W酒店",
                    "check_in_date": "2026-05-01",
                    "address": "上海市黄浦区中山东一路1号"
                },
                "suggested_actions": ["create_todo", "set_reminder", "open_map", "export_calendar"]
            }
        else:
            return {
                "scene_type": "unknown",
                "data": {},
                "suggested_actions": []
            }
