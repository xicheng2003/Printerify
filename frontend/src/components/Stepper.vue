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
  }
});

const steps = ['上传文件', '打印设置', '付款', '完成'];
const progressWidth = computed(() => {
  const progress = ((props.currentStep - 1) / (steps.length - 1)) * 100;
  return `${progress}%`;
});
</script>

<style scoped>
.stepper-container {
  /* *** FIX 1: Make this the positioning context *** */
  position: relative;
  padding: 1.5rem 0;
  margin-bottom: 2rem;
}

.stepper {
  display: flex;
  justify-content: space-between;
  position: relative;
  z-index: 1; /* Ensure icons and labels are above the line */
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
  background-color: #e2e8f0;
  color: #64748b;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 1.1rem;
  transition: all 0.4s ease;
  border: 3px solid #e2e8f0;
  /* Ensure icons have a white background to sit on top of the line */
  background-clip: padding-box;
}

.step-label {
  margin-top: 1rem; /* This now correctly only affects the label's position */
  font-size: 0.875rem;
  color: #64748b;
  transition: color 0.4s ease;
}

/* Active state */
.step.active .step-icon {
  background-color: #e0e7ff;
  border-color: var(--primary-color);
  color: var(--primary-color);
}
.step.active .step-label {
  color: var(--primary-color);
  font-weight: 600;
}

/* Completed state */
.step.completed .step-icon {
  background-color: var(--primary-color);
  border-color: var(--primary-color);
  color: white;
}
.step.completed .step-label {
  color: var(--text-dark);
}

.stepper-line {
  /* *** FIX 2: Use absolute positioning *** */
  position: absolute;
  top: calc(1.5rem + 20px); /* (Container padding + half of icon height) */
  left: 5%;
  right: 5%;
  height: 4px;
  background-color: #e2e8f0;
  z-index: 0; /* Place it behind the icons */
}

.stepper-progress {
  height: 100%;
  background-color: var(--primary-color);
  width: 0%;
  transition: width 0.5s ease;
}
</style>
