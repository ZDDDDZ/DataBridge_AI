<template>
  <div class="home">
    <a-layout class="layout">
      <!-- 顶部导航 -->
      <a-layout-header class="header">
        <div class="header-content">
          <div class="logo">
            <api-outlined class="logo-icon" />
            <span class="logo-text">管道信息智能查询系统</span>
          </div>
          <div class="header-actions">
            <a-space>
              <a-tooltip title="系统状态">
                <a-badge :status="systemStatus.type" :text="systemStatus.text">
                  <a-button type="text" @click="checkSystemStatus">
                    <template #icon>
                      <wifi-outlined />
                    </template>
                  </a-button>
                </a-badge>
              </a-tooltip>
              <a-tooltip title="关于系统">
                <a-button type="text" @click="showAbout">
                  <template #icon>
                    <info-circle-outlined />
                  </template>
                </a-button>
              </a-tooltip>
            </a-space>
          </div>
        </div>
      </a-layout-header>

      <!-- 主内容区 -->
      <a-layout-content class="content">
        <div class="content-wrapper">
          <!-- 系统介绍卡片 -->
          <a-card class="intro-card" v-if="!hasQueryResult">
            <template #title>
              <div class="intro-title">
                <bulb-outlined />
                欢迎使用管道信息智能查询系统
              </div>
            </template>
            
            <div class="intro-content">
              <p class="intro-description">
                这是一个基于大语言模型的智能查询系统，您可以使用自然语言查询管道信息数据。
                系统会自动理解您的问题并生成相应的SQL查询，然后以表格和图表的形式展示结果。
              </p>
              
              <div class="features">
                <a-row :gutter="[16, 16]">
                  <a-col :span="8">
                    <div class="feature-item">
                      <message-outlined class="feature-icon" />
                      <h4>自然语言查询</h4>
                      <p>直接输入中文问题，无需学习SQL语法</p>
                    </div>
                  </a-col>
                  <a-col :span="8">
                    <div class="feature-item">
                      <bar-chart-outlined class="feature-icon" />
                      <h4>可视化分析</h4>
                      <p>自动生成图表，支持多种可视化方式</p>
                    </div>
                  </a-col>
                  <a-col :span="8">
                    <div class="feature-item">
                      <database-outlined class="feature-icon" />
                      <h4>实时数据</h4>
                      <p>连接实时数据库，获取最新管道信息</p>
                    </div>
                  </a-col>
                </a-row>
              </div>
              
              <div class="quick-start">
                <h4>快速开始示例：</h4>
                <div class="example-queries">
                  <a-tag 
                    v-for="example in quickExamples" 
                    :key="example"
                    class="example-tag"
                    @click="tryExample(example)"
                  >
                    {{ example }}
                  </a-tag>
                </div>
              </div>
            </div>
          </a-card>

          <!-- 查询区域 -->
          <div class="query-section">
            <a-card class="chat-card">
              <ChatBox @query-result="handleQueryResult" />
            </a-card>
          </div>

          <!-- 结果展示区域 -->
          <div class="result-section" v-if="hasQueryResult">
            <DataVisualization :queryResult="currentQueryResult" />
          </div>

          <!-- 数据库统计信息 -->
          <a-card class="stats-card" v-if="databaseStats">
            <template #title>
              <div class="stats-title">
                <pie-chart-outlined />
                数据库概览
              </div>
            </template>
            
            <a-row :gutter="[16, 16]">
              <a-col :span="6">
                <a-statistic
                  title="管道总数"
                  :value="databaseStats.total_pipelines"
                  suffix="条"
                  :value-style="{ color: '#3f8600' }"
                />
              </a-col>
              <a-col :span="6">
                <a-statistic
                  title="覆盖省份"
                  :value="databaseStats.provinces_count"
                  suffix="个"
                  :value-style="{ color: '#1890ff' }"
                />
              </a-col>
              <a-col :span="6">
                <a-statistic
                  title="覆盖城市"
                  :value="databaseStats.cities_count"
                  suffix="个"
                  :value-style="{ color: '#722ed1' }"
                />
              </a-col>
              <a-col :span="6">
                <a-statistic
                  title="管道类型"
                  :value="Object.keys(databaseStats.pipeline_types || {}).length"
                  suffix="种"
                  :value-style="{ color: '#fa8c16' }"
                />
              </a-col>
            </a-row>
          </a-card>
        </div>
      </a-layout-content>

      <!-- 底部 -->
      <a-layout-footer class="footer">
        <div class="footer-content">
          <div class="footer-info">
            © 2023 管道信息智能查询系统 | 基于大语言模型技术
          </div>
          <div class="footer-links">
            <a-space>
              <a href="#" @click.prevent="showAbout">关于我们</a>
              <a-divider type="vertical" />
              <a href="#" @click.prevent="showHelp">使用帮助</a>
              <a-divider type="vertical" />
              <a href="#" @click.prevent="showContact">联系我们</a>
            </a-space>
          </div>
        </div>
      </a-layout-footer>
    </a-layout>

    <!-- 关于弹窗 -->
    <a-modal
      :visible="aboutVisible"
      @update:visible="aboutVisible = $event"
      title="关于系统"
      :footer="null"
      width="600px"
    >
      <div class="about-content">
        <div class="about-header">
          <api-outlined class="about-icon" />
          <h2>管道信息智能查询系统</h2>
          <p class="version">版本 1.0.0</p>
        </div>
        
        <a-descriptions :column="1" bordered size="small">
          <a-descriptions-item label="技术栈">
            Vue 3 + Ant Design Vue + FastAPI + LangChain
          </a-descriptions-item>
          <a-descriptions-item label="AI模型">
            阿里云百炼大模型
          </a-descriptions-item>
          <a-descriptions-item label="数据库">
            MySQL 8.0
          </a-descriptions-item>
          <a-descriptions-item label="开发团队">
            Pipeline System Team
          </a-descriptions-item>
        </a-descriptions>
        
        <div class="about-footer">
          <p>本系统采用先进的自然语言处理技术，让用户能够通过自然语言查询管道信息数据，提供智能化的数据分析体验。</p>
        </div>
      </div>
    </a-modal>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue'
