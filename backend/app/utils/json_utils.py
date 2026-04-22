import json
from typing import Dict, Any, Optional

def json_serialize(data: Any) -> str:
    """序列化数据为 JSON 字符串"""
    return json.dumps(data, ensure_ascii=False, indent=2)

def json_deserialize(json_str: str) -> Dict[str, Any]:
    """反序列化 JSON 字符串为字典"""
    try:
        return json.loads(json_str)
    except json.JSONDecodeError:
        return {}

def safe_json_deserialize(json_str: Optional[str]) -> Dict[str, Any]:
    """安全地反序列化 JSON 字符串，处理 None 或无效 JSON 的情况"""
    if not json_str:
        return {}
    try:
        return json.loads(json_str)
    except json.JSONDecodeError:
        return {}
