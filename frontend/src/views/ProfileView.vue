<template>
  <div class="profile-view">
    <div class="container">
      <h1 class="page-title">个人中心</h1>

      <!-- 用户信息卡片 -->
      <div class="profile-card">
        <div class="profile-header">
          <div class="avatar">
            <img
              v-if="userStore.userProfile?.avatar_url"
              :src="userStore.userProfile.avatar_url"
              :alt="userStore.userProfile?.username"
              class="avatar-image"
            />
            <svg v-else xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
              <circle cx="12" cy="7" r="4"></circle>
            </svg>
          </div>
          <div class="profile-info">
            <h2 class="username">{{ userStore.userProfile?.username || '未设置' }}</h2>
            <p class="registration-date">
              注册于 {{ formatDate(userStore.userProfile?.created_at) }}
            </p>
            <!-- OAuth状态指示器 -->
            <div v-if="isOAuthUser" class="oauth-indicator">
              <span class="oauth-badge">
                🔐 OAuth用户
              </span>
            </div>
          </div>
        </div>

        <div class="profile-details">
          <div class="detail-row">
            <div class="detail-item">
              <label class="detail-label">用户名</label>
              <p class="detail-value">{{ userStore.userProfile?.username || '未设置' }}</p>
            </div>
            <div class="detail-item">
              <label class="detail-label">手机号</label>
              <p class="detail-value">{{ userStore.userProfile?.phone_number || '未设置' }}</p>
            </div>
          </div>
          <div class="detail-row">
            <div class="detail-item">
              <label class="detail-label">邮箱</label>
              <p class="detail-value">{{ userStore.userProfile?.email || '未设置' }}</p>
            </div>
            <div class="detail-item">
              <label class="detail-label">注册时间</label>
              <p class="detail-value">{{ formatDate(userStore.userProfile?.created_at) }}</p>
            </div>
          </div>
          <!-- OAuth账户信息 -->
          <div v-if="isOAuthUser" class="detail-row">
            <div class="detail-item">
              <label class="detail-label">GitHub ID</label>
              <p class="detail-value">{{ userStore.userProfile?.github_id || '未绑定' }}</p>
            </div>
            <div class="detail-item">
              <label class="detail-label">Google ID</label>
              <p class="detail-value">{{ userStore.userProfile?.google_id || '未绑定' }}</p>
            </div>
          </div>
        </div>

        <!-- 编辑个人信息按钮 -->
        <div class="profile-actions">
          <button @click="handleEditClick" class="edit-button">
            编辑个人信息
          </button>
        </div>
      </div>

      <!-- OAuth账户管理 -->
      <div class="oauth-section">
        <OAuthBindingManager />
      </div>

      <!-- 订单统计卡片 -->
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-number total">{{ orderStats.total }}</div>
          <div class="stat-label">总订单数</div>
        </div>
        <div class="stat-card">
          <div class="stat-number pending">{{ orderStats.pending }}</div>
          <div class="stat-label">待处理</div>
        </div>
        <div class="stat-card">
          <div class="stat-number completed">{{ orderStats.completed }}</div>
          <div class="stat-label">已完成</div>
        </div>
        <div class="stat-card">
          <div class="stat-number cancelled">{{ orderStats.cancelled }}</div>
          <div class="stat-label">已取消</div>
        </div>
      </div>

      <!-- 订单历史 -->
      <div class="orders-section">
        <div class="section-header">
          <h2 class="section-title">订单历史</h2>
          <div class="section-controls">
            <select v-model="statusFilter" class="status-filter">
              <option value="">全部状态</option>
              <option value="pending">待处理</option>
              <option value="processing">处理中</option>
              <option value="completed">已完成</option>
              <option value="cancelled">已取消</option>
            </select>
            <button @click="refreshOrders" :disabled="isLoading" class="refresh-button">
              {{ isLoading ? '刷新中...' : '🔄 刷新' }}
            </button>
          </div>
        </div>

        <!-- 订单列表 -->
        <div v-if="isLoading" class="loading-state">
          <div class="loading-spinner"></div>
          <p>加载中...</p>
        </div>

        <div v-else-if="filteredOrders.length === 0" class="empty-state">
          <div class="empty-icon">📋</div>
          <p>暂无订单</p>
        </div>

        <div v-else class="orders-list">
          <div v-for="order in filteredOrders" :key="order.id" class="order-card">
            <div class="order-header">
              <div class="order-info">
                <h3 class="order-number">订单号: {{ order.order_number }}</h3>
                <p class="pickup-code">取件码: {{ order.pickup_code }}</p>
              </div>
              <div class="order-status">
                <span :class="['status-badge', getStatusClass(order.status)]">
                  {{ getStatusText(order.status) }}
                </span>
                <p class="order-price">¥{{ order.total_price }}</p>
              </div>
            </div>

            <div class="order-details">
              <div class="detail-item">
                <span class="detail-label">手机号:</span>
                <span class="detail-value">{{ order.phone_number }}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">创建时间:</span>
                <span class="detail-value">{{ formatDate(order.created_at) }}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">支付方式:</span>
                <span class="detail-value">{{ getPaymentMethodText(order.payment_method) }}</span>
              </div>
            </div>

            <!-- 订单详情展开/收起 -->
            <div class="order-actions">
              <button @click="toggleOrderDetail(order.id)" class="toggle-details">
                {{ expandedOrders.includes(order.id) ? '收起详情' : '查看详情' }}
                <span :class="['arrow', { 'rotated': expandedOrders.includes(order.id) }]">
                  ▼
                </span>
              </button>
            </div>

            <!-- 订单详情 -->
            <div v-if="expandedOrders.includes(order.id)" class="order-expanded">
              <h4 class="groups-title">装订组信息:</h4>
              <div class="groups-list">
                <div v-for="group in order.groups" :key="group.id" class="group-card">
                  <div class="group-header">
                    <span class="group-name">组 {{ group.sequence_in_order }}</span>
                    <span class="group-binding">
                      装订方式: {{ getBindingTypeText(group.binding_type) }}
                    </span>
                  </div>
                  <div class="documents-list">
                    <div v-for="doc in group.documents" :key="doc.id" class="document-item">
                      <span class="document-name">{{ doc.original_filename }}</span>
                      <span class="document-copies">{{ doc.copies }}份</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 编辑个人信息模态框 -->
    <Modal :show="showEditModal" @close="closeEditModal">
      <template #header>
        <h3 class="modal-title">编辑个人信息</h3>
      </template>
      <template #body>
        <form @submit.prevent="updateProfile" class="edit-form">
          <div class="form-group">
            <label class="form-label">手机号</label>
            <input
              v-model="editForm.phone_number"
              type="tel"
              class="form-input"
              placeholder="请输入手机号"
            >
          </div>
          <div class="form-group">
            <label class="form-label">邮箱</label>
            <input
              v-model="editForm.email"
              type="email"
              class="form-input"
              placeholder="请输入邮箱"
            >
          </div>
          <div class="form-actions">
            <button
              type="submit"
              :disabled="isUpdating"
              class="submit-button"
            >
              {{ isUpdating ? '保存中...' : '保存' }}
            </button>
            <button
              type="button"
              @click="closeEditModal"
              class="cancel-button"
            >
              取消
            </button>
          </div>
        </form>
      </template>
    </Modal>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useUserStore } from '../stores/user'
