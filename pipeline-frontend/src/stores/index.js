/**
 * Pinia 状态管理
 * 管道信息智能查询系统
 */

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import apiService from '../services/api'

/**
 * 主应用状态存储
 */
export const useAppStore = defineStore('app', () => {
  // 状态
  const loading = ref(false)
  const error = ref(null)
  const systemInfo = ref(null)
  
  // 计算属性
  const isLoading = computed(() => loading.value)
  const hasError = computed(() => !!error.value)
  
  // 操作
  const setLoading = (status) => {
    loading.value = status
  }
  
  const setError = (errorInfo) => {
    error.value = errorInfo
  }
  
  const clearError = () => {
    error.value = null
  }
  
  const setSystemInfo = (info) => {
    systemInfo.value = info
  }
  
  // 获取系统信息
  const fetchSystemInfo = async () => {
    try {
      setLoading(true)
      const info = await apiService.getDatabaseInfo()
      setSystemInfo(info)
      return info
    } catch (err) {
      setError(err)
      throw err
    } finally {
      setLoading(false)
    }
  }
  
  return {
    // 状态
    loading,
    error,
    systemInfo,
    
    // 计算属性
    isLoading,
    hasError,
    
    // 操作
    setLoading,
    setError,
    clearError,
    setSystemInfo,
    fetchSystemInfo
  }
})

/**
 * 查询相关状态存储
 */
export const useQueryStore = defineStore('query', () => {
  // 状态
  const currentQuery = ref('')
  const queryHistory = ref([])
  const queryResult = ref(null)
  const suggestions = ref([])
  const examples = ref({})
  const isQuerying = ref(false)
  
  // 计算属性
  const hasResult = computed(() => !!queryResult.value)
  const hasHistory = computed(() => queryHistory.value.length > 0)
  const recentQueries = computed(() => queryHistory.value.slice(-10).reverse())
  
  // 操作
  const setCurrentQuery = (query) => {
    currentQuery.value = query
  }
  
  const setQueryResult = (result) => {
    queryResult.value = result
  }
  
  const clearQueryResult = () => {
    queryResult.value = null
  }
  
  const addQueryToHistory = (query, result) => {
    const historyItem = {
      id: Date.now(),
      question: query,
      result: result,
      timestamp: new Date(),
      success: result?.status === 'success'
    }
    
    queryHistory.value.push(historyItem)
    
    // 限制历史记录数量
    if (queryHistory.value.length > 100) {
      queryHistory.value = queryHistory.value.slice(-100)
    }
    
    // 保存到本地存储
    saveQueryHistoryToLocal()
  }
  
  const clearQueryHistory = () => {
    queryHistory.value = []
    localStorage.removeItem('queryHistory')
  }
  
  const setSuggestions = (newSuggestions) => {
    suggestions.value = newSuggestions
  }
  
  const setExamples = (newExamples) => {
    examples.value = newExamples
  }
  
  const setQuerying = (status) => {
    isQuerying.value = status
  }
  
  // 从本地存储加载历史记录
  const loadQueryHistoryFromLocal = () => {
    try {
      const stored = localStorage.getItem('queryHistory')
      if (stored) {
        const parsed = JSON.parse(stored)
        queryHistory.value = parsed.map(item => ({
          ...item,
          timestamp: new Date(item.timestamp)
        }))
      }
    } catch (error) {
      console.error('加载查询历史失败:', error)
    }
  }
  
  // 保存历史记录到本地存储
  const saveQueryHistoryToLocal = () => {
    try {
      localStorage.setItem('queryHistory', JSON.stringify(queryHistory.value))
    } catch (error) {
      console.error('保存查询历史失败:', error)
    }
  }
  
  // 执行查询
  const executeQuery = async (question) => {
    try {
      setQuerying(true)
      setCurrentQuery(question)
      
      const result = await apiService.sendQuery(question)
      setQueryResult(result)
      addQueryToHistory(question, result)
      
      return result
    } catch (error) {
      const errorResult = {
        status: 'error',
        message: error.userMessage || '查询失败',
        execution_time: 0
      }
      setQueryResult(errorResult)
      addQueryToHistory(question, errorResult)
      throw error
    } finally {
      setQuerying(false)
    }
  }
  
  // 获取查询建议
  const fetchSuggestions = async (partialText = '') => {
    try {
      const response = await apiService.getQuerySuggestions(partialText)
      setSuggestions(response.suggestions || [])
      return response.suggestions
    } catch (error) {
      console.error('获取建议失败:', error)
      return []
    }
  }
  
  // 获取查询示例
  const fetchExamples = async () => {
    try {
      const response = await apiService.getQueryExamples()
      setExamples(response)
      return response
    } catch (error) {
      console.error('获取示例失败:', error)
      return {}
    }
  }
  
  // 初始化
  const init = () => {
    loadQueryHistoryFromLocal()
  }
  
  return {
    // 状态
    currentQuery,
    queryHistory,
    queryResult,
    suggestions,
    examples,
    isQuerying,
    
    // 计算属性
    hasResult,
    hasHistory,
    recentQueries,
    
    // 操作
    setCurrentQuery,
    setQueryResult,
    clearQueryResult,
    addQueryToHistory,
    clearQueryHistory,
    setSuggestions,
    setExamples,
    setQuerying,
    executeQuery,
    fetchSuggestions,
    fetchExamples,
    init
  }
})

