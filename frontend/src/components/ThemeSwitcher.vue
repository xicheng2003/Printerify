<template>
  <button @click="themeStore.toggleTheme" class="theme-switcher" aria-label="切换深色或浅色主题">
    <!-- 使用 Transition 组件为图标切换添加动画 -->
    <Transition name="fade-rotate" mode="out-in">
      <!-- 暗色模式下显示的太阳图标 (添加了 key) -->
      <svg v-if="themeStore.theme === 'dark'" key="sun" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="5"></circle>
        <line x1="12" y1="1" x2="12" y2="3"></line>
        <line x1="12" y1="21" x2="12" y2="23"></line>
        <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line>
        <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>
        <line x1="1" y1="12" x2="3" y2="12"></line>
        <line x1="21" y1="12" x2="23" y2="12"></line>
        <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line>
        <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>
      </svg>
      <!-- 亮色模式下显示的月亮图标 (添加了 key) -->
      <svg v-else key="moon" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
      </svg>
    </Transition>
  </button>
</template>

<script setup>
import { useThemeStore } from '@/stores/theme';

const themeStore = useThemeStore();
</script>

<style scoped>
.theme-switcher {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px; /* 调整按钮大小以适应图标 */
  height: 40px;
  transition: background-color 0.2s;
  color: var(--color-heading); /* 确保图标颜色与文本一致 */
  /* 确保 SVG 不会因为动画溢出 */
  overflow: hidden;
}

.theme-switcher:hover {
  background-color: var(--color-background-mute);
}

/*
  提示: 为确保所有图标按钮视觉统一，请确保它们共享相似的样式。
  以下属性对于居中对齐和统一尺寸至关重要，建议将它们也应用到 App.vue 中的 .mobile-menu-button 样式里。

  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 50%;
*/

/* 为图标切换添加的旋转与淡入淡出动画 */
.fade-rotate-enter-active,
.fade-rotate-leave-active {
  transition: opacity 0.2s ease, transform 0.3s ease;
}

.fade-rotate-enter-from,
.fade-rotate-leave-to {
  opacity: 0;
  transform: rotate(-90deg);
}
</style>
