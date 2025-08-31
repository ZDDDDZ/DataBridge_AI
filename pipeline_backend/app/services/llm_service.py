"""
大语言模型服务模块
集成阿里云百炼大模型，提供自然语言到SQL的转换功能
"""

import json
import logging
from typing import Optional, Dict, Any
import dashscope
from dashscope import Generation
from config import config

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LLMService:
    """大语言模型服务类"""
    
    def __init__(self):
        """初始化LLM服务"""
        self.api_key = config.DASHSCOPE_API_KEY
        if not self.api_key:
            raise ValueError("DASHSCOPE_API_KEY 未配置")
        
        # 设置API密钥
        dashscope.api_key = self.api_key
        
        # 模型配置
        self.model_name = "qwen-max"
        self.max_tokens = 2048
        self.temperature = 0.1  # 降低随机性，提高SQL准确性
        
        # 数据库表结构信息（用于生成更准确的SQL）
        self.schema_info = self._build_schema_info()
        
        logger.info("LLM服务初始化完成")
    
    def _build_schema_info(self) -> str:
        """构建数据库表结构信息"""
        schema_info = """
数据库表结构信息：

表名: pipeline_info (管道信息表)

字段说明：
- id (INT): 主键ID
- province (VARCHAR): 省份 (必填)
- city (VARCHAR): 城市 (必填) 
- street (VARCHAR): 街道
- road (VARCHAR): 道路
- location (VARCHAR): 具体位置
- disaster_type (VARCHAR): 灾害类型 (如：地震、洪水、滑坡、塌陷、台风、暴雨、无明显灾害等)
- geological_feature (VARCHAR): 地质特性 (如：砂质土、粘土、岩石、软土等)
- pipeline_type (VARCHAR): 管线类型 (必填，如：供水管道、排水管道、燃气管道、热力管道、电力管线、通信管线等)
- build_year (INT): 建成年份
- laying_method (VARCHAR): 敷设方式 (如：直埋、架空、沟槽、盾构、顶管等)
- created_at (TIMESTAMP): 创建时间
- updated_at (TIMESTAMP): 更新时间

常见的查询需求：
1. 按省份/城市统计管道数量
2. 按管道类型分类统计
3. 按建成年份范围查询
4. 按灾害类型筛选
5. 按敷设方式分组统计
6. 地质特性分析
7. 复合条件查询

注意事项：
- 只生成SELECT查询语句
- 字段名使用表中的实际字段名
- 字符串值使用单引号
- 年份范围查询使用BETWEEN或比较操作符
- 统计查询使用COUNT、GROUP BY等聚合函数
"""
        return schema_info
    
    def generate_sql_from_question(self, question: str) -> Optional[str]:
        """
        根据自然语言问题生成SQL查询语句
        
        Args:
            question: 用户的自然语言问题
            
        Returns:
            Optional[str]: 生成的SQL语句，失败时返回None
        """
        try:
            # 构建提示词
            prompt = self._build_prompt(question)
            
            # 调用大模型
            response = Generation.call(
                model=self.model_name,
                prompt=prompt,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                top_p=0.8
            )
            
            if response.status_code == 200:
                # 提取SQL语句
                sql = self._extract_sql_from_response(response.output.text)
                logger.info(f"成功生成SQL: {sql}")
                return sql
            else:
                logger.error(f"大模型调用失败: {response.status_code}, {response.message}")
                return None
                
        except Exception as e:
            logger.error(f"生成SQL失败: {e}")
            return None
    
    def _build_prompt(self, question: str) -> str:
        """
        构建发送给大模型的提示词
        
        Args:
            question: 用户问题
            
        Returns:
            str: 构建的提示词
        """
        prompt = f"""
你是一个专业的SQL查询生成助手，根据用户的自然语言问题生成对应的MySQL查询语句。

{self.schema_info}

用户问题: {question}

请根据上述数据库表结构信息，生成一个有效的MySQL SELECT查询语句。

要求：
1. 只生成SELECT查询语句，不要包含其他SQL操作
2. 使用正确的字段名和表名
3. 适当使用WHERE、GROUP BY、ORDER BY、LIMIT等子句
4. 如果是统计查询，使用COUNT()、SUM()等聚合函数
5. 字符串值使用单引号包围
6. 只返回SQL语句本身，不要包含任何解释或markdown格式

SQL语句:
"""
        return prompt
    
    def _extract_sql_from_response(self, response_text: str) -> str:
        """
        从大模型响应中提取SQL语句
        
        Args:
            response_text: 大模型返回的文本
            
        Returns:
            str: 提取的SQL语句
        """
        # 移除可能的markdown格式
        sql = response_text.strip()
        
        # 移除```sql 和 ```
        if sql.startswith("```sql"):
            sql = sql[6:]
        if sql.startswith("```"):
            sql = sql[3:]
        if sql.endswith("```"):
            sql = sql[:-3]
        
        # 移除多余的空白字符
        sql = sql.strip()
        
        # 确保SQL以SELECT开头
        if not sql.upper().startswith("SELECT"):
            # 尝试找到SELECT语句
            lines = sql.split('\n')
            for line in lines:
                line = line.strip()
                if line.upper().startswith("SELECT"):
                    sql = line
                    break
        
        # 移除末尾的分号
        if sql.endswith(';'):
            sql = sql[:-1]
        
        return sql
    
    def analyze_question_intent(self, question: str) -> Dict[str, Any]:
        """
        分析用户问题的意图
        
        Args:
            question: 用户问题
            
        Returns:
            Dict[str, Any]: 意图分析结果
        """
        intent_prompt = f"""
分析以下用户问题的查询意图，返回JSON格式的分析结果：

用户问题: {question}

请分析并返回以下信息的JSON格式：
{{
    "intent_type": "统计查询|详细查询|筛选查询|分析查询",
    "target_fields": ["相关字段列表"],
    "conditions": ["查询条件列表"], 
    "aggregation": "是否需要聚合统计",
    "confidence": "置信度(0-1)"
}}
"""
        
        try:
            response = Generation.call(
                model=self.model_name,
                prompt=intent_prompt,
                max_tokens=512,
                temperature=0.1
            )
            
            if response.status_code == 200:
                # 尝试解析JSON
                try:
                    intent_info = json.loads(response.output.text)
                    return intent_info
                except json.JSONDecodeError:
                    logger.warning("意图分析结果不是有效的JSON格式")
                    return {"intent_type": "未知", "confidence": 0.0}
            else:
                logger.error(f"意图分析失败: {response.message}")
                return {"intent_type": "未知", "confidence": 0.0}
                
        except Exception as e:
            logger.error(f"意图分析异常: {e}")
            return {"intent_type": "未知", "confidence": 0.0}
    
    def optimize_sql(self, sql: str) -> str:
        """
        优化生成的SQL语句
        
        Args:
            sql: 原始SQL语句
            
        Returns:
            str: 优化后的SQL语句
        """
        # 基本的SQL优化规则
        optimized_sql = sql.strip()
        
        # 添加LIMIT限制（防止返回过多数据）
        if "LIMIT" not in optimized_sql.upper() and "COUNT" not in optimized_sql.upper():
            optimized_sql += " LIMIT 1000"
        
        # 确保字段名正确
        # 这里可以添加更多的优化逻辑
        
        return optimized_sql 