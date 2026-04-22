from datetime import datetime, date, time
from typing import Optional, Tuple

def parse_datetime(datetime_str: str) -> Optional[datetime]:
    """解析日期时间字符串"""
    formats = [
        "%Y-%m-%d %H:%M",
        "%Y/%m/%d %H:%M",
        "%Y-%m-%d",
        "%Y/%m/%d"
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(datetime_str, fmt)
        except ValueError:
            continue
    
    return None

def format_datetime(dt: datetime) -> str:
    """格式化日期时间为字符串"""
    return dt.strftime("%Y-%m-%d %H:%M")

def format_date(dt: date) -> str:
    """格式化日期为字符串"""
    return dt.strftime("%Y-%m-%d")

def format_time(t: time) -> str:
    """格式化时间为字符串"""
    return t.strftime("%H:%M")
