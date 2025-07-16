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
import axios from 'axios'; // 【修改】我们直接使用axios，以保持一致

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

  // 使用 FormData 来包装文件数据
  const formData = new FormData();
  formData.append('file', file);

  try {
    // 【核心修改】调用我们新的、专门的付款凭证上传接口
    const response = await axios.post('/api/upload-payment/', formData, {
      withCredentials: true,
    });

    uploadState.value = 'success';

    // 【核心修改】发出事件，并将后端返回的 screenshot_id 传递出去
    emit('upload-success', response.data.screenshot_id);

  } catch (error) {
    uploadState.value = 'error';
    console.error('Payment screenshot upload failed:', error.response?.data || error);
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
