<template>
  <div
    class="file-uploader"
    :class="[uploadState, { 'is-disabled': disabled }]"
    @dragover.prevent="onDragOver"
    @dragleave.prevent="onDragLeave"
    @drop.prevent="onDrop"
  >
    <label class="uploader-label">
      <div class="icon-wrapper">
        <svg v-if="uploadState === 'idle' || uploadState === 'dragover'" xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="17 8 12 3 7 8"></polyline><line x1="12" y1="3" x2="12" y2="15"></line></svg>
        <div v-if="uploadState === 'loading'" class="spinner"></div>
        <svg v-if="uploadState === 'success'" xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
        <svg v-if="uploadState === 'error'" xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
      </div>
      <span class="uploader-text">{{ message }}</span>
      <p v-if="disabled && uploadState === 'idle'" class="disabled-notice">请先同意下方服务条款和隐私协议</p>
      <input
        type="file"
        @change="handleFileChange"
        accept=".pdf,.doc,.docx,.ppt,.pptx"
        hidden
        :disabled="uploadState === 'loading' || disabled"
        multiple
      />
    </label>
    <div v-if="uploadState === 'loading'" class="progress-bar-container">
        <div class="progress-bar" :style="{ width: uploadProgress + '%' }"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';

const props = defineProps({
  disabled: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['files-selected']);

const uploadState = ref('idle'); // idle, loading, success, error
const uploadedFileName = ref('');
const uploadProgress = ref(0);

const message = computed(() => {
  switch (uploadState.value) {
    case 'loading': return `正在上传: ${uploadProgress.value}%`;
    case 'success': return `文件上传成功: ${uploadedFileName.value}`;
    case 'error': return '上传失败，请点击重试。';
    case 'dragover': return '松开文件以上传';
    case 'idle': default: return '点击此处，或拖拽文件到这里';
  }
});

function handleFileChange(event) {
  if (props.disabled) return;
  const files = event.target.files;
  if (!files || files.length === 0) return;

  emit('files-selected', files);

  event.target.value = '';
}

function onDragOver(e) {
  if (props.disabled) return;
  uploadState.value = 'dragover';
}

function onDragLeave(e) {
  if (props.disabled) return;
  uploadState.value = 'idle';
}

function onDrop(e) {
  if (props.disabled) return;
  const files = e.dataTransfer.files;
  if (!files || files.length === 0) return;
  emit('files-selected', files);
  uploadState.value = 'idle';
}

function reset() {
  uploadState.value = 'idle';
}

defineExpose({
  reset
});
</script>

<style scoped>
/*
  FileUploader.vue 的样式已更新，使用 CSS 变量以支持主题切换。
  所有状态（默认、悬停、成功、失败、禁用）的样式均已适配。
*/
.file-uploader {
  border: 2px dashed var(--color-border); /* 已修改 */
  border-radius: 12px;
  padding: 2rem;
  text-align: center;
  cursor: pointer;
  background-color: var(--color-background-mute); /* 已修改 */
  transition: all 0.3s ease;
  position: relative;
}

.uploader-label {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  cursor: pointer;
}

.file-uploader.is-disabled .uploader-label {
  cursor: not-allowed;
}

.icon-wrapper {
  margin-bottom: 1rem;
}

.icon-wrapper svg {
  color: var(--color-text-mute); /* 已修改 */
  transition: color 0.3s;
}

.uploader-text {
  font-size: 1rem;
  font-weight: 500;
  color: var(--color-text); /* 已修改 */
  transition: color 0.3s;
}

/* --- 状态样式 --- */

.file-uploader:not(.is-disabled):hover {
  border-color: var(--color-primary); /* 已修改 */
}

/* 拖拽高亮样式 */
.file-uploader.dragover {
  border-color: var(--color-primary);
  background-color: rgba(var(--color-primary-rgb, 37, 99, 235), 0.08);
  box-shadow: 0 0 0 2px var(--color-primary);
}

.file-uploader.dragover .icon-wrapper svg,
.file-uploader.dragover .uploader-text {
  color: var(--color-primary);
}

.file-uploader.loading {
  cursor: not-allowed;
  border-color: var(--color-primary); /* 已修改 */
}

.file-uploader.success {
  border-color: var(--color-success); /* 已修改 */
  background-color: rgba(var(--color-success-rgb, 40, 167, 69), 0.1); /* 已修改：使用变量的 RGBA 形式 */
}

.file-uploader.success .icon-wrapper svg,
.file-uploader.success .uploader-text {
  color: var(--color-success); /* 已修改 */
}

.file-uploader.error {
  border-color: var(--color-danger); /* 已修改 */
  background-color: rgba(var(--color-danger-rgb, 220, 53, 69), 0.1); /* 已修改：使用变量的 RGBA 形式 */
}

.file-uploader.error .icon-wrapper svg,
.file-uploader.error .uploader-text {
  color: var(--color-danger); /* 已修改 */
}

.file-uploader.is-disabled {
  background-color: var(--color-background-mute); /* 已修改 */
  opacity: 0.7;
}

.disabled-notice {
  color: var(--color-danger); /* 已修改 */
  font-weight: 600;
  margin-top: 0.5rem;
  font-size: 0.875rem;
}

/* --- 加载动画 --- */
.spinner {
  display: inline-block;
  width: 48px;
  height: 48px;
  border: 4px solid rgba(var(--color-primary-rgb, 37, 99, 235), 0.2); /* 已修改 */
  border-radius: 50%;
  border-top-color: var(--color-primary); /* 已修改 */
  animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* --- 进度条 --- */
.progress-bar-container {
    margin-top: 1rem;
    height: 8px;
    width: 100%;
    background-color: var(--color-border); /* 已修改 */
    border-radius: 4px;
    overflow: hidden;
}

.progress-bar {
    height: 100%;
    background-color: var(--color-primary); /* 已修改 */
    transition: width 0.3s ease-in-out;
}
</style>
