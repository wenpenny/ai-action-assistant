import requests
from typing import Dict, Any
from .base import LLMService
from app.core.config import LLM_API_URL, LLM_API_KEY

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
                "data": {},
                "suggested_actions": []
            }
