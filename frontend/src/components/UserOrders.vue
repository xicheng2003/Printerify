<template>
  <div class="user-orders">
    <div class="orders-header">
      <h2 class="title">我的订单</h2>
      <button
        @click="refreshOrders"
        :disabled="orderStore.userOrdersLoading"
        class="refresh-btn"
      >
        {{ orderStore.userOrdersLoading ? '刷新中...' : '🔄 刷新' }}
      </button>
    </div>

    <!-- 加载状态 -->
    <div v-if="orderStore.userOrdersLoading" class="loading-state">
      <LoadingSpinner />
      <p>正在加载订单...</p>
    </div>

    <!-- 错误状态 -->
    <div v-else-if="orderStore.userOrdersError" class="error-state">
      <p class="error-message">{{ orderStore.userOrdersError }}</p>
      <button @click="refreshOrders" class="retry-btn">重试</button>
    </div>

    <!-- 空状态 -->
    <div v-else-if="orderStore.userOrders.length === 0" class="empty-state">
      <div class="empty-icon">📋</div>
      <h3>暂无订单</h3>
      <p>您还没有创建任何订单</p>
      <router-link to="/" class="create-order-btn">立即下单</router-link>
    </div>

    <!-- 订单列表 -->
    <div v-else class="orders-list">
      <div
        v-for="order in orderStore.userOrders"
        :key="order.id"
        class="order-card"
      >
        <div class="order-header">
          <div class="order-info">
            <h3 class="order-number">订单号: {{ order.order_number }}</h3>
            <span class="pickup-code">取件码: {{ order.pickup_code }}</span>
          </div>
          <div class="order-status">
            <span :class="['status-badge', `status-${order.status}`]">
              {{ getStatusText(order.status) }}
            </span>
          </div>
        </div>

        <div class="order-details">
          <div class="detail-row">
            <span class="detail-label">创建时间:</span>
            <span class="detail-value">{{ formatDate(order.created_at) }}</span>
          </div>
          <div class="detail-row">
            <span class="detail-label">总价:</span>
            <span class="detail-value price">¥{{ order.total_price }}</span>
          </div>
          <div class="detail-row">
            <span class="detail-label">联系电话:</span>
            <span class="detail-value">{{ order.phone_number || '未提供' }}</span>
          </div>
          <div v-if="order.payment_method" class="detail-row">
            <span class="detail-label">支付方式:</span>
            <span class="detail-value">{{ getPaymentMethodText(order.payment_method) }}</span>
          </div>
        </div>

        <!-- 装订组信息 -->
        <div v-if="order.groups && order.groups.length > 0" class="groups-section">
          <h4 class="groups-title">装订组详情</h4>
          <div class="groups-list">
            <div
              v-for="group in order.groups"
              :key="group.id"
              class="group-item"
            >
              <div class="group-header">
                <span class="group-binding">{{ getBindingTypeText(group.binding_type) }}</span>
                <span class="group-cost">¥{{ group.binding_cost }}</span>
              </div>

              <div class="documents-list">
                <div
                  v-for="doc in group.documents"
                  :key="doc.id"
                  class="document-item"
                >
                  <span class="doc-name">{{ doc.original_filename }}</span>
                  <div class="doc-specs">
                    <span class="doc-spec">{{ getColorModeText(doc.color_mode) }}</span>
                    <span class="doc-spec">{{ getPrintSidedText(doc.print_sided) }}</span>
                    <span class="doc-spec">{{ getPaperSizeText(doc.paper_size) }}</span>
                    <span class="doc-spec">{{ doc.copies }}份</span>
                    <span class="doc-cost">¥{{ doc.print_cost }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 操作按钮 -->
        <div class="order-actions">
          <button
            @click="downloadOrderSummary(order.id)"
            :disabled="!order.order_summary_pdf"
            class="action-btn download-btn"
            title="下载订单摘要"
          >
            📄 下载摘要
          </button>
          <button
            @click="copyPickupCode(order.pickup_code)"
            class="action-btn copy-btn"
            title="复制取件码"
          >
            📋 复制取件码
          </button>
        </div>
      </div>
    </div>

    <!-- 分页控件 -->
    <div v-if="hasMoreOrders" class="pagination">
      <button
        @click="loadMoreOrders"
        :disabled="loadingMore"
        class="load-more-btn"
      >
        {{ loadingMore ? '加载中...' : '加载更多订单' }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { onMounted, computed } from 'vue';
import { useOrderStore } from '../stores/order';
import { useUserStore } from '../stores/user';
import LoadingSpinner from './LoadingSpinner.vue';

const orderStore = useOrderStore();
const userStore = useUserStore();

const loadingMore = ref(false);
const hasMoreOrders = ref(false);

// 组件挂载时获取用户订单
onMounted(async () => {
  if (userStore.isAuthenticated) {
    await refreshOrders();
  }
});

// 刷新订单列表
async function refreshOrders() {
  if (userStore.isAuthenticated) {
    await orderStore.fetchUserOrders();
  }
}

// 加载更多订单
async function loadMoreOrders() {
  loadingMore.value = true;
  try {
    // 这里可以实现分页加载逻辑
    // 暂时简单刷新所有订单
    await refreshOrders();
  } finally {
    loadingMore.value = false;
  }
}

// 下载订单摘要
async function downloadOrderSummary(orderId) {
  try {
    const response = await fetch(`/api/orders/${orderId}/summary/`, {
      credentials: 'include'
    });

    if (response.ok) {
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `订单摘要_${orderId}.pdf`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    }
  } catch (error) {
    console.error('下载订单摘要失败:', error);
  }
}

// 复制取件码
async function copyPickupCode(pickupCode) {
  try {
    await navigator.clipboard.writeText(pickupCode);
    // 可以添加一个提示
    alert('取件码已复制到剪贴板');
  } catch (error) {
    console.error('复制失败:', error);
    // 降级方案
    const textArea = document.createElement('textarea');
    textArea.value = pickupCode;
    document.body.appendChild(textArea);
    textArea.select();
    document.execCommand('copy');
    document.body.removeChild(textArea);
    alert('取件码已复制到剪贴板');
  }
}

// 格式化日期
function formatDate(dateString) {
  const date = new Date(dateString);
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  });
}

