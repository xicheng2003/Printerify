<script setup>
// --- 脚本部分无需任何修改，保持原样即可 ---
import { ref, computed } from 'vue';
// 【新增】从 vue-router 导入 useRouter
import { useRouter } from 'vue-router';
// 【新增】从 Pinia store 导入 useUserStore
import { useUserStore } from '@/stores/user';
import apiService from '@/services/apiService';


// 【新增】初始化 store 和 router
const userStore = useUserStore();
const router = useRouter();


// 【新增】创建一个计算属性来实时反映用户的登录状态
// 这样当 userStore.isAuthenticated 变化时，isUserLoggedIn 会自动更新
const isUserLoggedIn = computed(() => userStore.isAuthenticated);

// 【新增】一个用于导航到个人中心的函数
function goToDashboard() {
  router.push('/profile'); // 使用 router 进行程序化导航
}

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
    // 新端点返回单个订单对象
    searchResult.value = response.data || null;
  } catch (error) {
    console.error('查询失败:', error);
    // 展示更友好的后端提示（若有）
    errorMessage.value = error?.response?.data?.error || error.friendlyMessage || '查询请求失败，请检查输入或稍后重试。';
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

    <section class="hero-section">
      <h2 class="animated-hero-title">订单追踪，状态尽在掌握</h2>
      <p>Printerify，为每一次打印赋能。</p>
    </section>

    <div v-if="isUserLoggedIn" class="user-redirect-banner">
      <div class="banner-content">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="banner-icon"><path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>
        <div class="banner-text">
          <strong>您已登录</strong>
          <p>所有订单记录已同步至您的账户，可直接前往个人中心查看。</p>
        </div>
      </div>
      <button @click="goToDashboard" class="banner-action-btn">
        前往个人中心
      </button>
    </div>
    <div class="query-card">
      <h2>访客订单查询</h2>
      <p class="subtitle">如果您下单时处于未登录状态，可在此处输入手机号和取件码进行查询。</p>
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

.hero-section {
  text-align: center;
  padding: 2rem 0;
  margin-bottom: 2rem;
}

.hero-section h2 {
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--color-heading);
  margin-bottom: 0.5rem;
}

.hero-section p {
  font-size: 1.125rem;
  color: var(--color-text-mute);
}

/* --- Animated Title --- */
.animated-hero-title {
  --scroll-width: 400px;
  /* 请确保项目中已引入 'Inter' 字体，否则将回退至 sans-serif */
  font-family: 'Inter', sans-serif;
  font-weight: 800;
  font-size: 3.2rem;
  text-align: center;
  letter-spacing: -1.5px;
  background: linear-gradient(
    100deg,
    #666666, #b2b2b2, #ffffff, #b2b2b2, #666666
  );
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  background-repeat: repeat-x;
  background-size: var(--scroll-width) 100%;
  animation: seamless-scroll 5s linear infinite;
  text-shadow:
    0px 1px 1px rgba(255, 255, 255, 0.1),
    0 0 10px rgba(192, 219, 255, 0.2),
    0 0 30px rgba(192, 219, 255, 0.1),
    0px -1px 1px rgba(0, 0, 0, 0.4);
}

/* 亮色模式下的专属样式 */
html:not(.dark) .animated-hero-title {
  --scroll-width: 300px;
  background: linear-gradient(
    100deg,
    #333333, #aeaeae, #232323, #aeaeae, #333333
  );
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  background-repeat: repeat-x;
  background-size: var(--scroll-width) 100%;
  text-shadow:
    0px 1px 1px rgba(255, 255, 255, 0.5),
    0px -1px 1px rgba(0, 0, 0, 0.1);
}

@keyframes seamless-scroll {
  from {
    background-position: 0 0;
  }
  to {
    background-position: calc(-1 * var(--scroll-width)) 0;
  }
}

/* --- 响应式调整 --- */
@media (max-width: 767px) {
  .hero-section h2 { font-size: 2rem; }
  .hero-section p { font-size: 1rem; }
  .animated-hero-title {
    font-size: 2.6rem;
    letter-spacing: -1px;
  }
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

.user-redirect-banner {
  background-color: var(--color-background-soft);
  border: 1px solid var(--color-border);
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1.5rem;
  box-shadow: var(--shadow-card);
}

.user-redirect-banner .banner-content {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.user-redirect-banner .banner-icon {
  color: var(--color-primary);
  flex-shrink: 0;
}

.user-redirect-banner .banner-text strong {
  display: block;
  font-weight: 600;
  font-size: 1.1rem;
  color: var(--color-heading);
  margin-bottom: 0.25rem;
}

.user-redirect-banner .banner-text p {
  margin: 0;
  font-size: 0.9rem;
  color: var(--color-text-mute);
}

.user-redirect-banner .banner-action-btn {
  white-space: nowrap;
  padding: 0.6rem 1.25rem;
  border: none;
  background-color: var(--color-primary);
  color: var(--color-text-on-primary);
  border-radius: 8px;
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s, transform 0.2s;
  text-decoration: none;
}

.user-redirect-banner .banner-action-btn:hover {
  background-color: var(--color-primary-hover);
  transform: translateY(-2px);
}

@media (max-width: 639px) {
  .user-redirect-banner {
    flex-direction: column;
    align-items: stretch;
    text-align: center;
    gap: 1.25rem;
  }
  .user-redirect-banner .banner-content {
    flex-direction: column;
    gap: 0.75rem;
  }
}

/* ▼▼▼ 在 style 标签末尾新增以下所有样式 ▼▼▼ */

/* 第 1 部分：设定 query-card 内部内容的“永久”样式 */
/* 这些规则将始终生效，确保了排版布局的一致性 */
.query-card h2 {
  text-align: left;
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--color-heading);
  margin-top: 0;
  margin-bottom: 0.25rem;
}

.query-card .subtitle {
  text-align: left;
  font-size: 0.9rem;
  margin-bottom: 1.5rem;
}

/* 第 2 部分：设定登录后的“条件弱化”样式 */
/* 这个规则只在用户登录时生效，且只改变容器外观，不影响内部排版 */
.user-redirect-banner + .query-card {
  background-color: transparent;
  box-shadow: none;
  border: 2px dashed var(--color-border);
  padding: 1.5rem; /* 调整内边距以适应虚线框 */
}
/* ▲▲▲ 新增样式结束 ▲▲▲ */


</style>
