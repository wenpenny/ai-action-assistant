from .base import OCRService
from .mock import MockOCRService
from .http import HttpOCRService
from app.core.config import OCR_SERVICE_TYPE

def get_ocr_service() -> OCRService:
    """根据配置获取 OCR 服务实例"""
    if OCR_SERVICE_TYPE == "mock":
        return MockOCRService()
    elif OCR_SERVICE_TYPE == "http":
        return HttpOCRService()
    else:
        raise ValueError(f"Invalid OCR service type: {OCR_SERVICE_TYPE}")
