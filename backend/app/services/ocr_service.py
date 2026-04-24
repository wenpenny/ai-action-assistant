from pathlib import Path
from services.ocr.factory import get_ocr_service as get_ocr_service_impl
from services.ocr.base import OCRService

def get_ocr_service() -> OCRService:
    """根据配置获取 OCR 服务实例"""
    return get_ocr_service_impl()
