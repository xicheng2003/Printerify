<template>
  <div class="oauth-login-container">
    <div class="divider">
      <span class="divider-text">或</span>
    </div>

    <div class="oauth-buttons-wrapper">
      <button @click="loginWithGitHub" :disabled="loading" class="oauth-button github-button">
        <div v-if="loading" class="spinner"></div>
        <template v-else>
          <svg class="oauth-icon" viewBox="0 0 24 24" fill="currentColor">
            <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
          </svg>
          <span>使用 GitHub 登录</span>
        </template>
      </button>

      <button @click="loginWithGoogle" :disabled="loading" class="oauth-button google-button">
        <div v-if="loading" class="spinner"></div>
        <template v-else>
          <svg class="oauth-icon" viewBox="0 0 48 48" fill="none" stroke="currentColor">
            <path fill="#4285F4" d="M45.12 24.5c0-1.56-.14-3.06-.4-4.5H24v8.51h11.84c-.51 2.75-2.06 5.08-4.39 6.64v5.52h7.11c4.16-3.83 6.56-9.47 6.56-16.17z"></path><path fill="#34A853" d="M24 46c5.94 0 10.92-1.96 14.56-5.3l-7.11-5.52c-1.96 1.32-4.48 2.1-7.45 2.1-5.73 0-10.58-3.87-12.31-9.07H4.5v5.7C8.14 40.73 15.58 46 24 46z"></path><path fill="#FBBC05" d="M11.69 28.18C11.25 26.86 11 25.45 11 24s.25-2.86.69-4.18v-5.7H4.5C2.82 17.45 2 20.58 2 24s.82 6.55 2.5 9.88l7.19-5.7z"></path><path fill="#EA4335" d="M24 10.75c3.23 0 6.13 1.11 8.41 3.29l6.31-6.31C34.91 4.18 29.93 2 24 2 15.58 2 8.14 7.27 4.5 14.12l7.19 5.7c1.73-5.2 6.58-9.07 12.31-9.07z"></path>
          </svg>
          <span>使用 Google 登录</span>
        </template>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const loading = ref(false)


const GITHUB_LOGIN_URL = '/api/oauth/github/'
const GOOGLE_LOGIN_URL = '/api/oauth/google/'

const loginWithGitHub = () => {
  loading.value = true
  window.location.href = GITHUB_LOGIN_URL
}

const loginWithGoogle = () => {
  loading.value = true
  window.location.href = GOOGLE_LOGIN_URL
}
</script>

<style scoped>
.oauth-login-container {
  width: 100%;
}

/* 统一的分隔线样式 */
.divider {
  display: flex;
  align-items: center;
  text-align: center;
  margin: 1.75rem 0;
  color: var(--color-text-mute);
}

.divider::before,
.divider::after {
  content: '';
  flex: 1;
  border-bottom: 1px solid var(--color-border);
}

.divider-text {
  padding: 0 1rem;
  font-size: 0.875rem;
  font-weight: 500;
}

/* 按钮容器 */
.oauth-buttons-wrapper {
  display: flex;
  flex-direction: column;
  gap: 1rem; /* 按钮间距 */
}

/* OAuth 按钮基础样式 */
.oauth-button {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  padding: 0.875rem 1.5rem;
  border-radius: 12px; /* 与 AuthForm.vue 输入框和按钮保持一致 */
  font-size: 1rem;
  font-weight: 600; /* 与 AuthForm.vue 按钮保持一致 */
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 1px 3px 0 var(--shadow-color);
}

.oauth-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.oauth-button:hover:not(:disabled) {
  transform: translateY(-2px); /* 与 AuthForm.vue 提交按钮的悬停效果一致 */
  box-shadow: 0 4px 12px rgba(var(--color-primary-rgb, 37, 99, 235), 0.1);
}

.oauth-icon {
  width: 1.25rem; /* 20px */
  height: 1.25rem; /* 20px */
  margin-right: 0.75rem; /* 12px */
}

/* GitHub 按钮特定样式 */
.github-button {
  background-color: #333;
  color: white;
  border: 1px solid #333;
}
html.dark .github-button {
  background-color: #24292e;
  border-color: #444c56;
}
.github-button:hover:not(:disabled) {
  background-color: #24292e;
}

/* Google 按钮特定样式 */
.google-button {
  background-color: var(--color-background-soft);
  color: var(--color-text);
  border: 1px solid var(--color-border);
}

.google-button:hover:not(:disabled) {
  border-color: var(--color-border-hover);
  background-color: var(--color-background-mute);
}

.google-button .oauth-icon {
  stroke-width: 0; /* Google SVG 是填充的，不需要描边 */
}

/* 加载动画 Spinner */
.spinner {
  width: 20px;
  height: 20px;
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

/* Google 按钮在加载时，Spinner 颜色不同 */
.google-button .spinner {
  border-color: rgba(var(--color-text-rgb), 0.2);
  border-top-color: var(--color-text);
}


@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>
