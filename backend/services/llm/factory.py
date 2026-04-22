from .base import LLMService
from .mock import MockLLMService
from .http import HttpLLMService
from ...config import LLM_SERVICE_TYPE

def get_llm_service() -> LLMService:
    """根据配置获取 LLM 服务实例"""
    if LLM_SERVICE_TYPE == "mock":
        return MockLLMService()
    elif LLM_SERVICE_TYPE == "http":
        return HttpLLMService()
    else:
        raise ValueError(f"Invalid LLM service type: {LLM_SERVICE_TYPE}")
