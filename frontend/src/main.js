// 导入Vue框架的createApp函数，这是创建Vue应用的核心函数
import { createApp } from 'vue'
// 导入根组件App.vue，这是整个应用的最顶层组件
import App from './App.vue'
// 导入路由配置，用于实现页面间的跳转功能
import router from './router'
// 导入ElementPlus组件库，这是一套基于Vue的UI组件库，提供了按钮、表单等常用组件
import ElementPlus from 'element-plus'
// 导入ElementPlus的样式文件
import 'element-plus/dist/index.css'
// 导入自定义的全局CSS样式
import './assets/main.css'

// 创建Vue应用实例，传入App作为根组件
const app = createApp(App)

// 将路由系统集成到Vue应用中
app.use(router)
// 将ElementPlus组件库集成到Vue应用中，使其组件可在全局使用
app.use(ElementPlus)

// 将Vue应用挂载到HTML中id为'app'的DOM元素上，这会替换该元素
app.mount('#app')