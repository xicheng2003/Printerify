<template>
  <div class="not-found-container">
    <div class="content-wrapper">
      <h1 class="error-code">404</h1>
      <h2 class="error-title">页面未找到</h2>
      <p class="not-found-message">
        抱歉，您访问的页面不存在或已被移除。
      </p>
      <div class="action-buttons">
        <button @click="goHome" class="btn-primary">
          返回首页
        </button>
        <button @click="goBack" class="btn-secondary">
          返回上一页
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const goHome = () => {
  router.push('/')
}

const goBack = () => {
  router.go(-1)
}
</script>

<style scoped>
.not-found-container {
  min-height: 70vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  text-align: center;
  background-color: var(--color-background);
}

.content-wrapper {
  max-width: 500px;
  animation: fadeIn 1s ease-out;
}

.error-code {
  font-size: 12rem;
  font-weight: 200;
  line-height: 1;
  color: var(--color-text);
  opacity: 0.03;
  margin-bottom: -4rem;
  user-select: none;
  letter-spacing: -0.05em;
  pointer-events: none;
}

.error-title {
  font-size: 2rem;
  font-weight: 600;
  color: var(--color-heading);
  margin-bottom: 1rem;
  letter-spacing: -0.02em;
}

.not-found-message {
  font-size: 1rem;
  color: var(--color-text-mute);
  margin-bottom: 3rem;
  line-height: 1.6;
  font-weight: 400;
}

.action-buttons {
  display: flex;
  gap: 1.5rem;
  justify-content: center;
  align-items: center;
}

.btn-primary {
  padding: 0.75rem 2.5rem;
  background-color: var(--color-heading);
  color: var(--color-background);
  border-radius: 4px;
  font-size: 0.95rem;
  font-weight: 500;
  transition: all 0.3s ease;
  border: 1px solid var(--color-heading);
  cursor: pointer;
  letter-spacing: 0.02em;
}

.btn-primary:hover {
  background-color: transparent;
  color: var(--color-heading);
  transform: translateY(-1px);
}

.btn-secondary {
  padding: 0.75rem 0;
  background-color: transparent;
  color: var(--color-text-mute);
  border: none;
  border-bottom: 1px solid transparent;
  font-size: 0.95rem;
  font-weight: 400;
  transition: all 0.3s ease;
  cursor: pointer;
}

.btn-secondary:hover {
  color: var(--color-heading);
  border-bottom-color: var(--color-heading);
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 640px) {
  .error-code {
    font-size: 8rem;
    margin-bottom: -2.5rem;
  }

  .error-title {
    font-size: 1.75rem;
  }

  .action-buttons {
    flex-direction: column;
    gap: 1rem;
  }

  .btn-primary {
    width: 100%;
  }
}
</style>
