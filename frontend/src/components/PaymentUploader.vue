<script setup>
import { ref, computed } from 'vue';
import api from '@/services/apiService'; // 导入我们的API服务

const emit = defineEmits(['upload-success']);

const uploadState = ref('idle'); // idle, loading, success, error
const uploadedFileName = ref('');

const message = computed(() => {
  // ... (message的computed逻辑保持不变) ...
  switch (uploadState.value) {
    case 'loading': return '正在上传截图...';
    case 'success': return `上传成功: ${uploadedFileName.value}`;
    case 'error': return '上传失败，请点击重试。';
    case 'idle': default: return '点击此处，上传付款截图';
  }
});

async function handleFileChange(event) {
  const file = event.target.files[0]; // 1. 获取到原始的文件对象
  if (!file) return;

  uploadState.value = 'loading';
  uploadedFileName.value = file.name;

  try {
    // 2. 将原始的 file 对象和用途字符串 'PAYMENT' 直接传递给 apiService
    const response = await api.uploadPrintFile(file, 'PAYMENT');

    uploadState.value = 'success';
    emit('upload-success', response.data.id);
  } catch (error) {
    uploadState.value = 'error';
    console.error(error); // 打印详细错误，以便进一步调试
  }

  event.target.value = '';
}
</script>

<template>
  <div class="payment-uploader" :class="uploadState">
    <label for="payment-input" class="uploader-label">
      <div class="icon-wrapper">
        <svg v-if="uploadState === 'idle'" xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="17 8 12 3 7 8"></polyline><line x1="12" y1="3" x2="12" y2="15"></line></svg>
        <div v-if="uploadState === 'loading'" class="spinner"></div>
        <svg v-if="uploadState === 'success'" xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
        <svg v-if="uploadState === 'error'" xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
      </div>
      <span class="uploader-text">{{ message }}</span>
    </label>
    <input
      id="payment-input"
      type="file"
      @change="handleFileChange"
      accept="image/png, image/jpeg"
      hidden
      :disabled="uploadState === 'loading'"
    />
  </div>
</template>

<style scoped>
/* 根容器样式 */
.payment-uploader {
  border: 2px dashed #d9d9d9;
  border-radius: 12px;
  padding: 2rem;
  text-align: center;
  cursor: pointer;
  background-color: #fafafa;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  margin-top: 1rem;
}

/* 标签作为主要交互元素 */
.uploader-label {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  cursor: pointer;
}

/* 图标容器 */
.icon-wrapper {
  margin-bottom: 1rem;
  transition: transform 0.3s ease;
}
.icon-wrapper svg {
  color: #8c8c8c;
  transition: color 0.3s ease;
}

/* 状态文字 */
.uploader-text {
  font-size: 1rem;
  font-weight: 500;
  color: #595959;
  transition: color 0.3s ease;
}

/* --- 状态变化 --- */

/* 悬停状态 */
.payment-uploader:hover {
  border-color: #007bff;
}
.payment-uploader:hover .icon-wrapper svg,
.payment-uploader:hover .uploader-text {
  color: #007bff;
}

/* 加载状态 */
.payment-uploader.loading {
  cursor: not-allowed;
  border-style: solid;
  border-color: #007bff;
  background-color: #f5faff;
}
.payment-uploader.loading .uploader-text {
  color: #007bff;
}

/* 成功状态 */
.payment-uploader.success {
  border-style: solid;
  border-color: #52c41a;
  background-color: #f6ffed;
}
.payment-uploader.success .icon-wrapper svg,
.payment-uploader.success .uploader-text {
  color: #52c41a;
}

/* 失败状态 */
.payment-uploader.error {
  border-style: solid;
  border-color: #f5222d;
  background-color: #fff1f0;
}
.payment-uploader.error .icon-wrapper svg,
.payment-uploader.error .uploader-text {
  color: #f5222d;
}


/* 加载动画 Spinner */
.spinner {
  display: inline-block;
  width: 48px;
  height: 48px;
  border: 4px solid rgba(0, 123, 255, 0.2);
  border-radius: 50%;
  border-top-color: #007bff;
  animation: spin 1s ease-in-out infinite;
}
@keyframes spin {
  to { transform: rotate(360deg); }
}

</style>
