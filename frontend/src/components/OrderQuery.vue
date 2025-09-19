<script setup>
import { ref, computed } from 'vue';
import apiService from '@/services/apiService';

const queryPhoneNumber = ref('');
const queryPickupCode = ref('');
const isLoading = ref(false);
const searchResult = ref(null);
const searchAttempted = ref(false);
const errorMessage = ref('');

const isQueryButtonDisabled = computed(() => {
  return !queryPhoneNumber.value || !queryPickupCode.value || isLoading.value;
});

const statusInfo = computed(() => {
  if (!searchResult.value) return {};
  const status = searchResult.value.status;
  const statusMap = {
    pending: { text: '待处理', class: 'status-pending' },
    processing: { text: '处理中', class: 'status-printing' },
    completed: { text: '已完成', class: 'status-completed' },
    cancelled: { text: '已取消', class: 'status-cancelled' },
  };
  return statusMap[status] || { text: status, class: 'status-default' };
});

async function performQuery() {
  if (isQueryButtonDisabled.value) return;
  isLoading.value = true;
  searchAttempted.value = true;
  searchResult.value = null;
  errorMessage.value = '';

  try {
    const response = await apiService.queryOrder(queryPhoneNumber.value, queryPickupCode.value);

    if (response.data && response.data.length > 0) {
      // 如果返回多个订单，取第一个
      searchResult.value = response.data[0];
    } else {
      searchResult.value = null;
    }
  } catch (error) {
    console.error('查询失败:', error);
    errorMessage.value = '查询请求失败，请检查输入或稍后重试。';
  } finally {
    isLoading.value = false;
  }
}

function formatDateTime(isoString) {
  if (!isoString) return 'N/A';
  const date = new Date(isoString);
  return date.toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai', hour12: false });
}

// 是否存在预估价格（订单级或任一文档级）
const anyEstimated = computed(() => {
  const order = searchResult.value;
  if (!order) return false;
  if (order.is_estimated || order.page_count_source === 'estimated') return true;
  if (!order.groups) return false;
  return order.groups.some(g => (g.documents || []).some(d => d.page_count_source !== 'exact'));
});
</script>

<template>
  <div class="query-container">
    <div class="query-card">
      <h2>订单状态查询</h2>
      <p class="subtitle">请输入您的手机号和取件码以获取最新状态。</p>

      <div class="query-form">
        <div class="input-group">
          <input type="tel" v-model.trim="queryPhoneNumber" placeholder="手机号" />
        </div>
        <div class="input-group">
          <input type="text" v-model.trim="queryPickupCode" placeholder="取件码 (例如 P-066)" />
        </div>
        <button @click="performQuery" :disabled="isQueryButtonDisabled">
          <span v-if="!isLoading">查询订单</span>
          <div v-else class="spinner"></div>
        </button>
      </div>
    </div>

    <div v-if="isLoading" class="result-card loading-state">
      <div class="spinner large"></div>
      <p>正在查询中...</p>
    </div>

    <div v-else-if="searchResult" class="result-card">
      <h3>查询结果</h3>
      <div v-if="anyEstimated" class="order-estimated-alert">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>
        订单价格为预估，后台将自动校正
      </div>
      <div class="result-grid">
        <div><strong>取件码:</strong> {{ searchResult.pickup_code }}</div>
        <div><strong>订单号:</strong> {{ searchResult.order_number }}</div>
        <div><strong>手机号:</strong> {{ searchResult.phone_number }}</div>
        <div><strong>下单时间:</strong> {{ formatDateTime(searchResult.created_at) }}</div>
        <div><strong>订单状态:</strong>
          <span class="status-badge" :class="statusInfo.class">{{ statusInfo.text }}</span>
        </div>
        <div><strong>订单总价:</strong> ¥{{ searchResult.total_price }}</div>
      </div>
      <hr />

      <div v-for="(group, index) in searchResult.groups" :key="group.id">
        <h4>装订组 #{{ index + 1 }} - (装订方式: {{ group.binding_type === 'none' ? '不装订' : group.binding_type }})</h4>

        <ul class="spec-list">
          <li v-for="doc in group.documents" :key="doc.id" class="document-details-item">
            <div class="doc-title-line">
              <strong>📄 {{ doc.original_filename }}</strong>
              <a :href="doc.file_path" target="_blank" rel="noopener noreferrer">查看文件</a>
            </div>
            <div class="doc-specs-line">
              <span>{{ doc.copies }} 份</span> |
              <span>{{ doc.color_mode === 'color' ? '彩色' : '黑白' }}</span> |
              <span>{{ doc.print_sided === 'double' ? '双面' : '单面' }}</span>
              <span
                class="doc-status-badge"
                :class="doc.page_count_source === 'exact' ? 'doc-badge-exact' : 'doc-badge-estimated'"
                :title="doc.page_count_source === 'exact' ? '价格已精确计算' : '价格为预估，后台将自动校正'"
              >{{ doc.page_count_source === 'exact' ? '精确' : '预估' }}</span>
            </div>
          </li>
        </ul>
      </div>
    </div>

    <div v-else-if="searchAttempted && !errorMessage" class="result-card info-state">
      <p>未找到相关订单，请检查您输入的信息是否正确。</p>
    </div>
    <div v-if="errorMessage" class="result-card error-state">
      <p>{{ errorMessage }}</p>
    </div>
  </div>
