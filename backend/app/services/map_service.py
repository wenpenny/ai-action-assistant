import urllib.parse

class MapService:
    def generate_map_url(self, payload: dict) -> str:
        """生成地图 URL"""
        # 从 payload 中提取位置信息
        location = payload.get("location")
        address = payload.get("address")
        
        # 优先使用地址，然后使用位置
        search_query = address if address else location
        
        if search_query:
            # 对搜索查询进行 URL 编码
            encoded_query = urllib.parse.quote(search_query)
            
            # 生成通用地图搜索链接
            # 使用 Google Maps 的通用搜索链接格式
            map_url = f"https://www.google.com/maps/search/?api=1&query={encoded_query}"
        else:
            # 如果没有位置信息，返回默认地图
            map_url = "https://www.google.com/maps/"
        
        return map_url