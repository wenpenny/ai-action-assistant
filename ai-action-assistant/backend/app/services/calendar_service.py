import os
from pathlib import Path
from datetime import datetime
from typing import Optional
from ..core.config import UPLOAD_DIR

class CalendarService:
    def generate_ics_file(self, title: str, start_time: str, end_time: Optional[str] = None, 
                        location: Optional[str] = None, description: Optional[str] = None) -> str:
        """生成 ICS 日历文件并返回下载地址"""
        # 创建日历文件目录
        calendar_dir = UPLOAD_DIR / "calendar"
        calendar_dir.mkdir(exist_ok=True)
        
        # 生成文件名
        filename = f"{title.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d%H%M%S')}.ics"
        file_path = calendar_dir / filename
        
        # 构建 ICS 内容
        ics_content = [
            "BEGIN:VCALENDAR",
            "VERSION:2.0",
            "PRODID:-//AI Action Assistant//Calendar//EN",
            "BEGIN:VEVENT",
            f"SUMMARY:{title}"
        ]
        
        # 添加开始时间
        if start_time:
            # 假设 start_time 格式为 "YYYY-MM-DD HH:MM"
            try:
                start_datetime = datetime.strptime(start_time, "%Y-%m-%d %H:%M")
                ics_content.append(f"DTSTART:{start_datetime.strftime('%Y%m%dT%H%M00')}")
            except ValueError:
                pass
        
        # 添加结束时间
        if end_time:
            # 假设 end_time 格式为 "YYYY-MM-DD HH:MM"
            try:
                end_datetime = datetime.strptime(end_time, "%Y-%m-%d %H:%M")
                ics_content.append(f"DTEND:{end_datetime.strftime('%Y%m%dT%H%M00')}")
            except ValueError:
                pass
        
        # 添加地点
        if location:
            ics_content.append(f"LOCATION:{location}")
        
        # 添加描述
        if description:
            ics_content.append(f"DESCRIPTION:{description}")
        
        # 添加结束标记
        ics_content.extend([
            "END:VEVENT",
            "END:VCALENDAR"
        ])
        
        # 写入文件
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("\r\n".join(ics_content))
        
        # 生成下载 URL
        download_url = f"/uploads/calendar/{filename}"
        return download_url
