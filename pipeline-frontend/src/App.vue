<template>
  <div id="app">
    <a-config-provider :locale="zhCN">
      <router-view />
    </a-config-provider>
  </div>
</template>

<script>
import { onMounted } from 'vue'
import zhCN from 'ant-design-vue/es/locale/zh_CN'
import { useAppStore } from './stores'

export default {
  name: 'App',
  setup() {
    const appStore = useAppStore()
    
    // 初始化应用
    const initApp = async () => {
      try {
        // 可以在这里添加初始化逻辑
        console.log('应用初始化完成')
      } catch (error) {
        console.error('应用初始化失败:', error)
      }
    }
    
    // 挂载时初始化
    onMounted(() => {
      initApp()
    })
    
    return {
      zhCN
    }
  }
}
</script>

<style>
/* 全局样式已在 global.css 中定义 */
</style> 