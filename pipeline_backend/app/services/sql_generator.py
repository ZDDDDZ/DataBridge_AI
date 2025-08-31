"""
SQL生成器模块
整合LLM服务和数据库服务，提供完整的查询处理流程
"""

import time
import logging
from typing import Dict, Any, Optional
from .llm_service import LLMService
from .database_service import DatabaseService
from ..models.schemas import QueryRequest, QueryResponse

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SQLGenerator:
    """SQL生成器类"""
    
    def __init__(self):
        """初始化SQL生成器"""
        try:
            self.llm_service = LLMService()
            self.db_service = DatabaseService()
            logger.info("SQL生成器初始化完成")
        except Exception as e:
            logger.error(f"SQL生成器初始化失败: {e}")
            raise
    
    def process_query(self, query_request: QueryRequest) -> QueryResponse:
        """
        处理用户查询请求
        
        Args:
            query_request: 查询请求对象
            
        Returns:
            QueryResponse: 查询响应对象
        """
        start_time = time.time()
        question = query_request.question.strip()
        
        logger.info(f"开始处理查询: {question}")
        
        try:
            # 1. 生成SQL语句
            sql = self.llm_service.generate_sql_from_question(question)
            if not sql:
                return QueryResponse(
                    status="error",
                    message="无法理解您的问题，请换一种表达方式",
                    execution_time=time.time() - start_time
                )
            
            # 2. 验证SQL安全性
            if not self.db_service.validate_sql(sql):
                return QueryResponse(
                    status="error",
                    message="生成的查询不符合安全要求",
                    sql=sql,
                    execution_time=time.time() - start_time
                )
            
            # 3. 优化SQL语句
            optimized_sql = self.llm_service.optimize_sql(sql)
            
            # 4. 执行查询
            results, query_execution_time = self.db_service.execute_query(optimized_sql)
            
            # 5. 格式化结果
            formatted_results = self.db_service.format_results(results)
            
            total_time = time.time() - start_time
            
            logger.info(f"查询处理完成，返回 {len(formatted_results)} 条结果，总耗时 {total_time:.3f} 秒")
            
            return QueryResponse(
                status="success",
                message="查询成功",
                data=formatted_results,
                sql=optimized_sql,
                count=len(formatted_results),
                execution_time=total_time
            )
            
        except Exception as e:
            error_time = time.time() - start_time
            logger.error(f"查询处理失败: {e}")
            
            return QueryResponse(
                status="error",
                message=f"查询执行失败: {str(e)}",
                execution_time=error_time
            )
    
    def get_suggestions(self, partial_question: str) -> list:
        """
        根据部分问题提供查询建议
        
        Args:
            partial_question: 部分问题文本
            
        Returns:
            list: 建议列表
        """
        # 预定义的查询建议
        suggestions = [
            "查询广东省的燃气管道数量",
            "统计各省市管道类型分布情况", 
            "2010年以后建成的供水管道有哪些？",
            "地震灾害地区的管道统计",
            "按敷设方式统计管道数量",
            "查询北京市的电力管线",
            "统计近5年建设的热力管道",
            "软土地质条件下的管道分布",
            "查询直埋敷设的管道总数",
            "按灾害类型分析管道风险分布"
        ]
        
        # 根据输入的部分文本进行过滤
        if not partial_question.strip():
            return suggestions[:5]  # 返回前5个建议
        
        filtered_suggestions = []
        keywords = partial_question.lower().split()
        
        for suggestion in suggestions:
            suggestion_lower = suggestion.lower()
            if any(keyword in suggestion_lower for keyword in keywords):
                filtered_suggestions.append(suggestion)
        
        # 如果没有匹配的建议，返回默认建议
        if not filtered_suggestions:
            return suggestions[:3]
        
        return filtered_suggestions[:5]
    
    def validate_question(self, question: str) -> Dict[str, Any]:
        """
        验证问题的有效性
        
        Args:
            question: 用户问题
            
        Returns:
            Dict[str, Any]: 验证结果
        """
        validation_result = {
            "is_valid": True,
            "errors": [],
            "warnings": []
        }
        
        # 检查问题长度
        if len(question.strip()) < 2:
            validation_result["is_valid"] = False
            validation_result["errors"].append("问题太短，请输入更详细的问题")
        
        if len(question) > 500:
            validation_result["is_valid"] = False
            validation_result["errors"].append("问题太长，请简化您的问题")
        
        # 检查是否包含敏感词汇
        sensitive_words = ["删除", "修改", "更新", "drop", "delete", "update", "insert"]
        question_lower = question.lower()
        
        for word in sensitive_words:
            if word in question_lower:
                validation_result["is_valid"] = False
                validation_result["errors"].append(f"问题包含不允许的操作: {word}")
        
        # 检查是否包含管道相关关键词
        pipeline_keywords = [
            "管道", "管线", "供水", "排水", "燃气", "热力", "电力", "通信", 
            "省", "市", "灾害", "地质", "年份", "敷设", "统计", "查询"
        ]
        
        has_pipeline_keyword = any(keyword in question for keyword in pipeline_keywords)
        if not has_pipeline_keyword:
            validation_result["warnings"].append("问题似乎与管道信息无关，建议包含相关关键词")
        
        return validation_result
    
    def get_query_examples(self) -> Dict[str, list]:
        """
        获取查询示例
        
        Returns:
            Dict[str, list]: 分类的查询示例
        """
        examples = {
            "统计查询": [
                "统计各省份的管道数量",
                "按管道类型统计总数",
                "统计2020年后建成的管道数量",
                "按敷设方式分组统计"
            ],
            "筛选查询": [
                "查询广东省的燃气管道",
                "查询地震灾害地区的管道",
                "查询2015-2020年间建成的供水管道",
                "查询直埋敷设的电力管线"
            ],
            "分析查询": [
                "分析各地质条件下的管道分布",
                "分析不同灾害类型对管道的影响",
                "分析管道建设年份趋势",
                "分析城市管道密度分布"
            ],
            "复合查询": [
                "查询北京市2020年后建成的燃气管道",
                "统计软土地质且有地震风险的管道数量",
                "查询采用盾构敷设的热力管道分布",
                "分析广东省各城市的管道类型分布"
            ]
        }
        
        return examples
    
    def get_database_info(self) -> Dict[str, Any]:
        """
        获取数据库基本信息
        
        Returns:
            Dict[str, Any]: 数据库信息
        """
        try:
            # 测试数据库连接
            is_connected = self.db_service.test_connection()
            
            if not is_connected:
                return {
                    "status": "disconnected",
                    "message": "数据库连接失败"
                }
            
            # 获取统计信息
            stats = self.db_service.get_database_stats()
            
            return {
                "status": "connected",
                "stats": stats.dict(),
                "message": "数据库连接正常"
            }
            
        except Exception as e:
            logger.error(f"获取数据库信息失败: {e}")
            return {
                "status": "error",
                "message": f"获取数据库信息失败: {str(e)}"
            } 