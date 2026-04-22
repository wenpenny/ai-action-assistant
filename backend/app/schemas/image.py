from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ImageBase(BaseModel):
    filename: str
    path: str
    url: str

class ImageCreate(ImageBase):
    pass

class ImageResponse(ImageBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class UploadResponse(BaseModel):
    image_id: int
    image_url: str
