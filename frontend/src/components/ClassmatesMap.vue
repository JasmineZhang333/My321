<template>
  <div class="map-wrapper">
    <div id="map" ref="mapContainer"></div>
    <div class="statistics-overlay">
      <el-card class="statistics-card">
        <template #header>
          <div class="card-header">
            <span>统计信息</span>
          </div>
        </template>
        <div v-if="statistics">
          <p><strong>总人数:</strong> {{ statistics.total }} 人</p>
          <el-divider></el-divider>
          <h4>按国家统计</h4>
          <ul class="stat-list">
            <li v-for="(count, country) in statistics.country_stats" :key="country">
              {{ country }}: {{ count }} 人
            </li>
          </ul>
          <el-divider></el-divider>
          <h4>按城市统计</h4>
          <ul class="stat-list">
            <li v-for="(count, city) in statistics.city_stats" :key="city">
              {{ city }}: {{ count }} 人
            </li>
          </ul>
        </div>
        <div v-else>
          <el-skeleton :rows="6" animated />
        </div>
      </el-card>
    </div>
  </div>
</template>

<script>
import 'leaflet/dist/leaflet.css'
import L from 'leaflet'
import apiService from '../services/api.js'
import eventBus from '../utils/eventBus.js'
import { ElMessage } from 'element-plus'

export default {
  name: 'ClassmatesMap',
  data() {
    return {
      map: null,
      markers: [],
      classmates: [],
      statistics: null
    }
  },
  mounted() {
    this.initMap()
    this.fetchClassmates()
    this.fetchStatistics()
    
    // 监听数据更新事件
    eventBus.on('data-updated', this.refreshData)
  },
  beforeUnmount() {
    // 移除事件监听
    eventBus.off('data-updated', this.refreshData)
  },
  methods: {
    initMap() {
      // 创建地图实例
      this.map = L.map(this.$refs.mapContainer, {
        center: [35.0, 105.0], // 中国中心位置
        zoom: 4,
        minZoom: 2,
        maxZoom: 18
      })

      // 添加地图图层
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      }).addTo(this.map)
    },
    async fetchClassmates() {
      try {
        this.classmates = await apiService.getClassmates()
        this.addMarkers()
      } catch (error) {
        console.error('获取同学数据失败:', error)
        ElMessage.error('获取同学数据失败')
      }
    },
    async fetchStatistics() {
      try {
        this.statistics = await apiService.getStatistics()
      } catch (error) {
        console.error('获取统计数据失败:', error)
        ElMessage.error('获取统计数据失败')
      }
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