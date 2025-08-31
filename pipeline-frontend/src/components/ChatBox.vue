<template>
  <div class="chat-box">
    <!-- 聊天头部 -->
    <div class="chat-header">
      <div class="chat-title">
        <a-avatar :size="32" style="background-color: #1890ff;">
          <template #icon>
            <robot-outlined />
          </template>
        </a-avatar>
        <span class="title-text">AI智能助手</span>
      </div>
      <div class="chat-actions">
        <a-tooltip title="清除历史">
          <a-button type="text" size="small" @click="clearHistory">
            <template #icon>
              <delete-outlined />
            </template>
          </a-button>
        </a-tooltip>
        <a-tooltip title="查看示例">
          <a-button type="text" size="small" @click="showExamples">
            <template #icon>
              <bulb-outlined />
            </template>
          </a-button>
        </a-tooltip>
      </div>
    </div>

    <!-- 消息列表 -->
    <div class="chat-messages" ref="messagesContainer">
      <!-- 欢迎消息 -->
      <div class="chat-message assistant" v-if="messages.length === 0">
        <a-avatar class="chat-avatar" style="background-color: #52c41a;">
          <template #icon>
            <robot-outlined />
          </template>
        </a-avatar>
        <div class="chat-content">
          <p>您好！我是管道信息智能助手。</p>
          <p>您可以询问关于管道信息的问题，例如：</p>
          <ul>
            <li>"查询广东省的燃气管道数量"</li>
            <li>"统计各省市管道类型分布情况"</li>
            <li>"2010年以后建成的供水管道有哪些？"</li>
          </ul>
        </div>
      </div>

      <!-- 历史消息 -->
      <div 
        v-for="(message, index) in messages" 
        :key="index"
        :class="['chat-message', message.type]"
      >
        <a-avatar 
          class="chat-avatar" 
          :style="{ backgroundColor: message.type === 'user' ? '#1890ff' : '#52c41a' }"
        >
          <template #icon>
            <user-outlined v-if="message.type === 'user'" />
            <robot-outlined v-else />
          </template>
        </a-avatar>
        <div class="chat-content">
          <div v-if="message.type === 'user'" class="user-message">
            {{ message.content }}
          </div>
          <div v-else class="assistant-message">
            <div v-if="message.loading" class="loading-message">
              <a-spin size="small" />
              <span class="ml-8">正在思考中...</span>
            </div>
            <div v-else>
              <p>{{ message.content }}</p>
              <div v-if="message.result" class="result-summary">
                <a-tag v-if="message.result.status === 'success'" color="green">
                  查询成功 - {{ message.result.count }} 条结果
                </a-tag>
                <a-tag v-else color="red">
                  查询失败
                </a-tag>
                <span class="execution-time">
                  耗时: {{ (message.result.execution_time || 0).toFixed(3) }}s
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 加载状态 -->
      <div v-if="isQuerying" class="chat-message assistant">
        <a-avatar class="chat-avatar" style="background-color: #52c41a;">
          <template #icon>
            <robot-outlined />
          </template>
        </a-avatar>
        <div class="chat-content">
          <div class="loading-message">
            <a-spin size="small" />
            <span class="ml-8">正在分析您的问题...</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 输入区域 -->
    <div class="chat-input">
      <!-- 建议标签 -->
      <div v-if="suggestions.length > 0 && !currentQuery" class="suggestions">
        <div class="suggestions-title">建议查询：</div>
        <div class="suggestions-list">
          <a-tag 
            v-for="(suggestion, index) in suggestions.slice(0, 3)" 
            :key="index"
            class="suggestion-tag"
            @click="selectSuggestion(suggestion)"
          >
            {{ suggestion }}
          </a-tag>
        </div>
      </div>

      <!-- 输入框 -->
      <div class="input-container">
        <a-input
          :value="currentQuery"
          @update:value="(val) => { currentQuery = val; onInputChange(); }"
          placeholder="请输入您的问题，例如：查询广东省的燃气管道数量"
          size="large"
          :disabled="isQuerying"
          @pressEnter="sendMessage"
          class="message-input"
        />
        <a-button 
          type="primary" 
          size="large"
          :loading="isQuerying"
          :disabled="!canSendMessage"
          @click="sendMessage"
          class="send-button"
          :title="`当前输入: '${currentQuery}' (长度: ${currentQuery.length})`"
        >
          <template #icon>
            <send-outlined />
          </template>
          发送
        </a-button>
      </div>

      <!-- 快捷操作 -->
      <div class="quick-actions">
        <a-button type="text" size="small" @click="showHistory">
          <template #icon>
            <history-outlined />
          </template>
          历史记录
        </a-button>
        <a-button type="text" size="small" @click="loadSuggestions">
          <template #icon>
            <reload-outlined />
          </template>
          获取建议
        </a-button>
      </div>
    </div>

    <!-- 示例弹窗 -->
         <a-modal
       :visible="examplesVisible"
       @update:visible="examplesVisible = $event"
       title="查询示例"
       :footer="null"
       width="600px"
     >
      <div class="examples-content">
        <div v-for="(examples, category) in exampleData" :key="category" class="example-category">
          <h4>{{ category }}</h4>
          <div class="example-list">
            <a-tag 
              v-for="(example, index) in examples" 
              :key="index"
              class="example-tag"
              @click="selectExample(example)"
            >
              {{ example }}
            </a-tag>
          </div>
        </div>
      </div>
    </a-modal>

    <!-- 历史记录弹窗 -->
         <a-modal
       :visible="historyVisible"
       @update:visible="historyVisible = $event"
       title="查询历史"
       :footer="null"
       width="800px"
     >
      <div class="history-content">
        <a-list 
          :data-source="recentQueries"
          :pagination="{ pageSize: 10 }"
        >
          <template #renderItem="{ item }">
            <a-list-item>
              <a-list-item-meta>
                <template #title>
                  <span 
                    class="history-question"
                    @click="selectHistoryItem(item)"
                  >
                    {{ item.question }}
                  </span>
                </template>
                <template #description>
                  <div class="history-meta">
                    <a-tag :color="item.success ? 'green' : 'red'">
                      {{ item.success ? '成功' : '失败' }}
                    </a-tag>
                    <span class="history-time">
                      {{ formatTime(item.timestamp) }}
                    </span>
                  </div>
                </template>
              </a-list-item-meta>
            </a-list-item>
          </template>
        </a-list>
      </div>
    </a-modal>
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted, nextTick, watch } from 'vue'
import { 
  RobotOutlined, 
  UserOutlined, 
  SendOutlined,
  DeleteOutlined,
  BulbOutlined,
  HistoryOutlined,
  ReloadOutlined
} from '@ant-design/icons-vue'
import { message } from 'ant-design-vue'
import { useQueryStore } from '../stores'