import Modal from '../components/Modal.vue'
import apiService from '../services/apiService'
import OAuthBindingManager from '../components/OAuthBindingManager.vue'

const userStore = useUserStore()

// 响应式数据
const showEditModal = ref(false)
const isLoading = ref(false)
const isUpdating = ref(false)
const statusFilter = ref('')
const expandedOrders = ref([])
const orders = ref([])

// 编辑表单
const editForm = ref({
  phone_number: '',
  email: ''
})

// 计算属性
const filteredOrders = computed(() => {
  if (!statusFilter.value) return orders.value
  return orders.value.filter(order => order.status === statusFilter.value)
})

const orderStats = computed(() => {
  const stats = {
    total: orders.value.length,
    pending: orders.value.filter(o => o.status === 'pending').length,
    processing: orders.value.filter(o => o.status === 'processing').length,
    completed: orders.value.filter(o => o.status === 'completed').length,
    cancelled: orders.value.filter(o => o.status === 'cancelled').length
  }
  return stats
})

const isOAuthUser = computed(() => {
  return userStore.userProfile?.github_id || userStore.userProfile?.google_id
})

// 生命周期
onMounted(async () => {
  // 先初始化store，确保token被正确设置
  await userStore.initializeStore()

  if (userStore.isAuthenticated) {
    await userStore.fetchProfile() // 先获取用户信息
    await fetchUserOrders()
    // 初始化编辑表单
    editForm.value.phone_number = userStore.userProfile?.phone_number || ''
    editForm.value.email = userStore.userProfile?.email || ''
  }
})

// 方法
async function fetchUserOrders() {
  if (!userStore.isAuthenticated) return

  isLoading.value = true
  try {
    const response = await apiService.getUserOrders()
    orders.value = response.data
  } catch (error) {
    console.error('获取用户订单失败:', error)
  } finally {
    isLoading.value = false
  }
}

async function refreshOrders() {
  await fetchUserOrders()
}

