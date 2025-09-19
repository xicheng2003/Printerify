<template>
  <div class="user-orders-container">
    <div class="page-header">
      <h1 class="page-title">我的订单</h1>
      <button @click="refreshOrders" :disabled="orderStore.userOrdersLoading" class="refresh-button">
        <svg v-if="orderStore.userOrdersLoading" class="animate-spin h-5 w-5 mr-2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        <span>{{ orderStore.userOrdersLoading ? '正在刷新' : '刷新' }}</span>
      </button>
    </div>

    <div v-if="orderStore.userOrdersLoading && !orderStore.userOrders.length" class="state-view loading-view">
      <LoadingSpinner />
      <p class="state-text">正在加载您的订单历史...</p>
    </div>

    <div v-else-if="orderStore.userOrdersError" class="state-view error-view">
      <div class="icon-wrapper error-icon">
        <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>
      </div>
      <h3 class="state-title">加载失败</h3>
      <p class="state-description">{{ orderStore.userOrdersError }}</p>
      <button @click="refreshOrders" class="state-action-button">重试</button>
    </div>

    <div v-else-if="!orderStore.userOrders.length" class="state-view empty-view">
      <div class="icon-wrapper empty-icon">
        <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"></path><line x1="3" y1="6" x2="21" y2="6"></line><path d="M16 10a4 4 0 0 1-8 0"></path></svg>
      </div>
      <h3 class="state-title">您还没有订单</h3>
      <p class="state-description">开始您的第一次打印，体验便捷服务吧！</p>
      <router-link to="/" class="state-action-button primary">立即下单</router-link>
    </div>

    <div v-else class="orders-grid">
      <div v-for="order in orderStore.userOrders" :key="order.id" class="order-card-new">
        <div class="card-header">
          <div class="header-info">
            <span class="order-number-new">订单号: {{ order.order_number }}</span>
            <span :class="['status-badge-new', `status-${order.status}`]">{{ getStatusText(order.status) }}</span>
          </div>
          <div class="order-date">{{ formatDate(order.created_at) }}</div>
        </div>

        <div class="card-body">
          <div v-if="order.is_estimated || order.page_count_source === 'estimated'" class="order-estimated-alert">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>
            订单价格为预估，后台将自动校正
          </div>
          <div class="main-info">
            <div class="info-item">
              <span class="info-label">取件码</span>
              <span class="info-value pickup-code-new">{{ order.pickup_code }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">总金额</span>
              <span class="info-value total-price-new">¥{{ order.total_price }}</span>
            </div>
             <div class="info-item">
              <span class="info-label">支付方式</span>
              <span class="info-value">{{ getPaymentMethodText(order.payment_method) }}</span>
            </div>
          </div>
           <details v-if="order.groups && order.groups.length > 0" class="groups-details">
            <summary class="details-summary">查看打印详情 ({{order.groups.length}}个装订组)</summary>
            <div class="groups-content">
              <div v-for="group in order.groups" :key="group.id" class="group-item-new">
                <div class="group-title-new">
                  <span>{{ getBindingTypeText(group.binding_type) }}</span>
                  <span>装订费: ¥{{ group.binding_cost }}</span>
                </div>
                <ul>
                  <li v-for="doc in group.documents" :key="doc.id" class="document-item-new">
                    <span class="doc-name-new">{{ doc.original_filename }} ({{ doc.copies }}份)</span>
                    <div class="doc-specs-new">
                      <span>{{ getColorModeText(doc.color_mode) }}</span>,
                      <span>{{ getPrintSidedText(doc.print_sided) }}</span>,
                      <span>{{ getPaperSizeText(doc.paper_size) }}</span>
                      <span class="doc-cost-new">¥{{ doc.print_cost }}</span>
                      <span
                        class="status-badge"
                        :class="doc.page_count_source === 'exact' ? 'badge-exact' : 'badge-estimated'"
                        :title="doc.page_count_source === 'exact' ? '价格已精确计算' : '价格为预估，后台将自动校正'"
                      >{{ doc.page_count_source === 'exact' ? '精确' : '预估' }}</span>
                    </div>
                  </li>
                </ul>
              </div>
            </div>
          </details>
        </div>

        <div class="card-footer">
          <button @click="copyPickupCode(order.pickup_code)" class="action-button-new">复制取件码</button>
          <button @click="downloadOrderSummary(order.id)" :disabled="!order.order_summary_pdf" class="action-button-new primary">下载摘要</button>
        </div>
      </div>
    </div>

    <div v-if="hasMoreOrders" class="pagination-container">
      <button @click="loadMoreOrders" :disabled="loadingMore" class="load-more-button">
        {{ loadingMore ? '加载中...' : '加载更多' }}
      </button>
    </div>
  </div>
</template>


<script setup>
// ===================================================================
// 脚本部分 (Script Section)
// ===================================================================
//
// 【重要】这里的业务逻辑完全没有改动，
// 只是为了适配新的模板结构，对 ref 变量的定义进行了补充。
// 所有核心功能、方法和 store 的使用均保持不变。
//
import { onMounted, ref } from 'vue'; // 引入 ref
import { useOrderStore } from '../stores/order';
import { useUserStore } from '../stores/user';
import LoadingSpinner from './LoadingSpinner.vue';

const orderStore = useOrderStore();
const userStore = useUserStore();

// 补充 ref 定义
const loadingMore = ref(false);
const hasMoreOrders = ref(false);

onMounted(async () => {
  if (userStore.isAuthenticated) {
    await refreshOrders();
  }
});

async function refreshOrders() {
  if (userStore.isAuthenticated) {
    await orderStore.fetchUserOrders();
  }
}

async function loadMoreOrders() {
  loadingMore.value = true;
  try {
    await refreshOrders();
  } finally {
    loadingMore.value = false;
  }
}

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

async function copyPickupCode(pickupCode) {
  try {
    await navigator.clipboard.writeText(pickupCode);
    alert('取件码已复制到剪贴板');
  } catch (error) {
    console.error('复制失败:', error);
    const textArea = document.createElement('textarea');
    textArea.value = pickupCode;
    document.body.appendChild(textArea);
    textArea.select();
    document.execCommand('copy');
    document.body.removeChild(textArea);
    alert('取件码已复制到剪贴板');
  }
}

function formatDate(dateString) {
  const date = new Date(dateString);
  return date.toLocaleString('zh-CN', { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' });
}

function getStatusText(status) {
  const statusMap = { 'pending': '待处理', 'processing': '处理中', 'completed': '已完成', 'cancelled': '已取消' };
  return statusMap[status] || status;
}

function getPaymentMethodText(method) {
  const methodMap = { 'ALIPAY': '支付宝', 'WECHAT': '微信支付' };
  return methodMap[method] || method || '未指定';
}

function getBindingTypeText(type) {
  const typeMap = { 'none': '不装订', 'staple_top_left': '左上角装订', 'staple_left_side': '左侧装订', 'staple': '骑马钉', 'ring_bound': '胶圈装订' };
  return typeMap[type] || type;
}

function getColorModeText(mode) {
  const modeMap = { 'black_white': '黑白', 'color': '彩色' };
  return modeMap[mode] || mode;
}

function getPrintSidedText(sided) {
  const sidedMap = { 'single': '单面', 'double': '双面', 'single_double': '封面单面' };
  return sidedMap[sided] || sided;
}

function getPaperSizeText(size) {
  const sizeMap = { 'a4': 'A4', 'b5': 'B5' };
  return sizeMap[size] || size;
}
</script>

<style scoped>
/* 整体容器和头部 */
.user-orders-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  font-family: inherit;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--color-border);
}

.page-title {
  font-size: 1.875rem; /* 30px */
  font-weight: 700;
  color: var(--color-heading);
}

.refresh-button {
  display: inline-flex;
  align-items: center;
  background-color: var(--color-background-soft);
  color: var(--color-text);
  border: 1px solid var(--color-border);
  padding: 0.625rem 1.25rem;
  border-radius: 8px;
  font-size: 0.95rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}
.refresh-button:hover:not(:disabled) {
  background-color: var(--color-background-mute);
  border-color: var(--color-border-hover);
  color: var(--color-primary);
}
.refresh-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* 状态视图 (加载、错误、空) */
.state-view {
  text-align: center;
  padding: 4rem 2rem;
  background-color: var(--color-background-soft);
  border-radius: 12px;
  border: 1px solid var(--color-border);
}
.state-view .icon-wrapper {
  margin: 0 auto 1.5rem;
  width: 64px;
  height: 64px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--color-background-mute);
  color: var(--color-text-mute);
}
.state-view .error-icon { background-color: rgba(var(--color-danger-rgb), 0.1); color: var(--color-danger); }
.state-view .empty-icon { background-color: rgba(var(--color-primary-rgb), 0.1); color: var(--color-primary); }
.state-title { font-size: 1.25rem; font-weight: 600; color: var(--color-heading); margin-bottom: 0.5rem; }
.state-description { color: var(--color-text-mute); margin-bottom: 1.5rem; }
.state-text { color: var(--color-text); margin-top: 1rem; }
.state-action-button {
  display: inline-block;
  background-color: var(--color-background-mute);
  color: var(--color-text);
  border: 1px solid var(--color-border);
  padding: 0.75rem 2rem;
  border-radius: 8px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.2s;
}
.state-action-button.primary, .state-action-button:hover {
  background-color: var(--color-primary);
  color: var(--color-text-on-primary);
  border-color: var(--color-primary);
}
.state-action-button.primary:hover {
  background-color: var(--color-primary-hover);
}

