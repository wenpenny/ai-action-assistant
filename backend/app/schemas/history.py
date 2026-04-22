from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Dict, Any
from .image import ImageResponse
from .parse_result import ParseResultResponse
from .action import ActionResponse

class HistoryItem(BaseModel):
    image: ImageResponse
    parse_result: Optional[ParseResultResponse] = None
    action_records: List[Dict[str, Any]] = []

class HistoryResponse(BaseModel):
    items: List[HistoryItem]

class HistoryDetailResponse(BaseModel):
    image: ImageResponse
    parse_result: Optional[ParseResultResponse] = None
    action_records: List[Dict[str, Any]] = []