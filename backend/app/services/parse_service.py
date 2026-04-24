import json
import logging
from pathlib import Path
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from ..models import Image, ParseResult, ParseItem, ParseStatus
from ..schemas import ParseResultCreate, ParseResultBase, Entities, ActionPlanItem, ParseItemBase
from .ocr_service import get_ocr_service
from .llm_service import get_llm_service

# 配置日志
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

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
            logger.info(f"开始解析图片 ID: {image_id}")
            logger.info(f"图片路径: {image.file_path}")
            
            # 构建图片路径
            image_path = Path(image.file_path)
            
            # 执行 OCR
            logger.info("执行 OCR 识别...")
            ocr_text = self.ocr_service.extract_text(image_path)
            logger.info(f"OCR 识别结果:\n{ocr_text}")
            
            # 第一阶段：事项切分
            logger.info("执行 LLM 事项切分...")
            segments = self.llm_service.split_segments(ocr_text)
            logger.info(f"LLM 切分结果: {segments}")
            
            # 第二阶段：逐条结构化并生成 action plan
            items = []
            for i, segment in enumerate(segments):
                # 提取文本内容（处理字典格式）
                segment_text = segment['text'] if isinstance(segment, dict) else segment
                logger.info(f"分析事项 {i+1}: {segment_text}")
                
                # 分析单个事项
                llm_result = self.llm_service.analyze_segment(segment_text)
                logger.info(f"LLM 分析结果: {llm_result}")
                
                # 规则 + LLM 双重判断场景类型
                scene_type = self._determine_scene_type(segment_text, llm_result.get("scene_type"))
                llm_result["scene_type"] = scene_type
                logger.info(f"确定场景类型: {scene_type}")
                
                # 校验并规范化 LLM 输出
                validated_result = self._validate_and_normalize_result(llm_result)
                logger.info(f"校验并规范化结果: {validated_result}")
                
                # 生成 action plan
                action_plan = self._generate_action_plan(validated_result)
                logger.info(f"生成 action plan: {[action.model_dump() for action in action_plan]}")
                
                # 构建事项
                item = {
                    "item_id": f"item_{i+1}",
                    "scene_type": validated_result["scene_type"],
                    "summary": validated_result["summary"],
                    "entities": validated_result["entities"],
                    "suggested_actions": validated_result["suggested_actions"],
                    "action_plan": action_plan
                }
                items.append(item)
                logger.info(f"构建事项 {i+1} 完成")
            
            # 保存解析结果
            logger.info("保存解析结果到数据库...")
            parse_result = ParseResult(
                image_id=image_id,
                ocr_text=ocr_text
            )
            db.add(parse_result)
            db.flush()  # 获取 parse_result.id
            
            # 保存每个事项
            for item in items:
                parse_item = ParseItem(
                    parse_result_id=parse_result.id,
                    item_id=item["item_id"],
                    scene_type=item["scene_type"],
                    summary=item["summary"],
                    entities_json=json.dumps(item["entities"]),
                    suggested_actions_json=json.dumps(item["suggested_actions"]),
                    action_plan_json=json.dumps([action.model_dump() for action in item["action_plan"]])
                )
                db.add(parse_item)
            
            # 更新图片解析状态
            image.parse_status = ParseStatus.COMPLETED
            
            db.commit()
            db.refresh(parse_result)
            
            logger.info(f"解析完成，共识别 {len(items)} 个事项")
            
            # 构建返回结果
            return {
                "image_id": image_id,
                "ocr_text": ocr_text,
                "items": items
            }
        except Exception as e:
            logger.error(f"解析失败: {str(e)}", exc_info=True)
            # 更新图片解析状态为失败
            image.parse_status = ParseStatus.FAILED
            db.commit()
            # 返回默认值，确保不会崩溃
            return {
                "image_id": image_id,
                "ocr_text": "",
                "items": []
            }
    
    def update_parse_result(self, image_id: int, update_data: Dict[str, Any], db: Session) -> Dict[str, Any]:
        """更新解析结果"""
        # 查找解析结果
        parse_result = db.query(ParseResult).filter(ParseResult.image_id == image_id).first()
        if not parse_result:
            raise ValueError(f"Parse result for image {image_id} not found")
        
        try:
            # 清理旧的事项
            db.query(ParseItem).filter(ParseItem.parse_result_id == parse_result.id).delete()
            
            # 处理更新的事项
            items = []
            for i, item_data in enumerate(update_data.get("items", [])):
                # 校验并规范化数据
                validated_item = self._validate_and_normalize_item(item_data)
                
                # 生成 action plan
                action_plan = self._generate_action_plan(validated_item)
                
                # 构建事项
                item = {
                    "item_id": item_data.get("item_id", f"item_{i+1}"),
                    "scene_type": validated_item["scene_type"],
                    "summary": validated_item["summary"],
                    "entities": validated_item["entities"],
                    "suggested_actions": validated_item["suggested_actions"],
                    "action_plan": action_plan
                }
                items.append(item)
                
                # 保存事项
                parse_item = ParseItem(
                    parse_result_id=parse_result.id,
                    item_id=item["item_id"],
                    scene_type=item["scene_type"],
                    summary=item["summary"],
                    entities_json=json.dumps(item["entities"]),
                    suggested_actions_json=json.dumps(item["suggested_actions"]),
                    action_plan_json=json.dumps([action.model_dump() for action in item["action_plan"]])
                )
                db.add(parse_item)
            
            db.commit()
            
            # 构建返回结果
            return {
                "image_id": image_id,
                "ocr_text": parse_result.ocr_text,
                "items": items
            }
        except Exception as e:
            # 返回当前解析结果，确保不会崩溃
            return self.get_parse_result(image_id, db)
    
    def get_parse_result(self, image_id: int, db: Session) -> Dict[str, Any]:
        """获取解析结果"""
        # 查找解析结果
        parse_result = db.query(ParseResult).filter(ParseResult.image_id == image_id).first()
        if not parse_result:
            raise ValueError(f"Parse result for image {image_id} not found")
        
        # 查找所有事项
        parse_items = db.query(ParseItem).filter(ParseItem.parse_result_id == parse_result.id).all()
        
        # 构建返回结果
        items = []
        for item in parse_items:
            items.append({
                "item_id": item.item_id,
                "scene_type": item.scene_type,
                "summary": item.summary,
                "entities": json.loads(item.entities_json),
                "suggested_actions": json.loads(item.suggested_actions_json),
                "action_plan": json.loads(item.action_plan_json)
            })
        
        return {
            "image_id": image_id,
            "ocr_text": parse_result.ocr_text,
            "items": items
        }
    
    def _determine_scene_type(self, ocr_text: str, llm_scene_type: str) -> str:
        """规则 + LLM 双重判断场景类型"""
        # 规则关键词
        task_keywords = ["缴费", "提交", "报名", "截止", "完成", "材料", "要求"]
        schedule_keywords = ["讲座", "会议", "答疑", "面试", "时间", "地点"]
        travel_keywords = ["车次", "航班", "酒店", "入住", "出发", "到达", "订单"]
        
        # 转换为小写进行匹配
        text_lower = ocr_text.lower()
        
        # 规则判断
        has_task_keywords = any(keyword in text_lower for keyword in task_keywords)
        has_schedule_keywords = any(keyword in text_lower for keyword in schedule_keywords)
        has_travel_keywords = any(keyword in text_lower for keyword in travel_keywords)
        
        # 检查是否有明确的时间地点信息（用于 schedule 判断）
        has_time_info = any(keyword in text_lower for keyword in ["时间", "几点", "点", "分", "上午", "下午", "晚上"])
        has_location_info = any(keyword in text_lower for keyword in ["地点", "地址", "在", "于"])
        
        # 规则优先级：
        # 1. 如果有 task 关键词，优先判为 task
        # 2. 如果有 travel 关键词，判为 travel
        # 3. 如果有 schedule 关键词且有明确时间地点，判为 schedule
        # 4. 否则使用 LLM 结果
        if has_task_keywords:
            return "task"
        elif has_travel_keywords:
            return "travel"
        elif has_schedule_keywords and (has_time_info or has_location_info):
            return "schedule"
        
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
        
        # 增强时间解析
        self._enhance_time_parsing(entities)
        
        # 校验并规范化 suggested_actions
        valid_actions = ["create_todo", "set_reminder", "open_map", "export_calendar"]
        validated_actions = []
        for action in validated_result["suggested_actions"]:
            if action in valid_actions and action not in validated_actions:
                validated_actions.append(action)
        validated_result["suggested_actions"] = validated_actions
        
        return validated_result
    
    def _enhance_time_parsing(self, entities: Dict[str, Any]) -> None:
        """增强时间解析能力"""
        from datetime import datetime, timedelta
        
        # 处理相对时间
        if entities.get("date"):
            date_str = entities["date"]
            
            # 处理相对时间表达式
            today = datetime.now()
            if "今天" in date_str:
                entities["date"] = today.strftime("%Y-%m-%d")
                entities["date_confidence"] = "high"
                entities["needs_user_confirm"] = False
            elif "明天" in date_str:
                tomorrow = today + timedelta(days=1)
                entities["date"] = tomorrow.strftime("%Y-%m-%d")
                entities["date_confidence"] = "high"
                entities["needs_user_confirm"] = False
            elif "后天" in date_str:
                day_after_tomorrow = today + timedelta(days=2)
                entities["date"] = day_after_tomorrow.strftime("%Y-%m-%d")
                entities["date_confidence"] = "high"
                entities["needs_user_confirm"] = False
            elif "本周" in date_str:
                # 本周的开始（周一）
                week_start = today - timedelta(days=today.weekday())
                entities["date"] = week_start.strftime("%Y-%m-%d")
                entities["date_confidence"] = "medium"
                entities["needs_user_confirm"] = True
            elif "下周" in date_str:
                # 下周的开始（周一）
                next_week_start = today + timedelta(days=7 - today.weekday())
                entities["date"] = next_week_start.strftime("%Y-%m-%d")
                entities["date_confidence"] = "medium"
                entities["needs_user_confirm"] = True
            else:
                # 检查日期格式
                try:
                    # 尝试解析日期
                    parsed_date = datetime.strptime(date_str, "%Y-%m-%d")
                    entities["date_confidence"] = "high"
                    entities["needs_user_confirm"] = False
                except ValueError:
                    try:
                        # 尝试解析月日格式
                        parsed_date = datetime.strptime(date_str, "%m-%d")
                        # 不要强行补年份
                        entities["date_confidence"] = "medium"
                        entities["needs_user_confirm"] = True
                    except ValueError:
                        entities["date_confidence"] = "low"
                        entities["needs_user_confirm"] = True
        else:
            # 没有日期信息
            entities["date_confidence"] = "low"
            entities["needs_user_confirm"] = False
        
        # 确保字段存在
        if "date_confidence" not in entities:
            entities["date_confidence"] = "low"
        if "needs_user_confirm" not in entities:
            entities["needs_user_confirm"] = False
    
    def _validate_and_normalize_item(self, item_data: Dict[str, Any]) -> Dict[str, Any]:
        """校验并规范化事项数据"""
        # 确保所有必要字段存在
        validated_item = {
            "scene_type": item_data.get("scene_type", "other"),
            "summary": item_data.get("summary", ""),
            "entities": item_data.get("entities", {}),
            "suggested_actions": item_data.get("suggested_actions", [])
        }
        
        # 校验场景类型
        valid_scene_types = ["schedule", "task", "travel", "other"]
        if validated_item["scene_type"] not in valid_scene_types:
            validated_item["scene_type"] = "other"
        
        # 校验并规范化 entities
        entities = validated_item["entities"]
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
        
        # 增强时间解析
        self._enhance_time_parsing(entities)
        
        # 校验并规范化 suggested_actions
        valid_actions = ["create_todo", "set_reminder", "open_map", "export_calendar"]
        validated_actions = []
        for action in validated_item["suggested_actions"]:
            if action in valid_actions and action not in validated_actions:
                validated_actions.append(action)
        validated_item["suggested_actions"] = validated_actions
        
        return validated_item
    
    def _generate_action_plan(self, result: Dict[str, Any]) -> List[ActionPlanItem]:
        """生成 action plan"""
        action_plan = []
        entities = result.get("entities", {})
        
        # 根据 suggested_actions 生成 action plan
        for action in result.get("suggested_actions", []):
            if action == "create_todo":
                # 生成创建待办事项的 action plan
                title = entities.get("title", entities.get("task_name", "未命名任务"))
                deadline = entities.get("deadline")
                
                # 校验：至少需要 title
                if title:
                    action_plan.append(ActionPlanItem(
                        action_type="create_todo",
                        label="创建待办",
                        payload={
                            "title": title,
                            "deadline": deadline
                        },
                        is_valid=True
                    ))
            
            elif action == "set_reminder":
                # 生成设置提醒的 action plan
                title = entities.get("title", entities.get("task_name", "未命名任务"))
                
                # 优先使用 deadline，然后使用 date + start_time
                remind_at = entities.get("deadline")
                if not remind_at and entities.get("date") and entities.get("start_time"):
                    remind_at = f"{entities['date']} {entities['start_time']}"
                
                # 校验：必须有 remind_at
                is_valid = bool(remind_at)
                action_plan.append(ActionPlanItem(
                    action_type="set_reminder",
                    label="设置提醒",
                    payload={
                        "title": title,
                        "remind_at": remind_at
                    },
                    is_valid=is_valid
                ))
            
            elif action == "open_map":
                # 生成打开地图的 action plan
                location = entities.get("location")
                address = entities.get("address")
                
                # 校验：必须有 location 或 address
                is_valid = bool(location or address)
                action_plan.append(ActionPlanItem(
                    action_type="open_map",
                    label="打开地图",
                    payload={
                        "location": location,
                        "address": address
                    },
                    is_valid=is_valid
                ))
            
            elif action == "export_calendar":
                # 生成导出日历的 action plan
                title = entities.get("title", "未命名事件")
                date = entities.get("date")
                start_time = entities.get("start_time")
                end_time = entities.get("end_time")
                location = entities.get("location")
                
                # 校验：必须有 title、date、start_time
                is_valid = bool(title and date and start_time)
                action_plan.append(ActionPlanItem(
                    action_type="export_calendar",
                    label="导出日历",
                    payload={
                        "title": title,
                        "date": date,
                        "start_time": start_time,
                        "end_time": end_time,
                        "location": location
                    },
                    is_valid=is_valid
                ))
        
        return action_plan
    
    def update_parse_item(self, item_id: str, update_data: Dict[str, Any], db: Session) -> Dict[str, Any]:
        """更新单个事项"""
        # 查找事项
        item = db.query(ParseItem).filter(ParseItem.item_id == item_id).first()
        if not item:
            raise ValueError("Item not found")
        
        # 校验并规范化数据
        validated_item = self._validate_and_normalize_item(update_data)
        
        # 生成 action plan
        action_plan = self._generate_action_plan(validated_item)
        
        # 更新字段
        item.scene_type = validated_item["scene_type"]
        item.summary = validated_item["summary"]
        item.entities_json = json.dumps(validated_item["entities"])
        item.suggested_actions_json = json.dumps(validated_item["suggested_actions"])
        item.action_plan_json = json.dumps([action.model_dump() for action in action_plan])
        
        db.commit()
        db.refresh(item)
        
        # 构建响应
        response_item = {
            "item_id": item.item_id,
            "scene_type": item.scene_type,
            "summary": item.summary,
            "entities": json.loads(item.entities_json),
            "suggested_actions": json.loads(item.suggested_actions_json),
            "action_plan": json.loads(item.action_plan_json)
        }
        
        return {
            "success": True,
            "message": "Item updated successfully",
            "data": response_item
        }