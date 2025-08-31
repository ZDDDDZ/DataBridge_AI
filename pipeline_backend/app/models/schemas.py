"""
数据模型定义
使用Pydantic进行数据验证和序列化
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class QueryRequest(BaseModel):
    """查询请求模型"""
    question: str = Field(..., description="用户查询问题", min_length=1, max_length=500)
    
    class Config:
        json_schema_extra = {
            "example": {
                "question": "查询广东省的燃气管道数量"
            }
        }


class PipelineInfo(BaseModel):
    """管道信息模型"""
    id: int = Field(..., description="主键ID")
    province: str = Field(..., description="省份")
    city: str = Field(..., description="城市")
    street: Optional[str] = Field(None, description="街道")
    road: Optional[str] = Field(None, description="道路")
    location: Optional[str] = Field(None, description="具体位置")
    disaster_type: Optional[str] = Field(None, description="灾害类型")
    geological_feature: Optional[str] = Field(None, description="地质特性")
    pipeline_type: str = Field(..., description="管线类型")
    build_year: Optional[int] = Field(None, description="建成年份")
    laying_method: Optional[str] = Field(None, description="敷设方式")
    created_at: Optional[datetime] = Field(None, description="创建时间")
    updated_at: Optional[datetime] = Field(None, description="更新时间")
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "province": "广东",
                "city": "广州",
                "street": "中心街",
                "road": "一号路",
                "location": "中心街与一号路交叉口北侧100米",
                "disaster_type": "无明显灾害",
                "geological_feature": "砂质土",
                "pipeline_type": "燃气管道",
                "build_year": 2020,
                "laying_method": "直埋"
            }
        }


class QueryResponse(BaseModel):
    """查询响应模型"""
    status: str = Field(..., description="响应状态", pattern="^(success|error)$")
    message: Optional[str] = Field(None, description="响应消息")
    data: Optional[List[Dict[str, Any]]] = Field(None, description="查询结果数据")
    sql: Optional[str] = Field(None, description="生成的SQL语句")
    count: Optional[int] = Field(None, description="结果数量")
    execution_time: Optional[float] = Field(None, description="执行时间(秒)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "success",
                "message": "查询成功",
                "data": [
                    {
                        "id": 1,
                        "province": "广东",
                        "city": "广州",
                        "pipeline_type": "燃气管道"
                    }
                ],
                "sql": "SELECT * FROM pipeline_info WHERE province = '广东' AND pipeline_type = '燃气管道'",
                "count": 1,
                "execution_time": 0.123
            }
        }


class DatabaseStats(BaseModel):
    """数据库统计信息模型"""
    total_pipelines: int = Field(..., description="管道总数")
    provinces_count: int = Field(..., description="省份数量")
    cities_count: int = Field(..., description="城市数量")
    pipeline_types: Dict[str, int] = Field(..., description="管道类型统计")
    disaster_types: Dict[str, int] = Field(..., description="灾害类型统计")
    yearly_distribution: Dict[str, int] = Field(..., description="年份分布")
    
    class Config:
        json_schema_extra = {
            "example": {
                "total_pipelines": 1000,
                "provinces_count": 10,
                "cities_count": 80,
                "pipeline_types": {
                    "燃气管道": 150,
                    "供水管道": 200,
                    "排水管道": 180
                },
                "disaster_types": {
                    "无明显灾害": 800,
                    "地震": 50,
                    "洪水": 30
                },
                "yearly_distribution": {
                    "2020": 100,
                    "2021": 120,
                    "2022": 110
                }
            }
        }


class ErrorResponse(BaseModel):
    """错误响应模型"""
    status: str = Field(default="error", description="响应状态")
    message: str = Field(..., description="错误信息")
    error_code: Optional[str] = Field(None, description="错误代码")
    details: Optional[Dict[str, Any]] = Field(None, description="错误详情")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "error",
                "message": "数据库连接失败",
                "error_code": "DB_CONNECTION_ERROR",
                "details": {
                    "host": "localhost",
                    "port": 3306
                }
            }
        } 