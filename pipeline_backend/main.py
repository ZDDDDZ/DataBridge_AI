"""
管道信息智能查询系统 - 主应用入口
FastAPI 后端服务
"""

import logging
import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from app.api.routes import router
from config import config

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时
    logger.info("=== 管道信息智能查询系统启动 ===")
    logger.info(f"调试模式: {config.DEBUG}")
    logger.info(f"数据库主机: {config.DB_HOST}:{config.DB_PORT}")
    logger.info(f"数据库名称: {config.DB_NAME}")
    
    # 验证配置
    if not config.validate_config():
        logger.error("配置验证失败，请检查环境变量")
        raise RuntimeError("配置验证失败")
    
    yield
    
    # 关闭时
    logger.info("=== 系统正在关闭 ===")


# 创建FastAPI应用
app = FastAPI(
    title="管道信息智能查询系统",
    description="基于大语言模型的管道信息自然语言查询系统",
    version="1.0.0",
    docs_url="/docs" if config.DEBUG else None,
    redoc_url="/redoc" if config.DEBUG else None,
    lifespan=lifespan
)

# 配置CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


# 全局异常处理器
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """全局异常处理"""
    logger.error(f"全局异常: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": "服务器内部错误",
            "detail": str(exc) if config.DEBUG else "请联系系统管理员"
        }
    )


# 根路径
@app.get("/")
async def root():
    """根路径欢迎信息"""
    return {
        "message": "欢迎使用管道信息智能查询系统",
        "version": "1.0.0",
        "docs": "/docs" if config.DEBUG else "文档在生产环境中不可用",
        "api": config.API_PREFIX
    }


# 注册API路由
app.include_router(router, prefix=config.API_PREFIX, tags=["管道查询API"])


# 健康检查（独立于API前缀）
@app.get("/health")
async def health_check():
    """系统健康检查"""
    return {
        "status": "healthy",
        "system": "管道信息智能查询系统",
        "version": "1.0.0"
    }


if __name__ == "__main__":
    # 开发环境启动
    logger.info(f"启动服务 - 地址: {config.HOST}:{config.PORT}")
    
    uvicorn.run(
        "main:app",
        host=config.HOST,
        port=config.PORT,
        reload=config.DEBUG,
        log_level="info" if config.DEBUG else "warning"
    ) 