export default {
  name: 'ChatBox',
  components: {
    RobotOutlined,
    UserOutlined, 
    SendOutlined,
    DeleteOutlined,
    BulbOutlined,
    HistoryOutlined,
    ReloadOutlined
  },
  emits: ['query-result'],
  setup(props, { emit }) {
    const queryStore = useQueryStore()
    
    // 响应式状态
    const currentQuery = ref('')
    const messages = reactive([])
    const suggestions = ref([])
    const exampleData = ref({})
    const examplesVisible = ref(false)
    const historyVisible = ref(false)
    const messagesContainer = ref(null)
    
    // 计算属性
    const isQuerying = computed(() => queryStore.isQuerying)
    const recentQueries = computed(() => queryStore.recentQueries)
    const canSendMessage = computed(() => {
      const hasContent = currentQuery.value.trim().length > 0
      const notQuerying = !isQuerying.value
      console.log('发送按钮状态检查:', { hasContent, notQuerying, input: currentQuery.value })
      return hasContent && notQuerying
    })
    
    // 方法
    const scrollToBottom = async () => {
      await nextTick()
      if (messagesContainer.value) {
        messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
      }
    }
    
    const addMessage = (type, content, result = null) => {
      messages.push({
        type,
        content,
        result,
        timestamp: new Date()
      })
      scrollToBottom()
    }
    
    const sendMessage = async () => {
      const question = currentQuery.value.trim()
      if (!question || isQuerying.value) return
      
      // 添加用户消息
      addMessage('user', question)
      
      // 清空输入框
      currentQuery.value = ''
      
      try {
        // 执行查询
        const result = await queryStore.executeQuery(question)
        
        // 添加AI回复
        if (result.status === 'success') {
          addMessage('assistant', `已为您查询到 ${result.count} 条结果。`, result)
          emit('query-result', result)
        } else {
          addMessage('assistant', `查询失败：${result.message}`, result)
        }
        
      } catch (error) {
        console.error('查询失败:', error)
        addMessage('assistant', '抱歉，查询过程中出现错误，请稍后重试。')
      }
    }
    
    const clearHistory = () => {
      messages.splice(0, messages.length)
      message.success('聊天记录已清除')
    }
    
    const selectSuggestion = (suggestion) => {
      currentQuery.value = suggestion
    }
    
    const selectExample = (example) => {
      currentQuery.value = example
      examplesVisible.value = false
    }
    
    const selectHistoryItem = (item) => {
      currentQuery.value = item.question
      historyVisible.value = false
    }
    
    const showExamples = async () => {
      try {
        const examples = await queryStore.fetchExamples()
        exampleData.value = examples
        examplesVisible.value = true
      } catch (error) {
        message.error('获取示例失败')
      }
    }
    
    const showHistory = () => {
      historyVisible.value = true
    }
    
    const loadSuggestions = async () => {
      try {
        const newSuggestions = await queryStore.fetchSuggestions()
        suggestions.value = newSuggestions
      } catch (error) {
        message.error('获取建议失败')
      }
    }
    
    const onInputChange = () => {
      // 调试信息
      console.log('输入变化:', currentQuery.value, '长度:', currentQuery.value.length)
      
      // 可以在这里实现实时建议功能
      if (currentQuery.value && currentQuery.value.length > 2) {
        // 延迟加载建议
        setTimeout(() => {
          loadSuggestions()
        }, 500)
      }
    }
    
    const formatTime = (timestamp) => {
      return new Date(timestamp).toLocaleString('zh-CN')
    }
    
    // 监听查询结果变化
    watch(() => queryStore.queryResult, (newResult) => {
      if (newResult) {
        emit('query-result', newResult)
      }
    })
    
    // 组件挂载时初始化
    onMounted(async () => {
      queryStore.init()
      await loadSuggestions()
    })
    
    return {
      // 状态
      currentQuery,
      messages,
      suggestions,
      exampleData,
      examplesVisible,
      historyVisible,
      messagesContainer,
      
      // 计算属性
      isQuerying,
      recentQueries,
      canSendMessage,
      
      // 方法
      sendMessage,
      clearHistory,
      selectSuggestion,
      selectExample,
      selectHistoryItem,
      showExamples,
      showHistory,
      loadSuggestions,
      onInputChange,
      formatTime
    }
  }
}
</script>

