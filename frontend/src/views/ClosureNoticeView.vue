<template>
  <div class="closure-notice-container">
    <!-- 主要内容 -->
    <div class="closure-notice-wrapper">
      <!-- 顶部系统维护提示 -->
      <div class="maintenance-banner">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="12" cy="12" r="10"></circle>
          <line x1="12" y1="8" x2="12" y2="12"></line>
          <line x1="12" y1="16" x2="12.01" y2="16"></line>
        </svg>
        <span>SYSTEM MAINTENANCE</span>
      </div>

      <!-- 主要内容卡片 -->
      <div class="content-card">
        <!-- 大图标 -->
        <div class="icon-wrapper">
          <svg xmlns="http://www.w3.org/2000/svg" width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round">
            <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
            <line x1="9" y1="9" x2="15" y2="15"></line>
            <line x1="15" y1="9" x2="9" y2="15"></line>
          </svg>
        </div>

        <!-- 标题 -->
        <h1 class="title">暂停营业</h1>

        <!-- 副标题/主要信息 -->
        <p class="subtitle">{{ closureReason }}</p>

        <!-- 重新营业时间（如果有） -->
        <div v-if="reopeningDate" class="reopening-section">
          <div class="reopening-label">
            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="10"></circle>
              <polyline points="12 6 12 12 16 14"></polyline>
            </svg>
            <span>预计恢复时间</span>
          </div>
          <p class="reopening-date">{{ formatDate(reopeningDate) }} 09:00</p>
        </div>

        <!-- 额外提示内容（如果有） -->
        <div v-if="noticeContent" class="notice-section">
          <p class="notice-text">{{ noticeContent }}</p>
        </div>

        <!-- 操作按钮 -->
        <div class="button-group">
          <button @click="refreshStatus" class="btn btn-primary">
            刷新状态
          </button>

          <button v-if="isAuthenticated && allowViewingHistory" @click="goToOrders" class="btn btn-secondary">
            查看历史订单
          </button>

          <button @click="logout" class="btn btn-text">
            退出登录
          </button>
        </div>

        <!-- 底部提示 -->
        <p class="footer-text">Printerify Service</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useUserStore } from '@/stores/user';
import axios from 'axios';

const router = useRouter();
const userStore = useUserStore();

// 系统配置
const closureReason = ref('放假暂停营业，感谢您的理解！');
const reopeningDate = ref(null);
const noticeContent = ref('');
const allowViewingHistory = ref(true);

// 计算属性
const isAuthenticated = computed(() => userStore.isAuthenticated);

onMounted(async () => {
  // 从后端获取系统配置
  try {
    const response = await axios.get('/api/system-config/');
    if (response.data) {
      closureReason.value = response.data.closure_reason || closureReason.value;
      reopeningDate.value = response.data.reopening_date;
      noticeContent.value = response.data.notice_content || '';
      allowViewingHistory.value = response.data.allow_viewing_history;
    }
  } catch (error) {
    console.error('获取系统配置失败:', error);
  }
});

// 格式化日期
const formatDate = (date) => {
  if (!date) return '';
  return new Date(date).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  });
};

// 刷新检查营业状态
const refreshStatus = async () => {
  try {
    const response = await axios.get('/api/system-config/');
    if (response.data && response.data.is_open) {
      // 营业已恢复，跳转到首页
      router.push('/');
    } else {
      // 仍然关闭，更新显示
      if (response.data) {
        closureReason.value = response.data.closure_reason || closureReason.value;
        reopeningDate.value = response.data.reopening_date;
        noticeContent.value = response.data.notice_content || '';
        allowViewingHistory.value = response.data.allow_viewing_history;
      }
      alert('仍在暂停营业中，请稍后再试。');
    }
  } catch (error) {
    console.error('检查营业状态失败:', error);
    alert('检查失败，请刷新页面重试。');
  }
};

// 查看历史订单
const goToOrders = () => {
  router.push('/profile');
};

