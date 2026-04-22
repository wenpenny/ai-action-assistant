from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from ..core.database import Base

class ParseResult(Base):
    __tablename__ = "parse_results"
    
    id = Column(Integer, primary_key=True, index=True)
    image_id = Column(Integer, ForeignKey("images.id"), nullable=False)
    scene_type = Column(String(50), nullable=False)  # schedule, task, travel, other
    summary = Column(Text, nullable=False)
    entities_json = Column(Text, nullable=False)  # JSON 字符串
    suggested_actions_json = Column(Text, nullable=False)  # JSON 字符串
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
