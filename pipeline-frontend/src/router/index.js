/**
 * Vue Router 路由配置
 * 管道信息智能查询系统
 */

import { createRouter, createWebHistory } from 'vue-router'

// 路由组件懒加载
const Home = () => import('../views/Home.vue')
const About = () => import('../views/About.vue')

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: {
      title: '首页',
      keepAlive: true
    }
  },
  {
    path: '/about',
    name: 'About',
    component: About,
    meta: {
      title: '关于系统'
    }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('../views/NotFound.vue'),
    meta: {
      title: '页面未找到'
    }
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
  scrollBehavior(to, from, savedPosition) {
    // 路由切换时的滚动行为
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  }
})

// 全局前置守卫
router.beforeEach((to, from, next) => {
  // 设置页面标题
  if (to.meta.title) {
    document.title = `${to.meta.title} - 管道信息智能查询系统`
  } else {
    document.title = '管道信息智能查询系统'
  }
  
  // NProgress 可以在这里添加进度条
  next()
})

// 全局后置钩子
router.afterEach((to, from) => {
  // 路由切换完成后的处理
  console.log(`路由从 ${from.name} 切换到 ${to.name}`)
})

export default router 