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

// 【修改】让组件接收一个名为 steps 的数组 prop
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

// 【修改】进度条的计算现在基于传入的 steps 数组的长度，更加灵活
const progressWidth = computed(() => {
  if (props.steps.length <= 1) {
    return '0%';
  }
  const progress = ((props.currentStep - 1) / (props.steps.length - 1)) * 100;
  return `${progress}%`;
});
</script>

<style scoped>
.stepper-container {
  position: relative;
  padding: 1.5rem 0;
  margin-bottom: 2rem;
}

.stepper {
  display: flex;
  justify-content: space-between;
  position: relative;
  z-index: 1; /* 确保图标在进度条上方 */
}

.step {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  /* 每个步骤的容器宽度为 80px */
  width: 80px;
}

.step-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: #e2e8f0;
  color: #64748b;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 1.1rem;
  transition: all 0.4s ease;
  border: 3px solid #e2e8f0;
  background-clip: padding-box;
}

.step-label {
  margin-top: 1rem;
  font-size: 0.875rem;
  color: #64748b;
  transition: color 0.4s ease;
}

.step.active .step-icon {
  background-color: #e0e7ff;
  border-color: var(--primary-color);
  color: var(--primary-color);
}
.step.active .step-label {
  color: var(--primary-color);
  font-weight: 600;
}

.step.completed .step-icon {
  background-color: var(--primary-color);
  border-color: var(--primary-color);
  color: white;
}
.step.completed .step-label {
  color: var(--text-dark);
}

.stepper-line {
  position: absolute;
  top: calc(1.5rem + 20px); /* 垂直居中于图标 */
  height: 4px;
  background-color: #e2e8f0;
  z-index: 0;

  /* --- ▼▼▼ 这是最关键的修改 ▼▼▼ --- */
  /* 使用固定的像素值（每个步骤宽度 80px 的一半）来确保精准对齐 */
  left: 40px;
  right: 40px;
  /* --- ▲▲▲ 修改结束 ▲▲▲ --- */
}

.stepper-progress {
  height: 100%;
  background-color: var(--primary-color);
  width: 0%;
  transition: width 0.5s ease;
}
</style>
