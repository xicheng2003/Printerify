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

      <button @click="toggleSettings" class="settings-toggle-btn" title="展开/折叠设置">
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" :class="{ 'is-expanded': isSettingsExpanded }">
          <polyline points="6 9 12 15 18 9"></polyline>
        </svg>
      </button>
    </div>

    <transition name="slide-fade">
      <div v-show="isSettingsExpanded" class="settings-container">
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

        <div class="remove-button-container">
            <button @click="remove" class="remove-file-btn">
                <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path></svg>
                <span>移除文件</span>
            </button>
        </div>
      </div>
    </transition>

    </div>
</template>

<script setup>
// --- script 部分的代码无需改动，保持原样即可 ---
import { ref } from 'vue';
import { useOrderStore } from '@/stores/order';

const props = defineProps({
  document: {
    type: Object,
    required: true,
  },
});

const orderStore = useOrderStore();
const isSettingsExpanded = ref(true);

function toggleSettings() {
  isSettingsExpanded.value = !isSettingsExpanded.value;
}
function updateSetting(key, value) {
  orderStore.updateDocumentSettings(props.document.id, { [key]: value });
}
function remove() {
  if (confirm(`确定要移除文件 "${props.document.fileName}" 吗？`)) {
    orderStore.removeDocument(props.document.id);
  }
}
function retryUpload() {
  alert('重试功能待开发');
}
</script>

<style scoped>
/* --- 【修改】这里是全新的样式，包含了新的移除按钮样式和布局调整 --- */
.doc-drag-handle {
  cursor: grab; color: #94a3b8; padding-right: 0.75rem; font-size: 1.25rem;
  align-self: flex-start; padding-top: 0.25rem;
}
.doc-drag-handle:active { cursor: grabbing; }

.document-item {
  background-color: #fff; border: 1px solid #e2e8f0; border-radius: 12px;
  padding: 1rem; margin-bottom: 1rem; position: relative;
  transition: box-shadow 0.2s; overflow: hidden;
}
.document-item:hover { border-color: #c7d2fe; }
.document-item.has-error { border-color: #ef4444; background-color: rgba(239, 68, 68, 0.05); }

.file-info { display: flex; align-items: center; gap: 0.5rem; }
.file-icon { font-size: 1.75rem; color: #94a3b8; }
.file-details { flex-grow: 1; }
.file-name { font-weight: 600; color: #1e293b; margin: 0 0 0.25rem 0; }
.file-meta { font-size: 0.875rem; color: #64748b; display: flex; align-items: center; gap: 0.5rem; }
.file-meta strong { color: var(--primary-color); }

.settings-toggle-btn {
  background: transparent; border: none; cursor: pointer; padding: 0.5rem;
  margin-left: auto; border-radius: 50%;
}
.settings-toggle-btn:hover { background-color: #f1f5f9; }
.settings-toggle-btn svg { transition: transform 0.2s ease-in-out; color: #64748b; }
.settings-toggle-btn svg.is-expanded { transform: rotate(180deg); }

.settings-container {
  margin-top: 1rem;
  border-top: 1px solid #f1f5f9;
  padding-top: 1rem;
}

.settings-grid {
  display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 1rem;
}
.settings-grid div { display: flex; flex-direction: column; }
.settings-grid label { font-size: 0.8rem; color: #475569; margin-bottom: 0.375rem; font-weight: 500; }
.settings-grid input, .settings-grid select {
  width: 100%; padding: 0.6rem; border-radius: 8px; border: 1px solid #cbd5e1;
  background-color: #fff; transition: border-color 0.2s, box-shadow 0.2s;
}
.settings-grid input:focus, .settings-grid select:focus {
  outline: none; border-color: var(--primary-color); box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.2);
}

/* 移除按钮的新样式和容器 */
.remove-button-container {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #f1f5f9;
  display: flex;
  justify-content: flex-end; /* 让按钮靠右对齐 */
}
.remove-file-btn {
  display: inline-flex; /* 让图标和文字在同一行 */
  align-items: center;
  gap: 0.5rem;
  background-color: transparent;
  border: 1px solid #e2e8f0;
  color: #ef4444; /* 红色文字，表示危险操作 */
  font-weight: 500;
  padding: 0.4rem 0.8rem;
  font-size: 0.875rem;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s ease;
}
.remove-file-btn:hover {
  background-color: #fef2f2; /* 悬浮时淡红色背景 */
  border-color: #fecaca;
}

/* 动画和响应式样式保持不变 */
.slide-fade-enter-active { transition: all 0.2s ease-out; }
.slide-fade-leave-active { transition: all 0.2s cubic-bezier(1, 0.5, 0.8, 1); }
.slide-fade-enter-from, .slide-fade-leave-to { transform: translateY(-10px); opacity: 0; }

@media (max-width: 767px) {
  .document-item { padding: 0.75rem; }
  .file-name { font-size: 0.9rem; }
  .settings-grid { grid-template-columns: 1fr 1fr; gap: 0.75rem; }
  .settings-grid div:first-child { grid-column: 1 / -1; }
  .settings-grid input, .settings-grid select { padding: 0.5rem; font-size: 0.9rem; }
}

/* 其他已有样式 */
.upload-progress { font-size: 0.875rem; color: #64748b; }
.upload-progress progress { width: 100%; height: 0.5rem; accent-color: var(--primary-color); }
.error-text { font-size: 0.875rem; color: #b91c1c; display: flex; align-items: center; }
.retry-btn { margin-left: 1rem; font-size: 0.75rem; padding: 0.2rem 0.5rem; }
</style>
