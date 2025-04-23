<template>
  <div class="location-search">
    <el-input
      v-model="searchQuery"
      placeholder="输入地址或城市名称搜索位置"
      class="search-input"
      clearable
      @keyup.enter="searchLocation"
    >
      <template #append>
        <el-button @click="searchLocation">搜索</el-button>
      </template>
    </el-input>
    
    <div v-if="loading" class="search-results">
      <el-skeleton :rows="3" animated />
    </div>
    
    <div v-else-if="searchResults.length > 0" class="search-results">
      <el-card v-for="(result, index) in searchResults" :key="index" class="result-card" @click="selectLocation(result)">
        <div class="result-item">
          <div class="result-name">{{ result.display_name }}</div>
          <div class="result-coords">经度: {{ result.lon }}, 纬度: {{ result.lat }}</div>
        </div>
      </el-card>
    </div>
    
    <div v-else-if="searchPerformed && searchResults.length === 0" class="no-results">
      未找到匹配的位置，请尝试其他关键词
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { ElMessage } from 'element-plus'

export default {
  name: 'LocationSearch',
  props: {
    initialLocation: {
      type: Object,
      default: () => ({ lat: 0, lng: 0 })
    }
  },
  data() {
    return {
      searchQuery: '',
      searchResults: [],
      loading: false,
      searchPerformed: false
    }
  },
  methods: {
    async searchLocation() {
      if (!this.searchQuery.trim()) {
        ElMessage.warning('请输入搜索关键词')
        return Promise.reject('搜索关键词为空')
      }
      
      this.loading = true
      this.searchPerformed = true
      
      try {
        // 使用OpenStreetMap的Nominatim API进行地理编码
        const response = await axios.get('https://nominatim.openstreetmap.org/search', {
          params: {
            q: this.searchQuery,
            format: 'json',
            limit: 5
          },
          headers: {
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
          }
        })
        
        this.searchResults = response.data
        return Promise.resolve(this.searchResults)
      } catch (error) {
        console.error('位置搜索失败:', error)
        ElMessage.error('位置搜索失败，请稍后重试')
        this.searchResults = []
        return Promise.reject(error)
      } finally {
        this.loading = false
      }
    },
    selectLocation(result) {
      const location = {
        lat: parseFloat(result.lat),
        lng: parseFloat(result.lon)
      }
      
      // 向父组件发送选中的位置信息
      this.$emit('location-selected', {
        location,
        address: result.display_name,
        // 尝试从结果中提取城市和国家信息
        city: this.extractCity(result),
        country: this.extractCountry(result)
      })
      
      // 清空搜索结果
      this.searchResults = []
      this.searchQuery = ''
    },
    extractCity(result) {
      // 尝试从结果中提取城市信息
      if (result.address) {
        return result.address.city || result.address.town || result.address.village || ''
      }
      return ''
    },
    extractCountry(result) {
      // 尝试从结果中提取国家信息
      if (result.address && result.address.country) {
        return result.address.country
      }
      return ''
    }
  }
}
</script>

<style scoped>
.location-search {
  margin-bottom: 20px;
}

.search-input {
  margin-bottom: 10px;
}

.search-results {
  max-height: 300px;
  overflow-y: auto;
  margin-top: 10px;
}

.result-card {
  margin-bottom: 10px;
  cursor: pointer;
  transition: all 0.3s;
}

.result-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.result-item {
  padding: 5px 0;
}

.result-name {
  font-weight: bold;
  margin-bottom: 5px;
}

.result-coords {
  font-size: 12px;
  color: #666;
}

.no-results {
  text-align: center;
  color: #909399;
  padding: 20px 0;
}
</style>