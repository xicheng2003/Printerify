<template>
  <Transition name="modal-fade">
    <div v-if="show" class="modal-mask" @click.self="$emit('close')">
      <div class="modal-container">
        <!-- 【新增】右上角的关闭按钮 -->
        <button class="close-button" @click="$emit('close')" aria-label="关闭弹窗">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </button>

        <div class="modal-header" v-if="$slots.header">
          <slot name="header">default header</slot>
        </div>

        <div class="modal-body">
          <slot name="body">default body</slot>
        </div>

        <div class="modal-footer" v-if="$slots.footer">
          <slot name="footer">
            <!-- 默认的页脚插槽，包含一个关闭按钮 -->
            <button class="footer-close-btn" @click="$emit('close')"> 关闭 </button>
          </slot>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup>
// Script 部分保持不变
defineProps({
  show: Boolean
})

defineEmits(['close'])
</script>

<style scoped>
/*
  Modal.vue 的样式已完全重写，以支持主题切换并优化视觉效果。
  所有核心功能和插槽均已完整保留。
*/
.modal-mask {
  position: fixed;
  z-index: 9998;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.6); /* 使用半透明黑色作为遮罩 */
  backdrop-filter: blur(4px); /* 添加背景模糊效果，更具现代感 */
  display: flex;
  justify-content: center;
  align-items: center;
  transition: opacity 0.3s ease;
}

.modal-container {
  width: 90%;
  max-width: 600px;
  margin: auto;
  padding: 1.5rem 2rem;
  background-color: var(--color-background-soft); /* 已修改 */
  border-radius: 12px; /* 增加圆角大小 */
  box-shadow: var(--shadow-card); /* 已修改 */
  border: 1px solid var(--color-border); /* 已修改 */
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  max-height: 85vh; /* 限制最大高度 */
  position: relative; /* 为关闭按钮定位 */
}

/* --- 【新增】右上角关闭按钮样式 --- */
.close-button {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: none;
  border: none;
  border-radius: 50%;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: var(--color-text-mute);
  transition: background-color 0.2s, color 0.2s;
}

.close-button:hover {
  background-color: var(--color-background-mute);
  color: var(--color-heading);
}

.modal-header {
  padding-right: 2rem; /* 为关闭按钮留出空间 */
}

.modal-header h3 {
  margin-top: 0;
  margin-bottom: 1rem;
  color: var(--color-heading); /* 已修改 */
  font-size: 1.25rem;
  font-weight: 600;
}

.modal-body {
  margin: 1rem 0;
  overflow-y: auto; /* 让内容可以滚动 */
  color: var(--color-text); /* 已修改 */
  padding-right: 0.5rem; /* 为滚动条留出空间，防止内容紧贴 */
}

/* 自定义滚动条样式 */
.modal-body::-webkit-scrollbar {
  width: 6px;
}
.modal-body::-webkit-scrollbar-track {
  background: transparent;
}
.modal-body::-webkit-scrollbar-thumb {
  background-color: var(--color-border);
  border-radius: 3px;
}
.modal-body::-webkit-scrollbar-thumb:hover {
  background-color: var(--color-border-hover);
}

.modal-footer {
  margin-top: auto; /* 将页脚推到底部 */
  padding-top: 1.5rem;
  text-align: right;
  border-top: 1px solid var(--color-border); /* 已修改 */
}

/* --- 【修复】页脚关闭按钮样式 --- */
.footer-close-btn {
  padding: 0.5rem 1.25rem;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  background-color: var(--color-background-mute); /* 已修改 */
  color: var(--color-text); /* 已修改 */
  border: 1px solid var(--color-border); /* 已修改 */
  transition: background-color 0.2s, border-color 0.2s;
}

.footer-close-btn:hover {
  background-color: var(--color-border);
  border-color: var(--color-border-hover);
}

/* --- 动画效果 --- */
.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}

.modal-fade-enter-from .modal-container,
.modal-fade-leave-to .modal-container {
  transform: scale(0.95) translateY(10px);
}
</style>
