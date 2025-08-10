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
        <h2>{{ isBinding ? '账户绑定成功！' : '登录成功！' }}</h2>
        <p>{{ isBinding ? '您的OAuth账户已成功绑定' : `欢迎回来，${userInfo.display_name || userInfo.username}！` }}</p>
        <div class="user-avatar" v-if="userInfo.avatar_url">
          <img :src="userInfo.avatar_url" :alt="userInfo.display_name || userInfo.username" />
        </div>
        <BaseButton @click="goToHome" class="home-btn">
          {{ isBinding ? '返回个人资料' : '前往首页' }}
        </BaseButton>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
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

    // 判断是否为账户绑定流程
    const isBinding = computed(() => {
      return route.query.bind === 'true'
    })

    // 清理URL中的敏感参数
    const cleanUrl = () => {
      const url = new URL(window.location.href)
      url.searchParams.delete('temp_token')
      url.searchParams.delete('code')
      url.searchParams.delete('state')

      // 使用replaceState更新URL，不添加历史记录
      window.history.replaceState({}, document.title, url.pathname + url.search)
    }

    const processOAuthCallback = async () => {
      try {
        // 从URL参数获取OAuth处理结果
        const { success: oauthSuccess, error: oauthError, username, temp_token, provider } = route.query

        console.log('OAuth回调参数:', route.query)

        if (oauthError) {
          throw new Error(`OAuth错误: ${oauthError}`)
        }

        if (oauthSuccess === 'true' && username) {
          // OAuth登录成功，检查是否有临时token
          console.log('OAuth登录成功，检查认证token...')

          if (temp_token) {
            // 后端已经提供了token，使用token验证端点获取用户信息
            console.log('使用后端提供的临时token进行验证')

            try {
              // 调用token验证端点
              const response = await fetch(`/api/oauth/validate-token/?token=${temp_token}`)

              if (response.ok) {
                const data = await response.json()
                console.log('token验证成功:', data)

                // 设置认证token
                userStore.setToken(data.token)

                // 设置用户信息
                userStore.user = data.user
                userInfo.value = data.user
                success.value = true

                // 如果是账户绑定流程，刷新用户信息
                if (isBinding.value) {
                  try {
                    await userStore.refreshUserInfo()
                    console.log('账户绑定后用户信息已刷新')
                  } catch (refreshError) {
                    console.warn('刷新用户信息失败，但不影响绑定结果:', refreshError)
                  }
                }

                console.log('用户store状态已更新，认证token已设置')

                // 清理URL中的敏感参数
                cleanUrl()
              } else {
                throw new Error('token验证失败')
              }
            } catch (tokenError) {
              console.warn('token验证失败，尝试使用登录API:', tokenError)

              // 回退到登录API
              await callLoginAPI(username, provider || 'github')
            }
          } else {
            // 没有临时token，使用登录API
            console.log('没有临时token，调用登录API...')
            await callLoginAPI(username, provider || 'github')
          }
        } else {
          throw new Error('OAuth登录失败或缺少用户名')
        }

      } catch (err) {
        console.error('OAuth回调处理失败:', err)
        error.value = err.message || '登录过程中发生未知错误'
      } finally {
        loading.value = false
      }
    }

    // 调用登录API的辅助函数
    const callLoginAPI = async (username, provider) => {
      try {
        const loginResponse = await fetch('/api/login/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            username: username,
            oauth_provider: provider
          })
        })

        if (loginResponse.ok) {
          const loginData = await loginResponse.json()
          console.log('登录API响应:', loginData)

          // 设置真实的认证token
          userStore.setToken(loginData.token)

          // 设置用户信息
          userStore.user = loginData.user

          success.value = true
          userInfo.value = loginData.user

          // 如果是账户绑定流程，刷新用户信息
          if (isBinding.value) {
            try {
              await userStore.refreshUserInfo()
              console.log('账户绑定后用户信息已刷新')
            } catch (refreshError) {
              console.warn('刷新用户信息失败，但不影响绑定结果:', refreshError)
            }
          }

          console.log('用户store状态已更新，认证token已设置')

          // 清理URL中的敏感参数
          cleanUrl()
        } else {
          throw new Error('登录API调用失败')
        }
      } catch (loginError) {
        console.warn('登录API调用失败，尝试session认证:', loginError)

        // 回退到session认证
        const response = await fetch('/api/oauth/userinfo/', {
          credentials: 'include'
        })

        if (response.ok) {
          const data = await response.json()
          userInfo.value = data
          success.value = true
          console.log('用户信息获取成功（session认证）:', data)

          // 设置认证状态为已登录（使用session认证）
          userStore.setToken('session_authenticated')
          userStore.user = data

          console.log('用户store状态已更新（session认证）')

          // 清理URL中的敏感参数
          cleanUrl()
        } else {
          throw new Error('获取用户信息失败')
        }
      }
    }

    const goToLogin = () => {
      router.push('/auth')
    }

    const goToHome = () => {
      if (isBinding.value) {
        // 如果是账户绑定，跳转到个人资料页面
        router.push('/profile')
      } else {
        // 如果是登录，跳转到首页
        router.push('/')
      }
    }

    onMounted(() => {
      processOAuthCallback()
    })

    return {
      loading,
      error,
      success,
      userInfo,
      isBinding,
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
