from abc import ABC, abstractmethod
from pathlib import Path

class OCRService(ABC):
    @abstractmethod
    def extract_text(self, image_path: Path) -> str:
        """从图片中提取文本"""
        pass
