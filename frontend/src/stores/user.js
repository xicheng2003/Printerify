import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import apiService from '@/services/apiService'

export const useUserStore = defineStore('user', () => {
  const user = ref(null)
  const token = ref(apiService.getToken() || null)
  const loading = ref(false)

  const isAuthenticated = computed(() => !!token.value)
  const userProfile = computed(() => user.value)

  // 初始化时尝试从localStorage恢复用户信息
  if (token.value) {
    // 可以在这里添加自动刷新用户信息的逻辑
    // 为了简化，我们暂时不自动获取用户信息
    apiService.setAuthToken(token.value)
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

  return {
    user,
    token,
    loading,
    isAuthenticated,
    userProfile,
    register,
    login,
    logout,
    fetchProfile,
    updateProfile,
    setToken // 导出setToken方法
  }
})