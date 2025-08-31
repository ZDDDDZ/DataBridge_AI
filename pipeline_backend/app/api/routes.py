"""
API路由定义
定义所有的HTTP API端点
"""

import logging
from typing import Dict, Any
from fastapi import APIRouter, HTTPException, Query, Body
from fastapi.responses import JSONResponse
from ..models.schemas import QueryRequest, QueryResponse, ErrorResponse
from ..services.sql_generator import SQLGenerator

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建路由器
router = APIRouter()

# 初始化SQL生成器
try:
    sql_generator = SQLGenerator()
    logger.info("API路由初始化完成")
except Exception as e:
    logger.error(f"API路由初始化失败: {e}")
    sql_generator = None


@router.get("/health")
async def health_check():
    """健康检查接口"""
    return {"status": "healthy", "message": "管道信息系统API运行正常"}


@router.get("/database/info")
async def get_database_info():
    """获取数据库信息接口"""
    try:
        if not sql_generator:
            raise HTTPException(status_code=500, detail="服务未正确初始化")
        
        info = sql_generator.get_database_info()
        return info
    except Exception as e:
        logger.error(f"获取数据库信息失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    """
    处理自然语言查询请求
    
    Args:
        request: 查询请求对象
        
    Returns:
        QueryResponse: 查询响应
    """
    try:
        if not sql_generator:
            raise HTTPException(status_code=500, detail="服务未正确初始化")
        
        # 验证问题
        validation = sql_generator.validate_question(request.question)
        if not validation["is_valid"]:
            raise HTTPException(
                status_code=400, 
                detail=f"问题验证失败: {', '.join(validation['errors'])}"
            )
        
        # 处理查询
        response = sql_generator.process_query(request)
        
        if response.status == "error":
            raise HTTPException(status_code=400, detail=response.message)
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"查询处理异常: {e}")
        raise HTTPException(status_code=500, detail=f"服务器内部错误: {str(e)}")


@router.get("/suggestions")
async def get_query_suggestions(q: str = Query(default="", description="部分查询文本")):
    """
    获取查询建议
    
    Args:
        q: 部分查询文本
        
    Returns:
        Dict: 查询建议列表
    """
    try:
        if not sql_generator:
            raise HTTPException(status_code=500, detail="服务未正确初始化")
        
        suggestions = sql_generator.get_suggestions(q)
        return {"suggestions": suggestions}
        
    except Exception as e:
        logger.error(f"获取查询建议失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/examples")
async def get_query_examples():
    """
    获取查询示例
    
    Returns:
        Dict: 分类的查询示例
    """
    try:
        if not sql_generator:
            raise HTTPException(status_code=500, detail="服务未正确初始化")
        
        examples = sql_generator.get_query_examples()
        return examples
        
    except Exception as e:
        logger.error(f"获取查询示例失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/validate")
async def validate_question(request: Dict[str, str] = Body(...)):
    """
    验证问题的有效性
    
    Args:
        request: 包含问题的请求体
        
    Returns:
        Dict: 验证结果
    """
    try:
        if not sql_generator:
            raise HTTPException(status_code=500, detail="服务未正确初始化")
        
        question = request.get("question", "")
        if not question:
            raise HTTPException(status_code=400, detail="缺少问题参数")
        
        validation = sql_generator.validate_question(question)
        return validation
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"问题验证失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats")
async def get_database_stats():
    """
    获取数据库统计信息
    
    Returns:
        Dict: 数据库统计信息
    """
    try:
        if not sql_generator:
            raise HTTPException(status_code=500, detail="服务未正确初始化")
        
        info = sql_generator.get_database_info()
        if info["status"] != "connected":
            raise HTTPException(status_code=503, detail=info["message"])
        
        return info["stats"]
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取统计信息失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# 注意：异常处理器应该在主应用中定义，而不是在路由中
# 这里移除了错误的异常处理器定义 