/* 订单卡片网格布局 */
.orders-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 1.5rem;
}

/* 新订单卡片样式 */
.order-card-new {
  background-color: var(--color-background);
  border: 1px solid var(--color-border);
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  transition: all 0.2s ease-in-out;
}
.order-card-new:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 25px var(--shadow-color);
  border-color: var(--color-primary);
}

.card-header { padding: 1rem 1.5rem; border-bottom: 1px solid var(--color-border); }
.header-info { display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.25rem; }
.order-number-new { font-weight: 600; color: var(--color-heading); }
.order-date { font-size: 0.8rem; color: var(--color-text-mute); }

.card-body { padding: 1.5rem; }
.main-info { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-bottom: 1.5rem; text-align: center; }
.info-label { font-size: 0.8rem; color: var(--color-text-mute); margin-bottom: 0.25rem; display: block; }
.info-value { font-weight: 600; color: var(--color-heading); }
.pickup-code-new { color: var(--color-primary); font-size: 1.1rem; }
.total-price-new { color: var(--color-primary); font-size: 1.1rem; }

/* 状态徽章 */
.status-badge-new { padding: 0.25rem 0.75rem; border-radius: 20px; font-size: 0.75rem; font-weight: 500; }
.status-badge-new.status-pending { background-color: #fef3c7; color: #b45309; }
.status-badge-new.status-processing { background-color: #dbeafe; color: #1e40af; }
.status-badge-new.status-completed { background-color: #d1fae5; color: #065f46; }
.status-badge-new.status-cancelled { background-color: #fee2e2; color: #991b1b; }
html.dark .status-badge-new.status-pending { background-color: #78350f; color: #fef3c7; }
html.dark .status-badge-new.status-processing { background-color: #1e40af; color: #dbeafe; }
html.dark .status-badge-new.status-completed { background-color: #065f46; color: #d1fae5; }
html.dark .status-badge-new.status-cancelled { background-color: #991b1b; color: #fee2e2; }

/* 打印详情折叠区 */
.details-summary { cursor: pointer; font-weight: 500; color: var(--color-text-mute); font-size: 0.9rem; }
.groups-content { margin-top: 1rem; background-color: var(--color-background-soft); padding: 1rem; border-radius: 8px; }
.group-item-new { margin-bottom: 1rem; }
.group-item-new:last-child { margin-bottom: 0; }
.group-title-new { display: flex; justify-content: space-between; font-weight: 600; font-size: 0.9rem; margin-bottom: 0.5rem; }
.group-item-new ul { list-style: none; padding-left: 0; display: flex; flex-direction: column; gap: 0.5rem; }
.document-item-new { display: flex; justify-content: space-between; flex-wrap: wrap; font-size: 0.85rem; }
.doc-name-new { font-weight: 500; color: var(--color-text); }
.doc-specs-new { color: var(--color-text-mute); font-size: 0.8rem; }
.doc-cost-new { font-weight: 500; margin-left: auto; padding-left: 1rem; }

/* 文档级 预估/精确 徽章样式（与 DocumentItem 保持一致） */
.status-badge {
  display: inline-flex;
  align-items: center;
  padding: 0.1rem 0.4rem;
  border-radius: 999px;
  font-size: 0.72rem;
  line-height: 1;
  border: 1px solid transparent;
  margin-left: 0.5rem;
}
.badge-estimated {
  color: #8a6d3b;
  background: #fcf8e3;
  border-color: #faebcc;
}
.badge-exact {
  color: #2f6b2f;
  background: #e6f4ea;
  border-color: #b7e1c1;
}

/* 订单级 预估提示条 */
.order-estimated-alert {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 0.75rem;
  border-radius: 8px;
  background: #fff7ed; /* amber-50 */
  border: 1px solid #fed7aa; /* amber-200 */
  color: #9a3412; /* amber-800 */
  margin-bottom: 1rem;
}
html.dark .order-estimated-alert {
  background: #78350f;
  border-color: #a16207;
  color: #fde68a;
}

/* 卡片脚部 */
.card-footer { margin-top: auto; padding: 1rem 1.5rem; border-top: 1px solid var(--color-border); display: flex; justify-content: flex-end; gap: 0.75rem; background-color: var(--color-background-soft); }
.action-button-new {
  background-color: transparent;
  color: var(--color-text);
  border: 1px solid var(--color-border);
  padding: 0.5rem 1rem;
  border-radius: 6px;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}
.action-button-new.primary {
  background-color: var(--color-primary);
  border-color: var(--color-primary);
  color: var(--color-text-on-primary);
}
.action-button-new:hover:not(:disabled) {
  transform: translateY(-1px);
  background-color: var(--color-background-mute);
}
.action-button-new.primary:hover:not(:disabled) {
  background-color: var(--color-primary-hover);
  border-color: var(--color-primary-hover);
}
.action-button-new:disabled { opacity: 0.5; cursor: not-allowed; }

/* 分页 */
.pagination-container { text-align: center; margin-top: 2rem; }
.load-more-button {
  background-color: var(--color-background-soft);
  color: var(--color-text);
  border: 1px solid var(--color-border);
  padding: 0.75rem 2rem;
  border-radius: 8px;
  font-weight: 600;
  transition: all 0.2s;
}

@media (max-width: 768px) {
  .user-orders-container { padding: 1rem; }
  .page-header { flex-direction: column; align-items: flex-start; gap: 1rem; }
  .main-info { grid-template-columns: 1fr 1fr; }
}

</style>
