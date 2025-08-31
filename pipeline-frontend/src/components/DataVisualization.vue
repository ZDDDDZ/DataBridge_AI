<template>
  <div class="data-visualization">
    <a-card v-if="hasData" class="visualization-card">
      <template #title>
        <div class="card-title">
          <bar-chart-outlined />
          查询结果分析
        </div>
      </template>
      
      <template #extra>
        <a-space>
          <a-tooltip title="导出数据">
            <a-button type="text" size="small" @click="exportData">
              <template #icon>
                <download-outlined />
              </template>
            </a-button>
          </a-tooltip>
          <a-tooltip title="刷新">
            <a-button type="text" size="small" @click="refreshData">
              <template #icon>
                <reload-outlined />
              </template>
            </a-button>
          </a-tooltip>
        </a-space>
      </template>

      <a-tabs v-model="activeTab" type="card" @change="handleTabChange">
        <!-- 表格视图 -->
        <a-tab-pane key="table" tab="表格视图">
          <template #tab>
            <table-outlined />
            表格视图
          </template>
          
          <div class="table-container">
            <div class="table-header">
              <div class="table-info">
                <a-statistic
                  title="数据总数"
                  :value="queryResult?.count || 0"
                  suffix="条"
                />
                <a-statistic
                  title="查询耗时"
                  :value="(queryResult?.execution_time || 0).toFixed(3)"
                  suffix="秒"
                />
              </div>
              <div class="table-actions">
                <a-input-search
                  v-model="searchText"
                  placeholder="搜索表格内容"
                  style="width: 200px"
                  @search="onSearch"
                />
              </div>
            </div>
            
            <a-table
              :dataSource="filteredData"
              :columns="tableColumns"
              :scroll="{ x: 1200, y: 400 }"
              :pagination="{
                pageSize: 10,
                showSizeChanger: true,
                showQuickJumper: true,
                showTotal: (total, range) => `第 ${range[0]}-${range[1]} 条，共 ${total} 条`
              }"
              size="middle"
              :loading="loading"
              row-key="id"
            >
              <template #bodyCell="{ column, record }">
                <template v-if="column.key === 'action'">
                  <a-space>
                    <a-button type="link" size="small" @click="viewDetails(record)">
                      详情
                    </a-button>
                  </a-space>
                </template>
              </template>
            </a-table>
          </div>
        </a-tab-pane>

        <!-- 图表视图 -->
        <a-tab-pane key="chart" tab="图表视图" v-if="canShowChart">
          <template #tab>
            <pie-chart-outlined />
            图表视图
          </template>
          
          <div class="chart-container">
            <div class="chart-controls">
              <a-space wrap>
                <div class="control-group">
                  <label>图表类型：</label>
                  <a-select
                    v-model="chartType"
                    style="width: 120px"
                    @change="handleChartTypeChange"
                  >
                    <a-select-option value="pie">饼图</a-select-option>
                    <a-select-option value="bar">柱状图</a-select-option>
                    <a-select-option value="line">折线图</a-select-option>
                  </a-select>
                </div>
                
                <div class="control-group">
                  <label>分析维度：</label>
                  <a-select
                    v-model="chartDimension"
                    style="width: 160px"
                    @change="handleChartDimensionChange"
                  >
                    <a-select-option 
                      v-for="col in chartableColumns" 
                      :key="col.dataIndex" 
                      :value="col.dataIndex"
                    >
                      {{ col.title }}
                    </a-select-option>
                  </a-select>
                </div>
                
                <div class="control-group">
                  <label>取值维度：</label>
                  <a-select
                    v-model="chartValueDimension"
                    style="width: 160px"
                    @change="handleChartValueDimensionChange"
                  >
                    <a-select-option 
                      v-for="col in tableColumns" 
                      :key="col.dataIndex" 
                      :value="col.dataIndex"
                    >
                      {{ col.title }}
                    </a-select-option>
                  </a-select>
                </div>
                
                <a-button @click="updateChart" type="primary" size="small">
                  <template #icon>
                    <sync-outlined />
                  </template>
                  更新图表
                </a-button>
              </a-space>
            </div>
            
            <div 
              ref="chartContainer" 
              class="chart-content"
              :class="{ 'chart-loading': chartLoading }"
            >
              <!-- 加载指示器 -->
              <a-spin v-if="chartLoading" class="chart-loading-spin" />
            </div>
          </div>
        </a-tab-pane>

        <!-- SQL语句 -->
        <a-tab-pane key="sql" tab="SQL查询">
          <template #tab>
            <code-outlined />
            SQL查询
          </template>
          
          <div class="sql-container">
            <div class="sql-header">
              <h4>生成的SQL语句</h4>
              <a-space>
                <a-button size="small" @click="copySql">
                  <template #icon>
                    <copy-outlined />
                  </template>
                  复制
                </a-button>
                <a-button size="small" @click="formatSql">
                  <template #icon>
                    <align-left-outlined />
                  </template>
                  格式化
                </a-button>
              </a-space>
            </div>
            
            <div class="sql-content">
              <pre><code>{{ formattedSql }}</code></pre>
            </div>
            
            <div class="sql-info">
              <a-descriptions size="small" :column="2">
                <a-descriptions-item label="执行状态">
                  <a-tag :color="queryResult?.status === 'success' ? 'green' : 'red'">
                    {{ queryResult?.status === 'success' ? '成功' : '失败' }}
                  </a-tag>
                </a-descriptions-item>
                <a-descriptions-item label="返回行数">
                  {{ queryResult?.count || 0 }}
                </a-descriptions-item>
                <a-descriptions-item label="执行时间">
                  {{ (queryResult?.execution_time || 0).toFixed(3) }}秒
                </a-descriptions-item>
                <a-descriptions-item label="查询时间">
                  {{ new Date().toLocaleString() }}
                </a-descriptions-item>
              </a-descriptions>
            </div>
          </div>
        </a-tab-pane>
      </a-tabs>
    </a-card>

    <!-- 空状态 -->
    <div v-else class="empty-state">
      <a-empty 
        description="暂无查询结果"
        :image="Empty.PRESENTED_IMAGE_SIMPLE"
      >
        <template #description>
          <span class="empty-description">
            请在上方输入您的问题进行查询
          </span>
        </template>
      </a-empty>
    </div>

    <!-- 详情弹窗 -->
    <a-modal
      :visible="detailVisible"
      @update:visible="detailVisible = $event"
      title="数据详情"
      :footer="null"
      width="600px"
    >
      <a-descriptions 
        v-if="selectedRecord"
        :column="1"
        bordered
        size="small"
      >
        <a-descriptions-item 
          v-for="(value, key) in selectedRecord" 
          :key="key"
          :label="getColumnTitle(key)"
        >
          {{ value || '-' }}
        </a-descriptions-item>
      </a-descriptions>
    </a-modal>
  </div>
