import { ref, readonly } from 'vue'
import MarkdownIt from 'markdown-it'

// 创建 Markdown 解析器实例
const md = new MarkdownIt({
  html: true,        // 允许 HTML 标签
  breaks: true,      // 将 \n 转换为 <br>
  linkify: true,     // 自动识别 URL
  typographer: true  // 启用一些语言中立的替换和引号美化
})

// 缓存已加载的 Markdown 内容
const cache = new Map()

/**
 * 用于加载和解析 Markdown 文件的 composable
 * @param {string} filePath - Markdown 文件的路径（相对于 public 目录）
 * @returns {object} 包含渲染内容、加载状态和错误信息
 */
export function useMarkdown(filePath) {
  const content = ref('')
  const loading = ref(false)
  const error = ref(null)

  /**
   * 加载并解析 Markdown 文件
   */
  const loadMarkdown = async () => {
    // 检查缓存
    if (cache.has(filePath)) {
      content.value = cache.get(filePath)
      return
    }

    loading.value = true
    error.value = null

    try {
      const response = await fetch(filePath)

      if (!response.ok) {
        throw new Error(`Failed to load ${filePath}: ${response.statusText}`)
      }

      const markdown = await response.text()

      // 解析 Markdown 为 HTML
      const html = md.render(markdown)

      // 缓存结果
      cache.set(filePath, html)
      content.value = html
    } catch (err) {
      console.error('Error loading markdown:', err)
      error.value = err.message
    } finally {
      loading.value = false
    }
  }

  /**
   * 直接渲染 Markdown 文本（不从文件加载）
   * @param {string} markdownText - Markdown 格式的文本
   */
  const renderMarkdown = (markdownText) => {
    try {
      content.value = md.render(markdownText)
    } catch (err) {
      console.error('Error rendering markdown:', err)
      error.value = err.message
    }
  }

  /**
   * 清除缓存
   */
  const clearCache = () => {
    cache.clear()
  }

  return {
    content: readonly(content),
    loading: readonly(loading),
    error: readonly(error),
    loadMarkdown,
    renderMarkdown,
    clearCache
  }
}
