<template>
  <div class="payment-uploader" :class="uploadState">
    <label class="uploader-label">
      <div class="icon-wrapper">
        <svg v-if="uploadState === 'idle'" xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="17 8 12 3 7 8"></polyline><line x1="12" y1="3" x2="12" y2="15"></line></svg>
        <div v-if="uploadState === 'loading'" class="spinner"></div>
        <svg v-if="uploadState === 'success'" xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
        <svg v-if="uploadState === 'error'" xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
      </div>
      <span class="uploader-text">{{ message }}</span>
      <input
        id="payment-input"
        type="file"
        @change="handleFileChange"
        accept="image/png, image/jpeg"
        hidden
        :disabled="uploadState === 'loading'"
      />
    </label>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import api from '@/services/apiService'; // 导入我们的API服务

// **修正 1: 事件名称与 HomeView 保持一致**
// HomeView 期望接收 'upload-success' 事件
const emit = defineEmits(['upload-success']);

const uploadState = ref('idle'); // idle, loading, success, error
const uploadedFileName = ref('');

const message = computed(() => {
  switch (uploadState.value) {
    case 'loading': return '正在上传...';
    case 'success': return `截图上传成功: ${uploadedFileName.value}`;
    case 'error': return '上传失败，请点击重试。';
    case 'idle': default: return '点击此处，上传付款截图';
  }
});

async function handleFileChange(event) {
  const file = event.target.files[0];
  if (!file) return;

  uploadState.value = 'loading';
  uploadedFileName.value = file.name;

  try {
    // **修正 2: 调用正确的 API 函数**
    // 使用通用的 uploadPrintFile 函数，并指明用途为 'PAYMENT'
    const response = await api.uploadPrintFile(file, 'PAYMENT');

    uploadState.value = 'success';

    // **修正 3: 发出 HomeView 期望的数据**
    // HomeView 的 onScreenshotUploaded 函数只期望接收一个参数：上传文件的 ID
    emit('upload-success', response.data.id);

  } catch (error) {
    uploadState.value = 'error';
    console.error('Payment screenshot upload failed:', error);
  }

  event.target.value = '';
}
</script>

<style scoped>
/* 样式保持不变，它们设计得很好 */
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
.uploader-label {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  cursor: pointer;
}
.icon-wrapper {
  margin-bottom: 1rem;
}
.uploader-text {
  font-size: 1rem;
  font-weight: 500;
  color: #595959;
}
.payment-uploader:hover {
  border-color: #007bff;
}
.payment-uploader.loading {
  cursor: not-allowed;
  border-style: solid;
  border-color: #007bff;
}
.payment-uploader.success {
  border-style: solid;
  border-color: #52c41a;
  background-color: #f6ffed;
}
.payment-uploader.success .icon-wrapper svg,
.payment-uploader.success .uploader-text {
  color: #52c41a;
}
.payment-uploader.error {
  border-style: solid;
  border-color: #f5222d;
  background-color: #fff1f0;
}
.payment-uploader.error .icon-wrapper svg,
.payment-uploader.error .uploader-text {
  color: #f5222d;
}
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
