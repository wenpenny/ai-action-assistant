import json
from pathlib import Path
from typing import Dict, Any
from sqlalchemy.orm import Session
from ..models import Image, ParseResult, ParseStatus
from ..schemas import ParseResultCreate, ParseResultBase, Entities
from .ocr_service import get_ocr_service
from .llm_service import get_llm_service

class ParseService:
    def __init__(self):
        self.ocr_service = get_ocr_service()
        self.llm_service = get_llm_service()
    
    def parse_image(self, image_id: int, db: Session) -> Dict[str, Any]:
        """解析图片并返回结构化数据"""
        # 查找图片
        image = db.query(Image).filter(Image.id == image_id).first()
        if not image:
            raise ValueError(f"Image with id {image_id} not found")
        
        try:
            # 构建图片路径
            image_path = Path(image.file_path)
            
            # 执行 OCR
            ocr_text = self.ocr_service.extract_text(image_path)
            
            # 执行 LLM 解析
            llm_result = self.llm_service.analyze_text(ocr_text)
            
            # 规则 + LLM 双重判断场景类型
            scene_type = self._determine_scene_type(ocr_text, llm_result.get("scene_type"))
            llm_result["scene_type"] = scene_type
            
            # 校验并规范化 LLM 输出
            validated_result = self._validate_and_normalize_result(llm_result)
            
            # 保存解析结果
            parse_result = ParseResult(
                image_id=image_id,
                scene_type=validated_result["scene_type"],
                summary=validated_result["summary"],
                entities_json=json.dumps(validated_result["entities"]),
                suggested_actions_json=json.dumps(validated_result["suggested_actions"])
            )
            db.add(parse_result)
            
            # 更新图片解析状态
            image.parse_status = ParseStatus.COMPLETED
            
            db.commit()
            db.refresh(parse_result)
            
            return validated_result
        except Exception as e:
            # 更新图片解析状态为失败
            image.parse_status = ParseStatus.FAILED
            db.commit()
            # 返回默认值，确保不会崩溃
            return {
                "scene_type": "other",
                "summary": "解析失败",
                "entities": {
                    "title": None,
                    "date": None,
                    "start_time": None,
                    "end_time": None,
                    "deadline": None,
                    "location": None,
                    "address": None,
                    "link": None,
                    "task_name": None,
                    "required_materials": None,
                    "departure_time": None,
                    "departure_location": None,
                    "destination": None,
                    "hotel_name": None,
                    "booking_no": None
                },
                "suggested_actions": []
            }
    
    def update_parse_result(self, image_id: int, update_data: Dict[str, Any], db: Session) -> Dict[str, Any]:
        """更新解析结果"""
        # 查找解析结果
        parse_result = db.query(ParseResult).filter(ParseResult.image_id == image_id).first()
        if not parse_result:
            raise ValueError(f"Parse result for image {image_id} not found")
        
        try:
            # 校验并规范化更新数据
            validated_data = self._validate_and_normalize_result(update_data)
            
            # 更新字段
            parse_result.scene_type = validated_data["scene_type"]
            parse_result.summary = validated_data["summary"]
            parse_result.entities_json = json.dumps(validated_data["entities"])
            parse_result.suggested_actions_json = json.dumps(validated_data["suggested_actions"])
            
            db.commit()
            db.refresh(parse_result)
            
            return validated_data
        except Exception as e:
            # 返回当前解析结果，确保不会崩溃
            return {
                "scene_type": parse_result.scene_type,
                "summary": parse_result.summary,
                "entities": json.loads(parse_result.entities_json),
                "suggested_actions": json.loads(parse_result.suggested_actions_json)
            }
    
    def _determine_scene_type(self, ocr_text: str, llm_scene_type: str) -> str:
        """规则 + LLM 双重判断场景类型"""
        # 规则关键词
        schedule_keywords = ["会议", "讲座", "面试", "时间", "地点", "活动"]
        task_keywords = ["作业", "截止", "提交", "报名", "材料", "要求"]
        travel_keywords = ["车次", "航班", "酒店", "入住", "出发", "到达", "订单"]
        
        # 转换为小写进行匹配
        text_lower = ocr_text.lower()
        
        # 规则判断
        schedule_count = sum(1 for keyword in schedule_keywords if keyword in text_lower)
        task_count = sum(1 for keyword in task_keywords if keyword in text_lower)
        travel_count = sum(1 for keyword in travel_keywords if keyword in text_lower)
        
        # 取规则判断的最高得分
        max_count = max(schedule_count, task_count, travel_count)
        
        # 如果规则判断有明确结果，使用规则结果
        if max_count > 0:
            if max_count == schedule_count:
                return "schedule"
            elif max_count == task_count:
                return "task"
            else:
                return "travel"
        
        # 否则使用 LLM 结果
        valid_scene_types = ["schedule", "task", "travel", "other"]
        if llm_scene_type in valid_scene_types:
            return llm_scene_type
        else:
            return "other"
    
    def _validate_and_normalize_result(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """校验并规范化 LLM 输出"""
        # 确保所有必要字段存在
        validated_result = {
            "scene_type": result.get("scene_type", "other"),
            "summary": result.get("summary", ""),
            "entities": result.get("entities", {}),
            "suggested_actions": result.get("suggested_actions", [])
        }
        
        # 校验场景类型
        valid_scene_types = ["schedule", "task", "travel", "other"]
        if validated_result["scene_type"] not in valid_scene_types:
            validated_result["scene_type"] = "other"
        
        # 校验并规范化 entities
        entities = validated_result["entities"]
        required_entity_fields = [
            "title", "date", "start_time", "end_time", "deadline",
            "location", "address", "link", "task_name", "required_materials",
            "departure_time", "departure_location", "destination", "hotel_name", "booking_no"
        ]
        
        for field in required_entity_fields:
            if field not in entities:
                entities[field] = None
            elif field == "required_materials" and not isinstance(entities[field], list):
                entities[field] = None
        
        # 校验并规范化 suggested_actions
        valid_actions = ["create_todo", "set_reminder", "open_map", "export_calendar"]
        validated_actions = []
        for action in validated_result["suggested_actions"]:
            if action in valid_actions and action not in validated_actions:
                validated_actions.append(action)
        validated_result["suggested_actions"] = validated_actions
        
        return validated_result