import { 
  ApiOutlined,
  WifiOutlined,
  InfoCircleOutlined,
  BulbOutlined,
  MessageOutlined,
  BarChartOutlined,
  DatabaseOutlined,
  PieChartOutlined
} from '@ant-design/icons-vue'
import { message } from 'ant-design-vue'
import ChatBox from '../components/ChatBox.vue'
import DataVisualization from '../components/DataVisualization.vue'
import { useAppStore, useQueryStore } from '../stores'
import apiService from '../services/api'

export default {
  name: 'Home',
  components: {
    ApiOutlined,
    WifiOutlined,
    InfoCircleOutlined,
    BulbOutlined,
    MessageOutlined,
    BarChartOutlined,
    DatabaseOutlined,
    PieChartOutlined,
    ChatBox,
    DataVisualization
  },
  setup() {
    const appStore = useAppStore()
    const queryStore = useQueryStore()
    
    // 响应式状态
    const currentQueryResult = ref(null)
    const databaseStats = ref(null)
    const aboutVisible = ref(false)
    const systemConnected = ref(false)
    
    // 快速示例
    const quickExamples = ref([
      '查询广东省的燃气管道数量',
      '统计各省市管道类型分布',
      '2010年以后建成的供水管道'
    ])
    
    // 计算属性
    const hasQueryResult = computed(() => {
      return currentQueryResult.value && 
             currentQueryResult.value.data && 
             currentQueryResult.value.data.length > 0
    })
    
    const systemStatus = computed(() => {
      if (systemConnected.value) {
        return { type: 'success', text: '系统正常' }
      } else {
        return { type: 'error', text: '连接异常' }
      }
    })
    
    // 方法
    const handleQueryResult = (result) => {
      currentQueryResult.value = result
    }
    
    const tryExample = (example) => {
      // 这里应该触发聊天组件执行查询
      // 可以通过事件总线或直接调用聊天组件的方法
      queryStore.setCurrentQuery(example)
    }
    
    const checkSystemStatus = async () => {
      try {
        await apiService.healthCheck()
        systemConnected.value = true
        message.success('系统连接正常')
      } catch (error) {
        systemConnected.value = false
        message.error('系统连接异常')
      }
    }
    
    const loadDatabaseStats = async () => {
      try {
        const stats = await apiService.getDatabaseStats()
        databaseStats.value = stats
      } catch (error) {
        console.error('获取数据库统计信息失败:', error)
      }
    }
    
    const showAbout = () => {
      aboutVisible.value = true
    }
    
    const showHelp = () => {
      message.info('使用帮助功能正在开发中...')
    }
    
    const showContact = () => {
      message.info('联系方式: admin@pipeline-system.com')
    }
    
    // 监听系统信息变化
    watch(() => appStore.systemInfo, (newInfo) => {
      if (newInfo && newInfo.status === 'connected') {
        systemConnected.value = true
        if (newInfo.stats) {
          databaseStats.value = newInfo.stats
        }
      } else {
        systemConnected.value = false
      }
    })
    
    // 组件挂载时初始化
    onMounted(async () => {
      try {
        await checkSystemStatus()
        await loadDatabaseStats()
      } catch (error) {
        console.error('初始化失败:', error)
      }
    })
    
    return {
      // 状态
      currentQueryResult,
      databaseStats,
      aboutVisible,
      systemConnected,
      quickExamples,
      
      // 计算属性
      hasQueryResult,
      systemStatus,
      
      // 方法
      handleQueryResult,
      tryExample,
      checkSystemStatus,
      showAbout,
      showHelp,
      showContact
    }
  }
}
</script>

