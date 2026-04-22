from typing import Dict, Any
import requests
import json
from ..core.config import (
    LLM_SERVICE_TYPE,
    BLUELM_API_URL, BLUELM_API_KEY, BLUELM_MODEL,
    DEEPSEEK_API_URL, DEEPSEEK_API_KEY, DEEPSEEK_MODEL
)

class LLMService:
    def __init__(self):
        if LLM_SERVICE_TYPE == "bluelm":
            self.service = BlueLMService()
        elif LLM_SERVICE_TYPE == "deepseek":
            self.service = DeepSeekService()
        else:
            raise ValueError(f"Invalid LLM service type: {LLM_SERVICE_TYPE}")
    
    def analyze_text(self, text: str) -> Dict[str, Any]:
        return self.service.analyze_text(text)

class BlueLMService:
    def analyze_text(self, text: str) -> Dict[str, Any]:
        """通过 HTTP 请求调用 BlueLM（蓝心大模型）服务"""
        try:
            # 构建 BlueLM API 请求（OpenAI 兼容格式）
            system_prompt = """你是一个智能助手，负责分析 OCR 文本并提取结构化信息。请按照以下 JSON 格式输出：

{
  "scene_type": "schedule|task|travel",
  "summary": "简要描述内容",
  "entities": {
    "title": "标题",
    "date": "YYYY-MM-DD",
    "start_time": "HH:MM",
    "end_time": "HH:MM",
    "deadline": "YYYY-MM-DD HH:MM",
    "location": "地点",
    "address": "地址",
    "link": "链接",
    "task_name": "任务名称",
    "required_materials": "所需材料",
    "departure_time": "出发时间",
    "departure_location": "出发地点",
    "destination": "目的地",
    "hotel_name": "酒店名称",
    "booking_no": "订单号"
  },
  "suggested_actions": ["create_todo", "set_reminder", "open_map", "export_calendar"]
}

场景类型说明：
- schedule：日程类（活动海报、面试通知、会议安排、课程安排）
- task：任务类（作业通知、群公告、报名要求、材料提交通知）
- travel：出行类（车票截图、酒店订单、航班信息、地址与预约信息）

建议动作说明：
- create_todo：创建待办事项
- set_reminder：设置提醒
- open_map：打开地图
- export_calendar：导出日历

请只返回 JSON 格式的结果，不要包含其他文字说明。"""

            payload = {
                "model": BLUELM_MODEL,
                "messages": [
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": f"请分析以下 OCR 文本，提取结构化信息：\n\n{text}"
                    }
                ],
                "temperature": 0.3,
                "max_tokens": 1000
            }
            
            headers = {
                "Authorization": f"Bearer {BLUELM_API_KEY}",
                "Content-Type": "application/json"
            }
            
            # 调用 BlueLM API
            response = requests.post(BLUELM_API_URL, json=payload, headers=headers, timeout=30)
            response.raise_for_status()
            
            # 解析响应
            result = response.json()
            content = result['choices'][0]['message']['content']
            
            # 尝试解析 JSON 响应
            try:
                # 清理可能的前后缀
                if '```json' in content:
                    content = content.split('```json')[1].split('```')[0].strip()
                elif '```' in content:
                    content = content.split('```')[1].split('```')[0].strip()
                
                parsed_result = json.loads(content)
                
                # 验证必需字段
                if not all(key in parsed_result for key in ['scene_type', 'summary', 'entities', 'suggested_actions']):
                    raise ValueError("缺少必需字段")
                
                return parsed_result
            except (json.JSONDecodeError, ValueError) as e:
                print(f"解析 BlueLM 响应失败: {e}")
                print(f"原始响应: {content}")
                # 返回默认值
                return self._get_default_result()
                
        except Exception as e:
            # 如果调用失败，返回默认值
            print(f"BlueLM service error: {e}")
            return self._get_default_result()
    
    def _get_default_result(self) -> Dict[str, Any]:
        """返回默认结果"""
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
                "link": None,
                "task_name": None,
                "required_materials": None,
                "departure_time": None,
                "departure_location": None,
                "destination": None,
                "hotel_name": None,
                "booking_no": None
            },
            "suggested_actions": []
        }

class DeepSeekService:
    def analyze_text(self, text: str) -> Dict[str, Any]:
        """通过 HTTP 请求调用 DeepSeek 服务"""
        try:
            # 构建 DeepSeek API 请求（OpenAI 兼容格式）
            system_prompt = """你是一个智能助手，负责分析 OCR 文本并提取结构化信息。请按照以下 JSON 格式输出：

{
  "scene_type": "schedule|task|travel",
  "summary": "简要描述内容",
  "entities": {
    "title": "标题",
    "date": "YYYY-MM-DD",
    "start_time": "HH:MM",
    "end_time": "HH:MM",
    "deadline": "YYYY-MM-DD HH:MM",
    "location": "地点",
    "address": "地址",
    "link": "链接",
    "task_name": "任务名称",
    "required_materials": "所需材料",
    "departure_time": "出发时间",
    "departure_location": "出发地点",
    "destination": "目的地",
    "hotel_name": "酒店名称",
    "booking_no": "订单号"
  },
  "suggested_actions": ["create_todo", "set_reminder", "open_map", "export_calendar"]
}

场景类型说明：
- schedule：日程类（活动海报、面试通知、会议安排、课程安排）
- task：任务类（作业通知、群公告、报名要求、材料提交通知）
- travel：出行类（车票截图、酒店订单、航班信息、地址与预约信息）

建议动作说明：
- create_todo：创建待办事项
- set_reminder：设置提醒
- open_map：打开地图
- export_calendar：导出日历

请只返回 JSON 格式的结果，不要包含其他文字说明。"""

            payload = {
                "model": DEEPSEEK_MODEL,
                "messages": [
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": f"请分析以下 OCR 文本，提取结构化信息：\n\n{text}"
                    }
                ],
                "temperature": 0.3,
                "max_tokens": 1000
            }
            
            headers = {
                "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                "Content-Type": "application/json"
            }
            
            # 调用 DeepSeek API
            response = requests.post(DEEPSEEK_API_URL, json=payload, headers=headers, timeout=30)
            response.raise_for_status()
            
            # 解析响应
            result = response.json()
            content = result['choices'][0]['message']['content']
            
            # 尝试解析 JSON 响应
            try:
                # 清理可能的前后缀
                if '```json' in content:
                    content = content.split('```json')[1].split('```')[0].strip()
                elif '```' in content:
                    content = content.split('```')[1].split('```')[0].strip()
                
                parsed_result = json.loads(content)
                
                # 验证必需字段
                if not all(key in parsed_result for key in ['scene_type', 'summary', 'entities', 'suggested_actions']):
                    raise ValueError("缺少必需字段")
                
                return parsed_result
            except (json.JSONDecodeError, ValueError) as e:
                print(f"解析 DeepSeek 响应失败: {e}")
                print(f"原始响应: {content}")
                # 返回默认值
                return self._get_default_result()
                
        except Exception as e:
            # 如果调用失败，返回默认值
            print(f"DeepSeek service error: {e}")
            return self._get_default_result()
    
    def _get_default_result(self) -> Dict[str, Any]:
        """返回默认结果"""
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
                "link": None,
                "task_name": None,
                "required_materials": None,
                "departure_time": None,
                "departure_location": None,
                "destination": None,
                "hotel_name": None,
                "booking_no": None
            },
            "suggested_actions": []
        }



def get_llm_service() -> LLMService:
    """获取 LLM 服务实例"""
    return LLMService()