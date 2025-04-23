import { ref } from 'vue'

// 简单的事件总线实现，用于组件间通信
class EventBus {
  constructor() {
    this.events = {}
  }

  // 订阅事件
  on(eventName, callback) {
    if (!this.events[eventName]) {
      this.events[eventName] = []
    }
    this.events[eventName].push(callback)
  }

  // 发布事件
  emit(eventName, data) {
    if (this.events[eventName]) {
      this.events[eventName].forEach(callback => callback(data))
    }
  }

  // 取消订阅
  off(eventName, callback) {
    if (this.events[eventName]) {
      if (callback) {
        this.events[eventName] = this.events[eventName].filter(cb => cb !== callback)
      } else {
        delete this.events[eventName]
      }
    }
  }
}

// 创建单例实例
const eventBus = new EventBus()

export default eventBus