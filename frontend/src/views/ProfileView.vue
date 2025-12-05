<template>
  <div class="profile-view-new">
    <div class="profile-container-new">
      <h1 class="page-title-new">个人中心</h1>

      <div class="content-card">
        <div class="profile-main-info">
          <div class="avatar-wrapper">
            <img v-if="userStore.userProfile?.avatar_url" :src="userStore.userProfile.avatar_url" alt="用户头像" class="avatar-img"/>
            <div v-else class="avatar-placeholder">
              <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>
            </div>
          </div>
          <div class="user-details">
            <h2 class="user-name">{{ userStore.userProfile?.username || '未命名用户' }}</h2>
            <p class="user-meta">注册于 {{ formatDate(userStore.userProfile?.created_at) }}</p>
          </div>
          <button @click="handleEditClick" class="edit-profile-btn">编辑资料</button>
        </div>
        <div class="profile-secondary-info">
          <div class="info-item"><label>邮箱</label><span>{{ userStore.userProfile?.email || '未设置' }}</span></div>
          <div class="info-item"><label>手机</label><span>{{ userStore.userProfile?.phone_number || '未设置' }}</span></div>
        </div>
      </div>

      <!-- 余额卡片 -->
      <div class="content-card balance-card">
        <div class="balance-header">
          <h3 class="card-title">账户余额</h3>
          <router-link to="/packages" class="recharge-btn">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="16"></line><line x1="8" y1="12" x2="16" y2="12"></line></svg>
            购买套餐
          </router-link>
        </div>
        <div v-if="loadingBalance" class="balance-loading">
          <div class="spinner"></div>
          <span>加载中...</span>
        </div>
        <div v-else class="balance-content">
          <div class="balance-main">
            <div class="balance-item-large">
              <label>剩余页数</label>
              <p class="balance-value">{{ balanceInfo?.page_balance || 0 }} <span class="unit">页</span></p>
            </div>
            <div class="balance-stats">
              <div class="balance-item-small">
                <label>累计购买</label>
                <p>{{ balanceInfo?.total_pages_purchased || 0 }} 页</p>
              </div>
              <div class="balance-item-small">
                <label>累计使用</label>
                <p>{{ balanceInfo?.total_pages_used || 0 }} 页</p>
              </div>
            </div>
          </div>

          <!-- 活跃套餐 -->
          <div v-if="balanceInfo?.active_packages && balanceInfo.active_packages.length > 0" class="active-packages">
            <h4>活跃套餐</h4>
            <div class="package-list">
              <div v-for="pkg in balanceInfo.active_packages" :key="pkg.id" class="package-item">
                <div class="package-info">
                  <span class="package-name">{{ pkg.package_name }}</span>
                  <span class="package-pages">剩余 {{ pkg.pages_remaining }}/{{ pkg.pages_total }} 页</span>
                </div>
                <div class="package-progress">
                  <div class="progress-bar" :style="{ width: `${(pkg.pages_remaining / pkg.pages_total) * 100}%` }"></div>
                </div>
              </div>
            </div>
          </div>

          <!-- 最近交易 -->
          <div v-if="balanceInfo?.recent_transactions && balanceInfo.recent_transactions.length > 0" class="recent-transactions">
            <h4>最近交易</h4>
            <div class="transaction-list">
              <div v-for="txn in balanceInfo.recent_transactions.slice(0, 5)" :key="txn.id" class="transaction-item">
                <div class="transaction-info">
                  <span class="transaction-type">{{ txn.transaction_type_display }}</span>
                  <span class="transaction-time">{{ formatDate(txn.created_at, true) }}</span>
                </div>
                <div class="transaction-amount" :class="{ 'positive': txn.pages > 0, 'negative': txn.pages < 0 }">
                  {{ txn.pages > 0 ? '+' : '' }}{{ txn.pages }} 页
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="stats-grid-new">
        <div class="stat-item"><p>{{ orderStats.total }}</p><label>总订单</label></div>
        <div class="stat-item"><p class="pending">{{ orderStats.pending }}</p><label>待处理</label></div>
        <div class="stat-item"><p class="completed">{{ orderStats.completed }}</p><label>已完成</label></div>
        <div class="stat-item"><p class="cancelled">{{ orderStats.cancelled }}</p><label>已取消</label></div>
      </div>

      <div class="content-card">
         <OAuthBindingManager />
      </div>

      <div class="content-card">
        <div class="orders-header-new">
          <h3 class="card-title">订单历史</h3>
          <div class="controls">
            <select v-model="statusFilter" class="order-filter">
              <option value="">全部状态</option>
              <option value="pending">待处理</option>
              <option value="completed">已完成</option>
              <option value="cancelled">已取消</option>
            </select>
             <button @click="refreshOrders" :disabled="isLoading" class="refresh-btn-icon" title="刷新">
                <svg :class="{'animate-spin': isLoading}" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 1 1-6.219-8.56"/></svg>
            </button>
          </div>
        </div>
        <div class="orders-list-wrapper">
          <div v-if="isLoading" class="order-state-view"><LoadingSpinner /><span>加载订单中...</span></div>
          <div v-else-if="filteredOrders.length === 0" class="order-state-view"><span>没有找到相关订单</span></div>
          <div v-else class="order-items-list">
            <div v-for="order in filteredOrders" :key="order.id" class="order-item-card">
              <div class="order-item-header" @click="toggleOrderDetail(order.id)">
                <div class="order-id-group">
                  <span class="order-id">订单号: {{ order.order_number }}</span>
                  <span class="order-time">{{ formatDate(order.created_at, true) }}</span>
                </div>
                <div class="order-status-group">
                  <span class="order-price">¥{{ order.total_price }}</span>
                  <span :class="['order-status-badge', getStatusClass(order.status)]">{{ getStatusText(order.status) }}</span>
                  <span :class="['arrow-icon', { 'rotated': expandedOrders.includes(order.id) }]">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="m6 9 6 6 6-6"/></svg>
                  </span>
                </div>
              </div>
              <div v-if="expandedOrders.includes(order.id)" class="order-item-details">
                <p><strong>取件码:</strong> {{ order.pickup_code }}</p>
                <p><strong>支付方式:</strong> {{ getPaymentMethodText(order.payment_method) }}</p>
                <div v-for="group in order.groups" :key="group.id" class="order-group-details">
                  <p class="group-title">{{ getBindingTypeText(group.binding_type) }}</p>
                  <ul><li v-for="doc in group.documents" :key="doc.id">{{ doc.original_filename }} ({{ doc.copies }}份)</li></ul>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <Modal :show="showEditModal" @close="closeEditModal">
      <template #header><h3>编辑个人信息</h3></template>
      <template #body>
        <form @submit.prevent="updateProfile" class="edit-form-new">
          <div class="form-group-new"><label for="phone">手机号</label><input id="phone" v-model="editForm.phone_number" type="tel" placeholder="请输入手机号"></div>
          <div class="form-group-new"><label for="email">邮箱</label><input id="email" v-model="editForm.email" type="email" placeholder="请输入邮箱"></div>
          <div class="form-actions-new">
            <button type="button" @click="closeEditModal" class="cancel-btn-new">取消</button>
            <button type="submit" :disabled="isUpdating" class="submit-btn-new">{{ isUpdating ? '保存中...' : '保存更改' }}</button>
          </div>
        </form>
      </template>
    </Modal>
  </div>
