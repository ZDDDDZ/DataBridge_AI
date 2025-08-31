"""
数据库服务模块
提供数据库连接、查询执行和统计功能
"""

import pymysql
import time
import logging
from typing import List, Dict, Any, Optional, Tuple
from contextlib import contextmanager
from ..models.schemas import DatabaseStats
from config import config

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DatabaseService:
    """数据库服务类"""
    
    def __init__(self):
        """初始化数据库服务"""
        self.connection_config = {
            "host": config.DB_HOST,
            "port": config.DB_PORT,
            "user": config.DB_USER,
            "password": config.DB_PASSWORD,
            "database": config.DB_NAME,
            "charset": "utf8mb4",
            "cursorclass": pymysql.cursors.DictCursor,
            "autocommit": True
        }
        
    @contextmanager
    def get_connection(self):
        """获取数据库连接上下文管理器"""
        connection = None
        try:
            connection = pymysql.connect(**self.connection_config)
            logger.info("数据库连接成功")
            yield connection
        except pymysql.Error as e:
            logger.error(f"数据库连接失败: {e}")
            raise
        finally:
            if connection and connection.open:
                connection.close()
                logger.debug("数据库连接已关闭")
    
    def test_connection(self) -> bool:
        """测试数据库连接"""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT 1")
                    result = cursor.fetchone()
                    return result is not None
        except Exception as e:
            logger.error(f"数据库连接测试失败: {e}")
            return False
    
    def execute_query(self, sql: str) -> Tuple[List[Dict[str, Any]], float]:
        """
        执行SQL查询
        
        Args:
            sql: SQL查询语句
            
        Returns:
            Tuple[List[Dict[str, Any]], float]: 查询结果和执行时间
        """
        start_time = time.time()
        
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    logger.info(f"执行SQL: {sql}")
                    cursor.execute(sql)
                    results = cursor.fetchall()
                    
                    execution_time = time.time() - start_time
                    logger.info(f"查询完成，返回 {len(results)} 条记录，耗时 {execution_time:.3f} 秒")
                    
                    return results, execution_time
                    
        except pymysql.Error as e:
            execution_time = time.time() - start_time
            logger.error(f"SQL执行失败: {e}")
            logger.error(f"SQL语句: {sql}")
            raise Exception(f"数据库查询失败: {str(e)}")
    
    def get_table_schema(self) -> List[Dict[str, Any]]:
        """
        获取表结构信息
        
        Returns:
            List[Dict[str, Any]]: 表结构信息
        """
        sql = """
        SELECT 
            COLUMN_NAME as column_name,
            DATA_TYPE as data_type,
            IS_NULLABLE as is_nullable,
            COLUMN_DEFAULT as column_default,
            COLUMN_COMMENT as column_comment
        FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_SCHEMA = %s AND TABLE_NAME = 'pipeline_info'
        ORDER BY ORDINAL_POSITION
        """
        
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql, (config.DB_NAME,))
                    return cursor.fetchall()
        except Exception as e:
            logger.error(f"获取表结构失败: {e}")
            raise
    
    def get_database_stats(self) -> DatabaseStats:
        """
        获取数据库统计信息
        
        Returns:
            DatabaseStats: 数据库统计信息
        """
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    stats = {}
                    
                    # 总管道数量
                    cursor.execute("SELECT COUNT(*) as total FROM pipeline_info")
                    stats['total_pipelines'] = cursor.fetchone()['total']
                    
                    # 省份数量
                    cursor.execute("SELECT COUNT(DISTINCT province) as count FROM pipeline_info")
                    stats['provinces_count'] = cursor.fetchone()['count']
                    
                    # 城市数量
                    cursor.execute("SELECT COUNT(DISTINCT city) as count FROM pipeline_info")
                    stats['cities_count'] = cursor.fetchone()['count']
                    
                    # 管道类型统计
                    cursor.execute("""
                        SELECT pipeline_type, COUNT(*) as count 
                        FROM pipeline_info 
                        GROUP BY pipeline_type 
                        ORDER BY count DESC
                    """)
                    stats['pipeline_types'] = {
                        row['pipeline_type']: row['count'] 
                        for row in cursor.fetchall()
                    }
                    
                    # 灾害类型统计
                    cursor.execute("""
                        SELECT disaster_type, COUNT(*) as count 
                        FROM pipeline_info 
                        WHERE disaster_type IS NOT NULL
                        GROUP BY disaster_type 
                        ORDER BY count DESC
                    """)
                    stats['disaster_types'] = {
                        row['disaster_type']: row['count'] 
                        for row in cursor.fetchall()
                    }
                    
                    # 年份分布统计
                    cursor.execute("""
                        SELECT build_year, COUNT(*) as count 
                        FROM pipeline_info 
                        WHERE build_year IS NOT NULL
                        GROUP BY build_year 
                        ORDER BY build_year DESC
                        LIMIT 10
                    """)
                    stats['yearly_distribution'] = {
                        str(row['build_year']): row['count'] 
                        for row in cursor.fetchall()
                    }
                    
                    return DatabaseStats(**stats)
                    
        except Exception as e:
            logger.error(f"获取数据库统计信息失败: {e}")
            raise
    
    def validate_sql(self, sql: str) -> bool:
        """
        验证SQL语句的安全性
        
        Args:
            sql: SQL语句
            
        Returns:
            bool: 是否安全
        """
        # 转换为小写进行检查
        sql_lower = sql.lower().strip()
        
        # 检查是否包含危险操作
        dangerous_keywords = [
            'drop', 'delete', 'update', 'insert', 'create', 'alter', 
            'truncate', 'grant', 'revoke', 'exec', 'execute'
        ]
        
        for keyword in dangerous_keywords:
            if keyword in sql_lower:
                logger.warning(f"SQL包含危险关键字: {keyword}")
                return False
        
        # 检查是否是SELECT语句
        if not sql_lower.startswith('select'):
            logger.warning("只允许SELECT查询")
            return False
        
        return True
    
    def format_results(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        格式化查询结果
        
        Args:
            results: 原始查询结果
            
        Returns:
            List[Dict[str, Any]]: 格式化后的结果
        """
        formatted_results = []
        
        for row in results:
            formatted_row = {}
            for key, value in row.items():
                # 处理日期时间类型
                if hasattr(value, 'strftime'):
                    formatted_row[key] = value.strftime('%Y-%m-%d %H:%M:%S')
                # 处理None值
                elif value is None:
                    formatted_row[key] = ""
                else:
                    formatted_row[key] = value
            
            formatted_results.append(formatted_row)
        
        return formatted_results 