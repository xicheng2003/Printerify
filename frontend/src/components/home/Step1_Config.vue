<template>
  <div>
    <h3 class="step-title">第一步：上传文档并设置规格</h3>

    <div class="billing-info-trigger" @click="$emit('show-billing')">
      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg>
      <span>计费规则说明</span>
    </div>

    <div class="upload-notice" v-if="orderStore.groups.length === 0">
      <p><strong>上传须知</strong></p>
      <ul>
        <li><strong>格式推荐</strong>: 为确保打印效果与排版格式一致，强烈建议您上传 <strong>PDF</strong> 格式的文档。</li>
        <li><strong>文件大小</strong>: 单个文件大小建议不超过 <strong>100MB</strong>，最大支持 200MB。大文件上传时间较长，请耐心等待。</li>
        <li><strong>隐私安全</strong>: 所有文件将通过加密通道上传，并存储在专用服务器上。打印完成后，您的文件将被<strong>立即销毁</strong>，绝不外泄。</li>
        <li><strong>合规声明</strong>: 请遵守相关法律法规，<strong>严禁上传</strong>任何涉密、涉政及其他违禁内容的文件。</li>
      </ul>
    </div>

    <FileUploader ref="uploaderRef" @files-selected="handleFilesSelected" :disabled="!agreedToTerms || !agreedToPrivacy" />

    <transition name="fade">
      <div v-if="orderStore.groups.length > 0 && isBindingHelpVisible" class="binding-help-alert">
        <div class="help-alert-content">
          <div class="help-alert-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg>
          </div>
          <div class="help-alert-text">
            <strong>装订组使用技巧：</strong>
            <ul>
              <li>
                <strong>合并装订：</strong>新上传时，每个文件都是独立的"装订组"。如需将多个文件装订在一起，请按住组标题旁的 <span>⠿</span> 拖拽，并覆盖到另一组上即可合并。
              </li>
              <li>
                <strong>调整顺序：</strong>当您为合并后的组选择了任意一项装订服务后，组内文件的从上到下顺序即为最终的打印和装订顺序。您可以按住单个文件左侧的 <span>⠿</span> 上下拖拽，自由调整它们的打印顺序。
              </li>
            </ul>
          </div>
        </div>
        <button @click="dismissBindingHelp" class="help-alert-close-btn" title="关闭提示">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
        </button>
      </div>
    </transition>

    <OrderConfiguration v-if="orderStore.groups.length > 0" />

    <div class="terms-agreement">
      <div class="terms-item">
        <input type="checkbox" id="terms-step1" :checked="agreedToTerms" @change="$emit('update:agreedToTerms', $event.target.checked)" />
        <label for="terms-step1">
          我已阅读并同意
          <a href="#" @click.prevent="$emit('open-terms')" class="terms-link">
            《服务条款》
            <span v-if="hasLegalUpdate" class="update-dot" title="条款已于2025年10月21日更新"></span>
          </a>
        </label>
      </div>
      <div class="terms-item">
        <input type="checkbox" id="privacy-step1" :checked="agreedToPrivacy" @change="$emit('update:agreedToPrivacy', $event.target.checked)" />
        <label for="privacy-step1">
          我已阅读并同意
          <a href="#" @click.prevent="$emit('open-privacy')" class="terms-link">
            《隐私协议》
            <span v-if="hasLegalUpdate" class="update-dot" title="协议已于2025年10月21日更新"></span>
          </a>
        </label>
      </div>
    </div>

    <BaseButton
      v-if="orderStore.groups.length > 0"
      @click="goNext"
      :disabled="!isReadyToGoNext"
      :loading="!orderStore.isReadyToSubmit"
      class="full-width-btn"
      style="margin-top: 2rem;"
    >
      <span>{{ nextStepButtonText }}</span>
    </BaseButton>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useOrderStore } from '@/stores/order';
import FileUploader from '@/components/FileUploader.vue';
import OrderConfiguration from '@/components/OrderConfiguration.vue';
import BaseButton from '@/components/BaseButton.vue';

const props = defineProps({
  agreedToTerms: { type: Boolean, required: true },
  agreedToPrivacy: { type: Boolean, required: true },
});
const emits = defineEmits(['update:agreedToTerms', 'update:agreedToPrivacy', 'next', 'open-terms', 'open-privacy', 'show-billing']);

const uploaderRef = ref(null);
const orderStore = useOrderStore();
const isBindingHelpVisible = ref(true);

function handleFilesSelected(files) {
  orderStore.addFiles(files);
}

function dismissBindingHelp() {
  isBindingHelpVisible.value = false;
}

const hasLegalUpdate = computed(() => {
  const lastViewedDate = localStorage.getItem('legalDocsLastViewed');
  return !lastViewedDate || lastViewedDate < '2025-10-21';
});

const isReadyToGoNext = computed(() => orderStore.isReadyToSubmit && props.agreedToTerms && props.agreedToPrivacy);

