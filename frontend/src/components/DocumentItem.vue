<template>
  <div class="document-item" :class="{ 'has-error': document.error }">
    <div class="file-info">
      <span class="doc-drag-handle" title="拖拽此文件可调整组内顺序">⠿</span>
      <span class="file-icon">📄</span>
      <div class="file-details">
        <p class="file-name">{{ document.fileName }}</p>
        <div v-if="document.isUploading" class="upload-progress">
          <progress :value="document.uploadProgress" max="100"></progress>
          <span>上传中... {{ document.uploadProgress }}%</span>
        </div>
        <div v-else-if="document.error" class="error-text">
          <span>错误: {{ document.error }}</span>
          <button @click="retryUpload" class="retry-btn">重试</button>
        </div>
         <div v-else class="file-meta">
          <span>{{ document.pageCount }} 页</span>
          <span class="dot-divider">•</span>
          <span>打印费: <strong>¥{{ Number(document.printCost).toFixed(2) }}</strong></span>
        </div>
      </div>
    </div>

    <div class="settings-grid">
      <div>
        <label :for="'copies-' + document.id">份数</label>
        <input
          type="number"
          :id="'copies-' + document.id"
          :value="document.settings.copies"
          @change="updateSetting('copies', $event.target.valueAsNumber)"
          min="1"
        />
      </div>
      <div>
        <label :for="'color-' + document.id">色彩</label>
        <select
          :id="'color-' + document.id"
          :value="document.settings.colorMode"
          @change="updateSetting('colorMode', $event.target.value)"
        >
          <option value="black_white">黑白</option>
          <option value="color">彩色</option>
        </select>
      </div>
      <div>
        <label :for="'sided-' + document.id">单/双面</label>
        <select
          :id="'sided-' + document.id"
          :value="document.settings.printSided"
          @change="updateSetting('printSided', $event.target.value)"
        >
          <option value="single">单面打印</option>
          <option value="double">双面打印</option>
        </select>
      </div>
    </div>

    <button @click="remove" class="remove-btn">×</button>

    <div v-if="document.isCalculatingPrice" class="loading-overlay">
      <span>重新计价中...</span>
    </div>
  </div>
</template>

<script setup>
import { useOrderStore } from '@/stores/order';

const props = defineProps({
  document: {
    type: Object,
    required: true,
  },
});

const orderStore = useOrderStore();

function updateSetting(key, value) {
  orderStore.updateDocumentSettings(props.document.id, { [key]: value });
}

function remove() {
  if (confirm(`确定要移除文件 "${props.document.fileName}" 吗？`)) {
    orderStore.removeDocument(props.document.id);
  }
}

function retryUpload() {
  // 【待办】这个重试逻辑需要在 store 中实现
  // orderStore.retryUpload(props.document.id);
  alert('重试功能待开发');
}
</script>

<style scoped>
/* 【新增】文件拖拽手柄的样式 */
.doc-drag-handle {
  cursor: grab;
  color: #94a3b8;
  padding-right: 0.75rem;
  font-size: 1.25rem;
}
.doc-drag-handle:active {
  cursor: grabbing;
}
.document-item {
  background-color: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 12px; /* 更大的圆角 */
  padding: 1rem;
  margin-bottom: 1rem;
  position: relative;
  transition: box-shadow 0.2s;
  overflow: hidden; /* 用于 loading-overlay */
}
.document-item:hover {
  border-color: #c7d2fe; /* 延续您 payment-method-selector 的悬浮效果 */
}
.document-item.has-error {
  border-color: #ef4444; /* 延续您 error-message 的颜色 */
  background-color: rgba(239, 68, 68, 0.05);
}
.file-info { display: flex; align-items: center; margin-bottom: 1rem; }
.file-icon { font-size: 1.75rem; margin-right: 1rem; color: #94a3b8; }
.file-details { flex-grow: 1; }
.file-name {
  font-weight: 600;
  color: #1e293b; /* 延续您 hero-section h2 的颜色 */
  margin: 0 0 0.25rem 0;
}
.file-meta { font-size: 0.875rem; color: #64748b; display: flex; align-items: center; gap: 0.5rem; }
.file-meta strong { color: var(--primary-color); }

.settings-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); /* 更好的响应式 */
  gap: 1rem;
  border-top: 1px solid #f1f5f9;
  padding-top: 1rem;
}
.settings-grid div { display: flex; flex-direction: column; }
.settings-grid label {
  font-size: 0.8rem;
  color: #475569;
  margin-bottom: 0.375rem;
  font-weight: 500;
}
.settings-grid input, .settings-grid select {
  width: 100%;
  padding: 0.6rem;
  border-radius: 8px;
  border: 1px solid #cbd5e1;
  background-color: #fff;
  transition: border-color 0.2s, box-shadow 0.2s;
}
.settings-grid input:focus, .settings-grid select:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.2);
}

.remove-btn {
  position: absolute;
  top: 0.75rem;
  right: 0.75rem;
  border: none;
  background: transparent;
  color: #94a3b8;
  font-size: 1.5rem;
  cursor: pointer;
  padding: 0.25rem;
  line-height: 1;
  border-radius: 50%;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.remove-btn:hover { color: #ef4444; background-color: rgba(239, 68, 68, 0.1); }

.loading-overlay {
  position: absolute; top: 0; left: 0; right: 0; bottom: 0;
  background-color: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(2px);
  display: flex; justify-content: center; align-items: center;
  border-radius: 12px;
  color: var(--primary-color); font-weight: 500;
}

/* 延续您原有的其他风格 */
.upload-progress { font-size: 0.875rem; color: #64748b; }
.upload-progress progress { width: 100%; height: 0.5rem; accent-color: var(--primary-color); }
.error-text { font-size: 0.875rem; color: #b91c1c; display: flex; align-items: center; }
.retry-btn { margin-left: 1rem; font-size: 0.75rem; padding: 0.2rem 0.5rem; }
</style>