// 登出
const logout = async () => {
  try {
    await userStore.logout();
    router.push('/');
  } catch (error) {
    console.error('登出失败:', error);
  }
};
</script>

<style scoped>
.closure-notice-container {
  width: 100%;
  min-height: 100vh;
  background: #f9fafb;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
}

.closure-notice-wrapper {
  width: 100%;
  max-width: 480px;
  animation: fadeInUp 0.8s cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 顶部维护提示 */
.maintenance-banner {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  color: #6b7280;
  font-size: 13px;
  margin-bottom: 32px;
  font-weight: 500;
  letter-spacing: 0.5px;
  text-transform: uppercase;
}

/* 主要内容卡片 */
.content-card {
  background: white;
  border-radius: 24px;
  padding: 56px 40px;
  text-align: center;
  box-shadow: 0 10px 40px -10px rgba(0, 0, 0, 0.05);
  border: 1px solid rgba(0, 0, 0, 0.02);
}

/* 大图标 */
.icon-wrapper {
  margin-bottom: 32px;
  display: flex;
  justify-content: center;
}

.icon-wrapper svg {
  width: 80px;
  height: 80px;
  color: #111827;
  opacity: 1;
  stroke-width: 1px;
}

/* 标题 */
.title {
  font-size: 28px;
  font-weight: 600;
  color: #111827;
  margin-bottom: 16px;
  letter-spacing: -0.5px;
  line-height: 1.2;
}

/* 副标题/主要信息 */
.subtitle {
  font-size: 15px;
  color: #6b7280;
  margin-bottom: 40px;
  line-height: 1.6;
  font-weight: 400;
}

/* 重新营业时间部分 */
.reopening-section {
  background: #f9fafb;
  border-radius: 16px;
  padding: 20px;
  margin-bottom: 32px;
  border: 1px solid #f3f4f6;
}

.reopening-label {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  color: #6b7280;
  font-size: 12px;
  margin-bottom: 8px;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.reopening-label svg {
  width: 14px;
  height: 14px;
  color: #111827;
}

.reopening-date {
  font-size: 16px;
  font-weight: 600;
  color: #111827;
  margin: 0;
  font-feature-settings: "tnum";
}

/* 通知部分 */
.notice-section {
  margin-bottom: 32px;
  padding: 16px;
  background: #fffbeb;
  border-radius: 12px;
  border: 1px solid #fcd34d;
}

.notice-text {
  color: #92400e;
  font-size: 14px;
  line-height: 1.6;
  margin: 0;
}

/* 按钮组 */
.button-group {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 32px;
}

.btn {
  padding: 14px 24px;
  border: none;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.2s ease;
  outline: none;
}

.btn:active {
  transform: scale(0.98);
}

.btn-primary {
  background: #111827;
  color: white;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.btn-primary:hover {
  background: #000000;
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.15);
}

.btn-secondary {
  background: white;
  color: #374151;
  border: 1px solid #e5e7eb;
}

.btn-secondary:hover {
  background: #f9fafb;
  border-color: #d1d5db;
  color: #111827;
}

.btn-text {
  background: transparent;
  color: #9ca3af;
  font-weight: 400;
  padding: 8px 0;
  font-size: 13px;
}

.btn-text:hover {
  color: #6b7280;
}

/* 底部文本 */
.footer-text {
  font-size: 12px;
  color: #9ca3af;
  margin: 0;
  padding-top: 24px;
  border-top: 1px solid #f3f4f6;
}

/* 响应式设计 */
@media (max-width: 640px) {
  .closure-notice-container {
    padding: 16px;
    background: white;
  }

  .content-card {
    padding: 40px 24px;
    box-shadow: none;
    border: none;
  }

  .icon-wrapper svg {
    width: 64px;
    height: 64px;
  }

  .title {
    font-size: 24px;
    margin-bottom: 12px;
  }

  .subtitle {
    font-size: 14px;
    margin-bottom: 32px;
  }

  .btn {
    padding: 12px 20px;
  }
}
</style>
