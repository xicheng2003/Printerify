<template>
  <div class="closure-notice-container">
    <!-- 暂停营业提示页面 -->
    <div class="closure-notice-wrapper">
      <!-- 背景装饰 -->
      <div class="closure-background">
        <div class="decoration-circle decoration-circle-1"></div>
        <div class="decoration-circle decoration-circle-2"></div>
      </div>

      <!-- 主要内容 -->
      <div class="closure-content">
        <!-- 关闭图标 -->
        <div class="closure-icon">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="80"
            height="80"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="1.5"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="8" y1="12" x2="16" y2="12"></line>
          </svg>
        </div>

        <!-- 标题 -->
        <h1 class="closure-title">暂停营业中</h1>

        <!-- 主要提示 -->
        <p class="closure-main-text">{{ closureReason }}</p>

        <!-- 重新营业时间（如果有） -->
        <div v-if="reopeningDate" class="reopening-info">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="20"
            height="20"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <circle cx="12" cy="12" r="10"></circle>
            <polyline points="12,6 12,12 16,14"></polyline>
          </svg>
          <span>预计 <strong>{{ formatDate(reopeningDate) }}</strong> 恢复营业</span>
        </div>

        <!-- 额外提示内容（如果有） -->
        <div v-if="noticeContent" class="notice-box">
          <div class="notice-title">📢 其他提示</div>
          <div class="notice-body">{{ noticeContent }}</div>
        </div>

        <!-- 可执行的操作 -->
        <div class="action-buttons">
          <!-- 查看历史订单按钮（仅对已登录用户） -->
          <button
            v-if="isAuthenticated && allowViewingHistory"
            @click="goToOrders"
            class="btn btn-secondary"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="18"
              height="18"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"></path>
              <polyline points="17,21 17,13 7,13 7,21"></polyline>
              <polyline points="7,3 7,8 15,8"></polyline>
            </svg>
            查看历史订单
          </button>

          <!-- 刷新页面按钮（检查是否恢复营业） -->
          <button @click="refreshStatus" class="btn btn-primary">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="18"
              height="18"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <polyline points="23 4 23 10 17 10"></polyline>
              <polyline points="1 20 1 14 7 14"></polyline>
              <path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"></path>
            </svg>
            刷新检查营业状态
          </button>

          <!-- 登出按钮（仅对已登录用户） -->
          <button
            v-if="isAuthenticated"
            @click="logout"
            class="btn btn-text"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="18"
              height="18"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
              <polyline points="16 17 21 12 16 7"></polyline>
              <line x1="21" y1="12" x2="9" y2="12"></line>
            </svg>
            登出账号
          </button>
        </div>

        <!-- 底部提示 -->
        <div class="closure-footer">
          <p>感谢您的理解与支持！我们很快将回来为您服务。</p>
          <p class="footer-contact">如有紧急事项，请通过其他渠道联系我们</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useUserStore } from '@/stores/user';
import apiService from '@/services/apiService';

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
    const response = await apiService.get('/system-config/');
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
    const response = await apiService.get('/system-config/');
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
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  position: relative;
  overflow: hidden;
}

.closure-notice-wrapper {
  position: relative;
  width: 100%;
  max-width: 600px;
  z-index: 1;
}

/* 背景装饰 */
.closure-background {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
  overflow: hidden;
}

.decoration-circle {
  position: absolute;
  border-radius: 50%;
  opacity: 0.1;
}

.decoration-circle-1 {
  width: 300px;
  height: 300px;
  background: white;
  top: -50px;
  right: -50px;
}

.decoration-circle-2 {
  width: 200px;
  height: 200px;
  background: white;
  bottom: -30px;
  left: -30px;
}

/* 主要内容 */
.closure-content {
  background: white;
  border-radius: 16px;
  padding: 60px 40px;
  text-align: center;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  animation: slideUp 0.6s ease-out;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 关闭图标 */
.closure-icon {
  color: #667eea;
  margin-bottom: 20px;
  animation: pulse 2s ease-in-out infinite;
}

.closure-icon svg {
  width: 80px;
  height: 80px;
}

@keyframes pulse {
  0%,
  100% {
    opacity: 1;
    transform: scale(1);
  }
  50% {
    opacity: 0.7;
    transform: scale(1.05);
  }
}

/* 标题 */
.closure-title {
  font-size: 36px;
  font-weight: 700;
  color: #333;
  margin-bottom: 16px;
  letter-spacing: -0.5px;
}

/* 主要提示文本 */
.closure-main-text {
  font-size: 18px;
  color: #666;
  margin-bottom: 20px;
  line-height: 1.6;
}

/* 重新营业信息 */
.reopening-info {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 16px;
  background: #f0f4ff;
  border-radius: 8px;
  margin-bottom: 24px;
  color: #667eea;
  font-size: 16px;
}

.reopening-info svg {
  color: #667eea;
  flex-shrink: 0;
}

.reopening-info strong {
  color: #333;
  font-weight: 600;
}

/* 通知框 */
.notice-box {
  background: #fff3cd;
  border-left: 4px solid #ffc107;
  padding: 16px;
  border-radius: 8px;
  margin-bottom: 24px;
  text-align: left;
}

.notice-title {
  font-weight: 600;
  color: #856404;
  margin-bottom: 8px;
  font-size: 14px;
}

.notice-body {
  color: #856404;
  font-size: 14px;
  line-height: 1.5;
}

/* 操作按钮 */
.action-buttons {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 24px;
}

.btn {
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.3s ease;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
}

.btn-secondary {
  background: #f0f4ff;
  color: #667eea;
  border: 2px solid #667eea;
}

.btn-secondary:hover {
  background: #e8ecff;
  transform: translateY(-2px);
}

.btn-text {
  background: transparent;
  color: #999;
  font-weight: 500;
}

.btn-text:hover {
  color: #666;
}

/* 底部提示 */
.closure-footer {
  padding-top: 24px;
  border-top: 1px solid #eee;
  color: #999;
  font-size: 14px;
}

.closure-footer p {
  margin: 8px 0;
  line-height: 1.5;
}

.footer-contact {
  font-size: 12px;
  color: #ccc;
}

/* 响应式设计 */
@media (max-width: 640px) {
  .closure-content {
    padding: 40px 24px;
  }

  .closure-title {
    font-size: 28px;
  }

  .closure-main-text {
    font-size: 16px;
  }

  .reopening-info {
    flex-direction: column;
    gap: 8px;
  }

  .notice-box {
    padding: 12px;
  }

  .btn {
    padding: 10px 16px;
    font-size: 14px;
  }
}
</style>
