from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from ..config import DATABASE_URL

Base = declarative_base()

# 创建数据库引擎
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 依赖项，用于获取数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 历史记录模型
class History(Base):
    __tablename__ = "history"
    
    id = Column(Integer, primary_key=True, index=True)
    image_path = Column(String(255), nullable=False)
    ocr_text = Column(Text, nullable=False)
    scene_type = Column(String(50), nullable=False)  # schedule, task, travel
    structured_data = Column(Text, nullable=False)  # JSON 字符串
    created_at = Column(DateTime, default=datetime.utcnow)

# 动作模型
class Action(Base):
    __tablename__ = "action"
    
    id = Column(Integer, primary_key=True, index=True)
    history_id = Column(Integer, ForeignKey("history.id"), nullable=False)
    action_type = Column(String(50), nullable=False)  # create_todo, set_reminder, open_map, export_calendar
    action_data = Column(Text, nullable=False)  # JSON 字符串
    executed = Column(Integer, default=0)  # 0: 未执行, 1: 已执行
    created_at = Column(DateTime, default=datetime.utcnow)

# 创建数据库表
def init_db():
    Base.metadata.create_all(bind=engine)
