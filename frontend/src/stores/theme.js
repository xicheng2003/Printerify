import { defineStore } from 'pinia'
import { ref, watchEffect } from 'vue'

export const useThemeStore = defineStore('theme', () => {
  // 1. 从 localStorage 读取初始主题，若无则默认为 'system'
  const theme = ref(localStorage.getItem('theme') || 'system')

  // 2. 系统暗色模式媒体查询
  const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')

  // 3. 应用主题的逻辑
  function applyTheme() {
    const isDark =
      theme.value === 'dark' ||
      (theme.value === 'system' && mediaQuery.matches)

    if (isDark) {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
  }

  // 4. 监听主题状态变化并应用
  watchEffect(() => {
    localStorage.setItem('theme', theme.value)
    applyTheme()
  })

  // 5. 监听系统主题变化
  mediaQuery.addEventListener('change', () => {
    if (theme.value === 'system') {
      applyTheme()
    }
  })

  // 6. 设置主题的方法
  function setTheme(newTheme) {
    theme.value = newTheme
  }

  return { theme, setTheme }
})
