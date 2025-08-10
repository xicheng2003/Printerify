<template>
  <div class="oauth-binding-manager rounded-xl border border-[var(--color-border)] bg-[var(--color-background-soft)] p-6 shadow-sm transition-colors duration-300 md:p-8">

    <h3 class="text-xl font-bold text-[var(--color-heading)] md:text-2xl">
      第三方账户绑定
    </h3>
    <p class="mb-6 text-sm text-[var(--color-text-mute)]">
      绑定后，您可以使用第三方账户快速登录，无需记住密码。
    </p>

    <div class="space-y-4">
      <div class="flex flex-col items-start gap-4 rounded-lg border border-[var(--color-border)] bg-[var(--color-background)] p-4 transition-all duration-300 hover:border-[var(--color-primary)] hover:shadow-md sm:flex-row sm:items-center">
        <div class="flex flex-1 items-center gap-4">
          <svg class="h-8 w-8 text-[var(--color-heading)]" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
            <path fill-rule="evenodd" d="M12 2C6.477 2 2 6.477 2 12c0 4.418 2.865 8.165 6.839 9.492.5.092.682-.217.682-.483 0-.237-.009-.868-.014-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.203 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.942.359.31.678.921.678 1.856 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" clip-rule="evenodd"></path>
          </svg>
          <div>
            <p class="font-semibold text-[var(--color-heading)]">GitHub</p>
            <span v-if="bindings.github_id" class="inline-flex items-center rounded-full bg-[var(--color-success)]/10 px-2 py-1 text-xs font-medium text-[var(--color-success)]">已绑定</span>
            <span v-else class="inline-flex items-center rounded-full bg-[var(--color-background-mute)] px-2 py-1 text-xs font-medium text-[var(--color-text-mute)]">未绑定</span>
          </div>
        </div>
        <div class="w-full sm:w-auto">
          <BaseButton v-if="!bindings.github_id" @click="bindGitHub" :loading="loading" :disabled="loading">
            立即绑定
          </BaseButton>
          <button v-else @click="promptUnbind('github')" :disabled="loading" class="unbind-button">
            解除绑定
          </button>
        </div>
      </div>

      <div class="flex flex-col items-start gap-4 rounded-lg border border-[var(--color-border)] bg-[var(--color-background)] p-4 transition-all duration-300 hover:border-[var(--color-primary)] hover:shadow-md sm:flex-row sm:items-center">
        <div class="flex flex-1 items-center gap-4">
          <svg class="h-8 w-8" viewBox="0 0 48 48" aria-hidden="true">
            <path fill="#4285F4" d="M45.12 24.5c0-1.56-.14-3.06-.4-4.5H24v8.51h11.84c-.51 2.75-2.06 5.08-4.39 6.64v5.52h7.11c4.16-3.83 6.56-9.47 6.56-16.17z"></path><path fill="#34A853" d="M24 46c5.94 0 10.92-1.96 14.56-5.3l-7.11-5.52c-1.96 1.32-4.48 2.1-7.45 2.1-5.73 0-10.58-3.87-12.31-9.07H4.5v5.7C8.14 40.73 15.58 46 24 46z"></path><path fill="#FBBC05" d="M11.69 28.18C11.25 26.86 11 25.45 11 24s.25-2.86.69-4.18v-5.7H4.5C2.82 17.45 2 20.58 2 24s.82 6.55 2.5 9.88l7.19-5.7z"></path><path fill="#EA4335" d="M24 10.75c3.23 0 6.13 1.11 8.41 3.29l6.31-6.31C34.91 4.18 29.93 2 24 2 15.58 2 8.14 7.27 4.5 14.12l7.19 5.7c1.73-5.2 6.58-9.07 12.31-9.07z"></path>
          </svg>
          <div>
            <p class="font-semibold text-[var(--color-heading)]">Google</p>
            <span v-if="bindings.google_id" class="inline-flex items-center rounded-full bg-[var(--color-success)]/10 px-2 py-1 text-xs font-medium text-[var(--color-success)]">已绑定</span>
            <span v-else class="inline-flex items-center rounded-full bg-[var(--color-background-mute)] px-2 py-1 text-xs font-medium text-[var(--color-text-mute)]">未绑定</span>
          </div>
        </div>
        <div class="w-full sm:w-auto">
           <BaseButton v-if="!bindings.google_id" @click="bindGoogle" :loading="loading" :disabled="loading">
            立即绑定
          </BaseButton>
           <button v-else @click="promptUnbind('google')" :disabled="loading" class="unbind-button">
            解除绑定
          </button>
        </div>
      </div>
    </div>

    <div v-if="bindings.bindings && bindings.bindings.length > 0" class="mt-8">
      <h4 class="mb-4 text-lg font-bold text-[var(--color-heading)]">绑定记录</h4>
      <div class="space-y-3 rounded-lg border border-[var(--color-border)] bg-[var(--color-background)] p-4">
        <div v-for="binding in bindings.bindings" :key="`${binding.provider}-${binding.uid}`" class="flex flex-col rounded-md p-3 transition-colors duration-300 hover:bg-[var(--color-background-mute)] md:flex-row md:items-center md:justify-between">
          <div class="flex items-center gap-3">
            <span class="font-semibold text-[var(--color-heading)]">{{ getProviderName(binding.provider) }}</span>
            <span class="text-xs text-[var(--color-text-mute)]">ID: {{ binding.uid }}</span>
          </div>
          <span class="mt-1 text-xs text-[var(--color-text-mute)] md:mt-0">
            绑定于 {{ formatDate(binding.date_joined) }}
          </span>
        </div>
      </div>
    </div>

    <div class="mt-8 rounded-lg bg-[var(--color-background-mute)]/50 p-4">
      <p class="text-sm text-[var(--color-text-mute)]">
        💡 您的账户信息由 OAuth 提供商安全保护，我们不会获取或存储您的密码。
      </p>
    </div>

  </div>

  <Modal :show="showConfirmModal" @close="showConfirmModal = false">
    <template #header>
      <h3 class="text-lg font-semibold text-[var(--color-heading)]">确认解绑</h3>
    </template>
    <template #body>
      <p class="text-[var(--color-text)]">
        您确定要解绑您的 {{ getProviderName(providerToUnbind) }} 账户吗？
      </p>
      <p class="mt-2 text-sm text-[var(--color-text-mute)]">
        解绑后，您将无法再使用此账户进行登录。此操作不可撤销。
      </p>
    </template>
    <template #footer>
      <div class="flex justify-end gap-3">
        <button @click="showConfirmModal = false" class="rounded-lg border border-[var(--color-border)] bg-transparent px-4 py-2 font-semibold text-[var(--color-text)] transition-colors hover:bg-[var(--color-background-mute)]">
          取消
        </button>
        <button @click="handleConfirmUnbind" :disabled="loading" class="flex items-center justify-center rounded-lg border border-transparent bg-[var(--color-danger)] px-4 py-2 font-semibold text-white transition-colors hover:bg-[var(--color-danger-hover)] disabled:opacity-50">
          <div v-if="loading" class="mr-2 h-4 w-4 animate-spin rounded-full border-2 border-white/30 border-t-white"></div>
          确认解绑
        </button>
      </div>
    </template>
  </Modal>

