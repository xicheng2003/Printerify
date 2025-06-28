<script setup>
import { ref, computed } from 'vue';
import axios from 'axios';

// --- 状态定义 ---
const queryPhoneNumber = ref('');
const queryOrderNumber = ref('');
const isLoading = ref(false);
const searchResult = ref(null); // 存储查询到的订单对象
const searchAttempted = ref(false); // 标记是否已经尝试过搜索
const errorMessage = ref(''); // 存储错误信息

// --- 计算属性 ---

// 控制查询按钮是否可点击
const isQueryButtonDisabled = computed(() => {
  return !queryPhoneNumber.value || !queryOrderNumber.value || isLoading.value;
});

// 根据订单状态返回对应的CSS类名，用于显示不同颜色的徽章
const statusInfo = computed(() => {
  if (!searchResult.value) return {};
  const status = searchResult.value.status;
  const statusMap = {
    PENDING: { text: '待处理', class: 'status-pending' },
    PRINTING: { text: '打印中', class: 'status-printing' },
    COMPLETED: { text: '已完成', class: 'status-completed' },
    PICKED_UP: { text: '已取件', class: 'status-picked-up' },
    CANCELLED: { text: '已取消', class: 'status-cancelled' },
  };
  return statusMap[status] || { text: status, class: 'status-default' };
});

// --- 方法定义 ---

// 执行查询
async function performQuery() {
  if (isQueryButtonDisabled.value) return;

  isLoading.value = true;
  searchAttempted.value = true;
  searchResult.value = null;
  errorMessage.value = '';

  try {
    const response = await axios.get('/api/orders/', {
      params: {
        phone_number: queryPhoneNumber.value,
        order_number: queryOrderNumber.value,
      },
    });

    if (response.data && response.data.length > 0) {
      searchResult.value = response.data[0]; // API返回的是列表，我们取第一个
    } else {
      searchResult.value = null; // 未找到结果
    }
  } catch (error) {
    console.error('查询失败:', error);
    errorMessage.value = '查询请求失败，请稍后重试。';
  } finally {
    isLoading.value = false;
  }
}

// 格式化日期
function formatDateTime(isoString) {
  if (!isoString) return 'N/A';
  const date = new Date(isoString);
  return date.toLocaleString('zh-CN', {
    year: 'numeric', month: 'long', day: 'numeric',
    hour: '2-digit', minute: '2-digit', second: '2-digit'
  });
}
</script>

<template>
  <div class="query-container">
    <div class="query-card">
      <h2>订单状态查询</h2>
      <p class="subtitle">请输入您的手机号和订单号以获取最新状态。</p>

      <div class="query-form">
        <div class="input-group">
          <input type="tel" v-model.trim="queryPhoneNumber" placeholder="手机号" />
        </div>
        <div class="input-group">
          <input type="text" v-model.trim="queryOrderNumber" placeholder="订单号" />
        </div>
        <button @click="performQuery" :disabled="isQueryButtonDisabled">
          <span v-if="!isLoading">查询订单</span>
          <span v-else class="spinner"></span>
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
        <div><strong>订单号:</strong> {{ searchResult.order_number }}</div>
        <div><strong>手机号:</strong> {{ searchResult.phone_number }}</div>
        <div><strong>下单时间:</strong> {{ formatDateTime(searchResult.created_at) }}</div>
        <div>
          <strong>订单状态:</strong>
          <span class="status-badge" :class="statusInfo.class">{{ statusInfo.text }}</span>
        </div>
      </div>

      <hr />

      <h4>打印规格</h4>
      <ul class="spec-list">
        <li><strong>纸张大小:</strong> {{ searchResult.specifications.paper_size }}</li>
        <li><strong>色彩:</strong> {{ searchResult.specifications.color }}</li>
        <li><strong>单/双面:</strong> {{ searchResult.specifications.sided }}</li>
        <li><strong>份数:</strong> {{ searchResult.specifications.copies }}</li>
      </ul>

      <hr />

      <h4>文件列表</h4>
      <ul class="file-list">
        <li v-for="file in searchResult.files" :key="file.file">
          <a :href="file.file" target="_blank" rel="noopener noreferrer">
            {{ file.file.split('/').pop() }}
          </a>
        </li>
      </ul>
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
/* Google Fonts - 可选，提升字体美感 */
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;700&display=swap');

:root {
  --primary-color: #007bff;
  --primary-hover: #0056b3;
  --background-color: #f8f9fa;
  --card-background: #ffffff;
  --text-color: #333;
  --subtitle-color: #6c757d;
  --border-color: #dee2e6;
}

.query-container {
  font-family: 'Noto Sans SC', sans-serif;
  background-color: var(--background-color);
  padding: 2rem;
  max-width: 800px;
  margin: 2rem auto;
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
  align-items: center;
}

.input-group {
  flex-grow: 1;
}

input[type="tel"], input[type="text"] {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.2s, box-shadow 0.2s;
}

input:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.2);
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
}

button:hover:not(:disabled) {
  background-color: var(--primary-hover);
}

button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* 结果卡片样式 */
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
.spec-list, .file-list {
  list-style-type: none;
  padding-left: 0;
}
hr {
  border: none;
  border-top: 1px solid #eee;
  margin: 1.5rem 0;
}
h3, h4 { margin: 1.5rem 0 0.5rem 0; }

/* 状态徽章 */
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

/* 各种提示状态 */
.info-state, .error-state, .loading-state {
  text-align: center;
  color: var(--subtitle-color);
  padding: 3rem;
}
.error-state { color: #dc3545; font-weight: 500; }

/* 加载动画 Spinner */
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
  border-color: var(--primary-color-light);
  border-width: 4px;
}
@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
