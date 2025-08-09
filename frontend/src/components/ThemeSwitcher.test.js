import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import ThemeSwitcher from '@/components/ThemeSwitcher.vue'
import { useThemeStore } from '@/stores/theme'

describe('ThemeSwitcher', () => {
  beforeEach(() => {
    // 创建新的 Pinia 实例并设置为活动实例
    setActivePinia(createPinia())
  })

  it('renders properly', () => {
    const wrapper = mount(ThemeSwitcher)
    expect(wrapper.find('button').exists()).toBe(true)
  })

  it('shows moon icon in light mode', () => {
    const themeStore = useThemeStore()
    themeStore.theme = 'light'
    
    const wrapper = mount(ThemeSwitcher)
    expect(wrapper.find('svg path[d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"]').exists()).toBe(true)
  })

  it('shows sun icon in dark mode', () => {
    const themeStore = useThemeStore()
    themeStore.theme = 'dark'
    
    const wrapper = mount(ThemeSwitcher)
    expect(wrapper.find('svg circle').exists()).toBe(true)
  })

  it('toggles theme when clicked', async () => {
    const themeStore = useThemeStore()
    themeStore.theme = 'light'
    
    const wrapper = mount(ThemeSwitcher)
    await wrapper.find('button').trigger('click')
    
    expect(themeStore.theme).toBe('dark')
  })
})