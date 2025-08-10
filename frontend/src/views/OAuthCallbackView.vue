<template>
  <div class="oauth-callback-view">
    <div class="auth-background">
      <div class="geometric-shape shape-1"></div>
      <div class="geometric-shape shape-2"></div>
      <div class="geometric-shape shape-3"></div>
    </div>

    <div class="callback-card">
      <div v-if="loading" class="state-container">
        <LoadingSpinner />
        <h2 class="state-title">正在安全验证...</h2>
        <p class="state-description">请稍候，我们正在为您完成最后的配置。</p>
      </div>

      <div v-else-if="error" class="state-container">
        <div class="icon-wrapper error-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="12" y1="8" x2="12" y2="12"></line>
            <line x1="12" y1="16" x2="12.01" y2="16"></line>
          </svg>
        </div>
        <h2 class="state-title">操作失败</h2>
        <p class="error-message">{{ error }}</p>
        <BaseButton @click="goToLogin" class="action-button error-button">
          返回重试
        </BaseButton>
      </div>

      <div v-else-if="success" class="state-container">
        <div class="icon-wrapper success-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
            <polyline points="22 4 12 14.01 9 11.01"></polyline>
          </svg>
        </div>
        <div v-if="!isBinding && userInfo.avatar_url" class="user-avatar">
          <img :src="userInfo.avatar_url" :alt="userInfo.display_name || userInfo.username" />
        </div>
        <h2 class="state-title">{{ isBinding ? '账户绑定成功！' : '欢迎回来！' }}</h2>
        <p class="state-description">
          {{ isBinding ? '现在您可以使用该账户进行登录' : `很高兴再次见到您, ${userInfo.display_name || userInfo.username}` }}
        </p>
        <BaseButton @click="goToHome" class="action-button">
          {{ isBinding ? '返回个人中心' : '进入工作台' }}
        </BaseButton>
      </div>
    </div>
  </div>
</template>

<script setup>
// ===================================================================
// 脚本部分 (Script Section)
// ===================================================================
//
// 【重要】这里的业务逻辑完全没有改动，
// 只是将原有的 Options API 结构转换为 Composition API (<script setup>)，
// 以符合项目其他新组件的编码风格。所有功能、变量和方法均保持不变。
//
import { ref, onMounted, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'
import LoadingSpinner from '@/components/LoadingSpinner.vue'
import BaseButton from '@/components/BaseButton.vue'

const loading = ref(true)
const error = ref('')
const success = ref(false)
const userInfo = ref({})
const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

const isBinding = computed(() => route.query.bind === 'true')

const cleanUrl = () => {
  const url = new URL(window.location.href)
  url.searchParams.delete('temp_token')
  url.searchParams.delete('code')
  url.searchParams.delete('state')
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
    // 根据实际路由配置，跳转到统一的认证页面
    router.push({ name: 'login' })
    }

    const goToHome = () => {
      const destination = isBinding.value ? '/profile' : '/'
      router.push(destination)
    }

    onMounted(() => {
      processOAuthCallback()
    })

</script>

<style scoped>
/* 根容器样式，与 AuthView 一致 */
.oauth-callback-view {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: calc(100vh - var(--header-height, 65px)); /* 减去头部高度，如果存在 */
  padding: 2rem 1rem;
  background: var(--color-background-soft);
  overflow: hidden;
}

/* 背景装饰，与 AuthView 一致 */
.auth-background {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
  overflow: hidden;
}

.geometric-shape {
  position: absolute;
  border-radius: 50%;
  background: linear-gradient(45deg,
    rgba(var(--color-primary-rgb, 37, 99, 235), 0.1),
    rgba(var(--color-primary-rgb, 37, 99, 235), 0.05)
  );
  animation: float 8s ease-in-out infinite;
}

.shape-1 { width: 220px; height: 220px; top: 15%; left: 5%; animation-delay: 0s; }
.shape-2 { width: 130px; height: 130px; top: 70%; right: 10%; animation-delay: 3s; }
.shape-3 { width: 80px; height: 80px; bottom: 10%; left: 65%; animation-delay: 6s; }

@keyframes float {
  0%, 100% { transform: translateY(0px) rotate(0deg) scale(1); }
  50% { transform: translateY(-25px) rotate(180deg) scale(1.05); }
}

/* 内容卡片样式 */
.callback-card {
  position: relative;
  z-index: 1;
  width: 100%;
  max-width: 450px;
  padding: 2.5rem 2rem;
  background: var(--color-background);
  border-radius: 20px;
  border: 1px solid var(--color-border);
  box-shadow: var(--shadow-card);
  text-align: center;
  transition: all 0.3s ease;
}

.state-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.state-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--color-heading);
  margin-top: 1rem;
  margin-bottom: 0;
}

.state-description {
  color: var(--color-text-mute);
  font-size: 1rem;
  line-height: 1.6;
  max-width: 320px;
  margin: 0;
}

/* 图标样式 */
.icon-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 80px;
  height: 80px;
  border-radius: 50%;
  margin-bottom: 1rem;
}

.success-icon {
  background-color: rgba(var(--color-primary-rgb, 37, 99, 235), 0.1);
  color: var(--color-primary);
  animation: pulse-success 2s infinite;
}

.error-icon {
  background-color: rgba(var(--color-danger-rgb, 220, 53, 69), 0.1);
  color: var(--color-danger);
  animation: pulse-error 2s infinite;
}

@keyframes pulse-success {
  0% { box-shadow: 0 0 0 0 rgba(var(--color-primary-rgb, 37, 99, 235), 0.4); }
  70% { box-shadow: 0 0 0 15px rgba(var(--color-primary-rgb, 37, 99, 235), 0); }
  100% { box-shadow: 0 0 0 0 rgba(var(--color-primary-rgb, 37, 99, 235), 0); }
}

@keyframes pulse-error {
  0% { box-shadow: 0 0 0 0 rgba(var(--color-danger-rgb, 220, 53, 69), 0.4); }
  70% { box-shadow: 0 0 0 15px rgba(var(--color-danger-rgb, 220, 53, 69), 0); }
  100% { box-shadow: 0 0 0 0 rgba(var(--color-danger-rgb, 220, 53, 69), 0); }
}


/* 错误信息特定样式 */
.error-message {
  color: var(--color-danger);
  font-weight: 500;
  background-color: rgba(var(--color-danger-rgb, 220, 53, 69), 0.1);
  border-radius: 8px;
  padding: 0.5rem 1rem;
  width: 100%;
}

/* 用户头像 */
.user-avatar {
  margin-top: 0.5rem;
}

.user-avatar img {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  border: 3px solid var(--color-primary);
  object-fit: cover;
  box-shadow: 0 4px 12px rgba(var(--color-primary-rgb, 37, 99, 235), 0.2);
}

/* 操作按钮 */
.action-button {
  margin-top: 1.5rem;
  width: 100%;
}

/* 错误状态的按钮样式 */
.error-button {
  background-color: var(--color-danger);
}
.error-button:hover:not(:disabled) {
  background-color: var(--color-danger-hover);
}

/* 响应式设计 */
@media (max-width: 640px) {
  .callback-card {
    padding: 2rem 1.5rem;
  }
  .state-title {
    font-size: 1.25rem;
  }
}
</style>