</template>

<script>
import { ref, computed, onMounted, onUnmounted, watch, nextTick } from 'vue'
import { 
  BarChartOutlined,
  TableOutlined,
  PieChartOutlined,
  CodeOutlined,
  DownloadOutlined,
  ReloadOutlined,
  SyncOutlined,
  CopyOutlined,
  AlignLeftOutlined
} from '@ant-design/icons-vue'
import { message, Empty } from 'ant-design-vue'
import * as echarts from 'echarts/core'
import { PieChart, BarChart, LineChart } from 'echarts/charts'
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent
} from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'
import { useChartStore } from '../stores'

// 注册echarts组件
echarts.use([
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
  PieChart,
  BarChart,
  LineChart,
  CanvasRenderer
])

export default {
  name: 'DataVisualization',
  components: {
    BarChartOutlined,
    TableOutlined,
    PieChartOutlined,
    CodeOutlined,
    DownloadOutlined,
    ReloadOutlined,
    SyncOutlined,
    CopyOutlined,
    AlignLeftOutlined
  },
  props: {
    queryResult: {
      type: Object,
      default: () => ({
        data: [],
        count: 0,
        status: 'pending',
        sql: '',
        execution_time: 0
      })
    }
  },
  setup(props) {
    const chartStore = useChartStore()
    
    // 响应式状态
    const activeTab = ref('table')
    const chartType = ref('pie')
    const chartDimension = ref('')
    const chartValueDimension = ref('')
    const searchText = ref('')
    const loading = ref(false)
    const chartLoading = ref(false)
    const detailVisible = ref(false)
    const selectedRecord = ref(null)
    const chartContainer = ref(null)
    const formattedSql = ref('')
    
    let chart = null
    
    // 计算属性
    const hasData = computed(() => {
      return props.queryResult && 
             props.queryResult?.data && 
             Array.isArray(props.queryResult?.data) && 
             props.queryResult?.data?.length > 0
    })
    
    const tableData = computed(() => {
      if (!hasData.value) return []
      return props.queryResult?.data?.map((item, index) => ({
        ...item,
        key: item.id || index
      })) || []
    })
    
    const filteredData = computed(() => {
      if (!searchText.value) return tableData.value
      
      const searchLower = searchText.value.toLowerCase()
      return tableData.value.filter(record => 
        Object.values(record).some(value => 
          String(value).toLowerCase().includes(searchLower)
        )
      )
    })
    
    const tableColumns = computed(() => {
      if (!hasData.value) return []
      
      const firstRow = props.queryResult?.data?.[0]
      if (!firstRow) return []
      
      const columns = Object.keys(firstRow).map(key => ({
        title: getColumnTitle(key),
        dataIndex: key,
        key,
        ellipsis: true,
        sorter: (a, b) => {
          const aVal = a[key]
          const bVal = b[key]
          if (typeof aVal === 'number' && typeof bVal === 'number') {
            return aVal - bVal
          }
          return String(aVal).localeCompare(String(bVal))
        }
      }))
      
      // 添加操作列
      columns.push({
        title: '操作',
        key: 'action',
        width: 100,
        fixed: 'right'
      })
      
      return columns
    })
    
    const chartableColumns = computed(() => {
      if (!hasData.value) return []
      
      return tableColumns.value.filter(col => {
        if (col.key === 'action') return false
        
        // 排除纯数值ID字段作为分析维度
        if (col.dataIndex === 'id') return false
        
        const sampleValue = props.queryResult?.data?.[0]?.[col.dataIndex]
        return typeof sampleValue !== 'number' || col.dataIndex.includes('year')
      })
    })
    
    const canShowChart = computed(() => {
      return hasData.value && chartableColumns.value.length > 0
    })
    
    // 方法
    const getColumnTitle = (key) => {
      const titleMap = {
        id: 'ID',
        province: '省份',
        city: '城市',
        street: '街道',
        road: '道路',
        location: '具体位置',
        disaster_type: '灾害类型',
        geological_feature: '地质特性',
        pipeline_type: '管线类型',
        build_year: '建成年份',
        laying_method: '敷设方式',
        created_at: '创建时间',
        updated_at: '更新时间'
      }
      return titleMap[key] || key
    }
    
    const onSearch = () => {
      // 搜索功能已在computed中实现
    }
    
    const viewDetails = (record) => {
      selectedRecord.value = record
      detailVisible.value = true
    }
    
    const initChart = async () => {
      console.log('开始初始化图表')
      await nextTick()
      
      if (!chartContainer.value) {
        console.error('图表容器不存在')
        return
      }
      
      console.log('图表容器存在，尺寸:', {
        offsetWidth: chartContainer.value.offsetWidth,
        offsetHeight: chartContainer.value.offsetHeight
      })
      
      // 确保容器有尺寸
      if (chartContainer.value.offsetHeight === 0) {
        chartContainer.value.style.height = '400px'
        console.log('设置容器高度为400px')
      }
      
      // 检查容器是否可见
      const rect = chartContainer.value.getBoundingClientRect()
      console.log('容器矩形信息:', rect)
      if (rect.width === 0 || rect.height === 0) {
        console.error('容器尺寸为0，无法初始化图表')
        return
      }
      
      // 销毁现有图表
      if (chart) {
        console.log('销毁现有图表')
        chart.dispose()
        chart = null
      }
      
      try {
        // 初始化新图表
        console.log('创建echarts实例')
        chart = echarts.init(chartContainer.value)
        console.log('图表实例创建成功')
        
        // 设置默认维度
        if (chartableColumns.value.length > 0) {
          if (!chartDimension.value) {
            chartDimension.value = chartableColumns.value[0].dataIndex
            console.log('设置默认分析维度:', chartDimension.value)
          }
          if (!chartValueDimension.value) {
            // 尝试找到一个数值类型的列作为默认取值维度
            const numericColumn = tableColumns.value.find(col => {
              if (col.key === 'action') return false
              const sampleValue = props.queryResult?.data?.[0]?.[col.dataIndex]
              const { isNumeric } = isNumericValue(sampleValue)
              return isNumeric
            })
            
            if (numericColumn) {
              chartValueDimension.value = numericColumn.dataIndex
              console.log('设置默认取值维度:', chartValueDimension.value)
            } else {
              // 如果没有数值列，使用第一个非操作列
              const firstColumn = tableColumns.value.find(col => col.key !== 'action')
              if (firstColumn) {
                chartValueDimension.value = firstColumn.dataIndex
                console.log('设置默认取值维度:', chartValueDimension.value)
              }
            }
          }
          updateChart()
        } else {
          console.warn('没有可用的图表维度')
        }
        
        // 简单的窗口大小变化监听
        const resizeHandler = () => {
          if (chart && chart.resize) {
            chart.resize()
          }
        }
        
        window.addEventListener('resize', resizeHandler)
        chart._resizeHandler = resizeHandler
        
      } catch (error) {
        console.error('图表初始化失败:', error)
        message.error('图表初始化失败: ' + error.message)
      }
    }
    
    const updateChart = () => {
      console.log('updateChart 被调用')
      console.log('当前状态:', {
        chart: !!chart,
        hasData: hasData.value,
        chartDimension: chartDimension.value,
        chartValueDimension: chartValueDimension.value,
        chartType: chartType.value,
        dataLength: props.queryResult?.data?.length
      })
      
      // 添加更详细的调试信息
      console.log('chartType 详细信息:', {
        value: chartType.value,
        type: typeof chartType.value,
        ref: chartType
      })
      console.log('chartDimension 详细信息:', {
        value: chartDimension.value,
        type: typeof chartDimension.value,
        ref: chartDimension
      })
      console.log('chartValueDimension 详细信息:', {
        value: chartValueDimension.value,
        type: typeof chartValueDimension.value,
        ref: chartValueDimension
      })
      
      if (!chart) {
        console.warn('图表实例不存在，无法更新')
        return
      }
      
      if (!hasData.value) {
        console.warn('没有数据，无法更新图表')
        return
      }
      
      if (!chartDimension.value) {
        console.warn('未选择分析维度，无法更新图表')
        return
      }
      
      if (!chartValueDimension.value) {
        console.warn('未选择取值维度，无法更新图表')
        return
      }
      
      chartLoading.value = true
      
      try {
        console.log('调用 chartStore.generateChartData')
        const options = chartStore.generateChartData(
          props.queryResult?.data || [],
          chartDimension.value,
          chartType.value,
          chartValueDimension.value
        )
        
        console.log('generateChartData 返回结果:', options)
        
        if (options) {
          console.log('设置图表配置')
          chart.setOption(options, true)
          console.log('图表更新成功')
        } else {
          console.warn('图表配置为空')
        }
      } catch (error) {
        console.error('图表更新失败:', error)
        message.error('图表更新失败: ' + error.message)
      } finally {
        chartLoading.value = false
      }
    }
    
    const exportData = () => {
      try {
        const dataStr = JSON.stringify(props.queryResult?.data || [], null, 2)
        const blob = new Blob([dataStr], { type: 'application/json' })
        const url = URL.createObjectURL(blob)
        
        const link = document.createElement('a')
        link.href = url
        link.download = `pipeline_data_${new Date().getTime()}.json`
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
        URL.revokeObjectURL(url)
        
        message.success('数据导出成功')
      } catch (error) {
        console.error('导出失败:', error)
        message.error('导出失败')
      }
    }
    
    const refreshData = () => {
      if (chart) {
        updateChart()
        message.success('数据已刷新')
      }
    }
    
    const copySql = () => {
      try {
        navigator.clipboard.writeText(props.queryResult?.sql || '')
        message.success('SQL语句已复制到剪贴板')
      } catch (error) {
        console.error('复制失败:', error)
        message.error('复制失败')
      }
    }
    
    const formatSql = () => {
      // 简单的SQL格式化
      const sql = props.queryResult?.sql || ''
      formattedSql.value = sql
        .replace(/\bSELECT\b/gi, 'SELECT')
        .replace(/\bFROM\b/gi, '\nFROM')
        .replace(/\bWHERE\b/gi, '\nWHERE')
        .replace(/\bGROUP BY\b/gi, '\nGROUP BY')
        .replace(/\bORDER BY\b/gi, '\nORDER BY')
        .replace(/\bLIMIT\b/gi, '\nLIMIT')
    }
    
    const handleTabChange = (key) => {
      console.log('Tabs change事件触发:', key)
      activeTab.value = key
    }
    
    const handleChartTypeChange = (value) => {
      console.log('图表类型变化:', value)
      chartType.value = value
      updateChart()
    }
    
    const handleChartDimensionChange = (value) => {
      console.log('图表维度变化:', value)
      chartDimension.value = value
      updateChart()
    }
    
    const handleChartValueDimensionChange = (value) => {
      console.log('取值维度变化:', value)
      chartValueDimension.value = value
      updateChart()
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
    
    // 监听数据变化
    watch(() => props.queryResult, async (newResult) => {
      if (newResult && newResult.data && newResult.data.length > 0) {
        formattedSql.value = newResult.sql || ''
        
        // 如果当前在图表标签页且数据支持图表，初始化图表
        if (activeTab.value === 'chart' && canShowChart.value) {
          await nextTick()
          
          // 延迟一点时间确保DOM完全渲染
          setTimeout(() => {
            if (!chart) {
              initChart()
            } else {
              updateChart()
            }
          }, 500)
        }
      }
    }, { deep: true })
    
    // 监听激活标签页变化
    watch(activeTab, async (newTab, oldTab) => {
      console.log('标签页切换监听器触发:', { newTab, oldTab })
      console.log('当前状态:', {
        canShowChart: canShowChart.value,
        hasData: hasData.value,
        chartableColumnsLength: chartableColumns.value.length
      })
      
      if (newTab === 'chart' && canShowChart.value) {
        console.log('准备初始化图表')
        // 等待DOM更新
        await nextTick()
        
        // 增加延迟，确保标签页切换动画完成，DOM完全可见
        setTimeout(() => {
          console.log('开始初始化图表')
          if (!chart) {
            initChart()
          } else {
            chart.resize()
            updateChart()
          }
        }, 500)
      } else {
        console.log('不满足图表初始化条件:', {
          newTab,
          canShowChart: canShowChart.value,
          hasData: hasData.value
        })
      }
    }, { immediate: true })
    
    // 组件挂载
    onMounted(async () => {
      console.log('组件挂载，当前activeTab:', activeTab.value)
      console.log('chartableColumns:', chartableColumns.value)
      console.log('tableColumns:', tableColumns.value)
      console.log('chartType:', chartType.value)
      console.log('chartDimension:', chartDimension.value)
      console.log('chartValueDimension:', chartValueDimension.value)
      
      if (props.queryResult?.sql) {
        formatSql()
      }
      
      // 测试activeTab的响应式
      setTimeout(() => {
        console.log('延迟检查activeTab:', activeTab.value)
        console.log('延迟检查chartableColumns:', chartableColumns.value)
        console.log('延迟检查chartValueDimension:', chartValueDimension.value)
      }, 1000)
    })
    
    // 组件卸载时清理图表
    onUnmounted(() => {
      if (chart) {
        // 移除事件监听器
        if (chart._resizeHandler) {
          window.removeEventListener('resize', chart._resizeHandler)
        }
        
        // 销毁图表实例
        chart.dispose()
        chart = null
      }
    })
    
    return {
      // 状态
      activeTab,
      chartType,
      chartDimension,
      chartValueDimension,
      searchText,
      loading,
      chartLoading,
      detailVisible,
      selectedRecord,
      chartContainer,
      formattedSql,
      Empty,
      queryResult: props.queryResult,
      
      // 计算属性
      hasData,
      tableData,
      filteredData,
      tableColumns,
      chartableColumns,
      canShowChart,
      
      // 方法
      getColumnTitle,
      onSearch,
      viewDetails,
      updateChart,
      exportData,
      refreshData,
      copySql,
      formatSql,
      handleTabChange,
      handleChartTypeChange,
      handleChartDimensionChange,
      handleChartValueDimensionChange,
      initChart,
      isNumericValue
    }
  }
}
</script>

<style scoped>
.data-visualization {
  margin-top: 24px;
}

.visualization-card {
  min-height: 500px;
}

.card-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
}

