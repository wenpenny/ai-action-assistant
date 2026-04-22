from pathlib import Path
from .base import OCRService

class MockOCRService(OCRService):
    def extract_text(self, image_path: Path) -> str:
        """模拟从图片中提取文本"""
        # 根据图片路径返回不同的模拟文本
        image_name = image_path.name.lower()
        
        if any(keyword in image_name for keyword in ["schedule", "meeting", "interview", "class"]):
            return "2026年4月25日 14:00-16:00\n产品会议\n会议室：A101\n参会人员：产品团队"
        elif any(keyword in image_name for keyword in ["task", "homework", "notice", "assignment"]):
            return "作业通知\n截止日期：2026年4月30日\n内容：完成项目报告\n提交方式：邮箱"
        elif any(keyword in image_name for keyword in ["travel", "ticket", "hotel", "flight"]):
            return "航班信息\n航班号：CA1234\n出发时间：2026年5月1日 08:30\n出发地：北京\n目的地：上海\n酒店预订：上海外滩W酒店\n入住日期：2026年5月1日\n地址：上海市黄浦区中山东一路1号"
        else:
            return "这是一张测试图片，包含一些示例文本。"