const nextStepButtonText = computed(() => {
  if (!props.agreedToTerms || !props.agreedToPrivacy) return '请先同意服务条款和隐私协议';
  if (!orderStore.isReadyToSubmit) return '处理文件中...';
  return `下一步，确认订单 (总计 ¥${orderStore.totalCost})`;
});

function goNext() {
  emits('next');
}

defineExpose({
  reset() {
    if (uploaderRef.value && uploaderRef.value.reset) uploaderRef.value.reset();
  }
});
</script>

<style scoped>
.step-title {
  font-size: 1.5rem;
  font-weight: 600;
  text-align: center;
  margin-bottom: 2rem;
  color: var(--color-heading);
}

.billing-info-trigger {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  color: var(--color-text-mute);
  font-size: 0.9rem;
  margin-bottom: 2rem;
  cursor: pointer;
  transition: color 0.2s;
}

.billing-info-trigger:hover {
  color: var(--color-primary);
}

.billing-info-trigger svg {
  margin-top: -2px;
}

.upload-notice {
  background-color: var(--color-background-mute);
  border: 1px solid var(--color-border);
  border-radius: 8px;
  padding: 1rem 1.5rem;
  margin-bottom: 2rem;
  font-size: 0.9rem;
  color: var(--color-text);
}

.upload-notice p {
  margin: 0 0 0.75rem 0;
  font-weight: 500;
  color: var(--color-heading);
}

.upload-notice p strong {
  font-weight: 700;
}

.upload-notice ul {
  list-style-type: none;
  padding-left: 0;
}

.upload-notice li {
  margin-bottom: 0.75rem;
  position: relative;
  padding-left: 1.25rem;
  font-weight: 500;
  line-height: 1.6;
}

.upload-notice li::before {
  content: '•';
  color: var(--color-primary);
  font-weight: bold;
  display: inline-block;
  position: absolute;
  left: 0;
  top: 0;
}

.upload-notice li:last-child {
  margin-bottom: 0;
}

.upload-notice li strong {
  color: var(--color-primary);
  font-weight: 600;
}

.binding-help-alert {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  background-color: rgba(var(--color-primary-rgb, 37, 99, 235), 0.08);
  border: 1px solid rgba(var(--color-primary-rgb, 37, 99, 235), 0.2);
  border-radius: 12px;
  padding: 1rem;
  margin-top: 2rem;
  margin-bottom: 1.5rem;
}

.help-alert-content {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
}

.help-alert-icon {
  color: var(--color-primary);
  flex-shrink: 0;
  margin-top: 2px;
}

.help-alert-close-btn {
  background: none;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  padding: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-text-mute);
  transition: background-color 0.2s, color 0.2s;
  flex-shrink: 0;
}

.help-alert-close-btn:hover {
  background-color: var(--color-background-mute);
  color: var(--color-text);
}

.help-alert-text strong {
  font-weight: 600;
  color: var(--color-heading);
  display: block;
  margin-bottom: 0.5rem;
}

.help-alert-text p,
.help-alert-text ul {
  font-size: 0.9rem;
  color: var(--color-text);
  margin: 0;
  line-height: 1.6;
  padding-left: 0.1em;
}

.help-alert-text li {
  margin-bottom: 0.5rem;
}

.help-alert-text li:last-child {
  margin-bottom: 0;
  padding-left: 0;
}

.help-alert-text li::marker {
  color: var(--color-primary);
}

.help-alert-text li strong {
  display: inline;
  margin-bottom: 0;
}

.help-alert-text span {
  font-family: monospace;
  background-color: var(--color-border);
  padding: 0 4px;
  border-radius: 3px;
  font-weight: 600;
  display: inline-block;
  line-height: 1;
}

.terms-agreement {
  font-size: 0.9rem;
  color: var(--color-text-mute);
  margin-top: 2rem;
  margin-bottom: 0;
  padding: 1rem;
  background-color: var(--color-background-mute);
  border: 1px solid var(--color-border);
  border-radius: 8px;
}

.terms-agreement .terms-item {
  margin-bottom: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.terms-agreement .terms-item:last-child {
  margin-bottom: 0;
}

.terms-agreement input[type="checkbox"] {
  margin-right: 0.5rem;
  width: auto;
  flex-shrink: 0;
}

.terms-agreement label {
  margin-bottom: 0;
  font-weight: normal;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.terms-agreement .terms-link {
  position: relative;
  display: inline-block;
  color: var(--color-primary);
  text-decoration: underline;
  cursor: pointer;
}

.update-dot {
  position: absolute;
  top: 1px;
  right: 2px;
  width: 8px;
  height: 8px;
  background: rgb(239, 68, 68);
  border-radius: 50%;
  border: 1.5px solid var(--color-background-mute);
  animation: none;
}

html.dark .update-dot {
  background: rgb(248, 113, 113);
  border-color: var(--color-background-mute);
}

.full-width-btn {
  width: 100%;
  padding: 0.875rem;
  font-size: 1.1rem;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.4s ease, transform 0.4s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

@media (max-width: 767px) {
  .step-title { font-size: 1.25rem; }
}
</style>