.table-container {
  margin-top: 16px;
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  padding: 16px;
  background: #fafafa;
  border-radius: 6px;
}

.table-info {
  display: flex;
  gap: 32px;
}

.chart-container {
  margin-top: 16px;
}

.chart-controls {
  padding: 16px;
  background: #fafafa;
  border-radius: 6px;
  margin-bottom: 16px;
}

.control-group {
  display: flex;
  align-items: center;
  gap: 8px;
}

.control-group label {
  font-weight: 500;
  color: #333;
  white-space: nowrap;
}

.chart-content {
  width: 100%;
  height: 400px;
  min-height: 400px;
  border: 1px solid #f0f0f0;
  border-radius: 6px;
  position: relative;
}

.sql-container {
  margin-top: 16px;
}

.sql-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.sql-header h4 {
  margin: 0;
  color: #333;
}

.sql-content {
  background: #f6f8fa;
  border: 1px solid #e1e4e8;
  border-radius: 6px;
  padding: 16px;
  margin-bottom: 16px;
  overflow-x: auto;
}

.sql-content pre {
  margin: 0;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: 13px;
  line-height: 1.45;
  color: #24292e;
  white-space: pre-wrap;
  word-wrap: break-word;
}

.sql-info {
  background: #fafafa;
  padding: 16px;
  border-radius: 6px;
}

.empty-state {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 300px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.empty-description {
  color: #999;
  font-size: 14px;
}

.chart-loading {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: rgba(255, 255, 255, 0.8);
  border-radius: 6px;
  z-index: 10;
}

.chart-loading-spin {
  color: #1890ff; /* 图表加载指示器的颜色 */
}

/* 响应式设计 */
@media (max-width: 768px) {
  .table-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }
  
  .table-info {
    flex-direction: column;
    gap: 16px;
    width: 100%;
  }
  
  .chart-controls {
    padding: 12px;
  }
  
  .chart-content {
    height: 300px;
  }
}
</style> 