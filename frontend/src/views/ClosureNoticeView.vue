<template>
  <div class="closure-notice-container">
    <!-- 主要内容 -->
    <div class="closure-notice-wrapper">
      <!-- 顶部系统维护提示 -->
      <div class="maintenance-banner">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2m0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8m.31-8.86c-1.52-.73-2.31-1.5-2.31-2.39 0-.87.6-1.41 1.54-1.41.84 0 1.54.5 2.17 1.35l1.19-1.05c-.74-1.19-1.77-1.9-3.35-1.9-2.15 0-3.72 1.42-3.72 3.12 0 1.659.985 2.99 2.737 3.69l.56.3c1.52.73 2.31 1.5 2.31 2.39 0 .87-.6 1.41-1.54 1.41-1.01 0-1.54-.5-2.17-1.35l-1.19 1.05c.74 1.19 1.77 1.9 3.35 1.9 2.15 0 3.72-1.42 3.72-3.12 0-1.659-.985-2.99-2.737-3.69l-.56-.3z"></path>
        </svg>
        <span>系统维护中</span>
      </div>

      <!-- 主要内容卡片 -->
      <div class="content-card">
        <!-- 大图标 -->
        <div class="icon-wrapper">
          <svg xmlns="http://www.w3.org/2000/svg" width="120" height="120" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="0.5" stroke-linecap="round" stroke-linejoin="round">
            <!-- 购物车关闭标志 -->
            <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path>
            <circle cx="9" cy="21" r="1"></circle>
            <circle cx="20" cy="21" r="1"></circle>
            <!-- 关闭符号 -->
            <line x1="3" y1="3" x2="21" y2="21" stroke-width="2"></line>
          </svg>
        </div>

        <!-- 标题 -->
        <h1 class="title">暂停营业中</h1>

        <!-- 副标题/主要信息 -->
        <p class="subtitle">{{ closureReason }}</p>

        <!-- 重新营业时间（如果有） -->
        <div v-if="reopeningDate" class="reopening-section">
          <div class="reopening-label">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
              <circle cx="12" cy="12" r="1"></circle>
              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm.31-8.86c-1.52-.73-2.31-1.5-2.31-2.39 0-.87.6-1.41 1.54-1.41.84 0 1.54.5 2.17 1.35l1.19-1.05c-.74-1.19-1.77-1.9-3.35-1.9-2.15 0-3.72 1.42-3.72 3.12 0 1.659.985 2.99 2.737 3.69l.56.3c1.52.73 2.31 1.5 2.31 2.39 0 .87-.6 1.41-1.54 1.41-1.01 0-1.54-.5-2.17-1.35l-1.19 1.05c.74 1.19 1.77 1.9 3.35 1.9 2.15 0 3.72-1.42 3.72-3.12 0-1.659-.985-2.99-2.737-3.69l-.56-.3z"></path>
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
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8"></path>
              <path d="M21 3v5h-5"></path>
              <path d="M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16"></path>
              <path d="M3 21v-5h5"></path>
            </svg>
            刷新检查营业状态
          </button>

          <button v-if="isAuthenticated && allowViewingHistory" @click="goToOrders" class="btn btn-secondary">
            查看历史订单
          </button>

          <button @click="logout" class="btn btn-text">
            登出
          </button>
        </div>

        <!-- 底部提示 -->
        <p class="footer-text">感谢您的理解与支持！我们很快回来为您服务。</p>
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
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
}

.closure-notice-wrapper {
  width: 100%;
  max-width: 500px;
  animation: fadeInUp 0.6s ease-out;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
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
  color: rgba(255, 255, 255, 0.8);
  font-size: 14px;
  margin-bottom: 24px;
  font-weight: 500;
}

/* 主要内容卡片 */
.content-card {
  background: white;
  border-radius: 20px;
  padding: 48px 32px;
  text-align: center;
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.15);
}

/* 大图标 */
.icon-wrapper {
  margin-bottom: 24px;
  display: flex;
  justify-content: center;
}

.icon-wrapper svg {
  width: 120px;
  height: 120px;
  color: #818cf8;
  opacity: 0.8;
}

/* 标题 */
.title {
  font-size: 32px;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 12px;
  letter-spacing: -0.3px;
}

/* 副标题/主要信息 */
.subtitle {
  font-size: 16px;
  color: #6b7280;
  margin-bottom: 28px;
  line-height: 1.6;
}

/* 重新营业时间部分 */
.reopening-section {
  background: #f3f4f6;
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 24px;
}

.reopening-label {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  color: #6b7280;
  font-size: 13px;
  margin-bottom: 8px;
  font-weight: 500;
}

.reopening-label svg {
  width: 16px;
  height: 16px;
  color: #818cf8;
}

.reopening-date {
  font-size: 18px;
  font-weight: 600;
  color: #1f2937;
  margin: 0;
}

/* 通知部分 */
.notice-section {
  margin-bottom: 28px;
  padding: 16px;
  background: #fef3c7;
  border-radius: 8px;
}

.notice-text {
  color: #78350f;
  font-size: 14px;
  line-height: 1.6;
  margin: 0;
}

/* 按钮组 */
.button-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 24px;
}

.btn {
  padding: 12px 24px;
  border: none;
  border-radius: 10px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.3s ease;
  outline: none;
}

.btn:active {
  transform: scale(0.98);
}

.btn-primary {
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
  color: white;
  box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(99, 102, 241, 0.4);
}

.btn-secondary {
  background: #f3f4f6;
  color: #4b5563;
  border: 1px solid #e5e7eb;
}

.btn-secondary:hover {
  background: #e5e7eb;
  color: #1f2937;
}

.btn-text {
  background: transparent;
  color: #9ca3af;
  font-weight: 500;
  padding: 8px 0;
}

.btn-text:hover {
  color: #6b7280;
}

/* 底部文本 */
.footer-text {
  font-size: 13px;
  color: #9ca3af;
  margin: 0;
  border-top: 1px solid #e5e7eb;
  padding-top: 20px;
}

/* 响应式设计 */
@media (max-width: 640px) {
  .closure-notice-container {
    padding: 16px;
  }

  .content-card {
    padding: 32px 24px;
  }

  .icon-wrapper svg {
    width: 100px;
    height: 100px;
  }

  .title {
    font-size: 28px;
    margin-bottom: 10px;
  }

  .subtitle {
    font-size: 15px;
    margin-bottom: 20px;
  }

  .btn {
    padding: 11px 20px;
    font-size: 14px;
    gap: 6px;
  }
}
</style>
