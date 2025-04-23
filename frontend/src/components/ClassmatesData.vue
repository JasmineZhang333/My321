<template>
  <div class="classmates-data">
    <h2>同学信息管理</h2>
    
    <!-- 操作按钮 -->
    <div class="action-buttons">
      <el-button type="primary" @click="showAddDialog">添加同学</el-button>
      <el-button type="success" @click="refreshData">刷新数据</el-button>
      <el-button type="warning" @click="showImportDialog">批量导入</el-button>
    </div>
    
    <!-- 批量导入对话框 -->
    <el-dialog
      title="批量导入同学数据"
      v-model="importDialogVisible"
      width="600px"
    >
      <p class="import-tip">请粘贴表格数据（包含ID、姓名、纬度、经度、城市、国家）</p>
      <el-input
        type="textarea"
        v-model="importData"
        :rows="10"
        placeholder="请粘贴表格数据，格式如：ID 姓名 纬度 经度 城市 国家"
      ></el-input>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="importDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="importClassmates" :loading="importLoading">导入</el-button>
        </span>
      </template>
    </el-dialog>
    
    <!-- 同学列表 -->
    <el-table :data="classmates" style="width: 100%" v-loading="loading">
      <el-table-column prop="name" label="姓名" width="100" />
      <el-table-column prop="city" label="城市" width="100" />
      <el-table-column prop="country" label="国家" width="100" />
      <el-table-column label="操作">
        <template #default="scope">
          <el-button size="small" @click="showEditDialog(scope.row)">编辑</el-button>
          <el-button size="small" type="danger" @click="confirmDelete(scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    
    <!-- 添加/编辑对话框 -->
    <el-dialog
      :title="isEdit ? '编辑同学信息' : '添加同学信息'"
      v-model="dialogVisible"
      width="600px"
    >
      <el-tabs v-model="activeTab">
        <el-tab-pane label="基本信息" name="basic">
          <el-form :model="form" label-width="100px" :rules="rules" ref="classmateForm">
            <el-form-item label="姓名" prop="name">
              <el-input v-model="form.name" placeholder="请输入姓名"></el-input>
            </el-form-item>
            <el-form-item label="城市" prop="city">
              <el-input v-model="form.city" placeholder="请输入城市" @change="autoSearchLocation"></el-input>
            </el-form-item>
            <el-form-item label="国家" prop="country">
              <el-input v-model="form.country" placeholder="请输入国家" @change="autoSearchLocation"></el-input>
            </el-form-item>
            <el-form-item label="纬度" prop="lat">
              <el-input-number v-model="form.location.lat" :precision="6" :step="0.000001" :min="-90" :max="90" style="width: 100%"></el-input-number>
            </el-form-item>
            <el-form-item label="经度" prop="lng">
              <el-input-number v-model="form.location.lng" :precision="6" :step="0.000001" :min="-180" :max="180" style="width: 100%"></el-input-number>
            </el-form-item>
          </el-form>
        </el-tab-pane>
        <el-tab-pane label="位置搜索" name="location">
          <p class="search-tip">通过地址或城市名称搜索位置坐标</p>
          <LocationSearch ref="locationSearch" @location-selected="handleLocationSelected" />
        </el-tab-pane>
      </el-tabs>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitForm">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ElMessage, ElMessageBox } from 'element-plus'
import apiService from '../services/api.js'
import eventBus from '../utils/eventBus.js'
import LocationSearch from './LocationSearch.vue'

