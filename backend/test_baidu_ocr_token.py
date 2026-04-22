import requests
from app.core.config import OCR_API_KEY, OCR_SECRET_KEY

def test_baidu_ocr_token():
    print("测试百度 OCR 获取 access token...")
    
    try:
        # 获取百度云 OCR access token
        url = f"https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={OCR_API_KEY}&client_secret={OCR_SECRET_KEY}"
        response = requests.get(url)
        response.raise_for_status()
        result = response.json()
        
        print(f"百度 OCR 获取 access token 响应: {result}")
        
        if 'access_token' in result:
            print(f"成功获取 access token: {result['access_token'][:20]}...")
            return True
        else:
            print("百度 OCR 未返回 access token")
            return False
    except Exception as e:
        print(f"百度 OCR 获取 access token 失败: {e}")
        return False

if __name__ == "__main__":
    success = test_baidu_ocr_token()
    if success:
        print("\n百度 OCR access token 测试成功！")
    else:
        print("\n百度 OCR access token 测试失败！")