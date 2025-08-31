const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  transpileDependencies: true,
  
  // 开发服务器配置
  devServer: {
    port: 8080,
    host: '0.0.0.0',
    open: true,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
        logLevel: 'debug'
      }
    }
  },
  
  // 生产环境配置
  publicPath: process.env.NODE_ENV === 'production' ? './' : '/',
  
  // 构建配置
  configureWebpack: {
    resolve: {
      alias: {
        '@': require('path').resolve(__dirname, 'src')
      }
    }
  },
  
  // CSS配置
  css: {
    loaderOptions: {
      less: {
        lessOptions: {
          modifyVars: {
            // 自定义主题色
            'primary-color': '#1890ff',
            'link-color': '#1890ff',
            'border-radius-base': '6px'
          },
          javascriptEnabled: true
        }
      }
    }
  },
  
  // PWA配置
  pwa: {
    name: '管道信息智能查询系统',
    themeColor: '#1890ff',
    msTileColor: '#1890ff',
    appleMobileWebAppCapable: 'yes',
    appleMobileWebAppStatusBarStyle: 'black'
  }
}) 