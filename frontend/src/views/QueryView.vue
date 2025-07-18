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

// ▼▼▼ 在此处新增以下函数 ▼▼▼
/**
 * 将 'print_sided' 字段的英文代码转换为中文。
 * @param {string} sidedCode - 后端返回的 print_sided 值
 */
function formatPrintSided(sidedCode) {
  const map = {
    'single': '单面打印',
    'double': '双面打印',
    'single_double': '封面单面'
  };
  return map[sidedCode] || sidedCode; // 如果没匹配到，返回原始值
}
// ▲▲▲ 新增函数结束 ▲▲▲
</script>

<template>
  <!-- --- 模板部分无需任何修改，保持原样即可 --- -->
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
                  <span>{{ doc.paper_size.toUpperCase() }}</span>
                  <span>{{ doc.color_mode === 'color' ? '彩色' : '黑白' }}</span>
                  <span>{{ formatPrintSided(doc.print_sided) }}</span>
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
/*
  QueryView.vue 的样式已完全重写，以支持主题切换。
  所有布局、尺寸和响应式逻辑均已完整保留。
*/
.query-container {
  font-family: 'Noto Sans SC', sans-serif;
  padding: 1rem;
  max-width: 800px;
  margin: 1rem auto;
}

.query-card,
.result-card {
  background-color: var(--color-background-soft);
  border-radius: 12px;
  padding: 2rem;
  box-shadow: var(--shadow-card);
  margin-bottom: 2rem;
  border: 1px solid var(--color-border);
}

h2 {
  text-align: center;
  color: var(--color-heading);
  margin-top: 0;
}

.subtitle {
  text-align: center;
  color: var(--color-text-mute);
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
  border: 1px solid var(--color-border);
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.2s, box-shadow 0.2s;
  background-color: var(--color-background);
  color: var(--color-text);
}

input:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(var(--color-primary-rgb, 37, 99, 235), 0.2);
}

button {
  padding: 0.75rem 1.5rem;
  border: none;
  background-color: var(--color-primary);
  color: var(--color-text-on-primary);
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
  background-color: var(--color-primary-hover);
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
  background-color: var(--color-background);
  padding: 0.75rem;
  border-radius: 6px;
  color: var(--color-text);
  border: 1px solid var(--color-border);
}

hr {
  border: none;
  border-top: 1px solid var(--color-border);
  margin: 1.5rem 0;
}

h3,
h4 {
  margin: 1.5rem 0 0.5rem 0;
  color: var(--color-heading);
}

.status-badge {
  padding: 0.25em 0.6em;
  font-size: 0.85em;
  font-weight: 700;
  border-radius: 2em;
  color: white;
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
  color: var(--color-text-mute);
  padding: 3rem 1rem;
}

.error-state {
  color: var(--color-danger);
  font-weight: 500;
}

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
  border-top-color: var(--color-primary);
  border-color: rgba(var(--color-primary-rgb, 37, 99, 235), 0.1);
  border-width: 4px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.result-group-card {
  border: 1px solid var(--color-border);
  border-radius: 12px;
  margin-top: 1.5rem;
  background-color: var(--color-background);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
  overflow: hidden;
}

.group-header {
  display: flex;
  justify-content: space-between;
  padding: 0.75rem 1.25rem;
  background-color: var(--color-background-soft);
  border-bottom: 1px solid var(--color-border);
  font-weight: 600;
  color: var(--color-heading);
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
  background-color: var(--color-background-soft);
}

.document-entry-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.file-icon {
  font-size: 1.5rem;
  color: var(--color-text-mute);
}

.file-text {
  display: flex;
  flex-direction: column;
}

.file-name {
  font-weight: 500;
  color: var(--color-text);
  margin: 0 0 0.25rem 0;
}

.file-specs {
  display: flex;
  gap: 1rem;
  font-size: 0.85rem;
  color: var(--color-text-mute);
}

.view-file-link {
  font-size: 0.9em;
  text-decoration: none;
  color: var(--color-primary);
  font-weight: 500;
  padding: 0.4rem 0.8rem;
  border-radius: 6px;
  background-color: transparent;
  border: 1px solid transparent;
  transition: background-color 0.2s, border-color 0.2s;
}

.view-file-link:hover {
  background-color: rgba(var(--color-primary-rgb, 37, 99, 235), 0.1);
  border-color: rgba(var(--color-primary-rgb, 37, 99, 235), 0.1);
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
