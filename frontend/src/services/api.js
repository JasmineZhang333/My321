import axios from 'axios'

// API服务类，集中管理与后端的通信
class ApiService {
  // 获取所有同学信息
  async getClassmates() {
    try {
      const response = await axios.get('/api/classmates')
      return response.data
    } catch (error) {
      console.error('获取同学数据失败:', error)
      throw error
    }
  }

  // 获取单个同学信息
  async getClassmate(id) {
    try {
      const response = await axios.get(`/api/classmates/${id}`)
      return response.data
    } catch (error) {
      console.error(`获取同学ID:${id}数据失败:`, error)
      throw error
    }
  }

  // 添加新同学
  async addClassmate(classmateData) {
    try {
      const response = await axios.post('/api/classmates', classmateData)
      return response.data
    } catch (error) {
      console.error('添加同学数据失败:', error)
      throw error
    }
  }

  // 更新同学信息
  async updateClassmate(id, classmateData) {
    try {
      const response = await axios.put(`/api/classmates/${id}`, classmateData)
      return response.data
    } catch (error) {
      console.error(`更新同学ID:${id}数据失败:`, error)
      throw error
    }
  }

  // 删除同学信息
  async deleteClassmate(id) {
    try {
      const response = await axios.delete(`/api/classmates/${id}`)
      return response.data
    } catch (error) {
      console.error(`删除同学ID:${id}失败:`, error)
      throw error
    }
  }

  // 获取统计信息
  async getStatistics() {
    try {
      const response = await axios.get('/api/statistics')
      return response.data
    } catch (error) {
      console.error('获取统计数据失败:', error)
      throw error
    }
  }
}

// 创建单例实例
const apiService = new ApiService()

export default apiService