function toggleOrderDetail(orderId) {
  const index = expandedOrders.value.indexOf(orderId)
  if (index > -1) {
    expandedOrders.value.splice(index, 1)
  } else {
    expandedOrders.value.push(orderId)
  }
}

function handleEditClick() {
  console.log('编辑按钮被点击了')
  // 重新初始化表单数据
  editForm.value.phone_number = userStore.userProfile?.phone_number || ''
  editForm.value.email = userStore.userProfile?.email || ''
  showEditModal.value = true
}

function closeEditModal() {
  showEditModal.value = false
}

async function updateProfile() {
  isUpdating.value = true
  try {
    await userStore.updateProfile(editForm.value)
    closeEditModal()
    // 刷新用户信息
    await userStore.fetchProfile()
  } catch (error) {
    console.error('更新个人信息失败:', error)
  } finally {
    isUpdating.value = false
  }
}

function formatDate(dateString) {
  if (!dateString) return '未知'
  return new Date(dateString).toLocaleString('zh-CN')
}

function getStatusClass(status) {
  const classes = {
    pending: 'pending',
    processing: 'processing',
    completed: 'completed',
    cancelled: 'cancelled'
  }
  return classes[status] || 'default'
}

function getStatusText(status) {
  const texts = {
    pending: '待处理',
    processing: '处理中',
    completed: '已完成',
    cancelled: '已取消'
  }
  return texts[status] || status
}

function getPaymentMethodText(method) {
  const texts = {
    ALIPAY: '支付宝',
    WECHAT: '微信支付',
    CASH: '现金支付'
  }
  return texts[method] || method || '未选择'
}

function getBindingTypeText(type) {
  const texts = {
    none: '无装订',
    staple_top_left: '左上角装订',
    staple_left_side: '左侧装订',
    staple: '订书机装订',
    ring_bound: '环装'
  }
  return texts[type] || type
}
</script>

<style scoped>
.profile-view {
  min-height: 100vh;
  background-color: var(--color-background);
}

.container {
  width: 90%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 0;
}

.page-title {
  font-size: 2rem;
  font-weight: 700;
  color: var(--color-heading);
  margin-bottom: 2rem;
  text-align: center;
}

/* 用户信息卡片 */
.profile-card {
  background-color: var(--color-background-soft);
  border: 1px solid var(--color-border);
  border-radius: 12px;
  padding: 2rem;
  margin-bottom: 2rem;
  box-shadow: var(--shadow-card);
}

.profile-header {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.avatar {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background-color: var(--color-primary);
  color: white;
}

.avatar-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 50%;
}

.profile-info {
  flex: 1;
}

.username {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--color-heading);
  margin: 0 0 0.5rem 0;
}

.registration-date {
  color: var(--color-text-mute);
  margin: 0;
}

.oauth-indicator {
  margin-top: 0.5rem;
}

.oauth-badge {
  background-color: #e0f2fe;
  color: #1e40af;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 500;
}

.profile-details {
  margin-bottom: 2rem;
}

.detail-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  margin-bottom: 1.5rem;
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.detail-label {
  font-weight: 500;
  color: var(--color-text-mute);
  font-size: 0.875rem;
}

.detail-value {
  color: var(--color-text);
  font-size: 1rem;
  margin: 0;
}

.profile-actions {
  text-align: center;
}

.edit-button {
  background-color: var(--color-primary);
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
}

.edit-button:hover {
  background-color: var(--color-primary-dark);
}

/* 统计卡片 */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  background-color: var(--color-background-soft);
  border: 1px solid var(--color-border);
  border-radius: 12px;
  padding: 1.5rem;
  text-align: center;
  box-shadow: var(--shadow-card);
}

.stat-number {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
}

.stat-number.total {
  color: var(--color-primary);
}

.stat-number.pending {
  color: #f59e0b;
}

.stat-number.completed {
  color: #10b981;
}

.stat-number.cancelled {
  color: var(--color-danger);
}

.stat-label {
  color: var(--color-text-mute);
  font-size: 0.875rem;
}

/* 订单历史部分 */
.orders-section {
  background-color: var(--color-background-soft);
  border: 1px solid var(--color-border);
  border-radius: 12px;
  padding: 2rem;
  box-shadow: var(--shadow-card);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.section-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--color-heading);
  margin: 0;
}

