<template>
  <div class="closure-notice-container">
    <div class="content-wrapper">
      <div class="icon-wrapper">
        <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
          <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
          <line x1="9" y1="9" x2="15" y2="15"></line>
          <line x1="15" y1="9" x2="9" y2="15"></line>
        </svg>
      </div>
      
      <h1 class="notice-title">暂停营业中</h1>
      
      <p class="notice-message">
        {{ closureReason }}
      </p>

      <div v-if="reopeningDate" class="info-section">
        <div class="info-item">
          <span class="label">预计恢复时间</span>
          <span class="value">{{ formatDate(reopeningDate) }} 09:00</span>
        </div>
      </div>

      <div v-if="noticeContent" class="additional-notice">
        {{ noticeContent }}
      </div>

      <div class="action-buttons">
        <button @click="refreshStatus" class="btn-primary">
          刷新状态
        </button>
        
        <button @click="goHome" class="btn-secondary">
          返回首页
        </button>

        <button v-if="isAuthenticated && allowViewingHistory" @click="goToOrders" class="btn-secondary">
          查看历史订单
        </button>
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
      // 仍然关闭，更新显示，并给予用户反馈
      if (response.data) {
        closureReason.value = response.data.closure_reason || closureReason.value;
        reopeningDate.value = response.data.reopening_date;
        noticeContent.value = response.data.notice_content || '';
        allowViewingHistory.value = response.data.allow_viewing_history;
      }
      
      // 添加一个简单的视觉反馈动画或其他提示更好，这里先用alert
      // 考虑到整体风格，最好避免alert，但为了保持逻辑简单先保留
      // 或者我们可以添加一个短暂的状态显示
      const btn = document.querySelector('.btn-primary');
      if(btn) {
        const originalText = btn.innerText;
        btn.innerText = '状态未变';
        setTimeout(() => {
          btn.innerText = originalText;
        }, 2000);
      }
    }
  } catch (error) {
    console.error('检查营业状态失败:', error);
  }
};

const goHome = () => {
  router.push('/');
}

// 查看历史订单
const goToOrders = () => {
  router.push('/profile');
};
</script>

<style scoped>
.closure-notice-container {
  min-height: 70vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  text-align: center;
  background-color: var(--color-background);
}

.content-wrapper {
  max-width: 500px;
  width: 100%;
  animation: fadeIn 0.8s ease-out;
}

.icon-wrapper {
  margin-bottom: 2rem;
  color: var(--color-text-mute);
  opacity: 0.5;
}

.notice-title {
  font-size: 2rem;
  font-weight: 600;
  color: var(--color-heading);
  margin-bottom: 1.5rem;
  letter-spacing: -0.02em;
}

.notice-message {
  font-size: 1.1rem;
  color: var(--color-text);
  margin-bottom: 2.5rem;
  line-height: 1.6;
}

.info-section {
  margin-bottom: 2rem;
  padding: 1rem;
  background-color: var(--color-background-soft);
  border-radius: 8px;
  display: inline-block;
  min-width: 200px;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.label {
  font-size: 0.85rem;
  color: var(--color-text-mute);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.value {
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--color-heading);
}

.additional-notice {
  margin-bottom: 2.5rem;
  padding: 1rem;
  background-color: var(--color-background-mute);
  border-radius: 8px;
  color: var(--color-text);
  font-size: 0.95rem;
  line-height: 1.6;
}

.action-buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
}

.btn-primary {
  padding: 0.75rem 2rem;
  background-color: var(--color-heading);
  color: var(--color-background);
  border-radius: 4px;
  font-size: 0.95rem;
  font-weight: 500;
  transition: all 0.3s ease;
  border: 1px solid var(--color-heading);
  cursor: pointer;
  letter-spacing: 0.02em;
}

.btn-primary:hover {
  background-color: transparent;
  color: var(--color-heading);
  transform: translateY(-1px);
}

.btn-secondary {
  padding: 0.75rem 1rem;
  background-color: transparent;
  color: var(--color-text-mute);
  border: none;
  border-bottom: 1px solid transparent;
  font-size: 0.95rem;
  font-weight: 400;
  transition: all 0.3s ease;
  cursor: pointer;
}

.btn-secondary:hover {
  color: var(--color-heading);
  border-bottom-color: var(--color-heading);
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 640px) {
  .notice-title {
    font-size: 1.75rem;
  }
  
  .action-buttons {
    flex-direction: column;
    gap: 1rem;
  }

  .btn-primary, .btn-secondary {
    width: 100%;
  }
}
</style>
