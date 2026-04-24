from typing import Dict, Any, List
import requests
import json
import logging
from datetime import datetime
from ..core.config import (
    LLM_SERVICE_TYPE,
    BLUELM_API_URL, BLUELM_API_KEY, BLUELM_MODEL,
    DEEPSEEK_API_URL, DEEPSEEK_API_KEY, DEEPSEEK_MODEL
)

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self):
        if LLM_SERVICE_TYPE == "bluelm":
            self.service = BlueLMService()
        elif LLM_SERVICE_TYPE == "deepseek":
            self.service = DeepSeekService()
        elif LLM_SERVICE_TYPE == "mock":
            self.service = MockLLMService()
        else:
            raise ValueError(f"Invalid LLM service type: {LLM_SERVICE_TYPE}")
    
    def analyze_text(self, text: str) -> Dict[str, Any]:
        return self.service.analyze_text(text)
    
    def split_segments(self, text: str) -> List[str]:
        return self.service.split_segments(text)
    
    def analyze_segment(self, segment: str) -> Dict[str, Any]:
        return self.service.analyze_segment(segment)

class BlueLMService:
    def split_segments(self, text: str) -> List[str]:
        """将 OCR 文本切分为多个独立事项"""
        try:
            system_prompt = """你是一个智能文本分析助手，负责将一段 OCR 识别的文本切分为多个独立的事项/通知/行程项。

请按照以下规则进行切分：
1. 每个事项应该是一个独立的通知、任务、行程或事件
2. 不同的事项之间通常会有明显的分隔，如空行、不同的标题等
3. 输出一个 JSON 格式的列表，包含所有切分后的事项文本

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
                        "content": f"请将以下 OCR 文本切分为多个独立的事项：\n\n{text}"
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
                
                segments = json.loads(content)
                if isinstance(segments, list):
                    return segments
                else:
                    return [text]
            except (json.JSONDecodeError, ValueError) as e:
                logger.error(f"解析 BlueLM 切分响应失败: {e}")
                logger.debug(f"原始响应: {content}")
                # 返回原始文本作为单个 segment
                return [text]
                
        except Exception as e:
            # 如果调用失败，返回原始文本作为单个 segment
            logger.error(f"BlueLM service error: {e}")
            return [text]
    
    def analyze_segment(self, segment: str) -> Dict[str, Any]:
        """分析单个事项文本并返回结构化信息"""
        try:
            system_prompt = """你是一个智能助手，负责分析 OCR 文本并提取结构化信息。请按照以下 JSON 格式输出：

