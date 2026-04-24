from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from ..core.database import Base

class ParseResult(Base):
    __tablename__ = "parse_results"
    
    id = Column(Integer, primary_key=True, index=True)
    image_id = Column(Integer, ForeignKey("images.id"), nullable=False)
    ocr_text = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class ParseItem(Base):
    __tablename__ = "parse_items"
    
    id = Column(Integer, primary_key=True, index=True)
    parse_result_id = Column(Integer, ForeignKey("parse_results.id"), nullable=False)
    item_id = Column(String(50), nullable=False)  # 唯一标识每个事项
    scene_type = Column(String(50), nullable=False)  # schedule, task, travel, other
    summary = Column(Text, nullable=False)
    entities_json = Column(Text, nullable=False)  # JSON 字符串
    suggested_actions_json = Column(Text, nullable=False)  # JSON 字符串
    action_plan_json = Column(Text, nullable=False)  # JSON 字符串
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())