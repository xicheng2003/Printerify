<script setup>
// --- 脚本部分无需任何修改，保持原样即可 ---
import { ref, computed } from 'vue';
import axios from 'axios';

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
    const response = await axios.get('/api/orders/', {
      params: {
        phone: queryPhoneNumber.value,
        code: queryPickupCode.value,
      },
      withCredentials: true,
    });

    if (response.data && response.data.length > 0) {
      const orderId = response.data[0].id;
      const detailedResponse = await axios.get(`/api/orders/${orderId}/`, {
        withCredentials: true,
      });
      searchResult.value = detailedResponse.data;
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
          <input type="text" v-model.trim="queryPickupCode" placeholder="取件码 (例如 P-071)" />
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

      <h4>订单内容详情</h4>
      <div v-for="(group, index) in searchResult.groups" :key="group.id" class="result-group-card">
        <div class="group-header">
          <strong>装订组 #{{ index + 1 }}</strong>
          <span>装订方式: {{ group.binding_type === 'none' ? '不装订' : group.binding_type }}</span>
        </div>
        <div class="document-list">
          <div v-for="doc in group.documents" :key="doc.id" class="document-entry">
            <div class="document-entry-info">
              <span class="file-icon">📄</span>
              <div class="file-text">
                <p class="file-name">{{ doc.original_filename }}</p>
                <div class="file-specs">
                  <span>{{ doc.copies }} 份</span>
                  <span>{{ doc.color_mode === 'color' ? '彩色' : '黑白' }}</span>
                  <span>{{ doc.print_sided === 'double' ? '双面' : '单面' }}</span>
                </div>
              </div>
            </div>
            <a :href="doc.file_path" target="_blank" class="view-file-link">查看文件</a>
          </div>
        </div>
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
/* 将 @import 移到最前面 */
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;700&display=swap');

/* --- 【核心修改】为新的卡片式布局添加样式 --- */
.result-group-card {
  border: 1px solid #e9ecef;
  border-radius: 12px;
  margin-top: 1.5rem;
  background-color: #ffffff;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  overflow: hidden;
}
.group-header {
  display: flex;
  justify-content: space-between;
  padding: 0.75rem 1.25rem;
  background-color: #f8f9fa;
  border-bottom: 1px solid #e9ecef;
  font-weight: 600;
  color: #34495e;
}
.document-list {
  padding: 0.5rem;
}
.document-entry {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem;
  transition: background-color 0.2s;
  border-radius: 8px;
}
.document-entry:hover {
  background-color: #f8f9fa;
}
.document-entry-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}
.file-icon {
  font-size: 1.5rem;
  color: #6c757d;
}
.file-text {
  display: flex;
  flex-direction: column;
}
.file-name {
  font-weight: 500;
  color: #333;
  margin: 0 0 0.25rem 0;
}
.file-specs {
  display: flex;
  gap: 1rem;
  font-size: 0.85rem;
  color: #6c757d;
}
.view-file-link {
  font-size: 0.9em;
  text-decoration: none;
  color: #007bff;
  font-weight: 500;
  padding: 0.4rem 0.8rem;
  border-radius: 6px;
  background-color: transparent;
  border: 1px solid transparent;
  transition: background-color 0.2s, border-color 0.2s;
}
.view-file-link:hover {
  background-color: rgba(0, 123, 255, 0.1);
  border-color: rgba(0, 123, 255, 0.1);
}

/* --- 您原有的所有样式保持不变 --- */
:root {
  --primary-color: #007bff;
  --primary-hover: #0056b3;
  --primary-color-light: rgba(0, 123, 255, 0.1);
  --background-color: #f8f9fa;
  --card-background: #ffffff;
  --text-color: #333;
  --subtitle-color: #6c757d;
  --border-color: #dee2e6;
}

.query-container {
  font-family: 'Noto Sans SC', sans-serif;
  padding: 1rem;
  max-width: 800px;
  margin: 1rem auto;
}
.query-card, .result-card {
  background-color: var(--card-background);
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  margin-bottom: 2rem;
}
h2 {
  text-align: center;
  color: var(--text-color);
  margin-top: 0;
}
.subtitle {
  text-align: center;
  color: var(--subtitle-color);
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
input[type="tel"], input[type="text"] {
  width: 100%;
  height: 100%;
  padding: 0.75rem 1rem;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.2s, box-shadow 0.2s;
}
input:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px var(--primary-color-light);
}
button {
  padding: 0.75rem 1.5rem;
  border: none;
  background-color: var(--primary-color);
  color: white;
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
  background-color: var(--primary-hover);
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
  background-color: #f8f9fa;
  padding: 0.75rem;
  border-radius: 6px;
}
hr {
  border: none;
  border-top: 1px solid #eee;
  margin: 1.5rem 0;
}
h3, h4 { margin: 1.5rem 0 0.5rem 0; }
.status-badge {
  padding: 0.25em 0.6em;
  font-size: 0.85em;
  font-weight: 700;
  border-radius: 2em;
  color: white;
}
.status-pending { background-color: #6c757d; }
.status-printing { background-color: #007bff; }
.status-completed { background-color: #28a745; }
.status-picked-up { background-color: #17a2b8; }
.status-cancelled { background-color: #dc3545; }
.status-default { background-color: #343a40; }
.info-state, .error-state, .loading-state {
  text-align: center;
  color: var(--subtitle-color);
  padding: 3rem 1rem;
}
.error-state { color: #dc3545; font-weight: 500; }
.spinner {
  display: inline-block;
  width: 20px;
  height: 20px;
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: #fff;
  animation: spin 1s ease-in-out infinite;
}
.spinner.large {
  width: 40px;
  height: 40px;
  border-top-color: var(--primary-color);
  border-color: rgba(0, 123, 255, 0.1);
  border-width: 4px;
}
@keyframes spin {
  to { transform: rotate(360deg); }
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
