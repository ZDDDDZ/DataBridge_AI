-- 管道信息系统数据库初始化脚本
-- 创建数据库
CREATE DATABASE IF NOT EXISTS pipeline_management CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE pipeline_management;

-- 创建管道信息表
CREATE TABLE IF NOT EXISTS pipeline_info (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    province VARCHAR(50) NOT NULL COMMENT '省份',
    city VARCHAR(50) NOT NULL COMMENT '城市',
    street VARCHAR(100) COMMENT '街道',
    road VARCHAR(100) COMMENT '道路',
    location VARCHAR(255) COMMENT '具体位置',
    disaster_type VARCHAR(50) COMMENT '灾害类型',
    geological_feature VARCHAR(100) COMMENT '地质特性',
    pipeline_type VARCHAR(50) NOT NULL COMMENT '管线类型',
    build_year INT COMMENT '建成年份',
    laying_method VARCHAR(50) COMMENT '敷设方式',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='管道信息表';

-- 创建索引以提高查询性能
CREATE INDEX idx_province_city ON pipeline_info(province, city);
CREATE INDEX idx_pipeline_type ON pipeline_info(pipeline_type);
CREATE INDEX idx_build_year ON pipeline_info(build_year);
CREATE INDEX idx_disaster_type ON pipeline_info(disaster_type); 