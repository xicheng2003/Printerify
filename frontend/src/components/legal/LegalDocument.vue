<template>
  <div class="legal-document">
    <!-- 加载状态 -->
    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>加载中...</p>
    </div>

    <!-- 错误状态 -->
    <div v-else-if="error" class="error-state">
      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="10"></circle>
        <line x1="12" y1="8" x2="12" y2="12"></line>
        <line x1="12" y1="16" x2="12.01" y2="16"></line>
      </svg>
      <p>{{ error }}</p>
    </div>

    <!-- 文档内容 -->
    <div
      v-else
      :class="['legal-content', styleClass]"
      v-html="displayContent"
    ></div>
  </div>
</template>

<script setup>
import { computed, onMounted, watch } from 'vue'
import { useMarkdown } from '@/composables/useMarkdown'

const props = defineProps({
  /**
   * 文档类型：'terms' (服务条款) 或 'privacy' (隐私协议)
   */
  type: {
    type: String,
    required: true,
    validator: (value) => ['terms', 'privacy'].includes(value)
  },

  /**
   * 样式模式：'full' (完整版) 或 'compact' (紧凑版，用于 Modal)
   */
  mode: {
    type: String,
    default: 'full',
    validator: (value) => ['full', 'compact'].includes(value)
  },

  /**
   * 可选：直接传入 HTML 内容（如果提供，则不从文件加载）
   */
  htmlContent: {
    type: String,
    default: null
  }
})

// 文件路径映射
const filePathMap = {
  terms: '/legal/terms-of-service.md',
  privacy: '/legal/privacy-policy.md'
}

// 使用 Markdown composable
const { content, loading, error, loadMarkdown } = useMarkdown(filePathMap[props.type])

// 计算显示内容
const displayContent = computed(() => {
  // 如果直接传入了 HTML 内容，使用传入的内容
  if (props.htmlContent) {
    return props.htmlContent
  }
  // 否则使用从 Markdown 加载的内容
  return content.value
})

// 计算样式类
const styleClass = computed(() => {
  return props.mode === 'compact' ? 'compact-mode' : 'full-mode'
})

// 组件挂载时加载内容（如果没有直接传入 HTML）
onMounted(() => {
  if (!props.htmlContent) {
    loadMarkdown()
  }
})

// 监听 type 变化，重新加载
watch(() => props.type, () => {
  if (!props.htmlContent) {
    loadMarkdown()
  }
})
</script>

<style scoped>
.legal-document {
  width: 100%;
}

/* 加载状态 */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem 1rem;
  color: var(--color-text-mute);
}

.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid rgba(var(--color-primary-rgb, 37, 99, 235), 0.2);
  border-top-color: var(--color-primary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* 错误状态 */
.error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem 1rem;
  color: var(--color-danger);
  text-align: center;
}

.error-state svg {
  margin-bottom: 1rem;
}

/* 法律文档内容样式 */
.legal-content {
  font-family: inherit;
  line-height: 1.7;
  color: var(--color-text);
}

/* 完整模式（用于关于页面） */
.legal-content.full-mode {
  font-size: 1rem;
}

/* 紧凑模式（用于 Modal） */
.legal-content.compact-mode {
  font-size: 0.9rem;
}

/* Markdown 渲染后的元素样式 */
.legal-content :deep(h1),
.legal-content :deep(h2) {
  font-size: 1.5rem;
  font-weight: 600;
  margin-top: 2em;
  margin-bottom: 0.75em;
  color: var(--color-heading);
  border-bottom: 1px solid var(--color-border);
  padding-bottom: 0.5em;
}

.legal-content :deep(h3) {
  font-size: 1.2rem;
  font-weight: 600;
  margin-top: 1.5em;
  margin-bottom: 0.5em;
  color: var(--color-heading);
}

.legal-content :deep(h4) {
  font-size: 1.1rem;
  font-weight: 600;
  margin-top: 1.5em;
  margin-bottom: 0.5em;
  color: var(--color-heading);
}

.legal-content :deep(p) {
  margin-bottom: 1em;
  text-align: justify;
}

.legal-content :deep(p:first-child) {
  margin-top: 0;
}

.legal-content :deep(strong) {
  font-weight: 600;
  color: var(--color-heading);
}

.legal-content :deep(ul),
.legal-content :deep(ol) {
  margin-bottom: 1em;
  padding-left: 2em;
}

.legal-content :deep(li) {
  margin-bottom: 0.5em;
}

.legal-content :deep(a) {
  color: var(--color-primary);
  text-decoration: underline;
}

.legal-content :deep(a:hover) {
  color: var(--color-primary);
  opacity: 0.8;
}

.legal-content :deep(code) {
  background-color: var(--color-background-mute);
  padding: 0.2em 0.4em;
  border-radius: 3px;
  font-family: 'Courier New', monospace;
  font-size: 0.9em;
}

.legal-content :deep(blockquote) {
  border-left: 4px solid var(--color-primary);
  padding-left: 1em;
  margin: 1em 0;
  color: var(--color-text-mute);
  font-style: italic;
}

/* 紧凑模式的特殊调整 */
.legal-content.compact-mode :deep(h1),
.legal-content.compact-mode :deep(h2) {
  font-size: 1.3rem;
  margin-top: 1.5em;
}

.legal-content.compact-mode :deep(h3) {
  font-size: 1.1rem;
  margin-top: 1.2em;
}

.legal-content.compact-mode :deep(h4) {
  font-size: 1rem;
  margin-top: 1em;
}

/* 响应式调整 */
@media (max-width: 767px) {
  .legal-content.full-mode {
    font-size: 0.95rem;
  }

  .legal-content.compact-mode {
    font-size: 0.85rem;
  }

  .legal-content :deep(h1),
  .legal-content :deep(h2) {
    font-size: 1.3rem;
  }

  .legal-content :deep(h3) {
    font-size: 1.1rem;
  }
}
</style>