</template>

<script setup>
// ===================================================================
// 脚本部分 (Script Section)
// ===================================================================
//
// 【重要】这里的业务逻辑完全没有改动，
// 只是为了适配新的模板结构，对 formatDate 方法增加了参数。
// 所有核心功能、方法和 store 的使用均保持不变。
//
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useUserStore } from '../stores/user'
import Modal from '../components/Modal.vue'
import apiService from '../services/apiService'
import OAuthBindingManager from '../components/OAuthBindingManager.vue'
import LoadingSpinner from '../components/LoadingSpinner.vue'

const userStore = useUserStore()
const showEditModal = ref(false)
const isLoading = ref(false)
const isUpdating = ref(false)
const statusFilter = ref('')
const expandedOrders = ref([])
const orders = ref([])
const editForm = ref({ phone_number: '', email: '' })

// 余额相关
const loadingBalance = ref(false)
const balanceInfo = ref(null)

const filteredOrders = computed(() => {
  if (!statusFilter.value) return orders.value
  return orders.value.filter(order => order.status === statusFilter.value)
})

const orderStats = computed(() => {
  return {
    total: orders.value.length,
    pending: orders.value.filter(o => o.status === 'pending').length,
    completed: orders.value.filter(o => o.status === 'completed').length,
    cancelled: orders.value.filter(o => o.status === 'cancelled').length
  }
})

