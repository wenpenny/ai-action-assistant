from typing import Optional

class MapService:
    def get_map_url(self, address: Optional[str] = None, location: Optional[str] = None) -> str:
        """生成地图 URL"""
        # 使用百度地图 API 生成地图 URL
        # 实际使用时可以根据需要选择其他地图服务
        base_url = "https://map.baidu.com"
        
        if address:
            # 如果有具体地址，直接搜索地址
            return f"{base_url}?q={address}"
        elif location:
            # 如果只有地点名称，搜索地点
            return f"{base_url}?q={location}"
        else:
            # 没有地址信息，返回默认地图
            return base_url
