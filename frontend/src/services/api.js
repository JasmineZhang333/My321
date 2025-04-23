import axios from 'axios'

/**
 * API服务类，用于集中管理前端与后端的所有通信
 * 使用axios库发送HTTP请求，实现与后端API的交互
 * 所有方法都返回Promise，支持异步操作
 */
class ApiService {
  /**
   * 获取所有同学的信息列表
   * @returns {Promise<Array>} 返回包含所有同学信息的数组
   * @throws {Error} 当API请求失败时抛出错误
   * 
   * 返回的数据格式示例：
   * [
   *   {
   *     id: 1,
   *     name: "张三",
   *     city: "北京",
   *     country: "中国",
   *     location: { lat: 39.9042, lng: 116.4074 }
   *   },
   *   ...
   * ]
   */
  async getClassmates() {
    try {
      const response = await axios.get('/api/classmates')
      return response.data
    } catch (error) {
      console.error('获取同学数据失败:', error)
      throw error
    }
  }

  /**
   * 获取单个同学的详细信息
   * @param {number} id - 要获取信息的同学ID
   * @returns {Promise<Object>} 返回包含该同学详细信息的对象
   * @throws {Error} 当API请求失败时抛出错误
   * 
   * 返回的数据格式示例：
   * {
   *   id: 1,
   *   name: "张三",
   *   city: "北京",
   *   country: "中国",
   *   location: { lat: 39.9042, lng: 116.4074 }
   * }
   */
  async getClassmate(id) {
    try {
      // 发送GET请求到特定同学的API端点
      const response = await axios.get(`/api/classmates/${id}`)
      // 返回响应中的数据
      return response.data
    } catch (error) {
      // 记录错误信息并抛出异常
      console.error(`获取同学ID:${id}数据失败:`, error)
      throw error
    }
  }

  /**
   * 添加新同学信息
   * @param {Object} classmateData - 新同学的信息对象
   * @param {string} classmateData.name - 同学姓名
   * @param {string} classmateData.city - 所在城市
   * @param {string} classmateData.country - 所在国家
   * @param {Object} classmateData.location - 位置信息
   * @param {number} classmateData.location.lat - 纬度
   * @param {number} classmateData.location.lng - 经度
   * @returns {Promise<Object>} 返回新创建的同学信息
   * @throws {Error} 当API请求失败时抛出错误
   */
  async addClassmate(classmateData) {
    try {
      const response = await axios.post('/api/classmates', classmateData)
      return response.data
    } catch (error) {
      console.error('添加同学数据失败:', error)
      throw error
    }
  }

  /**
   * 更新指定同学的信息
   * @param {number} id - 要更新的同学ID
   * @param {Object} classmateData - 更新的信息对象
   * @param {string} [classmateData.name] - 同学姓名
   * @param {string} [classmateData.city] - 所在城市
   * @param {string} [classmateData.country] - 所在国家
   * @param {Object} [classmateData.location] - 位置信息
   * @param {number} [classmateData.location.lat] - 纬度
   * @param {number} [classmateData.location.lng] - 经度
   * @returns {Promise<Object>} 返回更新后的同学信息
   * @throws {Error} 当API请求失败时抛出错误
   */
  async updateClassmate(id, classmateData) {
    try {
      const response = await axios.put(`/api/classmates/${id}`, classmateData)
      return response.data
    } catch (error) {
      console.error(`更新同学ID:${id}数据失败:`, error)
      throw error
    }
  }

  /**
   * 删除指定同学的信息
   * @param {number} id - 要删除的同学ID
   * @returns {Promise<Object>} 返回删除操作的结果
   * @throws {Error} 当API请求失败时抛出错误
   */
  async deleteClassmate(id) {
    try {
      const response = await axios.delete(`/api/classmates/${id}`)
      return response.data
    } catch (error) {
      console.error(`删除同学ID:${id}失败:`, error)
      throw error
    }
  }

  /**
   * 获取同学信息的统计数据
   * @returns {Promise<Object>} 返回统计信息对象
   * @throws {Error} 当API请求失败时抛出错误
   * 
   * 返回的数据格式示例：
   * {
   *   totalCount: 50,          // 总人数
   *   cityDistribution: {      // 城市分布
   *     "北京": 10,
   *     "上海": 8
   *   }
   * }
   */
  async getStatistics() {
    try {
      const response = await axios.get('/api/statistics')
      return response.data
    } catch (error) {
      console.error('获取统计数据失败:', error)
      throw error
    }
  }

  /**
   * 批量更新多个同学的信息
   * @param {Array<Object>} classmatesData - 包含多个同学信息的数组
   * @param {number} classmatesData[].id - 同学ID
   * @param {Object} classmatesData[].data - 更新的信息对象
   * @returns {Promise<Object>} 返回批量更新的结果
   * @throws {Error} 当API请求失败时抛出错误
   */
  async batchUpdateClassmates(classmatesData) {
    try {
      const response = await axios.post('/api/classmates/batch', classmatesData)
      return response.data
    } catch (error) {
      console.error('批量更新同学数据失败:', error)
      throw error
    }
  }
}

// 创建单例实例
const apiService = new ApiService()

export default apiService