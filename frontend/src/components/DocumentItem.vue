<template>
  <div class="document-item" :class="{ 'has-error': document.error }">
    <!-- 【修改】加载遮罩层现在使用方案一的“图标脉冲效果” -->
    <div v-if="document.isRecalculating" class="recalculating-overlay">
      <!-- 【新增】带有脉冲动画的齿轮 SVG 图标 -->
      <svg class="pulsating-icon" xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M12 20v-4"/><path d="M12 4V2"/><path d="m4.93 4.93 1.41 1.41"/><path d="m17.66 17.66 1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="m4.93 19.07 1.41-1.41"/><path d="m17.66 6.34 1.41-1.41"/>
      </svg>
      <span>重新计价中...</span>
    </div>

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
          <span class="dot-divider">•</span>
          <span
            class="status-badge"
            :class="document.isEstimated ? 'badge-estimated' : 'badge-exact'"
            :title="document.priceNote || (document.isEstimated ? '价格为预估，后台将自动校正' : '价格已精确计算')"
          >{{ document.isEstimated ? '预估' : '精确' }}</span>
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
            <label :for="'sided-' + document.id">单/双面</label>
            <select
              :id="'sided-' + document.id"
              :value="document.settings.printSided"
              @change="updateSetting('printSided', $event.target.value)"
            >
              <option value="single">单面打印</option>
              <option value="double">双面打印</option>
              <option value="single_double">首页单面，内容双面</option>
            </select>
          </div>
          <div>
            <label :for="'color-' + document.id">色彩</label>
            <select
              :id="'color-' + document.id"
              :value="document.settings.colorMode"
              @change="updateSetting('colorMode', $event.target.value)"
            >
              <option value="black_white">黑白</option>
              <!-- 【预留】添加彩色选项 -->
              <!-- <option value="color">彩色</option> -->
              <option value="" disabled>（由于机器限制，仅提供黑白打印）</option>
            </select>
          </div>
          <div>
            <label :for="'paper-' + document.id">纸张尺寸</label>
            <select
              :id="'paper-' + document.id"
              :value="document.settings.paperSize"
              @change="updateSetting('paperSize', $event.target.value)"
            >
              <option value="a4_70g">A4(70g)</option>
              <option value="a4_80g">A4(80g)</option>
              <option value="b5_70g">B5(70g)</option>
              <!-- <option value="a4_80g">（A4(70g) 规格纸张暂时用尽，待补货）</option> -->
              <!-- 【预留】添加更多纸张尺寸选项 -->
              <!-- <option value="a4">（暂时仅支持 A4 规格，后续可能增加 B5 ）</option> -->
              <option value="" disabled>（70g/80g 为纸张克重，数值越大表示纸张更厚）</option>
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
  alert('重试功能待开发。请移除文件后重新上传。');
}
</script>

<style scoped>
.document-item {
  background-color: var(--color-background);
  border: 1px solid var(--color-border);
  border-radius: 12px;
  padding: 1rem;
  margin-bottom: 1rem;
  position: relative;
  transition: box-shadow 0.2s, border-color 0.2s;
  overflow: hidden;
}

/* --- 【修改】加载遮罩样式更新为方案一 --- */
.recalculating-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(var(--color-background-rgb), 0.8);
  backdrop-filter: blur(2px);
  display: flex;
  flex-direction: column; /* 让图标和文字垂直排列 */
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  color: var(--color-text);
  font-weight: 500;
  z-index: 10;
  transition: opacity 0.2s;
  border-radius: 12px; /* 确保遮罩层也有圆角 */
}

/* 【新增】脉冲动画的容器 */
.recalculating-overlay .pulsating-icon {
  width: 28px;
  height: 28px;
  color: var(--color-primary);
  animation: pulse 1.5s infinite cubic-bezier(0.4, 0, 0.6, 1);
}

/* 【新增】定义脉冲动画 */
@keyframes pulse {
  0%, 100% {
    opacity: 1;
    transform: scale(1);
  }
  50% {
    opacity: 0.6;
    transform: scale(1.2);
  }
}

/* --- 原有样式保持不变 --- */
.document-item:hover {
  border-color: var(--color-primary);
}

.document-item.has-error {
  border-color: var(--color-danger);
  background-color: rgba(var(--color-danger-rgb, 220, 53, 69), 0.05);
}

.file-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}


.doc-drag-handle:active {
  cursor: grabbing;
}

.file-icon {
  font-size: 1.5rem;
  color: var(--color-text-mute);
}

.file-details {
  flex-grow: 1;
}

/* 请将 DocumentItem.vue 中 .file-name 的样式替换为以下代码 */
.file-name {
  font-weight: 600;
  color: var(--color-heading);
  margin: 0 0 0.25rem 0;
  word-break: break-word; /* 【修复】允许长文件名换行 */
}

