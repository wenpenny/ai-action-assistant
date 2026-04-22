from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional
import requests
from ..core.config import OCR_SERVICE_TYPE, OCR_API_URL, OCR_API_KEY

class OCRService(ABC):
    @abstractmethod
    def extract_text(self, image_path: Path) -> str:
        """从图片中提取文本"""
        pass

class MockOCRService(OCRService):
    def extract_text(self, image_path: Path) -> str:
        """模拟从图片中提取文本"""
        # 根据图片路径返回不同的模拟文本
        image_name = image_path.name.lower()
        
        if any(keyword in image_name for keyword in ["schedule", "meeting", "interview", "class"]):
            return "2026年4月28日 19:00\nAI创新讲座\n地点：图书馆报告厅\n链接：https://example.com"
        elif any(keyword in image_name for keyword in ["task", "homework", "notice", "assignment"]):
            return "作业通知\n截止日期：2026年4月30日\n内容：完成项目报告\n提交方式：邮箱"
        elif any(keyword in image_name for keyword in ["travel", "ticket", "hotel", "flight"]):
            return "航班信息\n航班号：CA1234\n出发时间：2026年5月1日 08:30\n出发地：北京\n目的地：上海\n酒店预订：上海外滩W酒店\n入住日期：2026年5月1日\n地址：上海市黄浦区中山东一路1号"
        else:
            return "这是一张测试图片，包含一些示例文本。"

class HttpOCRService(OCRService):
    def extract_text(self, image_path: Path) -> str:
        """通过 HTTP 请求调用 OCR 服务"""
        try:
            # 这里是预留的 HTTP OCR 服务调用代码
            # 实际使用时需要根据具体的 OCR 服务 API 进行调整
            with open(image_path, 'rb') as f:
                files = {'image': f}
                headers = {'Authorization': f'Bearer {OCR_API_KEY}'}
                response = requests.post(OCR_API_URL, files=files, headers=headers)
                response.raise_for_status()
                result = response.json()
                return result.get('text', '')
        except Exception as e:
            # 如果调用失败，返回空字符串或错误信息
            print(f"OCR service error: {e}")
            return ""

def get_ocr_service() -> OCRService:
    """根据配置获取 OCR 服务实例"""
    if OCR_SERVICE_TYPE == "mock":
        return MockOCRService()
    elif OCR_SERVICE_TYPE == "http":
        return HttpOCRService()
    else:
        raise ValueError(f"Invalid OCR service type: {OCR_SERVICE_TYPE}")
