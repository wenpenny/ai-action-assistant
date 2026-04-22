from .factory import get_ocr_service
from .base import OCRService
from .mock import MockOCRService
from .http import HttpOCRService

__all__ = ["get_ocr_service", "OCRService", "MockOCRService", "HttpOCRService"]
