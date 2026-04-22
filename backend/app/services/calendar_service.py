import os
from datetime import datetime
from ..core.config import UPLOAD_DIR
import uuid

class CalendarService:
    def __init__(self):
        # 创建日历文件存储目录
        self.calendar_dir = UPLOAD_DIR / "calendar"
        self.calendar_dir.mkdir(exist_ok=True, parents=True)
    
    def generate_ics(self, payload: dict) -> str:
        """生成 .ics 文件"""
        # 提取事件信息
        title = payload.get("title", "Untitled Event")
        date = payload.get("date")
        start_time = payload.get("start_time")
        end_time = payload.get("end_time")
        location = payload.get("location")
        description = payload.get("description", "")
        
        # 生成唯一文件名
        file_name = f"event_{uuid.uuid4()}.ics"
        file_path = self.calendar_dir / file_name
        
        # 构建 .ics 内容
        ics_content = [
            "BEGIN:VCALENDAR",
            "VERSION:2.0",
            "PRODID:-//AI Action Assistant//EN",
            "BEGIN:VEVENT"
        ]
        
        # 添加事件标题
        ics_content.append(f"SUMMARY:{title}")
        
        # 处理日期时间
        if date:
            if start_time:
                # 有开始时间
                start_datetime = f"{date}T{start_time.replace(':', '')}00"
                ics_content.append(f"DTSTART:{start_datetime}")
                
                # 有结束时间
                if end_time:
                    end_datetime = f"{date}T{end_time.replace(':', '')}00"
                    ics_content.append(f"DTEND:{end_datetime}")
                else:
                    # 没有结束时间，默认持续1小时
                    ics_content.append(f"DTEND:{start_datetime}")
            else:
                # 全天事件
                ics_content.append(f"DTSTART;VALUE=DATE:{date.replace('-', '')}")
                ics_content.append(f"DTEND;VALUE=DATE:{date.replace('-', '')}")
        
        # 添加位置
        if location:
            ics_content.append(f"LOCATION:{location}")
        
        # 添加描述
        if description:
            ics_content.append(f"DESCRIPTION:{description}")
        
        # 添加创建时间
        now = datetime.now().strftime("%Y%m%dT%H%M%SZ")
        ics_content.append(f"DTSTAMP:{now}")
        ics_content.append(f"UID:{uuid.uuid4()}@ai-action-assistant")
        
        ics_content.extend([
            "END:VEVENT",
            "END:VCALENDAR"
        ])
        
        # 写入文件
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("\r\n".join(ics_content))
        
        # 返回相对路径
        return f"/uploads/calendar/{file_name}"