<template>
  <div class="about-page">
    <a-layout>
      <a-layout-header class="header">
        <div class="header-content">
          <router-link to="/" class="back-link">
            <a-button type="text">
              <template #icon>
                <arrow-left-outlined />
              </template>
              返回首页
            </a-button>
          </router-link>
        </div>
      </a-layout-header>
      
      <a-layout-content class="content">
        <div class="about-container">
          <a-card class="about-card">
            <div class="about-header">
              <api-outlined class="about-icon" />
              <h1>关于管道信息智能查询系统</h1>
              <p class="version">版本 1.0.0</p>
            </div>
            
            <a-divider />
            
            <div class="about-section">
              <h2>系统简介</h2>
              <p>
                管道信息智能查询系统是一个基于大语言模型技术的智能数据查询平台。
                用户可以通过自然语言输入查询问题，系统会自动理解用户意图，
                生成相应的SQL查询语句，并将查询结果以表格和图表的形式直观展示。
              </p>
            </div>
            
            <div class="about-section">
              <h2>技术架构</h2>
              <a-descriptions bordered :column="1">
                <a-descriptions-item label="前端框架">
                  Vue 3 + Composition API
                </a-descriptions-item>
                <a-descriptions-item label="UI组件库">
                  Ant Design Vue 4.x
                </a-descriptions-item>
                <a-descriptions-item label="状态管理">
                  Pinia
                </a-descriptions-item>
                <a-descriptions-item label="后端框架">
                  FastAPI + Python
                </a-descriptions-item>
                <a-descriptions-item label="AI框架">
                  LangChain
                </a-descriptions-item>
                <a-descriptions-item label="大语言模型">
                  阿里云百炼大模型 (Qwen-Max)
                </a-descriptions-item>
                <a-descriptions-item label="数据库">
                  MySQL 8.0
                </a-descriptions-item>
                <a-descriptions-item label="图表库">
                  Apache ECharts
                </a-descriptions-item>
              </a-descriptions>
            </div>
            
            <div class="about-section">
              <h2>主要功能</h2>
              <a-list>
                <a-list-item>
                  <a-list-item-meta>
                    <template #title>自然语言查询</template>
                    <template #description>
                      支持中文自然语言输入，无需学习SQL语法，降低使用门槛
                    </template>
                  </a-list-item-meta>
                </a-list-item>
                <a-list-item>
                  <a-list-item-meta>
                    <template #title>智能SQL生成</template>
                    <template #description>
                      基于大语言模型技术，自动将自然语言转换为精确的SQL查询语句
                    </template>
                  </a-list-item-meta>
                </a-list-item>
                <a-list-item>
                  <a-list-item-meta>
                    <template #title>多维度数据可视化</template>
                    <template #description>
                      支持表格、饼图、柱状图、折线图等多种数据展示方式
                    </template>
                  </a-list-item-meta>
                </a-list-item>
                <a-list-item>
                  <a-list-item-meta>
                    <template #title>查询历史管理</template>
                    <template #description>
                      自动保存查询历史，支持快速重复查询和查询结果对比
                    </template>
                  </a-list-item-meta>
                </a-list-item>
                <a-list-item>
                  <a-list-item-meta>
                    <template #title>数据导出功能</template>
                    <template #description>
                      支持查询结果导出，便于进一步分析和报告制作
                    </template>
                  </a-list-item-meta>
                </a-list-item>
              </a-list>
            </div>
            
            <div class="about-section">
              <h2>开发团队</h2>
              <p>Pipeline System Team</p>
              <p>联系邮箱: admin@pipeline-system.com</p>
            </div>
            
            <div class="about-section">
              <h2>更新日志</h2>
              <a-timeline>
                <a-timeline-item color="green">
                  <template #dot>
                    <check-circle-outlined />
                  </template>
                  <div>
                    <h4>v1.0.0 (2023-12-01)</h4>
                    <ul>
                      <li>完成基础的自然语言查询功能</li>
                      <li>实现多种数据可视化展示</li>
                      <li>集成阿里云百炼大模型</li>
                      <li>支持查询历史管理</li>
                    </ul>
                  </div>
                </a-timeline-item>
              </a-timeline>
            </div>
          </a-card>
        </div>
      </a-layout-content>
    </a-layout>
  </div>
</template>

<script>
import { ArrowLeftOutlined, ApiOutlined, CheckCircleOutlined } from '@ant-design/icons-vue'

export default {
  name: 'About',
  components: {
    ArrowLeftOutlined,
    ApiOutlined,
    CheckCircleOutlined
  }
}
</script>

<style scoped>
.about-page {
  min-height: 100vh;
  background: #f0f2f5;
}

.header {
  background: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
  display: flex;
  align-items: center;
  height: 64px;
}

.back-link {
  text-decoration: none;
}

.content {
  padding: 24px;
}

.about-container {
  max-width: 800px;
  margin: 0 auto;
}

.about-card {
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.about-header {
  text-align: center;
  margin-bottom: 24px;
}

.about-icon {
  font-size: 64px;
  color: #1890ff;
  margin-bottom: 16px;
}

.about-header h1 {
  margin: 0 0 8px 0;
  color: #333;
  font-size: 28px;
}

.version {
  color: #999;
  font-size: 16px;
  margin: 0;
}

.about-section {
  margin-bottom: 32px;
}

.about-section h2 {
  color: #333;
  font-size: 20px;
  margin-bottom: 16px;
  border-left: 4px solid #1890ff;
  padding-left: 12px;
}

.about-section p {
  color: #666;
  line-height: 1.6;
  margin-bottom: 12px;
}

.about-section ul {
  color: #666;
  line-height: 1.6;
}

.about-section ul li {
  margin-bottom: 4px;
}
</style> 