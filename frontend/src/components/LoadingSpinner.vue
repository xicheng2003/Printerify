<template>
  <div class="loading-overlay">
    <div class="spinner"></div>
    <p class="loading-text">处理中，请稍候...</p>
  </div>
</template>

<style scoped>
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(255, 255, 255, 0.8);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  z-index: 9999;
  backdrop-filter: blur(4px);
}

.spinner {
  width: 50px;
  height: 50px;
  border: 5px solid rgba(37, 99, 235, 0.2);
  border-top-color: var(--primary-color);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.loading-text {
  margin-top: 1.5rem;
  font-size: 1rem;
  font-weight: 500;
  color: #4b5563;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>
