<template>
  <div class="oauth-binding-manager">
    <h3 class="binding-title">OAuth账户管理</h3>
    
    <!-- 绑定状态显示 -->
    <div class="binding-status">
      <div class="status-item">
        <div class="status-icon">
          <svg v-if="bindings.github_id" class="w-5 h-5 text-green-500" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
          </svg>
          <svg v-else class="w-5 h-5 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-11a1 1 0 10-2 0v2H7a1 1 0 100 2h2v2a1 1 0 102 0v-2h2a1 1 0 100-2h-2V7z" clip-rule="evenodd"></path>
          </svg>
        </div>
        <div class="status-info">
          <span class="status-label">GitHub</span>
          <span v-if="bindings.github_id" class="status-text text-green-600">已绑定</span>
          <span v-else class="status-text text-gray-500">未绑定</span>
        </div>
        <div class="status-actions">
          <button
            v-if="!bindings.github_id"
            @click="bindGitHub"
            class="bind-btn github-btn"
            :disabled="loading"
          >
            <svg class="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
              <path d="M10 0C4.477 0 0 4.484 0 10.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0110 4.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.203 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.942.359.31.678.921.678 1.856 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0020 10.017C20 4.484 15.522 0 10 0z"></path>
            </svg>
            绑定GitHub
          </button>
          <button
            v-else
            @click="unbindAccount('github')"
            class="unbind-btn"
            :disabled="loading"
          >
            解绑
          </button>
        </div>
      </div>
      
      <div class="status-item">
        <div class="status-icon">
          <svg v-if="bindings.google_id" class="w-5 h-5 text-green-500" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
          </svg>
          <svg v-else class="w-5 h-5 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-11a1 1 0 10-2 0v2H7a1 1 0 100 2h2v2a1 1 0 102 0v-2h2a1 1 0 100-2h-2V7z" clip-rule="evenodd"></path>
          </svg>
        </div>
        <div class="status-info">
          <span class="status-label">Google</span>
          <span v-if="bindings.google_id" class="status-text text-green-600">已绑定</span>
          <span v-else class="status-text text-gray-500">未绑定</span>
        </div>
        <div class="status-actions">
          <button
            v-if="!bindings.google_id"
            @click="bindGoogle"
            class="bind-btn google-btn"
            :disabled="loading"
          >
            <svg class="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
              <path d="M15.545 12.045a3.5 3.5 0 01-3.5 3.5h-8a3.5 3.5 0 01-3.5-3.5v-8a3.5 3.5 0 013.5-3.5h8a3.5 3.5 0 013.5 3.5v8z"></path>
            </svg>
            绑定Google
          </button>
          <button
            v-else
            @click="unbindAccount('google')"
            class="unbind-btn"
            :disabled="loading"
          >
            解绑
          </button>
        </div>
      </div>
    </div>
    
    <!-- 绑定详情 -->
    <div v-if="bindings.bindings && bindings.bindings.length > 0" class="binding-details">
      <h4 class="details-title">绑定详情</h4>
      <div class="details-list">
        <div
          v-for="binding in bindings.bindings"
          :key="`${binding.provider}-${binding.uid}`"
          class="detail-item"
        >
          <div class="detail-info">
            <span class="detail-provider">{{ getProviderName(binding.provider) }}</span>
            <span class="detail-uid">ID: {{ binding.uid }}</span>
            <span class="detail-date">绑定时间: {{ formatDate(binding.date_joined) }}</span>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 提示信息 -->
    <div class="binding-tips">
      <p class="tip-text">
        💡 绑定OAuth账户后，您可以使用多种方式登录，无需记住额外密码。
      </p>
      <p class="tip-text">
        🔒 您的账户信息由OAuth提供商安全保护，我们不会获取您的密码。
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
const loading = ref(false)
const bindings = ref({
  github_id: null,
  google_id: null,
  can_bind_github: true,
  can_bind_google: true,
  bindings: []
})

