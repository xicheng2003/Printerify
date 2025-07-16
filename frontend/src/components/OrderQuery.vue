<script setup>
import { ref, computed } from 'vue';
import axios from 'axios';

const queryPhoneNumber = ref('');
const queryPickupCode = ref('');
const isLoading = ref(false);
const searchResult = ref(null);
const searchAttempted = ref(false);
const errorMessage = ref('');

// 【恢复】恢复您原来的禁用逻辑：必须同时输入两者
const isQueryButtonDisabled = computed(() => {
  return !queryPhoneNumber.value || !queryPickupCode.value || isLoading.value;
});

// 【修改】状态的key值与我们新模型保持一致
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
    // 【修改】现在我们只根据取件码查询，因为它是唯一的
    // 但后端逻辑会同时验证手机号，保证安全
    const response = await axios.get('/api/orders/', {
      params: {
        phone: queryPhoneNumber.value,
        code: queryPickupCode.value,
      },
      withCredentials: true,
    });

    if (response.data && response.data.length > 0) {
      // 假设API返回一个数组，我们只取第一个，因为手机号和取件码组合应该是唯一的
      const orderId = response.data[0].id;
      // 请求详情接口以获取完整的 group 和 document 数据
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
/* 将 @import 移到最前面 */
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;700&display=swap');

/* --- 【新增】为新的卡片式布局添加样式 --- */
.result-group-card {
  border: 1px solid var(--border-color, #dee2e6);
  border-radius: 12px; /* 与您的 query-card 保持一致 */
  margin-top: 1.5rem;
  background-color: var(--card-background, #ffffff);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03); /* 柔和的阴影 */
  overflow: hidden; /* 防止内部元素溢出圆角 */
}
.group-header {
  display: flex;
  justify-content: space-between;
  padding: 0.75rem 1.25rem;
  background-color: var(--background-color, #f8f9fa); /* 复用背景色 */
  border-bottom: 1px solid var(--border-color, #dee2e6);
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
  background-color: var(--background-color, #f8f9fa);
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
.file-name {
  font-weight: 500;
  color: var(--text-color, #333);
  margin: 0 0 0.25rem 0;
}
.file-specs {
  display: flex;
  gap: 1rem;
  font-size: 0.85rem;
  color: var(--subtitle-color, #6c757d);
}
.view-file-link {
  font-size: 0.9em;
  text-decoration: none;
  color: var(--primary-color, #007bff);
  font-weight: 500;
  padding: 0.4rem 0.8rem;
  border-radius: 6px;
  background-color: transparent;
  border: 1px solid transparent;
  transition: background-color 0.2s, border-color 0.2s;
}
.view-file-link:hover {
  background-color: var(--primary-color-light, rgba(0, 123, 255, 0.1));
  border-color: var(--primary-color-light, rgba(0, 123, 255, 0.2));
}


:root {
  --primary-color: #007bff;
  --primary-hover: #0056b3;
  --primary-color-light: rgba(0, 123, 255, 0.2);
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
/* ... etc. (所有您之前的CSS代码都复制到这里) ... */
</style>