const isOAuthUser = computed(() => userStore.userProfile?.github_id || userStore.userProfile?.google_id)

onMounted(async () => {
  await userStore.initializeStore()
  if (userStore.isAuthenticated) {
    await userStore.fetchProfile()
    await Promise.all([fetchUserOrders(), fetchBalance()])
    editForm.value.phone_number = userStore.userProfile?.phone_number || ''
    editForm.value.email = userStore.userProfile?.email || ''
  }

  // 监听页面可见性变化，当用户回到页面时刷新余额
  const handleVisibilityChange = () => {
    if (!document.hidden && userStore.isAuthenticated) {
      fetchBalance()
    }
  }
  document.addEventListener('visibilitychange', handleVisibilityChange)

  // 组件卸载时移除监听器
  onUnmounted(() => {
    document.removeEventListener('visibilitychange', handleVisibilityChange)
  })
})

async function fetchUserOrders() {
  if (!userStore.isAuthenticated) return
  isLoading.value = true
  try {
    const response = await apiService.getUserOrders()
    orders.value = response.data
  } catch (error) { console.error('获取用户订单失败:', error) }
  finally { isLoading.value = false }
}

async function fetchBalance() {
  if (!userStore.isAuthenticated) return
  loadingBalance.value = true
  try {
    const response = await apiService.getUserBalance()
    balanceInfo.value = response.data
  } catch (error) {
    console.error('获取余额信息失败:', error)
  } finally {
    loadingBalance.value = false
  }
}

async function refreshOrders() { await fetchUserOrders() }

function toggleOrderDetail(orderId) {
  const index = expandedOrders.value.indexOf(orderId)
  if (index > -1) {
    expandedOrders.value.splice(index, 1)
  } else {
    expandedOrders.value.push(orderId)
  }
}

function handleEditClick() {
  editForm.value.phone_number = userStore.userProfile?.phone_number || ''
  editForm.value.email = userStore.userProfile?.email || ''
  showEditModal.value = true
}

function closeEditModal() { showEditModal.value = false }

async function updateProfile() {
  isUpdating.value = true
  try {
    await userStore.updateProfile(editForm.value)
    closeEditModal()
    await userStore.fetchProfile()
  } catch (error) { console.error('更新个人信息失败:', error) }
  finally { isUpdating.value = false }
}

function formatDate(dateString, short = false) {
  if (!dateString) return '未知'
  const options = short
    ? { year: '2-digit', month: '2-digit', day: '2-digit' }
    : { year: 'numeric', month: 'long', day: 'numeric' }
  return new Date(dateString).toLocaleString('zh-CN', options)
}

function getStatusClass(status) { return { pending: 'pending', processing: 'processing', completed: 'completed', cancelled: 'cancelled' }[status] || 'default' }
function getStatusText(status) { return { pending: '待处理', processing: '处理中', completed: '已完成', cancelled: '已取消' }[status] || status }
function getPaymentMethodText(method) { return { ALIPAY: '支付宝', WECHAT: '微信支付' }[method] || method || '未选择' }
function getBindingTypeText(type) { return { none: '无装订', staple_top_left: '左上角装订', staple_left_side: '左侧装订', staple: '骑马钉', ring_bound: '胶圈装订' }[type] || type }
</script>


<style scoped>
/* Base & Layout */
.profile-view-new { background-color: var(--color-background-soft); min-height: 100vh; padding: 2rem; }
.profile-container-new { max-width: 900px; margin: 0 auto; display: flex; flex-direction: column; gap: 2rem; }
.page-title-new { font-size: 2.25rem; font-weight: 800; color: var(--color-heading); margin-bottom: 1rem; }
.content-card { background-color: var(--color-background); border: 1px solid var(--color-border); border-radius: 12px; box-shadow: var(--shadow-card); }

