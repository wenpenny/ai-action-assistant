from abc import ABC, abstractmethod
from typing import Dict, Any
import requests
from ..core.config import LLM_SERVICE_TYPE, LLM_API_URL, LLM_API_KEY

class LLMService(ABC):
    @abstractmethod
    def analyze_text(self, text: str) -> Dict[str, Any]:
        """分析文本并返回结构化数据"""
        pass

class MockLLMService(LLMService):
    def analyze_text(self, text: str) -> Dict[str, Any]:
        """模拟分析文本并返回结构化数据"""
        text_lower = text.lower()
        
        # 检测场景类型
        if any(keyword in text_lower for keyword in ["会议", "面试", "课程", "活动", "时间"]):
            return {
                "scene_type": "schedule",
                "summary": "这是一个讲座活动海报，时间为2026-04-28 19:00，地点为图书馆报告厅",
                "entities": {
                    "title": "AI创新讲座",
                    "date": "2026-04-28",
                    "start_time": "19:00",
                    "end_time": None,
                    "deadline": None,
                    "location": "图书馆报告厅",
                    "address": None,
                    "link": "https://example.com"
                },
                "suggested_actions": ["create_todo", "set_reminder", "open_map", "export_calendar"]
            }
        elif any(keyword in text_lower for keyword in ["作业", "通知", "提交", "截止"]):
            return {
                "scene_type": "task",
                "summary": "这是一个作业通知，截止日期为2026-04-30，内容为完成项目报告",
                "entities": {
                    "title": "完成项目报告",
                    "date": None,
                    "start_time": None,
                    "end_time": None,
                    "deadline": "2026-04-30",
                    "location": None,
                    "address": None,
                    "link": None
                },
                "suggested_actions": ["create_todo", "set_reminder"]
            }
        elif any(keyword in text_lower for keyword in ["航班", "酒店", "车票", "地址"]):
            return {
                "scene_type": "travel",
                "summary": "这是一个航班信息，航班号为CA1234，出发时间为2026-05-01 08:30，从北京飞往上海",
                "entities": {
                    "title": "航班CA1234",
                    "date": "2026-05-01",
                    "start_time": "08:30",
                    "end_time": None,
                    "deadline": None,
                    "location": "北京",
                    "address": "上海市黄浦区中山东一路1号",
                    "link": None
                },
                "suggested_actions": ["create_todo", "set_reminder", "open_map", "export_calendar"]
            }
        else:
            return {
                "scene_type": "unknown",
                "summary": "无法识别的内容",
                "entities": {
                    "title": None,
                    "date": None,
                    "start_time": None,
                    "end_time": None,
                    "deadline": None,
                    "location": None,
                    "address": None,
                    "link": None
                },
                "suggested_actions": []
            }

class HttpLLMService(LLMService):
    def analyze_text(self, text: str) -> Dict[str, Any]:
        """通过 HTTP 请求调用 LLM 服务"""
        try:
            # 这里是预留的 HTTP LLM 服务调用代码
            # 实际使用时需要根据具体的 LLM 服务 API 进行调整
            payload = {
                "text": text,
                "task": "analyze_and_structurize"
            }
            headers = {
                "Authorization": f"Bearer {LLM_API_KEY}",
                "Content-Type": "application/json"
            }
            response = requests.post(LLM_API_URL, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            # 如果调用失败，返回默认值
            print(f"LLM service error: {e}")
            return {
                "scene_type": "unknown",
                "summary": "无法识别的内容",
                "entities": {
                    "title": None,
                    "date": None,
                    "start_time": None,
                    "end_time": None,
                    "deadline": None,
                    "location": None,
                    "address": None,
                    "link": None
                },
                "suggested_actions": []
            }

def get_llm_service() -> LLMService:
    """根据配置获取 LLM 服务实例"""
    if LLM_SERVICE_TYPE == "mock":
        return MockLLMService()
    elif LLM_SERVICE_TYPE == "http":
        return HttpLLMService()
    else:
        raise ValueError(f"Invalid LLM service type: {LLM_SERVICE_TYPE}")