/* 请将 DocumentItem.vue 中 .file-meta 的样式替换为以下代码 */
.file-meta {
  font-size: 0.875rem;
  color: var(--color-text-mute);
  display: flex;
  align-items: center;
  gap: 0.5rem;
  white-space: nowrap; /* 【保持】强制元数据不换行 */
}

.file-meta strong {
  color: var(--color-primary);
}

/* --- 【核心修复】为拖拽手柄和设置按钮应用统一的、居中的样式 --- */
.doc-drag-handle,
.settings-toggle-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  background: transparent;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  padding: 0;
  transition: background-color 0.2s;
}

.settings-toggle-btn:hover {
  background-color: var(--color-background-mute);
}

/* 新增：状态徽章样式 */
.status-badge {
  display: inline-flex;
  align-items: center;
  padding: 0.1rem 0.4rem;
  border-radius: 999px;
  font-size: 0.72rem;
  line-height: 1;
  border: 1px solid transparent;
}
.badge-estimated {
  color: #8a6d3b;
  background: #fcf8e3;
  border-color: #faebcc;
}
.badge-exact {
  color: #2f6b2f;
  background: #e6f4ea;
  border-color: #b7e1c1;
}

.settings-toggle-btn svg {
  transition: transform 0.2s ease-in-out;
  color: var(--color-text-mute);
}

.settings-toggle-btn svg.is-expanded {
  transform: rotate(180deg);
}

.settings-container {
  margin-top: 1rem;
  border-top: 1px solid var(--color-border);
  padding-top: 1rem;
}

.settings-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 1rem;
}

.settings-grid div {
  display: flex;
  flex-direction: column;
}

.settings-grid label {
  font-size: 0.8rem;
  color: var(--color-text);
  margin-bottom: 0.375rem;
  font-weight: 500;
}

/* 小型帮助文本（select 下方的说明） */
.field-help {
  display: block;
  margin-top: 0.375rem;
  font-size: 0.85rem;
  color: var(--color-text-mute);
}

.settings-grid input,
.settings-grid select {
  width: 100%;
  padding: 0.6rem;
  border-radius: 8px;
  border: 1px solid var(--color-border);
  background-color: var(--color-background);
  color: var(--color-text);
  transition: border-color 0.2s, box-shadow 0.2s;
}

.settings-grid input:focus,
.settings-grid select:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 2px rgba(var(--color-primary-rgb, 37, 99, 235), 0.2);
}

.remove-button-container {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid var(--color-border);
  display: flex;
  justify-content: flex-end;
}

.remove-file-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background-color: transparent;
  border: 1px solid var(--color-border);
  color: var(--color-danger);
  font-weight: 500;
  padding: 0.4rem 0.8rem;
  font-size: 0.875rem;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.remove-file-btn:hover {
  background-color: rgba(var(--color-danger-rgb, 220, 53, 69), 0.1);
  border-color: var(--color-danger);
}

.slide-fade-enter-active {
  transition: all 0.2s ease-out;
}

.slide-fade-leave-active {
  transition: all 0.2s cubic-bezier(1, 0.5, 0.8, 1);
}

.slide-fade-enter-from,
.slide-fade-leave-to {
  transform: translateY(-10px);
  opacity: 0;
}

@media (max-width: 767px) {
  .document-item { padding: 0.75rem; }
  .file-name { font-size: 0.9rem; }
  .settings-grid {
    grid-template-columns: 1fr 1fr; /* 每行两列 */
    gap: 0.75rem;
  }
.settings-grid input, .settings-grid select {
padding-top: 0.6rem;
padding-bottom: 0.6rem;
padding-left: 0.5rem;
padding-right: 0.5rem;
font-size: 0.9rem;
height: 2.5rem; /* 设置统一的高度，您可以尝试其他值 */
box-sizing: border-box;
}
}

.upload-progress {
  font-size: 0.875rem;
  color: var(--color-text-mute);
}

.upload-progress progress {
  width: 100%;
  height: 0.5rem;
  accent-color: var(--color-primary);
}

.error-text {
  font-size: 0.875rem;
  color: var(--color-danger);
  display: flex;
  align-items: center;
}

.retry-btn {
  margin-left: 1rem;
  font-size: 0.75rem;
  font-weight: 500;
  padding: 0.2rem 0.6rem;
  border-radius: 6px;
  cursor: pointer;
  border: 1px solid var(--color-danger);
  background-color: transparent;
  color: var(--color-danger);
  transition: all 0.2s ease;
}

.retry-btn:hover {
  background-color: rgba(var(--color-danger-rgb, 220, 53, 69), 0.1);
}
</style>
