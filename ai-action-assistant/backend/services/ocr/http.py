import requests
from pathlib import Path
from .base import OCRService
from ...config import OCR_API_URL, OCR_API_KEY

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
