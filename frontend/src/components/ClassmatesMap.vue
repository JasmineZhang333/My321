<template>
  <!-- 地图组件的主容器 -->
  <div class="map-wrapper">
    <!-- 地图将被渲染到这个div中，ref属性用于在JavaScript中引用这个DOM元素 -->
    <div id="map" ref="mapContainer"></div>
    <!-- 统计信息悬浮层，显示在地图上方 -->
    <div class="statistics-overlay">
      <!-- 使用Element Plus的卡片组件展示统计信息 -->
      <el-card class="statistics-card">
        <!-- 卡片头部模板 -->
        <template #header>
          <div class="card-header">
            <span>统计信息</span>
          </div>
        </template>
        <!-- 当统计数据加载完成时显示内容 -->
        <div v-if="statistics">
          <!-- 显示总人数 -->
          <p><strong>总人数:</strong> {{ statistics.total }} 人</p>
          <el-divider></el-divider>
          <h4>按国家统计</h4>
          <!-- 使用v-for循环渲染国家统计列表 -->
          <ul class="stat-list">
            <li v-for="(count, country) in statistics.country_stats" :key="country">
              {{ country }}: {{ count }} 人
            </li>
          </ul>
          <el-divider></el-divider>
          <h4>按城市统计</h4>
          <!-- 使用v-for循环渲染城市统计列表 -->
          <ul class="stat-list">
            <li v-for="(count, city) in statistics.city_stats" :key="city">
              {{ city }}: {{ count }} 人
            </li>
          </ul>
        </div>
        <!-- 当统计数据未加载完成时显示骨架屏 -->
        <div v-else>
          <el-skeleton :rows="6" animated />
        </div>
      </el-card>
    </div>
  </div>
</template>

<script>
// 导入Leaflet地图库的CSS样式
import 'leaflet/dist/leaflet.css'
// 导入Leaflet地图库，这是一个开源的JavaScript地图库
import L from 'leaflet'
// 导入API服务，用于与后端进行数据交互
import apiService from '../services/api.js'
// 导入事件总线，用于组件间通信
import eventBus from '../utils/eventBus.js'
// 导入Element Plus的消息提示组件
import { ElMessage } from 'element-plus'