// 获取状态文本
function getStatusText(status) {
  const statusMap = {
    'pending': '待处理',
    'processing': '处理中',
    'completed': '已完成',
    'cancelled': '已取消'
  };
  return statusMap[status] || status;
}

// 获取支付方式文本
function getPaymentMethodText(method) {
  const methodMap = {
    'ALIPAY': '支付宝',
    'WECHAT': '微信支付'
  };
  return methodMap[method] || method;
}

// 获取装订方式文本
function getBindingTypeText(type) {
  const typeMap = {
    'none': '不装订',
    'staple_top_left': '订书钉 (左上角)',
    'staple_left_side': '订书钉 (左侧)',
    'staple': '骑马钉',
    'ring_bound': '胶圈装'
  };
  return typeMap[type] || type;
}

// 获取色彩模式文本
function getColorModeText(mode) {
  const modeMap = {
    'black_white': '黑白',
    'color': '彩色'
  };
  return modeMap[mode] || mode;
}

// 获取打印方式文本
function getPrintSidedText(sided) {
  const sidedMap = {
    'single': '单面',
    'double': '双面',
    'single_double': '封面单面'
  };
  return sidedMap[sided] || sided;
}

// 获取纸张尺寸文本
function getPaperSizeText(size) {
  const sizeMap = {
    'a4': 'A4',
    'b5': 'B5'
  };
  return sizeMap[size] || size;
}
</script>

