from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

# 上传请求模型
class UploadRequest(BaseModel):
    pass

# OCR 响应模型
class OCRResponse(BaseModel):
    text: str

# 结构化数据模型
class StructuredData(BaseModel):
    scene_type: str
    data: Dict[str, Any]
    suggested_actions: List[str]

# 动作执行请求模型
class ActionRequest(BaseModel):
    history_id: int
    action_type: str
    action_data: Dict[str, Any]

# 历史记录响应模型
class HistoryResponse(BaseModel):
    id: int
    image_path: str
    ocr_text: str
    scene_type: str
    structured_data: Dict[str, Any]
    created_at: datetime
    
    class Config:
        from_attributes = True

# 动作响应模型
class ActionResponse(BaseModel):
    id: int
    history_id: int
    action_type: str
    action_data: Dict[str, Any]
    executed: int
    created_at: datetime
    
    class Config:
        from_attributes = True
