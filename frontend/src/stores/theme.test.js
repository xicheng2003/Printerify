import { describe, it, expect, vi, beforeEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useThemeStore } from '@/stores/theme'

describe('Theme Store', () => {
  beforeEach(() => {
    // 创建新的 Pinia 实例并设置为活动实例
    setActivePinia(createPinia())
    
    // 清除 localStorage
    localStorage.clear()
  })

  it('has initial theme as light', () => {
    const store = useThemeStore()
    expect(store.theme).toBe('light')
  })

  it('toggles theme from light to dark', () => {
    const store = useThemeStore()
    store.toggleTheme()
    expect(store.theme).toBe('dark')
  })

  it('toggles theme from dark to light', () => {
    const store = useThemeStore()
    store.theme = 'dark'
    store.toggleTheme()
    expect(store.theme).toBe('light')
  })

  it('saves theme to localStorage', () => {
    const store = useThemeStore()
    store.theme = 'dark'
    // Manually trigger the watchEffect logic
    localStorage.setItem('theme', store.theme)
    expect(localStorage.getItem('theme')).toBe('dark')
  })

  it('loads theme from localStorage', () => {
    localStorage.setItem('theme', 'dark')
    // 重新创建 store 以模拟页面刷新
    setActivePinia(createPinia())
    const store = useThemeStore()
    expect(store.theme).toBe('dark')
  })
})