/* Profile Card */
.profile-main-info { display: flex; align-items: center; gap: 1.5rem; padding: 1.5rem; }
.avatar-wrapper { flex-shrink: 0; width: 64px; height: 64px; border-radius: 50%; overflow: hidden; border: 2px solid var(--color-primary); }
.avatar-img, .avatar-placeholder { width: 100%; height: 100%; object-fit: cover; }
.avatar-placeholder { display: flex; align-items: center; justify-content: center; background-color: var(--color-background-mute); color: var(--color-text-mute); }
.user-details { flex-grow: 1; }
.user-name { font-size: 1.5rem; font-weight: 700; color: var(--color-heading); margin: 0; }
.user-meta { font-size: 0.875rem; color: var(--color-text-mute); margin: 0.25rem 0 0; }
.edit-profile-btn { background-color: var(--color-primary); color: var(--color-text-on-primary); border: none; padding: 0.6rem 1.2rem; border-radius: 8px; font-weight: 600; cursor: pointer; transition: all 0.2s; }
.edit-profile-btn:hover { background-color: var(--color-primary-hover); }
.profile-secondary-info { border-top: 1px solid var(--color-border); padding: 1rem 1.5rem; display: flex; gap: 2rem; font-size: 0.9rem; }
.info-item label { color: var(--color-text-mute); margin-right: 0.5rem; }
.info-item span { color: var(--color-text); font-weight: 500; }

