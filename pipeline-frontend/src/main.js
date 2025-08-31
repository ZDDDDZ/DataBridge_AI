/**
 * 管道信息智能查询系统前端入口文件
 */

import { createApp } from 'vue'
import App from './App.vue'
import { createPinia } from 'pinia'
import router from './router'

// Ant Design Vue
import Antd from 'ant-design-vue'
import 'ant-design-vue/dist/reset.css'

// 全局样式
import './assets/styles/global.css'

// 创建应用实例
const app = createApp(App)

// 使用插件
app.use(createPinia())
app.use(router)
app.use(Antd)

// 全局属性
app.config.globalProperties.$appName = '管道信息智能查询系统'
app.config.globalProperties.$version = '1.0.0'

// 全局错误处理
app.config.errorHandler = (err, vm, info) => {
  console.error('应用错误:', err)
  console.error('错误信息:', info)
  
  // 在生产环境中，这里可以发送错误报告到服务器
  if (process.env.NODE_ENV === 'production') {
    // 发送错误报告
    console.log('发送错误报告到服务器')
  }
}

// 挂载应用
app.mount('#app')

// 生产环境性能提示
if (process.env.NODE_ENV === 'development') {
  console.log('🚀 管道信息智能查询系统启动成功')
  console.log('📊 开发模式已启用')
} 