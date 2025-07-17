<script setup>
defineProps({
  loading: Boolean,
  disabled: Boolean,
});
</script>

<template>
  <button class="base-button" :disabled="loading || disabled">
    <div v-if="loading" class="spinner-wrapper">
      <div class="spinner"></div>
    </div>
    <span class="content-wrapper" :class="{ 'is-loading': loading }">
      <slot></slot>
    </span>
  </button>
</template>

<style scoped>
/*
  BaseButton.vue 的样式已完全重写，以支持主题切换、加载状态和禁用状态。
*/
.base-button {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  border: 1px solid transparent;
  user-select: none;
  transition: background-color 0.2s, border-color 0.2s, color 0.2s, box-shadow 0.2s;

  /* 默认样式使用主题色 */
  background-color: var(--color-primary);
  color: var(--color-text-on-primary);
}

.base-button:hover:not(:disabled) {
  background-color: var(--color-primary-hover);
  box-shadow: 0 4px 12px rgba(var(--color-primary-rgb, 37, 99, 235), 0.2);
}

.base-button:active:not(:disabled) {
  transform: translateY(1px);
}

/* --- 加载中状态 --- */
.spinner-wrapper {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.spinner {
  width: 20px;
  height: 20px;
  border: 3px solid rgba(var(--color-text-on-primary-rgb, 255, 255, 255), 0.3);
  border-top-color: var(--color-text-on-primary);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

.content-wrapper.is-loading {
  opacity: 0; /* 加载时隐藏文字内容 */
}

/* --- 禁用状态 --- */
.base-button:disabled {
  cursor: not-allowed;
  background-color: var(--color-secondary);
  opacity: 0.6;
  box-shadow: none;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>
