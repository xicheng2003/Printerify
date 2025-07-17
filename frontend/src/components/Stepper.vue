<template>
  <div class="stepper-container">
    <div class="stepper-line">
      <div class="stepper-progress" :style="{ width: progressWidth }"></div>
    </div>
    <div class="stepper">
      <div v-for="(step, index) in steps" :key="index" class="step" :class="{ 'active': index + 1 === currentStep, 'completed': index + 1 < currentStep }">
        <div class="step-icon">
          <svg v-if="index + 1 < currentStep" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
          <span v-else>{{ index + 1 }}</span>
        </div>
        <div class="step-label">{{ step }}</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  currentStep: {
    type: Number,
    required: true,
    default: 1
  },
  steps: {
    type: Array,
    required: true,
    default: () => ['第一步', '第二步', '第三步']
  }
});

const progressWidth = computed(() => {
  if (props.steps.length <= 1) {
    return '0%';
  }
  const progress = ((props.currentStep - 1) / (props.steps.length - 1)) * 100;
  return `${progress}%`;
});
</script>

<style scoped>
/*
  Stepper.vue 的样式已更新，使用 CSS 变量以支持主题切换。
  所有布局、尺寸和逻辑均已完整保留。
*/
.stepper-container {
  position: relative;
  padding: 1.5rem 0;
  margin-bottom: 2rem;
}

.stepper {
  display: flex;
  justify-content: space-between;
  position: relative;
  z-index: 1;
}

.step {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  width: 80px;
}

.step-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: var(--color-background-mute); /* 已修改 */
  color: var(--color-text-mute); /* 已修改 */
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 1.1rem;
  transition: all 0.4s ease;
  border: 3px solid var(--color-border); /* 已修改 */
  background-clip: padding-box;
}

.step-label {
  margin-top: 1rem;
  font-size: 0.875rem;
  color: var(--color-text-mute); /* 已修改 */
  transition: color 0.4s ease;
}

/* --- Active Step Styles --- */
.step.active .step-icon {
  background-color: var(--color-primary); /* 已修改：使用主题色填充背景 */
  border-color: var(--color-primary); /* 已修改：边框颜色保持一致 */
  color: var(--color-text-on-primary); /* 已修改：图标内文字颜色反白 */
}

.step.active .step-label {
  color: var(--color-primary); /* 已修改 */
  font-weight: 600;
}

/* --- Completed Step Styles --- */
.step.completed .step-icon {
  background-color: var(--color-primary); /* 已修改 */
  border-color: var(--color-primary); /* 已修改 */
  color: var(--color-text-on-primary); /* 已修改 */
}

.step.completed .step-label {
  color: var(--color-text); /* 已修改 */
}

/* --- Progress Line Styles --- */
.stepper-line {
  position: absolute;
  top: calc(1.5rem + 20px);
  height: 4px;
  background-color: var(--color-border); /* 已修改 */
  z-index: 0;
  left: 40px;
  right: 40px;
}

.stepper-progress {
  height: 100%;
  background-color: var(--color-primary); /* 已修改 */
  width: 0%;
  transition: width 0.5s ease;
  border-radius: 2px;
}
</style>