// 获取绑定状态
const fetchBindings = async () => {
  try {
    const response = await fetch('/api/oauth/bindings/', {
      credentials: 'include'
    })
    
    if (response.ok) {
      const data = await response.json()
      bindings.value = data
    }
  } catch (error) {
    console.error('获取OAuth绑定状态失败:', error)
  }
}

// 绑定GitHub
const bindGitHub = () => {
  window.location.href = '/api/oauth/github/'
}

// 绑定Google
const bindGoogle = () => {
  window.location.href = '/api/oauth/google/'
}

// 解绑账户
const unbindAccount = async (provider) => {
  if (!confirm(`确定要解绑${getProviderName(provider)}账户吗？`)) {
    return
  }
  
  loading.value = true
  try {
    const response = await fetch(`/api/oauth/bindings/${provider}/`, {
      method: 'DELETE',
      credentials: 'include'
    })
    
    if (response.ok) {
      // 刷新绑定状态
      await fetchBindings()
      // 刷新用户信息
      await userStore.fetchUserInfo()
    } else {
      const error = await response.json()
      alert(`解绑失败: ${error.error || '未知错误'}`)
    }
  } catch (error) {
    console.error('解绑失败:', error)
    alert('解绑失败，请稍后重试')
  } finally {
    loading.value = false
  }
}

// 获取提供商名称
const getProviderName = (provider) => {
  const names = {
    github: 'GitHub',
    google: 'Google'
  }
  return names[provider] || provider
}

// 格式化日期
const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

onMounted(() => {
  fetchBindings()
})
</script>

<style scoped>
.oauth-binding-manager {
  @apply bg-white dark:bg-gray-800 rounded-lg shadow-md p-6;
}

.binding-title {
  @apply text-xl font-semibold text-gray-900 dark:text-white mb-6;
}

.binding-status {
  @apply space-y-4 mb-6;
}

.status-item {
  @apply flex items-center justify-between p-4 border border-gray-200 dark:border-gray-700 rounded-lg;
}

.status-icon {
  @apply mr-4;
}

.status-info {
  @apply flex-1;
}

.status-label {
  @apply block font-medium text-gray-900 dark:text-white;
}

.status-text {
  @apply block text-sm;
}

.status-actions {
  @apply ml-4;
}

.bind-btn {
  @apply inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white transition-colors duration-200;
}

.github-btn {
  @apply bg-gray-900 hover:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500;
}

.google-btn {
  @apply bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500;
}

.unbind-btn {
  @apply inline-flex items-center px-4 py-2 border border-red-300 text-sm font-medium rounded-md text-red-700 bg-white hover:bg-red-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 transition-colors duration-200;
}

.binding-details {
  @apply mt-6 p-4 bg-gray-50 dark:bg-gray-700 rounded-lg;
}

.details-title {
  @apply text-lg font-medium text-gray-900 dark:text-white mb-3;
}

.details-list {
  @apply space-y-2;
}

.detail-item {
  @apply p-3 bg-white dark:bg-gray-600 rounded border border-gray-200 dark:border-gray-600;
}

.detail-info {
  @apply flex flex-col space-y-1;
}

.detail-provider {
  @apply font-medium text-gray-900 dark:text-white;
}

.detail-uid {
  @apply text-sm text-gray-600 dark:text-gray-300;
}

.detail-date {
  @apply text-sm text-gray-500 dark:text-gray-400;
}

.binding-tips {
  @apply mt-6 p-4 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg;
}

.tip-text {
  @apply text-sm text-blue-800 dark:text-blue-200 mb-2 last:mb-0;
}

/* 禁用状态 */
.bind-btn:disabled,
.unbind-btn:disabled {
  @apply opacity-50 cursor-not-allowed;
}

/* 响应式设计 */
@media (max-width: 640px) {
  .status-item {
    @apply flex-col items-start space-y-3;
  }
  
  .status-actions {
    @apply ml-0 w-full;
  }
  
  .bind-btn,
  .unbind-btn {
    @apply w-full justify-center;
  }
}
</style>