</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import apiService from '@/services/apiService'
// 【新增】导入所需组件
import BaseButton from '@/components/BaseButton.vue'
import Modal from '@/components/Modal.vue'

// --- State ---
const userStore = useUserStore()
const loading = ref(false)
const bindings = ref({
  github_id: null,
  google_id: null,
  can_bind_github: true,
  can_bind_google: true,
  bindings: []
})
// 【新增】模态框控制状态
const showConfirmModal = ref(false)
const providerToUnbind = ref(null)

// --- Methods ---

// 获取绑定状态
const fetchBindings = async () => {
  try {
    const response = await apiService.getOAuthBindings()
    bindings.value = response.data
  } catch (error) {
    console.error('获取OAuth绑定状态失败:', error)
  }
}

// 绑定GitHub
const bindGitHub = async () => {
  if (!userStore.isAuthenticated) {
    // 实际项目中可能会使用更优雅的提示组件
    alert('请先登录后再绑定OAuth账户')
    return
  }

  loading.value = true
  try {
    const response = await apiService.bindGitHubAccount()
    window.location.href = response.data.redirect_url
  } catch (error) {
    console.error('绑定GitHub失败:', error)
    alert(error.response?.data?.error || '绑定失败，请稍后重试')
  } finally {
    loading.value = false
  }
}

// 绑定Google
const bindGoogle = async () => {
  if (!userStore.isAuthenticated) {
    alert('请先登录后再绑定OAuth账户')
    return
  }

  loading.value = true
  try {
    const response = await apiService.bindGoogleAccount()
    window.location.href = response.data.redirect_url
  } catch (error) {
    console.error('绑定Google失败:', error)
    alert(error.response?.data?.error || '绑定失败，请稍后重试')
  } finally {
    loading.value = false
  }
}

// 【新增】触发解绑确认弹窗
const promptUnbind = (provider) => {
  providerToUnbind.value = provider
  showConfirmModal.value = true
}

// 【新增】处理确认解绑逻辑
const handleConfirmUnbind = async () => {
  if (!providerToUnbind.value) return
  await unbindAccount(providerToUnbind.value)
  showConfirmModal.value = false
  providerToUnbind.value = null
}

// 解绑账户 - 【修改】移除了 confirm()
const unbindAccount = async (provider) => {
  loading.value = true
  try {
    await apiService.unbindOAuthAccount(provider)
    await fetchBindings()
    if (userStore.fetchUserInfo) {
      await userStore.fetchUserInfo()
    }
  } catch (error) {
    console.error('解绑失败:', error)
    alert(error.response?.data?.error || '解绑失败，请稍后重试')
  } finally {
    loading.value = false
  }
}

// 获取提供商名称
const getProviderName = (provider) => {
  if (!provider) return ''
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
  })
}

// --- Lifecycle Hooks ---
onMounted(async () => {
  if (userStore.initializeStore) {
    await userStore.initializeStore()
  }
  await fetchBindings()
})
</script>

<style scoped>
/* 【新增】解绑按钮的专属样式
  使其与 BaseButton 风格统一（圆角、字体粗细），但颜色明确表示为危险操作。
*/
.unbind-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  user-select: none;
  border: 1px solid var(--color-border);
  background-color: transparent;
  color: var(--color-danger);
  transition: all 0.2s ease-in-out;
}

.unbind-button:hover:not(:disabled) {
  background-color: var(--color-danger);
  border-color: var(--color-danger);
  color: var(--color-text-on-danger);
  box-shadow: 0 4px 12px rgba(220, 53, 69, 0.2);
}

.unbind-button:disabled {
  cursor: not-allowed;
  opacity: 0.5;
}

/* 适配移动端，让按钮宽度100% */
@media (min-width: 640px) {
  .unbind-button {
    width: auto;
  }
}
</style>
