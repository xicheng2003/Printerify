<template>
  <div
    class="file-uploader"
    :class="[uploadState, { 'is-disabled': disabled }]"
  >
    <label class="uploader-label">
      <div class="icon-wrapper">
        <svg v-if="uploadState === 'idle'" xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="17 8 12 3 7 8"></polyline><line x1="12" y1="3" x2="12" y2="15"></line></svg>
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
      />
    </label>
    <div v-if="uploadState === 'loading'" class="progress-bar-container">
        <div class="progress-bar" :style="{ width: uploadProgress + '%' }"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import api from '@/services/apiService';

const props = defineProps({
  disabled: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['upload-success']);

const uploadState = ref('idle'); // idle, loading, success, error
const uploadedFileName = ref('');
const uploadProgress = ref(0);
let originalFile = null;

const message = computed(() => {
  switch (uploadState.value) {
    case 'loading': return `正在上传: ${uploadProgress.value}%`;
    case 'success': return `文件上传成功: ${uploadedFileName.value}`;
    case 'error': return '上传失败，请点击重试。';
    case 'idle': default: return '点击此处，或拖拽文件到这里';
  }
});

async function handleFileChange(event) {
  if (props.disabled) return;

  const file = event.target.files[0];
  if (!file) return;

  originalFile = file;
  uploadState.value = 'loading';
  uploadedFileName.value = file.name;
  uploadProgress.value = 0;

  try {
    const response = await api.uploadPrintFile(
      file,
      'PRINT',
      (progressEvent) => {
        uploadProgress.value = Math.round((progressEvent.loaded * 100) / progressEvent.total);
      }
    );

    uploadState.value = 'success';

    const payload = {
      id: response.data.id,
      file: originalFile,
    };
    emit('upload-success', payload);

  } catch (error) {
    uploadState.value = 'error';
    console.error("File upload failed:", error);
  }

  event.target.value = '';
}

function reset() {
  uploadState.value = 'idle';
  uploadedFileName.value = '';
  originalFile = null;
  uploadProgress.value = 0;
}

defineExpose({
  reset
});
</script>

<style scoped>
.file-uploader {
  border: 2px dashed #d9d9d9;
  border-radius: 12px;
  padding: 2rem;
  text-align: center;
  cursor: pointer;
  background-color: #fafafa;
  transition: all 0.3s ease;
  position: relative; /* For positioning the notice */
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
.icon-wrapper svg { color: #8c8c8c; }
.uploader-text { font-size: 1rem; font-weight: 500; color: #595959; }
.file-uploader:not(.is-disabled):hover { border-color: #007bff; }
.file-uploader.loading { cursor: not-allowed; border-color: #007bff; }
.file-uploader.success { border-color: #52c41a; background-color: #f6ffed; }
.file-uploader.success .icon-wrapper svg,
.file-uploader.success .uploader-text { color: #52c41a; }
.file-uploader.error { border-color: #f5222d; background-color: #fff1f0; }
.file-uploader.error .icon-wrapper svg,
.file-uploader.error .uploader-text { color: #f5222d; }
.spinner {
  display: inline-block;
  width: 48px;
  height: 48px;
  border: 4px solid rgba(0, 123, 255, 0.2);
  border-radius: 50%;
  border-top-color: #007bff;
  animation: spin 1s ease-in-out infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }
.progress-bar-container {
    margin-top: 1rem;
    height: 8px;
    width: 100%;
    background-color: #e9ecef;
    border-radius: 4px;
    overflow: hidden;
}
.progress-bar {
    height: 100%;
    background-color: var(--primary-color);
    transition: width 0.3s ease-in-out;
}
.file-uploader.is-disabled {
  background-color: #f3f4f6;
  opacity: 0.7;
}
.disabled-notice {
  color: #ef4444;
  font-weight: 600;
  margin-top: 0.5rem;
  font-size: 0.875rem;
}
</style>
