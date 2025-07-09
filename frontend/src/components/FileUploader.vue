<script setup>
import { ref, computed } from 'vue';
import api from '@/services/apiService'; // 假设apiService已封装好

const emit = defineEmits(['upload-success', 'upload-start', 'upload-error']);

const uploadState = ref('idle'); // idle, uploading, success, error
const uploadProgress = ref(0);
const fileName = ref('');
const errorMessage = ref('');

const containerClass = computed(() => `uploader-wrapper ${uploadState.value}`);

async function handleFileChange(event) {
  const file = event.target.files[0];
  if (!file) return;

  fileName.value = file.name;
  uploadState.value = 'uploading';
  uploadProgress.value = 0;
  errorMessage.value = '';
  emit('upload-start');

  try {
    // 使用axios的onUploadProgress来获取实时进度
    const config = {
      onUploadProgress: progressEvent => {
        const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
        uploadProgress.value = percentCompleted;
      }
    };

    // 我们需要一个新的API服务函数来支持这个配置
    const response = await api.uploadFileWithProgress(file, 'PRINT', config);

    uploadState.value = 'success';
    emit('upload-success', { id: response.data.id, file: file }); // 传递文件ID和文件对象

  } catch (error) {
    uploadState.value = 'error';
    errorMessage.value = '上传失败，请检查文件或网络。';
    emit('upload-error', error);
    console.error(error);
  } finally {
    event.target.value = ''; // 重置input以便可以重新上传同一个文件
  }
}

function reset() {
  uploadState.value = 'idle';
  fileName.value = '';
  uploadProgress.value = 0;
}

defineExpose({ reset }); // 允许父组件调用reset方法
</script>

<template>
  <div :class="containerClass">
    <div v-if="uploadState === 'idle' || uploadState === 'error'">
      <label for="file-input" class="file-label">
        <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="17 8 12 3 7 8"></polyline><line x1="12" y1="3" x2="12" y2="15"></line></svg>
        <span>点击选择或拖拽文件到此处</span>
        <p v-if="errorMessage" class="error-text">{{ errorMessage }}</p>
      </label>
      <input id="file-input" type="file" @change="handleFileChange" hidden />
    </div>

    <div v-else class="progress-view">
      <div class="file-info">
        <span class="file-name">{{ fileName }}</span>
        <span v-if="uploadState === 'success'" class="status-icon">✓</span>
      </div>
      <div class="progress-bar-container">
        <div class="progress-bar" :style="{ width: uploadProgress + '%' }"></div>
      </div>
      <div class="progress-text">
        <span v-if="uploadState === 'uploading'">正在上传... {{ uploadProgress }}%</span>
        <span v-if="uploadState === 'success'">上传完成！</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.uploader-wrapper {
  border: 2px dashed #d9d9d9;
  border-radius: 8px;
  padding: 2rem;
  transition: border-color 0.3s;
}
.uploader-wrapper:hover, .uploader-wrapper.uploading {
  border-color: #007bff;
}
.uploader-wrapper.error {
  border-color: #dc3545;
}
.file-label {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  cursor: pointer;
  color: #555;
}
.error-text {
  color: #dc3545;
  font-weight: 500;
  margin: 0;
}
.progress-view {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}
.file-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.file-name {
  font-weight: 500;
}
.status-icon {
  color: #28a745;
  font-weight: bold;
}
.progress-bar-container {
  width: 100%;
  height: 10px;
  background-color: #e9ecef;
  border-radius: 5px;
  overflow: hidden;
}
.progress-bar {
  height: 100%;
  background-color: #007bff;
  transition: width 0.2s linear;
}
.progress-text {
  font-size: 0.9rem;
  color: #6c757d;
}
</style>
