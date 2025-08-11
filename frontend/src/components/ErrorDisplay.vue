<template>
  <div v-if="error" class="error-compact">
    <div class="icon-compact">
      <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="10"></circle>
        <line x1="12" y1="8" x2="12" y2="12"></line>
        <line x1="12" y1="16" x2="12.01" y2="16"></line>
      </svg>
    </div>

    <div class="content-compact">
      <p class="message-compact">{{ error }}</p>

      <div v-if="showSuggestions" class="suggestions-compact">
        <ul>
          <li v-if="error.includes('用户名')">尝试一个独特的用户名，可包含字母和数字。</li>
          <li v-if="error.includes('邮箱')">请检查您的邮箱地址格式是否正确。</li>
          <li v-if="error.includes('密码')">确保密码至少为8位，并包含字母和数字。</li>
          <li v-if="error.includes('网络')">请检查您的网络连接是否正常，然后重试。</li>
        </ul>
      </div>
    </div>

    <button v-if="dismissible" @click="$emit('dismiss')" class="dismiss-compact">
      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
        <line x1="18" y1="6" x2="6" y2="18"></line>
        <line x1="6" y1="6" x2="18" y2="18"></line>
      </svg>
    </button>
  </div>
</template>

<script setup>
// 业务逻辑完全保持不变
import { computed } from 'vue'

const props = defineProps({
  error: {
    type: String,
    default: ''
  },
  dismissible: {
    type: Boolean,
    default: false
  }
})

defineEmits(['dismiss'])

const showSuggestions = computed(() => {
  return props.error && (
    props.error.includes('用户名') ||
    props.error.includes('邮箱') ||
    props.error.includes('密码') ||
    props.error.includes('网络')
  )
})
</script>

<style scoped>
.error-compact {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem; /* 减小元素间距 */
  padding: 0.75rem 1rem; /* 减小内边距 */
  background-color: var(--color-background);
  border: 1px solid var(--color-danger); /* 直接使用危险色作为边框，更明确 */
  border-radius: 10px;
  margin-bottom: 1.25rem;
  position: relative;
  box-shadow: 0 4px 12px rgba(var(--color-danger-rgb, 220, 53, 69), 0.1); /* 增加与危险色匹配的阴影 */
  animation: slideInCompact 0.3s ease-out;
}

.icon-compact {
  color: var(--color-danger);
  flex-shrink: 0;
  margin-top: 1px;
}

.content-compact {
  flex-grow: 1;
}

.message-compact {
  font-weight: 600;
  color: var(--color-heading);
  font-size: 0.9rem;
  line-height: 1.5;
  margin: 0;
}

.suggestions-compact {
  margin-top: 0.6rem; /* 减小与主信息的间距 */
}

.suggestions-compact ul {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 0.25rem; /* 减小建议之间的间距 */
  font-size: 0.8rem; /* 减小建议的字号 */
  color: var(--color-text-mute);
}

.dismiss-compact {
  background: none;
  border: none;
  border-radius: 50%;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: var(--color-text-mute);
  transition: all 0.2s;
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
}

.dismiss-compact:hover {
  background-color: var(--color-background-mute);
  color: var(--color-danger);
}

@keyframes slideInCompact {
  from {
    opacity: 0;
    transform: translateY(-8px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
