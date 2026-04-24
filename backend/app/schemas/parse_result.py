from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional, List, Dict, Any

class Entities(BaseModel):
    title: Optional[str] = None
    date: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    deadline: Optional[str] = None
    location: Optional[str] = None
    address: Optional[str] = None
    link: Optional[str] = None
    task_name: Optional[str] = None
    required_materials: Optional[List[str]] = None
    departure_time: Optional[str] = None
    departure_location: Optional[str] = None
    destination: Optional[str] = None
    hotel_name: Optional[str] = None
    booking_no: Optional[str] = None

class ActionPlanItem(BaseModel):
    action_type: str
    label: str
    payload: Dict[str, Any]

class ParseItemBase(BaseModel):
    item_id: str
    scene_type: str
    summary: str
    entities: Entities
    suggested_actions: List[str]
    action_plan: List[ActionPlanItem]
    
    @field_validator('scene_type')
    def validate_scene_type(cls, v):
        valid_scene_types = ["schedule", "task", "travel", "other"]
        if v not in valid_scene_types:
            raise ValueError(f"Invalid scene type. Must be one of: {valid_scene_types}")
        return v
    
    @field_validator('suggested_actions')
    def validate_suggested_actions(cls, v):
        valid_actions = ["create_todo", "set_reminder", "open_map", "export_calendar"]
        for action in v:
            if action not in valid_actions:
                raise ValueError(f"Invalid action: {action}. Must be one of: {valid_actions}")
        return v

class ParseResultBase(BaseModel):
    ocr_text: str
    items: List[ParseItemBase]

class ParseResultCreate(ParseResultBase):
    image_id: int

class ParseResultResponse(ParseResultBase):
    id: int
    image_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class ParseResultUpdate(BaseModel):
    items: Optional[List[ParseItemBase]] = None

class ParseItemResponse(ParseItemBase):
    id: int
    parse_result_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True