export default {
  name: 'ClassmatesData',
  components: {
    LocationSearch
  },
  data() {
    return {
      classmates: [],
      loading: false,
      dialogVisible: false,
      importDialogVisible: false,
      importData: '',
      importLoading: false,
      isEdit: false,
      activeTab: 'basic',
      form: {
        id: null,
        name: '',
        city: '',
        country: '',
        location: {
          lat: 0,
          lng: 0
        }
      },
      rules: {
        name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
        city: [{ required: true, message: '请输入城市', trigger: 'blur' }],
        country: [{ required: true, message: '请输入国家', trigger: 'blur' }],
        lat: [{ required: true, message: '请输入纬度', trigger: 'blur' }],
        lng: [{ required: true, message: '请输入经度', trigger: 'blur' }]
      }
    }
  },
  mounted() {
    this.fetchClassmates()
  },
  methods: {
    async fetchClassmates() {
      this.loading = true
      try {
        this.classmates = await apiService.getClassmates()
      } catch (error) {
        console.error('获取同学数据失败:', error)
        ElMessage.error('获取同学数据失败')
      } finally {
        this.loading = false
      }
    },
    showAddDialog() {
      this.isEdit = false
      this.form = {
        name: '',
        city: '',
        country: '',
        location: {
          lat: 0,
          lng: 0
        }
      }
      this.activeTab = 'basic'
      this.dialogVisible = true
    },
    showEditDialog(row) {
      this.isEdit = true
      this.form = JSON.parse(JSON.stringify(row)) // 深拷贝避免直接修改表格数据
      this.activeTab = 'basic'
      this.dialogVisible = true
    },
    handleLocationSelected(data) {
      // 更新表单中的位置信息
      this.form.location = data.location
      
      // 如果城市和国家为空，则使用搜索结果中的值
      if (!this.form.city && data.city) {
        this.form.city = data.city
      }
      
      if (!this.form.country && data.country) {
        this.form.country = data.country
      }
      
      // 切换回基本信息标签页
      this.activeTab = 'basic'
      
      ElMessage.success('位置已更新')
    },
    async submitForm() {
      try {
        if (this.isEdit) {
          // 更新同学信息
          await apiService.updateClassmate(this.form.id, this.form)
          ElMessage.success('更新成功')
        } else {
          // 添加新同学
          await apiService.addClassmate(this.form)
          ElMessage.success('添加成功')
        }
        this.dialogVisible = false
        this.fetchClassmates()
        // 通知其他组件刷新数据
        eventBus.emit('data-updated')
      } catch (error) {
        console.error('操作失败:', error)
        ElMessage.error('操作失败: ' + (error.response?.data?.error || error.message))
      }
    },
    confirmDelete(row) {
      ElMessageBox.confirm(
        `确定要删除 ${row.name} 的信息吗？`,
        '警告',
        {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning',
        }
      ).then(() => {
        this.deleteClassmate(row.id)
      }).catch(() => {
        // 取消删除
      })
    },
    async deleteClassmate(id) {
      try {
        await apiService.deleteClassmate(id)
        ElMessage.success('删除成功')
        this.fetchClassmates()
        // 通知其他组件刷新数据
        eventBus.emit('data-updated')
      } catch (error) {
        console.error('删除失败:', error)
        ElMessage.error('删除失败: ' + (error.response?.data?.error || error.message))
      }
    },
    refreshData() {
      this.fetchClassmates()
    },
    showImportDialog() {
      this.importDialogVisible = true
      this.importData = ''
    },
    async importClassmates() {
      if (!this.importData.trim()) {
        ElMessage.warning('请先粘贴表格数据')
        return
      }
      
      try {
        this.importLoading = true
        
        // 解析表格数据
        const lines = this.importData.trim().split('\n')
        const classmatesData = []
        
        // 跳过标题行（如果有）
        const startIndex = lines[0].includes('ID') || lines[0].includes('姓名') ? 1 : 0
        
        for (let i = startIndex; i < lines.length; i++) {
          const line = lines[i].trim()
          if (!line) continue
          
          // 按制表符或多个空格分割
          const parts = line.split(/\s+/)
          if (parts.length < 6) {
            ElMessage.warning(`第${i+1}行数据格式不正确，已跳过`)
            continue
          }
          
          // 解析数据
          const id = parseInt(parts[0])
          const name = parts[1]
          const lat = parseFloat(parts[2])
          const lng = parseFloat(parts[3])
          const city = parts[4]
          const country = parts[5]
          
          // 验证数据
          if (isNaN(id) || isNaN(lat) || isNaN(lng)) {
            ElMessage.warning(`第${i+1}行数据格式不正确，已跳过`)
            continue
          }
          
          classmatesData.push({
            id,
            name,
            city,
            country,
            location: {
              lat,
              lng
            }
          })
        }
        
        if (classmatesData.length === 0) {
          ElMessage.warning('没有有效的数据可以导入')
          return
        }
        
        // 调用批量更新API
        const result = await apiService.batchUpdateClassmates(classmatesData)
        
        // 显示结果
        ElMessage.success(`导入成功！更新: ${result.updated}, 新增: ${result.created}, 错误: ${result.errors}`)
        
        // 关闭对话框并刷新数据
        this.importDialogVisible = false
        this.fetchClassmates()
        
        // 通知其他组件刷新数据
        eventBus.emit('data-updated')
      } catch (error) {
        console.error('导入失败:', error)
        ElMessage.error('导入失败: ' + (error.response?.data?.error || error.message))
      } finally {
        this.importLoading = false
      }
    },
    async autoSearchLocation() {
      // 当城市或国家信息变化时，自动搜索位置
      if (this.form.city && this.form.country) {
        // 构建搜索查询
        const searchQuery = `${this.form.city}, ${this.form.country}`
        
        // 访问LocationSearch组件并调用其搜索方法
        if (this.$refs.locationSearch) {
          try {
            // 设置搜索查询
            this.$refs.locationSearch.searchQuery = searchQuery
            // 执行搜索
            await this.$refs.locationSearch.searchLocation()
            
            // 如果有搜索结果，自动选择第一个结果
            if (this.$refs.locationSearch.searchResults && this.$refs.locationSearch.searchResults.length > 0) {
              const firstResult = this.$refs.locationSearch.searchResults[0]
              this.$refs.locationSearch.selectLocation(firstResult)
              ElMessage.success('已自动更新位置坐标')
            } else {
              ElMessage.warning(`未找到"${this.form.city}, ${this.form.country}"的位置信息`)
            }
          } catch (error) {
            console.error('自动搜索位置失败:', error)
            ElMessage.error('自动搜索位置失败，请手动使用位置搜索功能')
          }
        }
      }
    }
  }
}
</script>

<style scoped>
.classmates-data {
  height: 100%;
  display: flex;
  flex-direction: column;
}

h2 {
  margin-bottom: 20px;
  color: #409EFF;
  text-align: center;
}

.action-buttons {
  margin-bottom: 20px;
  display: flex;
  justify-content: space-between;
}

.el-table {
  margin-bottom: 20px;
  --el-table-border-color: #EBEEF5;
  --el-table-header-background-color: #F5F7FA;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.search-tip {
  margin-bottom: 15px;
  color: #909399;
  font-size: 14px;
}

:deep(.el-tabs__content) {
  padding: 15px 0;
}

:deep(.el-dialog__body) {
  padding-top: 10px;
}
</style>