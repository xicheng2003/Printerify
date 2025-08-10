<template>
  <div class="oauth-login">
    <h3 class="oauth-title">使用第三方账号登录</h3>
    <div class="oauth-buttons">
      <button
        @click="loginWithGitHub"
        class="oauth-btn github-btn"
        :disabled="loading"
      >
        <svg class="oauth-icon" viewBox="0 0 24 24" fill="currentColor">
          <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
        </svg>
        <span v-if="!loading">使用GitHub登录</span>
        <span v-else>登录中...</span>
      </button>

      <button
        @click="loginWithGoogle"
        class="oauth-btn google-btn"
        :disabled="loading"
      >
        <svg class="oauth-icon" viewBox="0 0 24 24" fill="currentColor">
          <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
          <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
          <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
          <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
        </svg>
        <span v-if="!loading">使用Google登录</span>
        <span v-else>登录中...</span>
      </button>
    </div>

    <div class="oauth-divider">
      <span>或</span>
    </div>

    <p class="oauth-note">
      使用第三方账号登录，无需记住密码，更安全便捷
    </p>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'

export default {
  name: 'OAuthLogin',
  setup() {
    const loading = ref(false)
    const router = useRouter()
    const userStore = useUserStore()

    const loginWithGitHub = async () => {
      try {
        loading.value = true
        // 重定向到后端GitHub OAuth端点
        window.location.href = '/api/oauth/github/'
      } catch (error) {
        console.error('GitHub登录失败:', error)
        loading.value = false
      }
    }

    const loginWithGoogle = async () => {
      try {
        loading.value = true
        // 重定向到后端Google OAuth端点
        window.location.href = '/api/oauth/google/'
      } catch (error) {
        console.error('Google登录失败:', error)
        loading.value = false
      }
    }

    return {
      loading,
      loginWithGitHub,
      loginWithGoogle
    }
  }
}
</script>

<style scoped>
.oauth-login {
  max-width: 400px;
  margin: 0 auto;
  padding: 2rem;
  text-align: center;
}

.oauth-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 1.5rem;
}

.oauth-buttons {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.oauth-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  padding: 0.875rem 1.5rem;
  border: 2px solid transparent;
  border-radius: 0.5rem;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  position: relative;
  overflow: hidden;
}

.oauth-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.oauth-btn:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.github-btn {
  background-color: #24292e;
  color: white;
}

.github-btn:hover:not(:disabled) {
  background-color: #1b1f23;
  border-color: #1b1f23;
}

.google-btn {
  background-color: white;
  color: #757575;
  border-color: #dadce0;
}

.google-btn:hover:not(:disabled) {
  background-color: #f8f9fa;
  border-color: #dadce0;
  color: #5f6368;
}

.oauth-icon {
  width: 1.5rem;
  height: 1.5rem;
  flex-shrink: 0;
}

.oauth-divider {
  position: relative;
  text-align: center;
  margin: 1.5rem 0;
}

.oauth-divider::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  height: 1px;
  background-color: var(--border-color);
}

.oauth-divider span {
  background-color: var(--bg-primary);
  padding: 0 1rem;
  color: var(--text-secondary);
  font-size: 0.875rem;
}

.oauth-note {
  color: var(--text-secondary);
  font-size: 0.875rem;
  line-height: 1.5;
  margin: 0;
}

/* 响应式设计 */
@media (max-width: 640px) {
  .oauth-login {
    padding: 1.5rem;
  }

  .oauth-btn {
    padding: 0.75rem 1.25rem;
    font-size: 0.875rem;
  }

  .oauth-icon {
    width: 1.25rem;
    height: 1.25rem;
  }
}

/* 深色模式支持 */
@media (prefers-color-scheme: dark) {
  .google-btn {
    background-color: #2d3748;
    color: #e2e8f0;
    border-color: #4a5568;
  }

  .google-btn:hover:not(:disabled) {
    background-color: #4a5568;
    border-color: #718096;
    color: #f7fafc;
  }
}
</style>