<style scoped>
.user-orders {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.orders-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.title {
  font-size: 2rem;
  font-weight: 700;
  color: var(--text-color);
  margin: 0;
}

.refresh-btn {
  background-color: #3b82f6;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.refresh-btn:hover:not(:disabled) {
  background-color: #2563eb;
}

.refresh-btn:disabled {
  background-color: #9ca3af;
  cursor: not-allowed;
}

.loading-state, .error-state, .empty-state {
  text-align: center;
  padding: 3rem;
}

.loading-state p {
  margin-top: 1rem;
  color: var(--text-color);
}

.error-message {
  color: #ef4444;
  font-size: 1.1rem;
  margin-bottom: 1rem;
}

.retry-btn {
  background-color: #ef4444;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
}

.retry-btn:hover {
  background-color: #dc2626;
}

.empty-state .empty-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.empty-state h3 {
  color: var(--text-color);
  margin-bottom: 0.5rem;
}

.empty-state p {
  color: #6b7280;
  margin-bottom: 1.5rem;
}

.create-order-btn {
  display: inline-block;
  background-color: #10b981;
  color: white;
  text-decoration: none;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 500;
  transition: background-color 0.2s;
}

.create-order-btn:hover {
  background-color: #059669;
}

.orders-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.order-card {
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 1.5rem;
  background-color: var(--bg-color);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.order-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--border-color);
}

.order-info {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.order-number {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--text-color);
  margin: 0;
}

.pickup-code {
  font-size: 1rem;
  color: #10b981;
  font-weight: 500;
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.875rem;
  font-weight: 500;
}

.status-pending {
  background-color: #fef3c7;
  color: #d97706;
}

.status-processing {
  background-color: #dbeafe;
  color: #2563eb;
}

.status-completed {
  background-color: #d1fae5;
  color: #059669;
}

.status-cancelled {
  background-color: #fee2e2;
  color: #dc2626;
}

.order-details {
  margin-bottom: 1.5rem;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 0;
  border-bottom: 1px solid #f3f4f6;
}

.detail-row:last-child {
  border-bottom: none;
}

.detail-label {
  font-weight: 500;
  color: var(--text-color);
}

.detail-value {
  color: #6b7280;
}

.detail-value.price {
  color: #10b981;
  font-weight: 600;
  font-size: 1.1rem;
}

.groups-section {
  margin-bottom: 1.5rem;
}

.groups-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--text-color);
  margin-bottom: 1rem;
}

.groups-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.group-item {
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 1rem;
  background-color: #f9fafb;
}

.group-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.group-binding {
  font-weight: 500;
  color: var(--text-color);
}

.group-cost {
  color: #10b981;
  font-weight: 500;
}

.documents-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.document-item {
  padding: 0.5rem;
  background-color: white;
  border-radius: 4px;
  border: 1px solid #e5e7eb;
}

.doc-name {
  font-weight: 500;
  color: var(--text-color);
  margin-bottom: 0.25rem;
  display: block;
}

.doc-specs {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.doc-spec {
  font-size: 0.8rem;
  color: #6b7280;
  background-color: #f3f4f6;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
}

.doc-cost {
  color: #10b981;
  font-weight: 500;
}

.order-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  padding-top: 1rem;
  border-top: 1px solid var(--border-color);
}

.action-btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 6px;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.2s;
}

.download-btn {
  background-color: #3b82f6;
  color: white;
}

.download-btn:hover:not(:disabled) {
  background-color: #2563eb;
}

.download-btn:disabled {
  background-color: #9ca3af;
  cursor: not-allowed;
}

.copy-btn {
  background-color: #6b7280;
  color: white;
}

.copy-btn:hover {
  background-color: #4b5563;
}

.pagination {
  text-align: center;
  margin-top: 2rem;
}

.load-more-btn {
  background-color: #f3f4f6;
  color: var(--text-color);
  border: 1px solid var(--border-color);
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.2s;
}

.load-more-btn:hover:not(:disabled) {
  background-color: #e5e7eb;
}

.load-more-btn:disabled {
  background-color: #f9fafb;
  color: #9ca3af;
  cursor: not-allowed;
}

@media (max-width: 768px) {
  .user-orders {
    padding: 1rem;
  }

  .orders-header {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }

  .order-header {
    flex-direction: column;
    gap: 1rem;
  }

  .order-actions {
    flex-direction: column;
  }

  .doc-specs {
    flex-direction: column;
  }
}
</style>
