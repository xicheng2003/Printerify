import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import apiService from '@/services/apiService'

export const useUserStore = defineStore('user', () => {
  const user = ref(null)
  const token = ref(apiService.getToken() || null)
  const loading = ref(false)

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

  // 初始化函数
  async function initializeStore() {
    if (token.value) {
      apiService.setAuthToken(token.value)
      try {
        // 自动获取用户信息
        await fetchProfile()
      } catch (error) {
        console.error('自动获取用户信息失败:', error)
        // 如果获取失败，清除无效的token
        setToken(null)
      }
    }
  }

  function setToken(newToken) {
    token.value = newToken
    if (newToken) {
      localStorage.setItem('token', newToken)
      apiService.setAuthToken(newToken)
    } else {
      localStorage.removeItem('token')
      apiService.removeAuthToken()
    }
  }

  async function register(userData) {
    loading.value = true
    try {
      const response = await apiService.register(userData)
      const { user: userDataResponse, token: userToken } = response.data

      user.value = userDataResponse
      setToken(userToken)

      return response.data
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
      return response.data
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
      return response.data
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

  return {
    user,
    token,
    loading,
    isAuthenticated,
    userProfile,
    isOAuthUser,
    oAuthProviders,
    hasMultipleOAuthAccounts,
    setToken,
    register,
    login,
    logout,
    fetchProfile,
    updateProfile,
    fetchOAuthUserInfo,
    fetchUserInfo,
    refreshUserInfo,
    initializeStore
  }
})
