import { describe, it, expect, beforeEach, vi } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useUserStore } from './user'
import apiService from '@/services/apiService'

// Mock apiService
vi.mock('@/services/apiService', () => ({
  default: {
    getToken: vi.fn(),
    setAuthToken: vi.fn(),
    removeAuthToken: vi.fn(),
    register: vi.fn(),
    login: vi.fn(),
    logout: vi.fn(),
    getProfile: vi.fn(),
    updateProfile: vi.fn(),
    getOAuthUserInfo: vi.fn(),
    getUserProfile: vi.fn()
  }
}))

describe('User Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    vi.clearAllMocks()
    // 清除localStorage
    localStorage.clear()
  })

  describe('State Management', () => {
    it('should initialize with default values', () => {
      const store = useUserStore()
      expect(store.user).toBe(null)
      expect(store.token).toBe(null)
      expect(store.loading).toBe(false)
      expect(store.isAuthenticated).toBe(false)
    })

    it('should compute isAuthenticated correctly', () => {
      const store = useUserStore()
      expect(store.isAuthenticated).toBe(false)

      store.token = 'test-token'
      expect(store.isAuthenticated).toBe(true)
    })

    it('should compute OAuth properties correctly', () => {
      const store = useUserStore()
      store.user = {
        username: 'testuser',
        github_id: '123',
        google_id: '456'
      }

      expect(store.isOAuthUser).toBe(true)
      expect(store.oAuthProviders).toEqual(['github', 'google'])
      expect(store.hasMultipleOAuthAccounts).toBe(true)
    })
  })

  describe('Token Management', () => {
    it('should set token correctly', () => {
      const store = useUserStore()
      const testToken = 'test-token'

      store.setToken(testToken)

      expect(store.token).toBe(testToken)
      expect(localStorage.getItem('token')).toBe(testToken)
      expect(apiService.setAuthToken).toHaveBeenCalledWith(testToken)
    })

    it('should clear token correctly', () => {
      const store = useUserStore()
      store.token = 'test-token'
      store.user = { username: 'test' }

      store.setToken(null)

      expect(store.token).toBe(null)
      expect(store.user).toBe(null)
      expect(localStorage.getItem('token')).toBe(null)
      expect(apiService.removeAuthToken).toHaveBeenCalled()
    })

    it('should update lastActivity when setting token', () => {
      const store = useUserStore()
      const before = Date.now()

      store.setToken('test-token')

      expect(store.lastActivity).toBeGreaterThanOrEqual(before)
    })
  })

  describe('Authentication', () => {
    it('should handle login successfully', async () => {
      const store = useUserStore()
      const mockResponse = {
        data: {
          user: { username: 'testuser' },
          token: 'test-token'
        }
      }

      apiService.login.mockResolvedValue(mockResponse)

      const result = await store.login({ username: 'testuser', password: 'password' })

      expect(store.user).toEqual(mockResponse.data.user)
      expect(store.token).toBe(mockResponse.data.token)
      expect(result).toEqual(mockResponse.data)
      expect(store.loading).toBe(false)
    })

    it('should handle login failure', async () => {
      const store = useUserStore()
      const mockError = new Error('Login failed')

      apiService.login.mockRejectedValue(mockError)

      await expect(store.login({ username: 'testuser', password: 'password' }))
        .rejects.toThrow('Login failed')

      expect(store.loading).toBe(false)
    })

    it('should handle register successfully', async () => {
      const store = useUserStore()
      const mockResponse = {
        data: {
          user: { username: 'newuser' },
          token: 'new-token'
        }
      }

      apiService.register.mockResolvedValue(mockResponse)

      const result = await store.register({
        username: 'newuser',
        email: 'test@example.com',
        password: 'password',
        password_confirm: 'password'
      })

      expect(store.user).toEqual(mockResponse.data.user)
      expect(store.token).toBe(mockResponse.data.token)
      expect(result).toEqual(mockResponse.data)
      expect(store.loading).toBe(false)
    })
  })

  describe('Profile Management', () => {
    it('should fetch profile successfully', async () => {
      const store = useUserStore()
      store.token = 'test-token'
      const mockProfile = { username: 'testuser', email: 'test@example.com' }

      apiService.getProfile.mockResolvedValue({ data: mockProfile })

      const result = await store.fetchProfile()

      expect(store.user).toEqual(mockProfile)
      expect(result).toEqual(mockProfile)
      expect(store.loading).toBe(false)
    })

    it('should handle profile fetch failure', async () => {
      const store = useUserStore()
      store.token = 'test-token'
      const mockError = { response: { status: 401 } }

      apiService.getProfile.mockRejectedValue(mockError)

      await expect(store.fetchProfile()).rejects.toEqual(mockError)
      expect(store.token).toBe(null) // Should clear token on 401
      expect(store.loading).toBe(false)
    })

    it('should update profile successfully', async () => {
      const store = useUserStore()
      store.token = 'test-token'
      store.user = { username: 'olduser' }
      const updateData = { username: 'newuser' }
      const mockResponse = { data: { username: 'newuser' } }

      apiService.updateProfile.mockResolvedValue(mockResponse)

      const result = await store.updateProfile(updateData)

      expect(store.user).toEqual(mockResponse.data)
      expect(result).toEqual(mockResponse.data)
      expect(store.loading).toBe(false)
    })
  })

  describe('OAuth Management', () => {
    it('should fetch OAuth user info successfully', async () => {
      const store = useUserStore()
      store.token = 'test-token'
      store.user = { username: 'testuser' }
      const mockOAuthInfo = { github_id: '123' }

      apiService.getOAuthUserInfo.mockResolvedValue({ data: mockOAuthInfo })

      const result = await store.fetchOAuthUserInfo()

      expect(store.user).toEqual({ username: 'testuser', github_id: '123' })
      expect(result).toEqual(mockOAuthInfo)
    })

    it('should refresh user info successfully', async () => {
      const store = useUserStore()
      store.token = 'test-token'

      apiService.getUserProfile.mockResolvedValue({ data: { username: 'testuser' } })
      apiService.getOAuthUserInfo.mockResolvedValue({ data: { github_id: '123' } })

      await store.refreshUserInfo()

      expect(apiService.getUserProfile).toHaveBeenCalled()
      expect(apiService.getOAuthUserInfo).toHaveBeenCalled()
    })
  })

  describe('Token Expiration', () => {
    it('should detect expired token', () => {
      const store = useUserStore()
      store.lastActivity = Date.now() - (25 * 60 * 60 * 1000) // 25 hours ago

      expect(store.isTokenExpired).toBe(true)
    })

    it('should detect valid token', () => {
      const store = useUserStore()
      store.lastActivity = Date.now() - (12 * 60 * 60 * 1000) // 12 hours ago

      expect(store.isTokenExpired).toBe(false)
    })

    it('should check and refresh user status', async () => {
      const store = useUserStore()
      store.token = 'test-token'
      store.lastActivity = Date.now() - (25 * 60 * 60 * 1000) // Expired

      apiService.getProfile.mockResolvedValue({ data: { username: 'testuser' } })

      await store.checkAndRefreshUserStatus()

      expect(apiService.getProfile).toHaveBeenCalled()
      expect(store.lastActivity).toBeGreaterThan(Date.now() - (25 * 60 * 60 * 1000))
    })
  })

  describe('Initialization', () => {
    it('should initialize store with valid token', async () => {
      const store = useUserStore()
      localStorage.setItem('token', 'test-token')
      store.token = 'test-token'

      apiService.getProfile.mockResolvedValue({ data: { username: 'testuser' } })

      await store.initializeStore()

      expect(apiService.setAuthToken).toHaveBeenCalledWith('test-token')
      expect(apiService.getProfile).toHaveBeenCalled()
      expect(store.user).toEqual({ username: 'testuser' })
    })

    it('should handle initialization failure', async () => {
      const store = useUserStore()
      localStorage.setItem('token', 'test-token')
      store.token = 'test-token'

      apiService.getProfile.mockRejectedValue({ response: { status: 401 } })

      await store.initializeStore()

      expect(store.token).toBe(null) // Should clear invalid token
    })
  })
})
