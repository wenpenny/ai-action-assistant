from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional
import requests
import base64
from ..core.config import OCR_SERVICE_TYPE, OCR_API_URL, OCR_API_KEY, OCR_SECRET_KEY

class OCRService(ABC):
    @abstractmethod
    def extract_text(self, image_path: Path) -> str:
        """从图片中提取文本"""
        pass



class HttpOCRService(OCRService):
    def extract_text(self, image_path: Path) -> str:
        """通过 HTTP 请求调用百度云 OCR 服务"""
        try:
            # 获取百度云 OCR access token
            def get_access_token():
                url = f"https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={OCR_API_KEY}&client_secret={OCR_SECRET_KEY}"
                response = requests.get(url)
                response.raise_for_status()
                result = response.json()
                return result.get('access_token')
            
            # 读取图片并进行 base64 编码
            with open(image_path, 'rb') as f:
                image_data = f.read()
                image_base64 = base64.b64encode(image_data).decode('utf-8')
            
            # 构建请求参数
            access_token = get_access_token()
            url = f"{OCR_API_URL}?access_token={access_token}"
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            data = {'image': image_base64}
            
            # 调用百度云 OCR API
            response = requests.post(url, headers=headers, data=data)
            response.raise_for_status()
            
            # 解析响应
            result = response.json()
            if 'words_result' in result:
                # 提取识别的文本
                text = '\n'.join([item['words'] for item in result['words_result']])
                return text
            else:
                return ""
        except Exception as e:
            # 如果调用失败，返回空字符串或错误信息
            print(f"百度云 OCR 服务错误: {e}")
            return ""



def get_ocr_service() -> OCRService:
    """根据配置获取 OCR 服务实例"""
    if OCR_SERVICE_TYPE == "http":
        return HttpOCRService()
    else:
        raise ValueError(f"Invalid OCR service type: {OCR_SERVICE_TYPE}")