<style scoped>
.chat-box {
  height: 600px;
  display: flex;
  flex-direction: column;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.chat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  border-bottom: 1px solid #f0f0f0;
  background: #fafafa;
}

.chat-title {
  display: flex;
  align-items: center;
  gap: 12px;
}

.title-text {
  font-weight: 600;
  font-size: 16px;
  color: #333;
}

.chat-actions {
  display: flex;
  gap: 8px;
}

.chat-messages {
  flex: 1;
  padding: 16px;
  overflow-y: auto;
  background: #ffffff;
}

.chat-message {
  display: flex;
  margin-bottom: 16px;
  align-items: flex-start;
}

.chat-message.user {
  flex-direction: row-reverse;
}

.chat-avatar {
  flex-shrink: 0;
  margin: 0 12px;
}

.chat-content {
  max-width: 75%;
  padding: 12px 16px;
  border-radius: 8px;
  line-height: 1.6;
  word-wrap: break-word;
}

.chat-message.user .chat-content {
  background: #1890ff;
  color: white;
  border-bottom-right-radius: 4px;
}

.chat-message.assistant .chat-content {
  background: #f6f6f6;
  color: #333;
  border-bottom-left-radius: 4px;
}

.user-message {
  font-size: 14px;
}

.assistant-message {
  font-size: 14px;
}

.assistant-message p {
  margin: 0 0 8px 0;
}

.assistant-message ul {
  margin: 8px 0;
  padding-left: 20px;
}

.result-summary {
  margin-top: 8px;
  padding-top: 8px;
  border-top: 1px solid #e8e8e8;
  font-size: 12px;
}

.execution-time {
  margin-left: 8px;
  color: #999;
}

.loading-message {
  display: flex;
  align-items: center;
  color: #999;
  font-size: 12px;
}

.chat-input {
  padding: 16px;
  border-top: 1px solid #f0f0f0;
  background: #fafafa;
}

.suggestions {
  margin-bottom: 12px;
}

.suggestions-title {
  font-size: 12px;
  color: #666;
  margin-bottom: 8px;
}

.suggestions-list {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.suggestion-tag {
  cursor: pointer;
  transition: all 0.2s;
}

.suggestion-tag:hover {
  background: #e6f7ff;
  border-color: #1890ff;
}

.input-container {
  display: flex;
  gap: 12px;
  margin-bottom: 8px;
}

.message-input {
  flex: 1;
}

.send-button {
  min-width: 80px;
}

.quick-actions {
  display: flex;
  gap: 16px;
  justify-content: center;
}

.examples-content {
  max-height: 400px;
  overflow-y: auto;
}

.example-category {
  margin-bottom: 24px;
}

.example-category h4 {
  margin-bottom: 12px;
  color: #333;
  font-size: 14px;
  font-weight: 600;
}

.example-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.example-tag {
  cursor: pointer;
  transition: all 0.2s;
  margin-bottom: 8px;
}

.example-tag:hover {
  background: #e6f7ff;
  border-color: #1890ff;
}

.history-content {
  max-height: 500px;
  overflow-y: auto;
}

.history-question {
  cursor: pointer;
  color: #1890ff;
  font-size: 14px;
}

.history-question:hover {
  text-decoration: underline;
}

.history-meta {
  display: flex;
  align-items: center;
  gap: 8px;
}

.history-time {
  font-size: 12px;
  color: #999;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .chat-content {
    max-width: 85%;
  }
  
  .input-container {
    flex-direction: column;
  }
  
  .suggestions-list {
    justify-content: center;
  }
}
</style> 