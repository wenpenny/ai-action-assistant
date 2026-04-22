import urllib.parse

class MapService:
    def generate_map_url(self, location: str) -> str:
        """生成地图 URL"""
        # 对位置进行 URL 编码
        encoded_location = urllib.parse.quote(location)
        
        # 生成通用地图搜索链接
        # 使用 Google Maps 的通用搜索链接格式
        map_url = f"https://www.google.com/maps/search/?api=1&query={encoded_location}"
        
        return map_url