{
  "scene_type": "schedule|task|travel|other",
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
    "required_materials": ["所需材料1", "所需材料2"],
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
- other：其他类型

建议动作说明：
- create_todo：创建待办事项
- set_reminder：设置提醒
- open_map：打开地图
- export_calendar：导出日历

请只返回 JSON 格式的结果，不要包含其他文字说明。"""

            # 获取当前日期
            current_date = datetime.now().strftime("%Y-%m-%d")
            
            payload = {
                "model": BLUELM_MODEL,
                "messages": [
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": f"当前日期：{current_date}\n\n请分析以下事项文本，提取结构化信息：\n\n{segment}"
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
                logger.error(f"解析 BlueLM 响应失败: {e}")
                logger.debug(f"原始响应: {content}")
                # 返回默认值
                return self._get_default_result()
                
        except Exception as e:
            # 如果调用失败，返回默认值
            logger.error(f"BlueLM service error: {e}")
            return self._get_default_result()
    
    def analyze_text(self, text: str) -> Dict[str, Any]:
        """分析文本并返回结构化信息（兼容旧接口）"""
        segments = self.split_segments(text)
        if segments:
            return self.analyze_segment(segments[0])
        else:
            return self._get_default_result()
    
    def _get_default_result(self) -> Dict[str, Any]:
        """返回默认结果"""
        return {
            "scene_type": "other",
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
    def split_segments(self, text: str) -> List[str]:
        """将 OCR 文本切分为多个独立事项"""
        try:
            system_prompt = """你是一个智能文本分析助手，负责将一段 OCR 识别的文本切分为多个独立的事项/通知/行程项。

请按照以下规则进行切分：
1. 每个事项应该是一个独立的通知、任务、行程或事件
2. 不同的事项之间通常会有明显的分隔，如空行、不同的标题等
3. 输出一个 JSON 格式的列表，包含所有切分后的事项文本

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
                        "content": f"请将以下 OCR 文本切分为多个独立的事项：\n\n{text}"
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
                
                segments = json.loads(content)
                if isinstance(segments, list):
                    return segments
                else:
                    return [text]
            except (json.JSONDecodeError, ValueError) as e:
                logger.error(f"解析 DeepSeek 切分响应失败: {e}")
                logger.debug(f"原始响应: {content}")
                # 返回原始文本作为单个 segment
                return [text]
                
        except Exception as e:
            # 如果调用失败，返回原始文本作为单个 segment
            logger.error(f"DeepSeek service error: {e}")
            return [text]
    
    def analyze_segment(self, segment: str) -> Dict[str, Any]:
        """分析单个事项文本并返回结构化信息"""
        try:
            system_prompt = """你是一个智能助手，负责分析 OCR 文本并提取结构化信息。请按照以下 JSON 格式输出：

{
  "scene_type": "schedule|task|travel|other",
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
    "required_materials": ["所需材料1", "所需材料2"],
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
- other：其他类型

建议动作说明：
- create_todo：创建待办事项
- set_reminder：设置提醒
- open_map：打开地图
- export_calendar：导出日历

请只返回 JSON 格式的结果，不要包含其他文字说明。"""

            # 获取当前日期
            current_date = datetime.now().strftime("%Y-%m-%d")
            
            payload = {
                "model": DEEPSEEK_MODEL,
                "messages": [
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": f"当前日期：{current_date}\n\n请分析以下事项文本，提取结构化信息：\n\n{segment}"
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
                logger.error(f"解析 DeepSeek 响应失败: {e}")
                logger.debug(f"原始响应: {content}")
                # 返回默认值
                return self._get_default_result()
                
        except Exception as e:
            # 如果调用失败，返回默认值
            logger.error(f"DeepSeek service error: {e}")
            return self._get_default_result()
    
    def analyze_text(self, text: str) -> Dict[str, Any]:
        """分析文本并返回结构化信息（兼容旧接口）"""
        segments = self.split_segments(text)
        if segments:
            return self.analyze_segment(segments[0])
        else:
            return self._get_default_result()
    
    def _get_default_result(self) -> Dict[str, Any]:
        """返回默认结果"""
        return {
            "scene_type": "other",
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

class MockLLMService:
    def split_segments(self, text: str) -> List[str]:
        """模拟将 OCR 文本切分为多个独立事项"""
        # 简单的模拟逻辑：根据空行切分
        segments = [segment.strip() for segment in text.split('\n\n') if segment.strip()]
        if not segments:
            # 如果没有空行，则返回原始文本作为单个 segment
            segments = [text.strip()]
        return segments
    
    def analyze_segment(self, segment: str) -> Dict[str, Any]:
        """模拟分析单个事项文本并返回结构化信息"""
        # 简单的模拟逻辑：根据关键词判断场景类型
        segment_lower = segment.lower()
        
        if any(keyword in segment_lower for keyword in ['会议', '讲座', '面试', '时间', '地点', '活动']):
            scene_type = "schedule"
            suggested_actions = ["set_reminder", "export_calendar"]
        elif any(keyword in segment_lower for keyword in ['作业', '截止', '提交', '报名', '材料', '要求']):
            scene_type = "task"
            suggested_actions = ["create_todo", "set_reminder"]
        elif any(keyword in segment_lower for keyword in ['车次', '航班', '酒店', '入住', '出发', '到达', '订单']):
            scene_type = "travel"
            suggested_actions = ["open_map", "set_reminder"]
        else:
            scene_type = "other"
            suggested_actions = []
        
        # 模拟 entities
        entities = {
            "title": segment[:50] + "..." if len(segment) > 50 else segment,
            "date": "2026-04-25",
            "start_time": "09:00",
            "end_time": "10:00",
            "deadline": "2026-04-25 23:59",
            "location": "会议室",
            "address": "北京市海淀区",
            "link": None,
            "task_name": None,
            "required_materials": ["材料1", "材料2"],
            "departure_time": None,
            "departure_location": None,
            "destination": None,
            "hotel_name": None,
            "booking_no": None
        }
        
        return {
            "scene_type": scene_type,
            "summary": f"这是一个{scene_type}类型的事项：{segment[:100]}..." if len(segment) > 100 else f"这是一个{scene_type}类型的事项：{segment}",
            "entities": entities,
            "suggested_actions": suggested_actions
        }
    
    def analyze_text(self, text: str) -> Dict[str, Any]:
        """分析文本并返回结构化信息（兼容旧接口）"""
        segments = self.split_segments(text)
        if segments:
            return self.analyze_segment(segments[0])
        else:
            return {
                "scene_type": "other",
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