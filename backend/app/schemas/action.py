from pydantic import BaseModel
from typing import Dict, Any, Optional

class ActionRequest(BaseModel):
    image_id: int
    action_type: str
    payload: Dict[str, Any]

class ActionResponse(BaseModel):
    success: bool
    message: str
    data: Dict[str, Any]
