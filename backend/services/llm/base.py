from abc import ABC, abstractmethod
from typing import Dict, Any

class LLMService(ABC):
    @abstractmethod
    def analyze_text(self, text: str) -> Dict[str, Any]:
        """分析文本并返回结构化数据"""
        pass
