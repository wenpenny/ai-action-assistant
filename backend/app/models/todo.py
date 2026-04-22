from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
import enum
from ..core.database import Base

class TodoStatus(enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class TodoPriority(enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class Todo(Base):
    __tablename__ = "todos"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    deadline = Column(DateTime, nullable=True)
    priority = Column(Enum(TodoPriority), default=TodoPriority.MEDIUM)
    source_image_id = Column(Integer, ForeignKey("images.id"), nullable=False)
    status = Column(Enum(TodoStatus), default=TodoStatus.PENDING)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
