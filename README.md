# 管道信息智能查询系统

## 项目简介

管道信息智能查询系统是一个基于大语言模型技术的智能数据查询平台。用户可以通过自然语言输入查询问题，系统会自动理解用户意图，生成相应的SQL查询语句，并将查询结果以表格和图表的形式直观展示。

## 系统架构

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   前端 (Vue3)   │    │  后端 (FastAPI) │    │  数据库 (MySQL) │
│                 │    │                 │    │                 │
│ • Ant Design    │◄──►│ • LangChain     │◄──►│ • 管道信息表    │
│ • ECharts       │    │ • 阿里云百炼    │    │ • 索引优化      │
│ • Pinia         │    │ • Pydantic      │    │ • 模拟数据      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 技术栈

### 前端
- **框架**: Vue 3 + Composition API
- **UI库**: Ant Design Vue 4.x
- **状态管理**: Pinia
- **图表库**: Apache ECharts
- **构建工具**: Vue CLI

### 后端
- **框架**: FastAPI + Python 3.8+
- **AI框架**: LangChain
- **大语言模型**: 阿里云百炼大模型 (Qwen-Max)
- **数据库**: MySQL 8.0
- **ORM**: PyMySQL

### 数据库
- **MySQL 8.0**: 主数据库
- **表结构**: 管道信息表 (pipeline_info)
- **数据量**: 支持千万级数据查询

## 主要功能

- ✨ **自然语言查询**: 支持中文自然语言输入，无需学习SQL语法
- 🤖 **智能SQL生成**: 基于大语言模型自动生成精确的SQL查询语句
- 📊 **多维度可视化**: 支持表格、饼图、柱状图、折线图等展示方式
- 📝 **查询历史**: 自动保存查询历史，支持快速重复查询
- 💾 **数据导出**: 支持查询结果导出为JSON格式
- 🔍 **实时搜索**: 表格内容实时搜索和过滤
- 📱 **响应式设计**: 适配桌面和移动端设备

## 快速开始

### 环境要求

- Node.js 16+ 
- Python 3.8+
- MySQL 8.0+
- 阿里云百炼大模型API密钥

### 1. 数据库初始化

```bash
# 连接到MySQL
mysql -u root -p

# 执行数据库初始化脚本
source database/init.sql

# 生成模拟数据
cd database
python mock_data.py
```

### 2. 后端启动

```bash
cd pipeline_backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填入数据库和API配置

# 启动后端服务
python main.py
```

后端服务将在 `http://localhost:8000` 启动

### 3. 前端启动

```bash
cd pipeline-frontend

# 安装依赖
npm install

# 启动开发服务器
npm run serve
```

前端应用将在 `http://localhost:8080` 启动

### 4. 环境变量配置

#### 后端环境变量 (pipeline_backend/.env)

```env
# 数据库配置
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=pipeline_management

# 阿里云百炼大模型配置
DASHSCOPE_API_KEY=your_dashscope_api_key

# 应用配置
API_PREFIX=/api/v1
DEBUG=True
CORS_ORIGINS=http://localhost:8080,http://127.0.0.1:8080
```

#### 前端环境变量 (pipeline-frontend/.env)

```env
VUE_APP_API_URL=http://localhost:8000/api/v1
```

## 使用示例

### 自然语言查询示例

1. **统计查询**:
   - "查询广东省的燃气管道数量"
   - "统计各省市管道类型分布情况"
   - "按敷设方式统计管道数量"

2. **筛选查询**:
   - "查询2010年以后建成的供水管道"
   - "地震灾害地区的管道统计"
   - "查询直埋敷设的电力管线"

3. **复合查询**:
   - "查询北京市2020年后建成的燃气管道"
   - "统计软土地质且有地震风险的管道数量"

### API接口

#### 查询接口
```
POST /api/v1/query
Content-Type: application/json

{
  "question": "查询广东省的燃气管道数量"
}
```

#### 响应格式
```json
{
  "status": "success",
  "message": "查询成功",
  "data": [...],
  "sql": "SELECT COUNT(*) FROM pipeline_info WHERE province = '广东' AND pipeline_type = '燃气管道'",
  "count": 150,
  "execution_time": 0.123
}
```

## 项目结构

```
├── database/                    # 数据库相关
│   ├── init.sql                # 数据库初始化脚本
│   └── mock_data.py            # 模拟数据生成脚本
├── pipeline_backend/           # 后端项目
│   ├── app/                    # 应用代码
│   │   ├── api/               # API路由
│   │   ├── models/            # 数据模型
│   │   └── services/          # 业务服务
│   ├── config.py              # 配置文件
│   ├── main.py                # 应用入口
│   └── requirements.txt       # Python依赖
├── pipeline-frontend/          # 前端项目
│   ├── src/                   # 源代码
│   │   ├── components/        # Vue组件
│   │   ├── views/             # 页面组件
│   │   ├── services/          # API服务
│   │   └── stores/            # 状态管理
│   ├── package.json           # 项目配置
│   └── vue.config.js          # Vue配置
└── README.md                  # 项目说明
```

## API文档

系统提供了完整的RESTful API接口：

- `GET /api/v1/health` - 健康检查
- `POST /api/v1/query` - 自然语言查询
- `GET /api/v1/suggestions` - 获取查询建议
- `GET /api/v1/examples` - 获取查询示例
- `GET /api/v1/stats` - 获取数据库统计信息

启动后端服务后，可以访问 `http://localhost:8000/docs` 查看详细的API文档。

## 部署说明

### Docker部署

```bash
# 构建后端镜像
cd pipeline_backend
docker build -t pipeline-backend .

# 构建前端镜像
cd pipeline-frontend
docker build -t pipeline-frontend .

# 使用docker-compose启动
docker-compose up -d
```

### 生产环境部署

1. **后端部署**:
   - 使用 Gunicorn + Nginx
   - 配置HTTPS和反向代理
   - 设置环境变量和日志

2. **前端部署**:
   - 构建生产版本: `npm run build`
   - 部署到CDN或静态文件服务器
   - 配置Nginx静态文件服务

3. **数据库部署**:
   - MySQL主从配置
   - 定期备份策略
   - 性能监控和优化

## 贡献指南

1. Fork 本仓库
2. 创建特性分支: `git checkout -b feature/your-feature`
3. 提交更改: `git commit -am 'Add some feature'`
4. 推送分支: `git push origin feature/your-feature`
5. 提交Pull Request

## 许可证

本项目采用 MIT 许可证。查看 [LICENSE](LICENSE) 文件了解更多信息。

## 联系我们

- 项目地址: https://github.com/pipeline-system/intelligent-query
- 问题反馈: https://github.com/pipeline-system/intelligent-query/issues
- 邮箱联系: admin@pipeline-system.com

## 更新日志

### v1.0.0 (2023-12-01)
- 🎉 首次发布
- ✨ 完成基础的自然语言查询功能
- 📊 实现多种数据可视化展示
- 🤖 集成阿里云百炼大模型
- 📝 支持查询历史管理
- 💾 数据导出功能
- 📱 响应式UI设计

---

**注意**: 本系统仅用于演示和学习目的，生产环境使用请确保数据安全和隐私保护。 