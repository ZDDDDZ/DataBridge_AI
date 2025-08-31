"""
管道信息系统配置模块
负责加载和管理所有系统配置
"""

import os
from typing import List
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


class Config:
    """系统配置类"""
    
    # 数据库配置
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: int = int(os.getenv("DB_PORT", "3306"))
    DB_USER: str = os.getenv("DB_USER", "root")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "your_password")
    DB_NAME: str = os.getenv("DB_NAME", "pipeline_management")
    
    # 阿里云百炼大模型配置
    DASHSCOPE_API_KEY: str = os.getenv("DASHSCOPE_API_KEY", "")
    
    # 应用配置
    API_PREFIX: str = os.getenv("API_PREFIX", "/api/v1")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")
    
    # CORS配置
    CORS_ORIGINS: List[str] = os.getenv(
        "CORS_ORIGINS", 
        "http://localhost:8080,http://127.0.0.1:8080"
    ).split(",")
    
    # 服务配置
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    
    # 数据库URL构建
    @property
    def database_url(self) -> str:
        """构建数据库连接URL"""
        return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    @classmethod
    def validate_config(cls) -> bool:
        """验证配置是否完整"""
        config = cls()
        
        # 检查必要配置
        required_configs = [
            ("DB_HOST", config.DB_HOST),
            ("DB_USER", config.DB_USER),
            ("DB_PASSWORD", config.DB_PASSWORD),
            ("DB_NAME", config.DB_NAME),
            ("DASHSCOPE_API_KEY", config.DASHSCOPE_API_KEY)
        ]
        
        missing_configs = []
        for config_name, config_value in required_configs:
            if not config_value or config_value == "your_password":
                missing_configs.append(config_name)
        
        if missing_configs:
            print(f"缺少必要配置: {', '.join(missing_configs)}")
            return False
        
        return True


# 配置实例
config = Config() 