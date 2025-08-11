import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import apiService from '@/services/apiService'

export const useUserStore = defineStore('user', () => {
  const user = ref(null)
  const token = ref(apiService.getToken() || null)
  const loading = ref(false)
  const lastActivity = ref(Date.now())

  const isAuthenticated = computed(() => !!token.value)
  const userProfile = computed(() => user.value)

  // OAuth相关计算属性
  const isOAuthUser = computed(() => {
    return user.value?.github_id || user.value?.google_id
  })

  const oAuthProviders = computed(() => {
    const providers = []
    if (user.value?.github_id) providers.push('github')
    if (user.value?.google_id) providers.push('google')
    return providers
  })

  const hasMultipleOAuthAccounts = computed(() => {
    return oAuthProviders.value.length > 1
  })

  // 检查token是否过期（简单实现，实际项目中可能需要JWT解码）
  const isTokenExpired = computed(() => {
    if (!lastActivity.value) return true
    // 假设token有效期为24小时
    const tokenLifetime = 24 * 60 * 60 * 1000
    return Date.now() - lastActivity.value > tokenLifetime
  })

  // 初始化函数
  async function initializeStore() {
    if (token.value && !isTokenExpired.value) {
      apiService.setAuthToken(token.value)
      try {
        // 自动获取用户信息
        await fetchProfile()
        updateLastActivity()
      } catch (error) {
        console.error('自动获取用户信息失败:', error)
        // 如果获取失败，清除无效的token
        if (error.response?.status === 401) {
          setToken(null)
        }
      }
    }
  }

  function setToken(newToken) {
    token.value = newToken
    if (newToken) {
      localStorage.setItem('token', newToken)
      apiService.setAuthToken(newToken)
      updateLastActivity()
    } else {
      localStorage.removeItem('token')
      apiService.removeAuthToken()
      user.value = null
      lastActivity.value = null
    }
  }

  function updateLastActivity() {
    lastActivity.value = Date.now()
  }

  async function register(userData) {
    loading.value = true
    try {
      const response = await apiService.register(userData)
      const { user: userDataResponse, token: userToken } = response.data

      user.value = userDataResponse
      setToken(userToken)

      return response.data
    } catch (error) {
      console.error('注册失败:', error)
      // 使用友好的错误提示
      const errorMessage = error.friendlyMessage || error.message || '注册失败，请重试'
      throw new Error(errorMessage)
    } finally {
      loading.value = false
    }
  }

  async function login(credentials) {
    loading.value = true
    try {
      const response = await apiService.login(credentials)
      const { user: userDataResponse, token: userToken } = response.data

      user.value = userDataResponse
      setToken(userToken)

      return response.data
    } catch (error) {
      console.error('登录失败:', error)
      // 使用友好的错误提示
      const errorMessage = error.friendlyMessage || error.message || '登录失败，请重试'
      throw new Error(errorMessage)
    } finally {
      loading.value = false
    }
  }

  async function logout() {
    try {
      if (token.value) {
        await apiService.logout()
      }
    } catch (error) {
      // 即使登出API失败，我们也清除本地状态
      console.error('Logout API error:', error)
    } finally {
      user.value = null
      setToken(null)
    }
  }

  async function fetchProfile() {
    if (!token.value) {
      throw new Error('User not authenticated')
    }

    loading.value = true
    try {
      const response = await apiService.getProfile()
      user.value = response.data
      updateLastActivity()
      return response.data
    } catch (error) {
      console.error('获取用户资料失败:', error)
      if (error.response?.status === 401) {
        // Token无效，清除状态
        setToken(null)
      }
      throw error
    } finally {
      loading.value = false
    }
  }

  async function updateProfile(updateData) {
    if (!token.value) {
      throw new Error('User not authenticated')
    }

    loading.value = true
    try {
      const response = await apiService.updateProfile(updateData)
      user.value = response.data
      updateLastActivity()
      return response.data
    } catch (error) {
      console.error('更新用户资料失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  // OAuth相关方法
  async function fetchOAuthUserInfo() {
    if (!token.value) {
      throw new Error('User not authenticated')
    }

    try {
      const response = await apiService.getOAuthUserInfo()
      // 更新用户信息中的OAuth相关字段
      if (user.value) {
        user.value = { ...user.value, ...response.data }
      }
      updateLastActivity()
      return response.data
    } catch (error) {
      console.error('获取OAuth用户信息失败:', error)
      throw error
    }
  }

  async function fetchUserInfo() {
    if (!token.value) {
      throw new Error('User not authenticated')
    }

    try {
      const response = await apiService.getUserProfile()
      user.value = response.data
      updateLastActivity()
      return response.data
    } catch (error) {
      console.error('获取用户信息失败:', error)
      throw error
    }
  }

  async function refreshUserInfo() {
    // 同时获取用户资料和OAuth信息
    try {
      await Promise.all([
        fetchUserInfo(),
        fetchOAuthUserInfo()
      ])
    } catch (error) {
      console.error('刷新用户信息失败:', error)
      throw error
    }
  }

  // 检查并刷新用户状态
  async function checkAndRefreshUserStatus() {
    if (token.value && isTokenExpired.value) {
      try {
        await fetchProfile()
      } catch (error) {
        console.error('Token已过期，清除用户状态:', error)
        setToken(null)
      }
    }
  }

  return {
    user,
    token,
    loading,
    lastActivity,
    isAuthenticated,
    userProfile,
    isOAuthUser,
    oAuthProviders,
    hasMultipleOAuthAccounts,
    isTokenExpired,
    setToken,
    register,
    login,
    logout,
    fetchProfile,
    updateProfile,
    fetchOAuthUserInfo,
    fetchUserInfo,
    refreshUserInfo,
    initializeStore,
    checkAndRefreshUserStatus,
    updateLastActivity
  }
})
