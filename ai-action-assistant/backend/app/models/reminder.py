from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
import enum
from ..core.database import Base

class ReminderStatus(enum.Enum):
    PENDING = "pending"
    TRIGGERED = "triggered"
    CANCELLED = "cancelled"

class Reminder(Base):
    __tablename__ = "reminders"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    remind_at = Column(DateTime, nullable=False)
    source_image_id = Column(Integer, ForeignKey("images.id"), nullable=False)
    status = Column(Enum(ReminderStatus), default=ReminderStatus.PENDING)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