export default {
  // 组件名称
  name: 'ClassmatesMap',
  // 组件的数据
  data() {
    return {
      map: null,         // 存储Leaflet地图实例
      markers: [],       // 存储地图上的标记点
      classmates: [],    // 存储同学数据
      statistics: null   // 存储统计信息
    }
  },
  // 组件挂载到DOM后执行
  mounted() {
    // 初始化地图
    this.initMap()
    // 获取同学数据
    this.fetchClassmates()
    // 获取统计数据
    this.fetchStatistics()
    
    // 监听数据更新事件，当数据更新时刷新地图
    eventBus.on('data-updated', this.refreshData)
  },
  // 组件卸载前执行
  beforeUnmount() {
    // 移除事件监听，防止内存泄漏
    eventBus.off('data-updated', this.refreshData)
  },
  // 组件的方法
  methods: {
    // 初始化地图
    initMap() {
      // 创建Leaflet地图实例，绑定到mapContainer这个DOM元素
      this.map = L.map(this.$refs.mapContainer, {
        center: [35.0, 105.0], // 设置地图中心为中国中心位置
        zoom: 4,               // 设置初始缩放级别
        minZoom: 2,            // 设置最小缩放级别
        maxZoom: 18            // 设置最大缩放级别
      })

      // 添加OpenStreetMap的瓦片图层
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors' // 地图版权信息
      }).addTo(this.map) // 将图层添加到地图上
    },
    // 从后端获取同学数据
    async fetchClassmates() {
      try {
        // 调用API服务获取同学数据
        this.classmates = await apiService.getClassmates()
        // 在地图上添加标记点
        this.addMarkers()
      } catch (error) {
        // 错误处理
        console.error('获取同学数据失败:', error)
        ElMessage.error('获取同学数据失败') // 显示错误提示
      }
    },
    // 从后端获取统计数据
    async fetchStatistics() {
      try {
        // 调用API服务获取统计数据
        this.statistics = await apiService.getStatistics()
      } catch (error) {
        // 错误处理
        console.error('获取统计数据失败:', error)
        ElMessage.error('获取统计数据失败') // 显示错误提示
      }
    },
    // 添加地图标记点
    addMarkers() {
      // 先清除现有的所有标记点
      this.clearMarkers()
      
      // 按城市对同学数据进行分组
      const cityGroups = this.groupClassmatesByCity()
      
      // 遍历每个城市分组
      for (const city in cityGroups) {
        const group = cityGroups[city]
        const firstClassmate = group[0]
        
        // 创建标记点
        const marker = L.marker([firstClassmate.location.lat, firstClassmate.location.lng])
        
        // 创建弹出窗口内容
        let popupContent = `<div class="marker-popup"><h3>${city}</h3><ul>`
        
        // 添加该城市的所有同学到弹出窗口
        group.forEach(classmate => {
          popupContent += `<li>${classmate.name}</li>`
        })
        
        popupContent += `</ul></div>`
        
        // 将弹出窗口绑定到标记点
        marker.bindPopup(popupContent)
        
        // 将标记点添加到地图
        marker.addTo(this.map)
        
        // 将标记点保存到数组中，方便后续管理
        this.markers.push(marker)
      }
    },
    
    // 清除地图上的所有标记点
    clearMarkers() {
      // 遍历所有标记点并从地图中移除
      this.markers.forEach(marker => {
        marker.remove()
      })
      
      // 清空标记点数组
      this.markers = []
    },
    
    // 刷新地图数据
    refreshData() {
      // 重新获取同学数据
      this.fetchClassmates()
      // 重新获取统计数据
      this.fetchStatistics()
    },
    
    // 按城市对同学数据进行分组
    groupClassmatesByCity() {
      const cityGroups = {}
      
      this.classmates.forEach(classmate => {
        const cityKey = `${classmate.city}-${classmate.country}`
        
        if (!cityGroups[cityKey]) {
          cityGroups[cityKey] = {
            city: classmate.city,
            country: classmate.country,
            location: classmate.location,
            classmates: []
          }
        }
        
        cityGroups[cityKey].classmates.push(classmate.name)
      })
      
      return Object.values(cityGroups)
    },
    addMarkers() {
      // 清除现有标记
      this.clearMarkers()
      
      // 按城市分组
      const cityGroups = this.groupClassmatesByCity()
      
      // 为每个城市添加标记
      cityGroups.forEach(group => {
        const { lat, lng } = group.location
        
        // 创建自定义图标
        const marker = L.marker([lat, lng], {
          icon: L.divIcon({
            className: 'location-marker',
            html: '<span>★</span>',
            iconSize: [30, 30]
          })
        }).addTo(this.map)
        
        // 生成同学姓名列表
        const classmatesList = group.classmates.map(name => `<li>${name}</li>`).join('')
        
        // 添加弹出信息
        marker.bindPopup(`
          <div class="location-popup">
            <h3>${group.city}, ${group.country}</h3>
            <p>纬度: ${lat.toFixed(4)}, 经度: ${lng.toFixed(4)}</p>
            <p>同学名单:</p>
            <ul class="classmates-list">
              ${classmatesList}
            </ul>
          </div>
        `)
        
        this.markers.push(marker)
      })
      
      // 如果有标记，调整地图视图以显示所有标记
      if (this.markers.length > 0) {
        const group = L.featureGroup(this.markers)
        this.map.fitBounds(group.getBounds(), { padding: [50, 50] })
      }
    },
    clearMarkers() {
      this.markers.forEach(marker => {
        this.map.removeLayer(marker)
      })
      this.markers = []
    },
    refreshData() {
      this.fetchClassmates()
      this.fetchStatistics()
    }
  }
}
</script>

<style scoped>
.map-wrapper {
  position: relative;
  width: 100%;
  height: 100%;
}

#map {
  width: 100%;
  height: 100%;
}

.statistics-overlay {
  position: absolute;
  top: 20px;
  right: 20px;
  z-index: 1000;
  max-width: 300px;
  max-height: 80%;
  overflow-y: auto;
  background-color: rgba(255, 255, 255, 0.9);
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.statistics-card {
  width: 100%;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.stat-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.stat-list li {
  padding: 5px 0;
  border-bottom: 1px dashed #eee;
}
</style>