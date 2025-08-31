#!/usr/bin/env python3
"""
管道信息模拟数据生成脚本
生成真实可信的管道信息数据用于系统测试
"""

import mysql.connector
import random
from datetime import datetime
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 数据库连接配置
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "127.0.0.1"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "123456"),
    "database": os.getenv("DB_NAME", "pipeline_management"),
    "charset": "utf8mb4"
}

# 模拟数据定义
PROVINCES = ["北京", "上海", "广东", "浙江", "江苏", "四川", "湖北", "山东", "河南", "湖南"]

CITIES = {
    "北京": ["朝阳区", "海淀区", "丰台区", "西城区", "东城区", "石景山区", "通州区", "昌平区"],
    "上海": ["浦东新区", "黄浦区", "静安区", "徐汇区", "长宁区", "虹口区", "杨浦区", "闵行区"],
    "广东": ["广州", "深圳", "珠海", "佛山", "东莞", "中山", "惠州", "江门"],
    "浙江": ["杭州", "宁波", "温州", "嘉兴", "湖州", "绍兴", "金华", "台州"],
    "江苏": ["南京", "苏州", "无锡", "常州", "镇江", "南通", "泰州", "扬州"],
    "四川": ["成都", "绵阳", "德阳", "自贡", "宜宾", "泸州", "达州", "乐山"],
    "湖北": ["武汉", "黄石", "襄阳", "宜昌", "十堰", "荆州", "荆门", "鄂州"],
    "山东": ["济南", "青岛", "烟台", "威海", "潍坊", "淄博", "东营", "济宁"],
    "河南": ["郑州", "洛阳", "开封", "平顶山", "新乡", "焦作", "许昌", "漯河"],
    "湖南": ["长沙", "株洲", "湘潭", "衡阳", "邵阳", "岳阳", "常德", "张家界"]
}

STREETS = [
    "中心街", "文化路", "新华街", "解放路", "建设大道", "和平路", 
    "友谊大街", "长江路", "黄河路", "人民大道", "工业路", "商业街",
    "科技路", "学府路", "环城路", "滨河路", "花园路", "体育路"
]

ROADS = [
    "一号路", "二号路", "三号路", "四号路", "主干道", "辅路", 
    "环线", "联络道", "快速路", "高架路", "隧道", "立交桥"
]

DISASTER_TYPES = [
    "地震", "洪水", "滑坡", "塌陷", "冻土融化", "台风", "暴雨", 
    "干旱", "泥石流", "地面沉降", "无明显灾害"
]

GEOLOGICAL_FEATURES = [
    "砂质土", "粘土", "岩石", "软土", "硬土", "沙土", "碎石", 
    "黏土夹砂", "卵石层", "花岗岩", "石灰岩", "砂岩"
]

PIPELINE_TYPES = [
    "供水管道", "排水管道", "燃气管道", "热力管道", "电力管线", 
    "通信管线", "石油管道", "化工管道", "污水管道", "雨水管道"
]

LAYING_METHODS = [
    "直埋", "架空", "沟槽", "盾构", "顶管", "定向钻", 
    "悬吊", "综合管廊", "明挖", "暗挖"
]


def create_connection():
    """创建数据库连接"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        print("数据库连接成功")
        return connection
    except mysql.connector.Error as e:
        print(f"数据库连接失败: {e}")
        return None


def generate_location(street, road):
    """生成具体位置描述"""
    locations = [
        f"{street}与{road}交叉口北侧{random.randint(10, 500)}米",
        f"{street}与{road}交叉口南侧{random.randint(10, 500)}米", 
        f"{street}与{road}交叉口东侧{random.randint(10, 500)}米",
        f"{street}与{road}交叉口西侧{random.randint(10, 500)}米",
        f"{street}{random.randint(1, 999)}号附近",
        f"{road}沿线{random.randint(1, 50)}公里处"
    ]
    return random.choice(locations)


def generate_mock_data(count=1000):
    """生成模拟数据"""
    connection = create_connection()
    if not connection:
        return False
    
    try:
        cursor = connection.cursor()
        
        # 清空现有数据（可选）
        # cursor.execute("TRUNCATE TABLE pipeline_info")
        
        print(f"开始生成{count}条模拟数据...")
        
        for i in range(count):
            # 随机选择省份和对应城市
            province = random.choice(PROVINCES)
            city = random.choice(CITIES[province])
            street = random.choice(STREETS)
            road = random.choice(ROADS)
            location = generate_location(street, road)
            
            # 灾害类型权重分配（大部分地区无明显灾害）
            disaster_weights = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 10]  # "无明显灾害"权重更高
            disaster_type = random.choices(DISASTER_TYPES, weights=disaster_weights)[0]
            
            geological_feature = random.choice(GEOLOGICAL_FEATURES)
            pipeline_type = random.choice(PIPELINE_TYPES)
            
            # 建成年份分布（近年来建设较多）
            year_weights = []
            for year in range(1980, 2024):
                if year >= 2000:
                    year_weights.append(3)  # 2000年后权重更高
                elif year >= 1990:
                    year_weights.append(2)
                else:
                    year_weights.append(1)
            
            build_year = random.choices(range(1980, 2024), weights=year_weights)[0]
            laying_method = random.choice(LAYING_METHODS)
            
            # 插入数据
            query = """
            INSERT INTO pipeline_info 
            (province, city, street, road, location, disaster_type, geological_feature, 
            pipeline_type, build_year, laying_method)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            values = (
                province, city, street, road, location, disaster_type,
                geological_feature, pipeline_type, build_year, laying_method
            )
            
            cursor.execute(query, values)
            
            # 每100条提交一次
            if (i + 1) % 100 == 0:
                connection.commit()
                print(f"已生成 {i + 1} 条数据")
        
        # 最终提交
        connection.commit()
        print(f"成功生成并插入 {count} 条模拟数据")
        
        # 显示统计信息
        cursor.execute("SELECT COUNT(*) FROM pipeline_info")
        total_count = cursor.fetchone()[0]
        print(f"数据库中总计有 {total_count} 条管道信息记录")
        
        return True
        
    except mysql.connector.Error as e:
        print(f"数据插入失败: {e}")
        connection.rollback()
        return False
        
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("数据库连接已关闭")


def main():
    """主函数"""
    print("=== 管道信息模拟数据生成器 ===")
    
    # 检查数据库连接
    connection = create_connection()
    if not connection:
        print("无法连接到数据库，请检查配置")
        return
    connection.close()
    
    # 生成数据
    count = int(input("请输入要生成的数据条数 (默认1000): ") or "1000")
    
    if generate_mock_data(count):
        print("数据生成完成！")
    else:
        print("数据生成失败！")


if __name__ == "__main__":
    main() 