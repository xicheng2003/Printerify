<template>
  <div class="file-uploader" :class="uploadState">
    <label class="uploader-label">
      <div class="icon-wrapper">
        <svg v-if="uploadState === 'idle'" xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="17 8 12 3 7 8"></polyline><line x1="12" y1="3" x2="12" y2="15"></line></svg>
        <div v-if="uploadState === 'loading'" class="spinner"></div>
        <svg v-if="uploadState === 'success'" xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
        <svg v-if="uploadState === 'error'" xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
      </div>
      <span class="uploader-text">{{ message }}</span>
      <input
        type="file"
        @change="handleFileChange"
        accept=".pdf,.doc,.docx,.ppt,.pptx"
        hidden
        :disabled="uploadState === 'loading'"
      />
    </label>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import api from '@/services/apiService';

const emit = defineEmits(['upload-success']);

const uploadState = ref('idle'); // idle, loading, success, error
const uploadedFileName = ref('');
let originalFile = null; // Variable to store the original file object

const message = computed(() => {
  switch (uploadState.value) {
    case 'loading': return '正在上传...';
    case 'success': return `文件上传成功: ${uploadedFileName.value}`;
    case 'error': return '上传失败，请点击重试。';
    case 'idle': default: return '点击此处，或拖拽文件到这里';
  }
});

async function handleFileChange(event) {
  const file = event.target.files[0];
  if (!file) return;

  originalFile = file; // Store the file object for later use
  uploadState.value = 'loading';
  uploadedFileName.value = file.name;

  try {
    // Assuming your apiService has an `uploadPrintFile` method
    const response = await api.uploadPrintFile(file, 'PRINT');

    uploadState.value = 'success';

    // *** THE FIX IS HERE ***
    // Create a payload object that includes both the ID and the original file
    const payload = {
      id: response.data.id,
      file: originalFile,
    };
    // Emit the complete payload object
    emit('upload-success', payload);

  } catch (error) {
    uploadState.value = 'error';
    console.error("File upload failed:", error);
  }

  event.target.value = ''; // Clear input to allow re-uploading the same file
}

// The reset method that HomeView can call
function reset() {
  uploadState.value = 'idle';
  uploadedFileName.value = '';
  originalFile = null;
}

// Expose the reset method to the parent component
defineExpose({
  reset
});
</script>

<style scoped>
/* Styles are kept the same as they are well-designed */
.file-uploader {
  border: 2px dashed #d9d9d9;
  border-radius: 12px;
  padding: 2rem;
  text-align: center;
  cursor: pointer;
  background-color: #fafafa;
  transition: all 0.3s ease;
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
.icon-wrapper svg { color: #8c8c8c; }
.uploader-text { font-size: 1rem; font-weight: 500; color: #595959; }
.file-uploader:hover { border-color: #007bff; }
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
</style>