/* Balance Card */
.balance-card { margin-bottom: 2rem; }
.balance-header { display: flex; justify-content: space-between; align-items: center; padding: 1rem 1.5rem; border-bottom: 1px solid var(--color-border); }
.recharge-btn { display: inline-flex; align-items: center; gap: 0.5rem; background-color: var(--color-primary); color: white; padding: 0.6rem 1.2rem; border-radius: 8px; font-weight: 600; text-decoration: none; transition: all 0.2s; }
.recharge-btn:hover { background-color: var(--color-primary-hover); }
.balance-loading { display: flex; justify-content: center; align-items: center; padding: 3rem; gap: 1rem; color: var(--color-text-mute); }
.balance-loading .spinner { width: 24px; height: 24px; border: 3px solid var(--color-border); border-top-color: var(--color-primary); border-radius: 50%; animation: spin 1s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }
.balance-content { padding: 1.5rem; }
.balance-main { display: flex; gap: 2rem; margin-bottom: 2rem; }
.balance-item-large { flex: 1; background-color: var(--color-primary); color: white; padding: 2rem; border-radius: 12px; }
.balance-item-large label { font-size: 0.875rem; opacity: 0.9; margin-bottom: 0.5rem; display: block; }
.balance-value { font-size: 3rem; font-weight: 700; margin: 0; }
.balance-value .unit { font-size: 1.5rem; font-weight: 500; }
.balance-stats { flex: 1; display: flex; flex-direction: column; gap: 1rem; }
.balance-item-small { background-color: var(--color-background-soft); padding: 1.5rem; border-radius: 12px; }
.balance-item-small label { font-size: 0.875rem; color: var(--color-text-mute); display: block; margin-bottom: 0.5rem; }
.balance-item-small p { font-size: 1.5rem; font-weight: 700; color: var(--color-heading); margin: 0; }
.active-packages, .recent-transactions { margin-top: 2rem; padding-top: 2rem; border-top: 1px solid var(--color-border); }
.active-packages h4, .recent-transactions h4 { font-size: 1rem; font-weight: 600; color: var(--color-heading); margin: 0 0 1rem; }
.package-list, .transaction-list { display: flex; flex-direction: column; gap: 0.75rem; }
.package-item { background-color: var(--color-background-soft); padding: 1rem; border-radius: 8px; }
.package-info { display: flex; justify-content: space-between; margin-bottom: 0.5rem; }
.package-name { font-weight: 600; color: var(--color-heading); }
.package-pages { font-size: 0.875rem; color: var(--color-text-mute); }
.package-progress { height: 6px; background-color: var(--color-border); border-radius: 3px; overflow: hidden; }
.progress-bar { height: 100%; background-color: var(--color-primary); transition: width 0.3s; }
.transaction-item { display: flex; justify-content: space-between; align-items: center; padding: 0.75rem; background-color: var(--color-background-soft); border-radius: 8px; }
.transaction-info { display: flex; flex-direction: column; gap: 0.25rem; }
.transaction-type { font-weight: 600; color: var(--color-heading); }
.transaction-time { font-size: 0.75rem; color: var(--color-text-mute); }
.transaction-amount { font-weight: 700; font-size: 1.125rem; }
.transaction-amount.positive { color: #10b981; }
.transaction-amount.negative { color: #ef4444; }

/* Stats Grid */
.stats-grid-new { display: grid; grid-template-columns: repeat(2, 1fr); gap: 1.5rem; }
@media(min-width: 640px) { .stats-grid-new { grid-template-columns: repeat(4, 1fr); } }
.stat-item { background-color: var(--color-background); border: 1px solid var(--color-border); border-radius: 12px; padding: 1.5rem; text-align: center; }
.stat-item p { font-size: 2rem; font-weight: 700; color: var(--color-heading); margin: 0; line-height: 1; }
.stat-item label { font-size: 0.875rem; color: var(--color-text-mute); margin-top: 0.5rem; display: block; }
.stat-item p.pending { color: #f59e0b; }
.stat-item p.completed { color: #10b981; }
.stat-item p.cancelled { color: var(--color-danger); }

/* Orders History */
.orders-header-new { display: flex; justify-content: space-between; align-items: center; padding: 1rem 1.5rem; border-bottom: 1px solid var(--color-border); }
.card-title { font-size: 1.25rem; font-weight: 600; color: var(--color-heading); margin: 0; }
.controls { display: flex; align-items: center; gap: 1rem; }
.order-filter, .refresh-btn-icon { background-color: var(--color-background-soft); border: 1px solid var(--color-border); border-radius: 6px; padding: 0.5rem; color: var(--color-text); transition: all 0.2s; }
.refresh-btn-icon { cursor: pointer; display: flex; }
.order-filter:focus, .refresh-btn-icon:hover { border-color: var(--color-primary); }
.orders-list-wrapper { padding: 1rem; }
.order-state-view { padding: 2rem; text-align: center; color: var(--color-text-mute); display: flex; justify-content: center; align-items: center; gap: 0.5rem; }
.order-items-list { display: flex; flex-direction: column; gap: 1rem; }
.order-item-card { border: 1px solid var(--color-border); border-radius: 8px; overflow: hidden; }
.order-item-header { display: flex; justify-content: space-between; align-items: center; padding: 0.75rem 1rem; cursor: pointer; transition: background-color 0.2s; }
.order-item-header:hover { background-color: var(--color-background-soft); }
.order-id-group, .order-status-group { display: flex; align-items: center; gap: 1rem; }
.order-id { font-weight: 600; color: var(--color-heading); }
.order-time { font-size: 0.8rem; color: var(--color-text-mute); }
.order-price { font-weight: 600; }
.order-status-badge { padding: 0.2rem 0.6rem; border-radius: 12px; font-size: 0.75rem; font-weight: 500; }
.order-status-badge.pending { background-color: #fef3c7; color: #b45309; }
.order-status-badge.completed { background-color: #d1fae5; color: #065f46; }
.order-status-badge.cancelled { background-color: #fee2e2; color: #991b1b; }
.arrow-icon { transition: transform 0.2s ease; }
.arrow-icon.rotated { transform: rotate(180deg); }
.order-item-details { padding: 1rem 1.5rem; border-top: 1px solid var(--color-border); background-color: var(--color-background-soft); font-size: 0.9rem; }
.order-item-details p { margin: 0.5rem 0; }
.order-group-details .group-title { font-weight: 600; margin-top: 0.75rem; }
.order-group-details ul { padding-left: 1.5rem; margin: 0.25rem 0 0; color: var(--color-text-mute); }

/* Edit Modal Form */
.edit-form-new { display: flex; flex-direction: column; gap: 1rem; }
.form-group-new { display: flex; flex-direction: column; gap: 0.5rem; }
.form-group-new label { font-weight: 500; font-size: 0.875rem; }
.form-group-new input { width: 100%; padding: 0.75rem; border: 1px solid var(--color-border); border-radius: 6px; background-color: var(--color-background); font-size: 1rem; }
.form-group-new input:focus { outline: none; border-color: var(--color-primary); }
.form-actions-new { display: flex; justify-content: flex-end; gap: 0.75rem; padding-top: 1rem; }
.cancel-btn-new, .submit-btn-new { padding: 0.6rem 1.25rem; border-radius: 8px; font-weight: 600; cursor: pointer; transition: all 0.2s; border: 1px solid transparent; }
.cancel-btn-new { background-color: var(--color-background-mute); color: var(--color-text); border-color: var(--color-border); }
.submit-btn-new { background-color: var(--color-primary); color: var(--color-text-on-primary); border-color: var(--color-primary); }
</style>
