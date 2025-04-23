<template>
  <!-- 应用的主容器，采用flex布局将页面分为左右两部分 -->
  <div class="app-container">
    <!-- 左侧地图容器，占据70%的宽度 -->
    <div class="map-container">
      <!-- 引入地图组件，用于显示同学分布地图 -->
      <ClassmatesMap />
    </div>
    <!-- 右侧数据容器，占据30%的宽度，用于显示和管理同学数据 -->
    <div class="data-container">
      <!-- 引入数据管理组件，用于添加、编辑、删除同学信息 -->
      <ClassmatesData />
    </div>
  </div>
</template>

<script>
// 导入地图组件，负责显示地图和同学位置标记
import ClassmatesMap from './components/ClassmatesMap.vue'
// 导入数据管理组件，负责同学数据的增删改查操作
import ClassmatesData from './components/ClassmatesData.vue'

// 定义并导出Vue组件
export default {
  // 组件名称
  name: 'App',
  // 注册要使用的子组件
  components: {
    ClassmatesMap,
    ClassmatesData
  }
}
</script>

<style>
/* CSS重置，确保所有元素没有默认的外边距和内边距 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box; /* 使元素的宽度包含padding和border */
}

/* 全局字体和文本渲染设置 */
body {
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', '微软雅黑', Arial, sans-serif;
  -webkit-font-smoothing: antialiased; /* 在WebKit浏览器中平滑字体 */
  -moz-osx-font-smoothing: grayscale; /* 在Firefox中平滑字体 */
  color: #2c3e50; /* 设置文本颜色 */
}

/* 应用主容器样式，使用flex布局将页面分为左右两部分 */
.app-container {
  display: flex; /* 启用弹性盒子布局 */
  height: 100vh; /* 设置高度为视口高度的100% */
  width: 100%; /* 设置宽度为父容器的100% */
  overflow: hidden; /* 隐藏溢出内容 */
}

/* 地图容器样式，占据左侧70%的宽度 */
.map-container {
  width: 70%; /* 设置宽度为父容器的70% */
  height: 100%; /* 设置高度为父容器的100% */
}

.data-container {
  width: 30%; /* 设置宽度为父容器的30% */
  height: 100%; /* 设置高度为父容器的100% */
  padding: 20px; /* 设置内边距为20像素 */
  overflow-y: auto; /* 内容超出高度时显示垂直滚动条 */
  border-left: 1px solid #ddd;
  background-color: #f9f9f9; /* 设置浅灰色背景 */
}
</style>