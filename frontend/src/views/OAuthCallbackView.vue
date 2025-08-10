<template>
  <div class="oauth-callback">
    <div class="callback-container">
      <div v-if="loading" class="loading-state">
        <LoadingSpinner />
        <h2>正在处理登录...</h2>
        <p>请稍候，我们正在为您完成登录流程</p>
      </div>

      <div v-else-if="error" class="error-state">
        <div class="error-icon">❌</div>
        <h2>登录失败</h2>
        <p class="error-message">{{ error }}</p>
        <BaseButton @click="goToLogin" class="retry-btn">
          返回登录页面
        </BaseButton>
      </div>

      <div v-else-if="success" class="success-state">
        <div class="success-icon">✅</div>
        <h2>登录成功！</h2>
        <p>欢迎回来，{{ userInfo.display_name || userInfo.username }}！</p>
        <div class="user-avatar" v-if="userInfo.avatar_url">
          <img :src="userInfo.avatar_url" :alt="userInfo.display_name || userInfo.username" />
        </div>
        <BaseButton @click="goToHome" class="home-btn">
          前往首页
        </BaseButton>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'
import LoadingSpinner from '@/components/LoadingSpinner.vue'
import BaseButton from '@/components/BaseButton.vue'

export default {
  name: 'OAuthCallbackView',
  components: {
    LoadingSpinner,
    BaseButton
  },
  setup() {
    const loading = ref(true)
    const error = ref('')
    const success = ref(false)
    const userInfo = ref({})
    const router = useRouter()
    const route = useRoute()
    const userStore = useUserStore()

    const processOAuthCallback = async () => {
      try {
        // 从URL参数获取OAuth处理结果
        const { provider, success: oauthSuccess, username, error: oauthError } = route.query

        console.log('OAuth回调参数:', route.query)

        if (oauthError) {
          throw new Error(`OAuth错误: ${oauthError}`)
        }

        if (oauthSuccess === 'true') {
          // OAuth登录成功，获取用户信息
          console.log('OAuth登录成功，获取用户信息...')

          const response = await fetch('/api/oauth/userinfo/', {
            credentials: 'include'
          })

          if (response.ok) {
            const data = await response.json()
            userInfo.value = data
            success.value = true
            console.log('用户信息获取成功:', data)

            // 直接更新用户store状态，而不是调用fetchProfile
            if (userStore.user) {
              // 如果用户store中已有用户信息，则更新
              userStore.user = { ...userStore.user, ...data }
            } else {
              // 如果用户store中没有用户信息，则设置
              userStore.user = data
            }

            // 设置认证状态为已登录
            userStore.setToken('oauth_authenticated')

            console.log('用户store状态已更新')
          } else {
            throw new Error('获取用户信息失败')
          }
        } else {
          throw new Error('OAuth登录失败')
        }

      } catch (err) {
        console.error('OAuth回调处理失败:', err)
        error.value = err.message || '登录过程中发生未知错误'
      } finally {
        loading.value = false
      }
    }

    const goToLogin = () => {
      router.push('/auth')
    }

    const goToHome = () => {
      router.push('/')
    }

    onMounted(() => {
      processOAuthCallback()
    })

    return {
      loading,
      error,
      success,
      userInfo,
      goToLogin,
      goToHome
    }
  }
}
</script>

<style scoped>
.oauth-callback {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 2rem;
}

.callback-container {
  background: white;
  border-radius: 1rem;
  padding: 3rem;
  text-align: center;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  max-width: 500px;
  width: 100%;
}

.loading-state,
.error-state,
.success-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.5rem;
}

.loading-state h2,
.error-state h2,
.success-state h2 {
  color: var(--text-primary);
  font-size: 1.75rem;
  font-weight: 600;
  margin: 0;
}

.loading-state p,
.error-state p,
.success-state p {
  color: var(--text-secondary);
  font-size: 1rem;
  line-height: 1.6;
  margin: 0;
}

.error-icon,
.success-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.error-message {
  color: #e53e3e;
  font-weight: 500;
}

.user-avatar {
  margin: 1rem 0;
}

.user-avatar img {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  border: 4px solid #e2e8f0;
  object-fit: cover;
}

.retry-btn,
.home-btn {
  margin-top: 1rem;
  padding: 0.75rem 2rem;
  font-size: 1rem;
  font-weight: 500;
}

.retry-btn {
  background-color: #e53e3e;
  color: white;
}

.retry-btn:hover {
  background-color: #c53030;
}

.home-btn {
  background-color: #38a169;
  color: white;
}

.home-btn:hover {
  background-color: #2f855a;
}

/* 响应式设计 */
@media (max-width: 640px) {
  .oauth-callback {
    padding: 1rem;
  }

  .callback-container {
    padding: 2rem;
  }

  .loading-state h2,
  .error-state h2,
  .success-state h2 {
    font-size: 1.5rem;
  }

  .user-avatar img {
    width: 60px;
    height: 60px;
  }
}
</style>