/**
 * 图表相关状态存储
 */
export const useChartStore = defineStore('chart', () => {
  // 状态
  const chartType = ref('table') // table, pie, bar, line
  const chartDimension = ref('')
  const chartOptions = ref(null)
  
  // 操作
  const setChartType = (type) => {
    chartType.value = type
  }
  
  const setChartDimension = (dimension) => {
    chartDimension.value = dimension
  }
  
  const setChartOptions = (options) => {
    chartOptions.value = options
  }
  
  // 生成图表数据
  const generateChartData = (data, dimension, type, valueDimension) => {
    console.log('generateChartData 被调用:', { data, dimension, type, valueDimension })
    
    if (!data || !Array.isArray(data) || data.length === 0) {
      console.warn('数据为空或格式不正确')
      return null
    }
    
    if (!dimension) {
      console.warn('分析维度参数为空')
      return null
    }
    
    if (!valueDimension) {
      console.warn('取值维度参数为空')
      return null
    }
    
    // 辅助函数：检测和转换数字类型
    const isNumericValue = (value) => {
      if (typeof value === 'number') {
        return { isNumeric: true, numericValue: value }
      }
      
      if (typeof value === 'string') {
        const trimmedValue = value.trim()
        if (trimmedValue !== '') {
          // 尝试转换为整数
          const intValue = parseInt(trimmedValue, 10)
          if (!isNaN(intValue) && trimmedValue === intValue.toString()) {
            return { isNumeric: true, numericValue: intValue }
          }
          // 尝试转换为浮点数
          const floatValue = parseFloat(trimmedValue)
          if (!isNaN(floatValue) && trimmedValue === floatValue.toString()) {
            return { isNumeric: true, numericValue: floatValue }
          }
        }
      }
      
      return { isNumeric: false, numericValue: 0 }
    }
    
    // 按维度分组统计
    const groupedData = {}
    data.forEach(item => {
      const key = item[dimension] || '未知'
      const value = item[valueDimension]
      
      if (!groupedData[key]) {
        groupedData[key] = 0
      }
      
      // 使用辅助函数检测和转换数字类型
      const { isNumeric, numericValue } = isNumericValue(value)
      
      // 根据转换结果决定计算方式
      if (isNumeric) {
        // 数值类型：累加数值
        groupedData[key] += numericValue
        console.log(`分组 "${key}": 累加数值 ${numericValue} (原值: ${value})`)
      } else {
        // 非数值类型：累加出现次数
        groupedData[key] += 1
        console.log(`分组 "${key}": 累加次数 1 (原值: ${value})`)
      }
    })
    
    console.log('分组后的数据:', groupedData)
    
    const chartData = Object.entries(groupedData).map(([name, value]) => ({
      name,
      value
    }))
    
    console.log('图表数据:', chartData)
    
    // 根据图表类型生成配置
    let options = {}
    
    switch (type) {
      case 'pie':
        options = {
          title: {
            text: `按${dimension}统计`,
            left: 'center'
          },
          tooltip: {
            trigger: 'item',
            formatter: '{a} <br/>{b}: {c} ({d}%)'
          },
          legend: {
            orient: 'vertical',
            left: 'left'
          },
          series: [{
            name: '数量',
            type: 'pie',
            radius: '50%',
            data: chartData,
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            }
          }]
        }
        break
        
      case 'bar':
        options = {
          title: {
            text: `按${dimension}统计`,
            left: 'center'
          },
          tooltip: {
            trigger: 'axis',
            axisPointer: {
              type: 'shadow'
            }
          },
          xAxis: {
            type: 'category',
            data: chartData.map(item => item.name),
            axisLabel: {
              rotate: 45,
              interval: 0
            }
          },
          yAxis: {
            type: 'value'
          },
          series: [{
            data: chartData.map(item => item.value),
            type: 'bar',
            itemStyle: {
              color: '#1890ff'
            }
          }]
        }
        break
        
      case 'line':
        options = {
          title: {
            text: `按${dimension}统计`,
            left: 'center'
          },
          tooltip: {
            trigger: 'axis'
          },
          xAxis: {
            type: 'category',
            data: chartData.map(item => item.name),
            axisLabel: {
              rotate: 45,
              interval: 0
            }
          },
          yAxis: {
            type: 'value'
          },
          series: [{
            data: chartData.map(item => item.value),
            type: 'line',
            smooth: true,
            itemStyle: {
              color: '#52c41a'
            }
          }]
        }
        break
        
      default:
        console.warn('不支持的图表类型:', type)
        return null
    }
    
    console.log('生成的图表配置:', options)
    setChartOptions(options)
    return options
  }
  
  return {
    // 状态
    chartType,
    chartDimension,
    chartOptions,
    
    // 操作
    setChartType,
    setChartDimension,
    setChartOptions,
    generateChartData
  }
}) 