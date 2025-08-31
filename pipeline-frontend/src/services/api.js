/**
 * API服务模块
 * 处理所有与后端的HTTP通信
 */

import axios from 'axios'
import { message } from 'ant-design-vue'

// 创建axios实例
const apiClient = axios.create({
  baseURL: process.env.VUE_APP_API_URL || 'http://localhost:8000/api/v1',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  }
})

// 请求拦截器
apiClient.interceptors.request.use(
  (config) => {
    // 在发送请求之前添加loading状态或token等
    console.log(`发送请求: ${config.method?.toUpperCase()} ${config.url}`)
    
    // 可以在这里添加认证token
    // const token = localStorage.getItem('token')
    // if (token) {
    //   config.headers.Authorization = `Bearer ${token}`
    // }
    
    return config
  },
  (error) => {
    console.error('请求拦截器错误:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
apiClient.interceptors.response.use(
  (response) => {
    // 成功响应的处理
    console.log(`响应成功: ${response.config.url}`, response.data)
    return response.data
  },
  (error) => {
    // 错误响应的处理
    console.error('响应错误:', error)
    
    let errorMessage = '网络错误，请稍后重试'
    
    if (error.response) {
      // 服务器返回的错误
      const { status, data } = error.response
      
      switch (status) {
        case 400:
          errorMessage = data.detail || '请求参数错误'
          break
        case 401:
          errorMessage = '未授权，请重新登录'
          // 可以在这里处理登录失效
          break
        case 403:
          errorMessage = '访问被拒绝'
          break
        case 404:
          errorMessage = '请求的资源不存在'
          break
        case 500:
          errorMessage = '服务器内部错误'
          break
        case 503:
          errorMessage = '服务暂时不可用'
          break
        default:
          errorMessage = data.message || data.detail || '未知错误'
      }
    } else if (error.request) {
      // 网络错误
      errorMessage = '网络连接失败，请检查网络设置'
    } else {
      // 其他错误
      errorMessage = error.message || '请求失败'
    }
    
    // 显示错误消息
    message.error(errorMessage)
    
    return Promise.reject({
      ...error,
      userMessage: errorMessage
    })
  }
)

/**
 * API服务对象
 */
const apiService = {
  /**
   * 处理查询请求
   * @param {string} question - 用户问题
   * @returns {Promise} 查询结果
   */
  async sendQuery(question) {
    try {
      const response = await apiClient.post('/query', { question })
      return response
    } catch (error) {
      throw error
    }
  },

  /**
   * 获取查询建议
   * @param {string} partialText - 部分文本
   * @returns {Promise} 建议列表
   */
  async getQuerySuggestions(partialText = '') {
    try {
      const response = await apiClient.get('/suggestions', {
        params: { q: partialText }
      })
      return response
    } catch (error) {
      throw error
    }
  },

  /**
   * 获取查询示例
   * @returns {Promise} 示例列表
   */
  async getQueryExamples() {
    try {
      const response = await apiClient.get('/examples')
      return response
    } catch (error) {
      throw error
    }
  },

  /**
   * 验证问题
   * @param {string} question - 用户问题
   * @returns {Promise} 验证结果
   */
  async validateQuestion(question) {
    try {
      const response = await apiClient.post('/validate', { question })
      return response
    } catch (error) {
      throw error
    }
  },

  /**
   * 获取数据库统计信息
   * @returns {Promise} 统计数据
   */
  async getDatabaseStats() {
    try {
      const response = await apiClient.get('/stats')
      return response
    } catch (error) {
      throw error
    }
  },

  /**
   * 获取数据库连接信息
   * @returns {Promise} 连接状态
   */
  async getDatabaseInfo() {
    try {
      const response = await apiClient.get('/database/info')
      return response
    } catch (error) {
      throw error
    }
  },

  /**
   * 健康检查
   * @returns {Promise} 健康状态
   */
  async healthCheck() {
    try {
      const response = await apiClient.get('/health')
      return response
    } catch (error) {
      throw error
    }
  }
}

export default apiService

// 导出axios实例以供高级用法
export { apiClient } 