.section-controls {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.status-filter {
  padding: 0.5rem 0.75rem;
  border: 1px solid var(--color-border);
  border-radius: 6px;
  background-color: var(--color-background);
  color: var(--color-text);
  font-size: 0.875rem;
}

.refresh-button {
  background-color: var(--color-background-mute);
  color: var(--color-text);
  border: 1px solid var(--color-border);
  padding: 0.5rem 0.75rem;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.875rem;
  transition: background-color 0.2s;
}

.refresh-button:hover:not(:disabled) {
  background-color: var(--color-border);
}

.refresh-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* 加载和空状态 */
.loading-state, .empty-state {
  text-align: center;
  padding: 3rem;
  color: var(--color-text-mute);
}

.loading-spinner {
  width: 2rem;
  height: 2rem;
  border: 3px solid var(--color-background-mute);
  border-top: 3px solid var(--color-primary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

/* 订单列表 */
.orders-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.order-card {
  border: 1px solid var(--color-border);
  border-radius: 8px;
  padding: 1.5rem;
  background-color: var(--color-background);
  transition: box-shadow 0.2s;
}

.order-card:hover {
  box-shadow: var(--shadow-card);
}

.order-header {
  display: flex;
  justify-content: space-between;
  align-items: start;
  margin-bottom: 1rem;
}

.order-number {
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--color-heading);
  margin: 0 0 0.25rem 0;
}

.pickup-code {
  color: var(--color-text-mute);
  font-size: 0.875rem;
  margin: 0;
}

.order-status {
  text-align: right;
}

.status-badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 500;
  margin-bottom: 0.5rem;
}

.status-badge.pending {
  background-color: #fef3c7;
  color: #92400e;
}

.status-badge.processing {
  background-color: #dbeafe;
  color: #1e40af;
}

.status-badge.completed {
  background-color: #d1fae5;
  color: #065f46;
}

.status-badge.cancelled {
  background-color: #fee2e2;
  color: #991b1b;
}

.order-price {
  font-size: 1.1rem;
  font-weight: 700;
  color: #10b981;
  margin: 0;
}

.order-details {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 1rem;
}

.order-details .detail-item {
  display: flex;
  gap: 0.5rem;
  font-size: 0.875rem;
}

.order-details .detail-label {
  color: var(--color-text-mute);
  font-weight: 500;
}

.order-details .detail-value {
  color: var(--color-text);
}

.order-actions {
  border-top: 1px solid var(--color-border);
  padding-top: 1rem;
}

.toggle-details {
  background: none;
  border: none;
  color: var(--color-primary);
  cursor: pointer;
  font-size: 0.875rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: color 0.2s;
}

.toggle-details:hover {
  color: var(--color-primary-dark);
}

.arrow {
  transition: transform 0.2s;
}

.arrow.rotated {
  transform: rotate(180deg);
}

/* 展开的订单详情 */
.order-expanded {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid var(--color-border);
}

.groups-title {
  font-weight: 600;
  color: var(--color-heading);
  margin: 0 0 1rem 0;
}

.groups-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.group-card {
  background-color: var(--color-background-mute);
  border-radius: 6px;
  padding: 1rem;
}

.group-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.group-name {
  font-weight: 500;
  color: var(--color-heading);
}

.group-binding {
  font-size: 0.875rem;
  color: var(--color-text-mute);
}

.documents-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.document-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.875rem;
  color: var(--color-text);
}

.document-name {
  flex: 1;
}

.document-copies {
  color: var(--color-text-mute);
}

/* 模态框样式 */
.modal-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--color-heading);
  margin: 0;
}

.edit-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-label {
  font-weight: 500;
  color: var(--color-text);
  font-size: 0.875rem;
}

.form-input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid var(--color-border);
  border-radius: 6px;
  background-color: var(--color-background);
  color: var(--color-text);
  font-size: 1rem;
  transition: border-color 0.2s;
}

.form-input:focus {
  outline: none;
  border-color: var(--color-primary);
}

.form-actions {
  display: flex;
  gap: 1rem;
  padding-top: 1rem;
}

.submit-button {
  flex: 1;
  background-color: var(--color-primary);
  color: white;
  border: none;
  padding: 0.75rem;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
}

.submit-button:hover:not(:disabled) {
  background-color: var(--color-primary-dark);
}

.submit-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.cancel-button {
  flex: 1;
  background-color: var(--color-background-mute);
  color: var(--color-text);
  border: 1px solid var(--color-border);
  padding: 0.75rem;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
}

.cancel-button:hover {
  background-color: var(--color-border);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .container {
    width: 95%;
    padding: 1rem 0;
  }

  .page-title {
    font-size: 1.5rem;
  }

  .profile-header {
    flex-direction: column;
    text-align: center;
    gap: 1rem;
  }

  .detail-row {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .section-header {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }

  .section-controls {
    justify-content: center;
  }

  .order-header {
    flex-direction: column;
    gap: 1rem;
  }

  .order-status {
    text-align: left;
  }

  .order-details {
    grid-template-columns: 1fr;
  }

  .group-header {
    flex-direction: column;
    align-items: start;
    gap: 0.5rem;
  }

  .form-actions {
    flex-direction: column;
  }
}
</style>