<style scoped>
.home {
  min-height: 100vh;
  background: #f0f2f5;
}

.layout {
  min-height: 100vh;
}

.header {
  background: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 64px;
  padding: 0 24px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 20px;
  font-weight: bold;
  color: #333;
}

.logo-icon {
  font-size: 28px;
  color: #1890ff;
}

.logo-text {
  color: #333;
}

.header-actions {
  display: flex;
  align-items: center;
}

.content {
  padding: 24px;
  background: #f0f2f5;
}

.content-wrapper {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.intro-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 12px;
}

.intro-card :deep(.ant-card-head) {
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
}

.intro-card :deep(.ant-card-head-title) {
  color: white;
}

.intro-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 18px;
  font-weight: 600;
}

.intro-content {
  color: white;
}

.intro-description {
  font-size: 16px;
  line-height: 1.6;
  margin-bottom: 24px;
  opacity: 0.9;
}

.features {
  margin-bottom: 32px;
}

.feature-item {
  text-align: center;
  padding: 20px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  backdrop-filter: blur(10px);
}

.feature-icon {
  font-size: 32px;
  margin-bottom: 12px;
  display: block;
  color: #fff;
}

.feature-item h4 {
  margin: 0 0 8px 0;
  color: white;
  font-size: 16px;
}

.feature-item p {
  margin: 0;
  opacity: 0.8;
  font-size: 14px;
}

.quick-start h4 {
  color: white;
  margin-bottom: 16px;
  font-size: 16px;
}

.example-queries {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.example-tag {
  cursor: pointer;
  background: rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: white;
  transition: all 0.3s;
}

.example-tag:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: translateY(-1px);
}

.query-section {
  display: flex;
  justify-content: center;
}

.chat-card {
  width: 100%;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.result-section {
  margin-top: 24px;
}

.stats-card {
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.stats-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
}

.footer {
  background: #fff;
  border-top: 1px solid #f0f0f0;
  text-align: center;
  padding: 24px 0;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 24px;
}

.footer-info {
  color: #666;
  font-size: 14px;
}

.footer-links a {
  color: #666;
  text-decoration: none;
  font-size: 14px;
}

.footer-links a:hover {
  color: #1890ff;
}

.about-content {
  text-align: center;
}

.about-header {
  margin-bottom: 24px;
}

.about-icon {
  font-size: 48px;
  color: #1890ff;
  margin-bottom: 16px;
}

.about-header h2 {
  margin: 0 0 8px 0;
  color: #333;
}

.version {
  color: #999;
  font-size: 14px;
  margin: 0;
}

.about-footer {
  margin-top: 24px;
  padding-top: 24px;
  border-top: 1px solid #f0f0f0;
}

.about-footer p {
  color: #666;
  line-height: 1.6;
  margin: 0;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .header-content {
    padding: 0 16px;
  }
  
  .logo-text {
    display: none;
  }
  
  .content {
    padding: 16px;
  }
  
  .footer-content {
    flex-direction: column;
    gap: 16px;
    padding: 0 16px;
  }
  
  .features .ant-col {
    margin-bottom: 16px;
  }
  
  .example-queries {
    justify-content: center;
  }
}
</style> 