<template>
  <div class="test-page">
    <h1>流程演示交互测试</h1>

    <div class="test-controls">
      <h2>当前状态</h2>
      <p>当前步骤: {{ currentWorkflowStep }}</p>
      <p>拖拽状态: {{ isDragActive }}</p>
      <p>显示文件: {{ showUploadedFiles }}</p>

      <h2>手动控制</h2>
      <button @click="setWorkflowStep(1)">步骤 1</button>
      <button @click="setWorkflowStep(2)">步骤 2</button>
      <button @click="setWorkflowStep(3)">步骤 3</button>
      <button @click="simulateUpload">模拟上传</button>
      <button @click="playDemo">播放演示</button>
    </div>

    <div class="mini-demo">
      <div class="progress-display">
        进度: {{ progressWidth }}
      </div>

      <div class="step-display">
        <div v-for="n in 3" :key="n"
             :class="['step', { active: currentWorkflowStep === n }]"
             @click="setWorkflowStep(n)">
          {{ n }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';

// 状态变量
const currentWorkflowStep = ref(1);
const isDragActive = ref(false);
const showUploadedFiles = ref(false);

const workflowSteps = ref([
  { id: 'upload', title: '上传文件' },
  { id: 'settings', title: '个性设置' },
  { id: 'complete', title: '完成取件' }
]);

// 计算属性
const progressWidth = computed(() => {
  return `${((currentWorkflowStep.value - 1) / (workflowSteps.value.length - 1)) * 100}%`;
});

// 方法
const setWorkflowStep = (step) => {
  console.log('Setting workflow step to:', step);
  currentWorkflowStep.value = step;

  if (step === 1) {
    showUploadedFiles.value = false;
    isDragActive.value = false;
  }
};

const simulateUpload = () => {
  console.log('Simulating upload...');
  isDragActive.value = true;

  setTimeout(() => {
    isDragActive.value = false;
    showUploadedFiles.value = true;
    console.log('Upload simulation completed');
  }, 1500);
};

const playDemo = () => {
  console.log('Starting demo playback...');
  currentWorkflowStep.value = 1;
  showUploadedFiles.value = false;

  const autoPlay = async () => {
    try {
      console.log('Auto-play sequence started');

      await new Promise(resolve => setTimeout(resolve, 1000));
      simulateUpload();

      await new Promise(resolve => setTimeout(resolve, 2500));

      console.log('Moving to step 2');
      currentWorkflowStep.value = 2;
      await new Promise(resolve => setTimeout(resolve, 2000));

      console.log('Moving to step 3');
      currentWorkflowStep.value = 3;
      await new Promise(resolve => setTimeout(resolve, 3000));

      console.log('Resetting to step 1');
      currentWorkflowStep.value = 1;
      showUploadedFiles.value = false;
      console.log('Demo playback completed');
    } catch (error) {
      console.error('Demo playback error:', error);
    }
  };

  autoPlay();
};
</script>

<style scoped>
.test-page {
  max-width: 800px;
  margin: 2rem auto;
  padding: 2rem;
  background: var(--color-background);
  border-radius: 12px;
  border: 1px solid var(--color-border);
}

.test-controls {
  margin-bottom: 2rem;
}

.test-controls button {
  margin-right: 1rem;
  margin-bottom: 1rem;
  padding: 0.5rem 1rem;
  background: var(--color-primary);
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

.test-controls button:hover {
  background: var(--color-primary-dark);
}

.progress-display {
  margin-bottom: 1rem;
  padding: 1rem;
  background: var(--color-background-soft);
  border-radius: 8px;
}

.step-display {
  display: flex;
  gap: 1rem;
}

.step {
  width: 3rem;
  height: 3rem;
  border-radius: 50%;
  background: var(--color-border);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.step.active {
  background: var(--color-primary);
  color: white;
  transform: scale(1.1);
}
</style>
