from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
import enum
from ..core.database import Base

class ExecuteStatus(enum.Enum):
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"

class ActionRecord(Base):
    __tablename__ = "action_records"
    
    id = Column(Integer, primary_key=True, index=True)
    image_id = Column(Integer, ForeignKey("images.id"), nullable=False)
    item_id = Column(String(50), nullable=True)  # 关联到 parse_items 的 item_id
    action_type = Column(String(50), nullable=False)  # create_todo, set_reminder, open_map, export_calendar
    action_payload_json = Column(Text, nullable=False)  # JSON 字符串
    execute_status = Column(Enum(ExecuteStatus), default=ExecuteStatus.PENDING)
    execute_result_json = Column(Text, nullable=True)  # JSON 字符串，存储动作执行结果
    created_at = Column(DateTime(timezone=True), server_default=func.now())
