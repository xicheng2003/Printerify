import { describe, it, expect, vi, beforeEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useUserStore } from '@/stores/user'

// Mock the apiService
vi.mock('@/services/apiService', () => {
  return {
    default: {
      register: vi.fn().mockResolvedValue({
        data: {
          user: { id: 1, username: 'testuser', email: 'test@example.com' },
          token: 'test-token'
        }
      }),
      login: vi.fn().mockResolvedValue({
        data: {
          user: { id: 1, username: 'testuser', email: 'test@example.com' },
          token: 'test-token'
        }
      }),
      logout: vi.fn().mockResolvedValue({}),
      getProfile: vi.fn().mockResolvedValue({
        data: { id: 1, username: 'testuser', email: 'test@example.com' }
      }),
      updateProfile: vi.fn().mockResolvedValue({
        data: { id: 1, username: 'testuser', email: 'updated@example.com' }
      }),
      setAuthToken: vi.fn(),
      removeAuthToken: vi.fn(),
      getToken: vi.fn().mockReturnValue(null)
    }
  }
})

describe('User Store', () => {
  beforeEach(() => {
    // Create a new Pinia instance and make it active
    setActivePinia(createPinia())
    
    // Clear localStorage
    localStorage.clear()
  })

  it('initializes with no user and no token', () => {
    const store = useUserStore()
    expect(store.user).toBe(null)
    expect(store.token).toBe(null)
    expect(store.isAuthenticated).toBe(false)
  })

  it('sets token and updates localStorage', () => {
    const store = useUserStore()
    store.setToken('test-token')
    
    expect(store.token).toBe('test-token')
    expect(localStorage.getItem('token')).toBe('test-token')
  })

  it('clears token and removes from localStorage', () => {
    const store = useUserStore()
    localStorage.setItem('token', 'test-token')
    
    store.setToken(null)
    
    expect(store.token).toBe(null)
    expect(localStorage.getItem('token')).toBe(null)
  })

  it('registers user and sets token', async () => {
    const store = useUserStore()
    const userData = {
      username: 'testuser',
      email: 'test@example.com',
      password: 'password123',
      password_confirm: 'password123'
    }
    
    await store.register(userData)
    
    expect(store.user).toEqual({
      id: 1,
      username: 'testuser',
      email: 'test@example.com'
    })
    expect(store.token).toBe('test-token')
    expect(store.isAuthenticated).toBe(true)
  })

  it('logs in user and sets token', async () => {
    const store = useUserStore()
    const credentials = {
      username: 'testuser',
      password: 'password123'
    }
    
    await store.login(credentials)
    
    expect(store.user).toEqual({
      id: 1,
      username: 'testuser',
      email: 'test@example.com'
    })
    expect(store.token).toBe('test-token')
    expect(store.isAuthenticated).toBe(true)
  })

  it('logs out user and clears state', async () => {
    const store = useUserStore()
    
    // First login
    await store.login({ username: 'testuser', password: 'password123' })
    expect(store.isAuthenticated).toBe(true)
    
    // Then logout
    await store.logout()
    
    expect(store.user).toBe(null)
    expect(store.token).toBe(null)
    expect(store.isAuthenticated).toBe(false)
  })

  it('fetches user profile', async () => {
    const store = useUserStore()
    store.setToken('test-token')
    
    await store.fetchProfile()
    
    expect(store.user).toEqual({
      id: 1,
      username: 'testuser',
      email: 'test@example.com'
    })
  })

  it('updates user profile', async () => {
    const store = useUserStore()
    store.setToken('test-token')
    
    // First fetch profile
    await store.fetchProfile()
    expect(store.user.email).toBe('test@example.com')
    
    // Then update profile
    await store.updateProfile({ email: 'updated@example.com' })
    
    expect(store.user.email).toBe('updated@example.com')
  })
})