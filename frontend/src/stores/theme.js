import { defineStore } from 'pinia'
import { ref, watchEffect } from 'vue'

export const useThemeStore = defineStore('theme', () => {
  // 1. 从 localStorage 读取初始主题，若无则默认为 'light'
  const theme = ref(localStorage.getItem('theme') || 'light')

  // 2. 切换主题的方法
  function toggleTheme() {
    theme.value = theme.value === 'light' ? 'dark' : 'light'
  }

  // 3. 使用 watchEffect 监听主题变化，执行副作用
  watchEffect(() => {
    // 3.1 将当前主题存入 localStorage
    localStorage.setItem('theme', theme.value)

    // 3.2 根据当前主题，更新根元素 <html> 的 class
    if (theme.value === 'dark') {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
  })

  // 4. 应用加载时，立即根据初始主题设置一次 class，防止刷新时闪烁
  if (theme.value === 'dark') {
    document.documentElement.classList.add('dark')
  }

  return { theme, toggleTheme }
})
