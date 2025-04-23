<template>
  <div class="app-container">
    <div class="map-container">
      <ClassmatesMap />
    </div>
    <div class="data-container">
      <ClassmatesData />
    </div>
  </div>
</template>

<script>
import ClassmatesMap from './components/ClassmatesMap.vue'
import ClassmatesData from './components/ClassmatesData.vue'

export default {
  name: 'App',
  components: {
    ClassmatesMap,
    ClassmatesData
  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', '微软雅黑', Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}

.app-container {
  display: flex;
  height: 100vh;
  width: 100%;
  overflow: hidden;
}

.map-container {
  width: 70%;
  height: 100%;
}

.data-container {
  width: 30%;
  height: 100%;
  padding: 20px;
  overflow-y: auto;
  border-left: 1px solid #ddd;
  background-color: #f9f9f9;
}
</style>