import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any
from ..core.database import get_db
from ..services.parse_service import ParseService
from ..schemas import ParseResultResponse, ParseResultUpdate, ParseResultCreate

# 配置日志
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

router = APIRouter()
parse_service = ParseService()

@router.post("/{image_id}")
async def parse_image(
    image_id: int,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """解析图片并返回结构化数据"""
    try:
        logger.info(f"开始解析图片，ID: {image_id}")
        result = parse_service.parse_image(image_id, db)
        logger.info(f"解析完成，返回 {len(result.get('items', []))} 个事项")
        return result
    except ValueError as e:
        logger.warning(f"解析失败 - 图片不存在: {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"解析失败 - 内部错误: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/{image_id}")
async def get_parse_result(
    image_id: int,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """获取解析结果"""
    try:
        logger.info(f"获取解析结果，图片 ID: {image_id}")
        result = parse_service.get_parse_result(image_id, db)
        logger.info(f"获取成功，共 {len(result.get('items', []))} 个事项")
        return result
    except ValueError as e:
        logger.warning(f"获取解析结果失败 - 结果不存在: {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"获取解析结果失败 - 内部错误: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.put("/{image_id}")
async def update_parse_result(
    image_id: int,
    update_data: Dict[str, Any],
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """更新解析结果"""
    try:
        logger.info(f"更新解析结果，图片 ID: {image_id}")
        logger.info(f"更新数据: {update_data}")
        result = parse_service.update_parse_result(image_id, update_data, db)
        logger.info(f"更新成功，返回 {len(result.get('items', []))} 个事项")
        return result
    except ValueError as e:
        logger.warning(f"更新解析结果失败 - 结果不存在: {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"更新解析结果失败 - 内部错误: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.put("/item/{item_id}")
async def update_parse_item(
    item_id: str,
    update_data: Dict[str, Any],
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """更新单个事项"""
    try:
        logger.info(f"更新单个事项，事项 ID: {item_id}")
        logger.info(f"更新数据: {update_data}")
        result = parse_service.update_parse_item(item_id, update_data, db)
        logger.info(f"更新成功: {result}")
        return result
    except ValueError as e:
        logger.warning(f"更新单个事项失败 - 事项不存在: {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"更新单个事项失败 - 内部错误: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")