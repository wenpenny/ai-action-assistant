from .base import LLMService
from .mock import MockLLMService
from .http import HttpLLMService
from app.core.config import LLM_SERVICE_TYPE

def get_llm_service() -> LLMService:
    """根据配置获取 LLM 服务实例"""
    if LLM_SERVICE_TYPE == "mock":
        return MockLLMService()
    elif LLM_SERVICE_TYPE == "http":
        return HttpLLMService()
    else:
        # 对于 deepseek 和 bluelm，使用 app/services/llm_service.py 中的实现
        from app.services.llm_service import get_llm_service as get_app_llm_service
        return get_app_llm_service()