</template>

<style scoped>
/*
  OrderQuery.vue 的样式已更新，使用 CSS 变量以支持主题切换。
*/
.query-container {
  font-family: 'Noto Sans SC', sans-serif;
  padding: 1rem;
  max-width: 800px;
  margin: 1rem auto;
}

.query-card,
.result-card {
  background-color: var(--color-background-soft); /* 已修改 */
  border-radius: 12px;
  padding: 2rem;
  box-shadow: var(--shadow-card); /* 已修改 */
  margin-bottom: 2rem;
  border: 1px solid var(--color-border); /* 已修改 */
}

h2 {
  text-align: center;
  color: var(--color-heading); /* 已修改 */
  margin-top: 0;
}

.subtitle {
  text-align: center;
  color: var(--color-text-mute); /* 已修改 */
  margin-bottom: 2rem;
}

.query-form {
  display: flex;
  gap: 1rem;
  align-items: stretch;
}

.input-group {
  flex-grow: 1;
}

input[type="tel"],
input[type="text"] {
  width: 100%;
  height: 100%;
  padding: 0.75rem 1rem;
  border: 1px solid var(--color-border); /* 已修改 */
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.2s, box-shadow 0.2s;
  background-color: var(--color-background); /* 已修改 */
  color: var(--color-text); /* 已修改 */
}

input:focus {
  outline: none;
  border-color: var(--color-primary); /* 已修改 */
  box-shadow: 0 0 0 3px rgba(var(--color-primary-rgb, 37, 99, 235), 0.2); /* 已修改 */
}

button {
  padding: 0.75rem 1.5rem;
  border: none;
  background-color: var(--color-primary); /* 已修改 */
  color: var(--color-text-on-primary); /* 已修改 */
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
  white-space: nowrap;
  min-width: 110px;
  display: flex;
  align-items: center;
  justify-content: center;
}

button:hover:not(:disabled) {
  background-color: var(--color-primary-hover); /* 已修改 */
}

button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.result-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
  margin-top: 1rem;
}

.result-grid div {
  background-color: var(--color-background); /* 已修改 */
  padding: 0.75rem;
  border-radius: 6px;
  color: var(--color-text); /* 已修改 */
  border: 1px solid var(--color-border); /* 已修改 */
}

hr {
  border: none;
  border-top: 1px solid var(--color-border); /* 已修改 */
  margin: 1.5rem 0;
}

h3,
h4 {
  margin: 1.5rem 0 0.5rem 0;
  color: var(--color-heading); /* 已修改 */
}

.status-badge {
  padding: 0.25em 0.6em;
  font-size: 0.85em;
  font-weight: 700;
  border-radius: 2em;
  color: white; /* 状态徽章背景色已足够区分，文字用白色即可 */
}

.status-pending { background-color: var(--color-secondary); }
.status-printing { background-color: var(--color-primary); }
.status-completed { background-color: var(--color-success); }
.status-cancelled { background-color: var(--color-danger); }
.status-default { background-color: var(--color-text); }

.info-state,
.error-state,
.loading-state {
  text-align: center;
  color: var(--color-text-mute); /* 已修改 */
  padding: 3rem 1rem;
}

.error-state {
  color: var(--color-danger); /* 已修改 */
  font-weight: 500;
}

.spinner {
  display: inline-block;
  width: 20px;
  height: 20px;
  border: 3px solid rgba(255, 255, 255, 0.3); /* 按钮内的 spinner，背景是深色，所以用白色 */
  border-radius: 50%;
  border-top-color: #fff;
  animation: spin 1s ease-in-out infinite;
}

.spinner.large {
  width: 40px;
  height: 40px;
  border-top-color: var(--color-primary); /* 已修改 */
  border-color: rgba(var(--color-primary-rgb, 37, 99, 235), 0.1); /* 已修改 */
  border-width: 4px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.spec-list {
  list-style-type: none;
  padding: 0;
}

.document-details-item {
  background-color: var(--color-background); /* 已修改 */
  border: 1px solid var(--color-border); /* 已修改 */
  padding: 0.75rem 1rem;
  border-radius: 8px;
  margin-bottom: 0.5rem;
}

.doc-title-line {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.doc-title-line strong {
  color: var(--color-heading); /* 已修改 */
  font-weight: 500;
}

.doc-title-line a {
  font-size: 0.9em;
  color: var(--color-primary); /* 已修改 */
}

.doc-specs-line {
  font-size: 0.85rem;
  color: var(--color-text-mute); /* 已修改 */
}

/* 文档级 预估/精确 徽章样式（避免与订单状态徽章冲突） */
.doc-status-badge {
  display: inline-flex;
  align-items: center;
  padding: 0.1rem 0.4rem;
  border-radius: 999px;
  font-size: 0.72rem;
  line-height: 1;
  border: 1px solid transparent;
  margin-left: 0.5rem;
}
.doc-badge-estimated {
  color: #8a6d3b;
  background: #fcf8e3;
  border-color: #faebcc;
}
.doc-badge-exact {
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

@media (max-width: 639px) {
  .query-form {
    flex-direction: column;
  }
  button {
    width: 100%;
  }
}
</style>
