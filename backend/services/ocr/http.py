import requests
import base64
import logging
from pathlib import Path
from .base import OCRService
from app.core.config import OCR_API_URL, OCR_API_KEY, OCR_SECRET_KEY

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

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
            logger.error(f"百度云 OCR 服务错误: {e}")
            return ""
