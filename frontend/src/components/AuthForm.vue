<template>
  <div class="auth-form-container">
    <!-- 品牌头部 -->
    <div class="brand-header">
      <div class="brand-logo">
        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M7 17H5C3.89543 17 3 16.1046 3 15V11C3 9.89543 3.89543 9 5 9H19C20.1046 9 21 9.89543 21 11V15C21 16.1046 20.1046 17 19 17H17" stroke="var(--color-primary)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M17 9V7C17 5.89543 16.1046 5 15 5H9C7.89543 5 7 5.89543 7 7V9" stroke="var(--color-primary)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          <rect x="7" y="13" width="10" height="8" rx="1" stroke="var(--color-heading)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M17 13H19V11" stroke="var(--color-heading)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <h1 class="brand-name">Printerify</h1>
      </div>

      <!-- 引导语 -->
      <div class="welcome-message">
        <h2 class="form-title">{{ isLogin ? '欢迎回来' : '加入我们' }}</h2>
        <p class="form-subtitle">
          {{ isLogin ? '登录您的账户，继续您的打印之旅' : '创建账户，开始便捷的打印服务' }}
        </p>
      </div>
    </div>

    <form @submit.prevent="handleSubmit" class="auth-form">
      <!-- 用户名字段 -->
      <div class="form-group">
        <label for="username" class="form-label">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
            <circle cx="12" cy="7" r="4"></circle>
          </svg>
          用户名
        </label>
        <div class="input-wrapper">
          <input
            id="username"
            v-model="formData.username"
            type="text"
            required
            :disabled="loading"
            class="form-input"
            placeholder="请输入用户名"
          />
          <div class="input-border"></div>
        </div>
      </div>

      <!-- 邮箱字段（仅注册时显示） -->
      <div v-if="!isLogin" class="form-group">
        <label for="email" class="form-label">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path>
            <polyline points="22,6 12,13 2,6"></polyline>
          </svg>
          电子邮件
        </label>
        <div class="input-wrapper">
          <input
            id="email"
            v-model="formData.email"
            type="email"
            required
            :disabled="loading"
            class="form-input"
            placeholder="请输入邮箱地址"
          />
          <div class="input-border"></div>
        </div>
      </div>

      <!-- 手机号字段（仅注册时显示） -->
      <div v-if="!isLogin" class="form-group">
        <label for="phone" class="form-label">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path>
          </svg>
          手机号码
        </label>
        <div class="input-wrapper">
          <input
            id="phone"
            v-model="formData.phone_number"
            type="tel"
            :disabled="loading"
            class="form-input"
            placeholder="请输入手机号码（可选）"
          />
          <div class="input-border"></div>
        </div>
      </div>

      <!-- 密码字段 -->
      <div class="form-group">
        <label for="password" class="form-label">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
            <circle cx="12" cy="16" r="1"></circle>
            <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
          </svg>
          密码
        </label>
        <div class="input-wrapper">
          <input
            id="password"
            v-model="formData.password"
            :type="showPassword ? 'text' : 'password'"
            required
            :disabled="loading"
            class="form-input"
            :placeholder="isLogin ? '请输入密码' : '至少8位字符'"
          />
          <button
            type="button"
            @click="togglePasswordVisibility"
            class="password-toggle"
            :aria-label="showPassword ? '隐藏密码' : '显示密码'"
          >
            <svg v-if="showPassword" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path>
              <line x1="1" y1="1" x2="23" y2="23"></line>
            </svg>
            <svg v-else width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
              <circle cx="12" cy="12" r="3"></circle>
            </svg>
          </button>
          <div class="input-border"></div>
        </div>
      </div>

      <!-- 确认密码字段（仅注册时显示） -->
      <div v-if="!isLogin" class="form-group">
        <label for="password_confirm" class="form-label">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M9 12l2 2 4-4"></path>
            <path d="M21 12c-1 0-3-1-3-3s2-3 3-3 3 1 3 3-2 3-3 3"></path>
            <path d="M3 12c1 0 3-1 3-3s-2-3-3-3-3 1-3 3 2 3 3 3"></path>
            <path d="M3 12h6m6 0h6"></path>
          </svg>
          确认密码
        </label>
        <div class="input-wrapper">
          <input
            id="password_confirm"
            v-model="formData.password_confirm"
            :type="showConfirmPassword ? 'text' : 'password'"
            required
            :disabled="loading"
            class="form-input"
            placeholder="请再次输入密码"
          />
          <button
            type="button"
            @click="toggleConfirmPasswordVisibility"
            class="password-toggle"
            :aria-label="showConfirmPassword ? '隐藏密码' : '显示密码'"
          >
            <svg v-if="showConfirmPassword" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path>
              <line x1="1" y1="1" x2="23" y2="23"></line>
            </svg>
            <svg v-else width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
              <circle cx="12" cy="12" r="3"></circle>
            </svg>
          </button>
          <div class="input-border"></div>
        </div>
      </div>

      <!-- 提交按钮 -->
      <BaseButton
        type="submit"
        :loading="loading"
        :disabled="!isFormValid"
        class="submit-button"
      >
        <template v-if="!loading">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path v-if="isLogin" d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4m-5-4l-3-3 3-3m-3 3h9"></path>
            <path v-else d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
            <circle v-if="!isLogin" cx="8.5" cy="7" r="4"></circle>
            <path v-if="!isLogin" d="M20 8v6M23 11l-3 3-3-3"></path>
          </svg>
          {{ isLogin ? '立即登录' : '创建账户' }}
        </template>
      </BaseButton>

      <!-- 错误信息 -->
      <div v-if="error" class="error-message">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="12" cy="12" r="10"></circle>
          <line x1="15" y1="9" x2="9" y2="15"></line>
          <line x1="9" y1="9" x2="15" y2="15"></line>
        </svg>
        {{ error }}
      </div>

      <!-- 切换登录/注册 -->
      <div class="auth-toggle">
        <p>
          {{ isLogin ? '还没有账户？' : '已有账户？' }}
          <a href="#" @click.prevent="toggleAuthMode" class="toggle-link">
            {{ isLogin ? '立即注册' : '立即登录' }}
          </a>
        </p>
      </div>
    </form>

    <!-- 装饰性元素 -->
    <div class="form-decoration">
      <div class="decoration-dot"></div>
      <div class="decoration-dot"></div>
      <div class="decoration-dot"></div>
    </div>

    <!-- OAuth登录选项 -->
    <OAuthLogin />
  </div>
</template>

<script setup>
import { ref, computed, reactive, watch } from 'vue'
import { useUserStore } from '@/stores/user'
import { useRouter, useRoute } from 'vue-router'
import BaseButton from '@/components/BaseButton.vue'
import OAuthLogin from './OAuthLogin.vue'

const props = defineProps({
  isLogin: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['update:isLogin', 'auth-success'])

const userStore = useUserStore()
const router = useRouter()
const route = useRoute()
const loading = ref(false)
const error = ref('')
const showPassword = ref(false)
const showConfirmPassword = ref(false)

const formData = reactive({
  username: '',
  email: '',
  phone_number: '',
  password: '',
  password_confirm: ''
})

// 当isLogin属性改变时，重置错误信息和表单
watch(() => props.isLogin, () => {
  error.value = ''
  // 清空表单
  Object.keys(formData).forEach(key => {
    formData[key] = ''
  })
})

const isFormValid = computed(() => {
  if (props.isLogin) {
    return formData.username && formData.password
  } else {
    return (
      formData.username &&
      formData.email &&
      formData.password &&
      formData.password === formData.password_confirm &&
      formData.password.length >= 8
    )
  }
})

function toggleAuthMode() {
  emit('update:isLogin', !props.isLogin)
  error.value = ''
}

function togglePasswordVisibility() {
  showPassword.value = !showPassword.value
}

function toggleConfirmPasswordVisibility() {
  showConfirmPassword.value = !showConfirmPassword.value
}

async function handleSubmit() {
  if (!isFormValid.value) return

  loading.value = true
  error.value = ''

  try {
    if (props.isLogin) {
      await userStore.login({
        username: formData.username,
        password: formData.password
      })
    } else {
      await userStore.register({
        username: formData.username,
        email: formData.email,
        phone_number: formData.phone_number,
        password: formData.password,
        password_confirm: formData.password_confirm
      })
    }

    // 重置表单
    Object.keys(formData).forEach(key => {
      formData[key] = ''
    })

    // 处理登录成功后的重定向
    const redirectPath = route.query.redirect || '/'
    router.push(redirectPath)

    emit('auth-success')
  } catch (err) {
    error.value = err.response?.data?.detail || err.message || '操作失败，请重试'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.auth-form-container {
  position: relative;
  max-width: 420px;
  margin: 0 auto;
  padding: 3rem 2.5rem;
  background: var(--color-background);
  border-radius: 20px;
  box-shadow:
    0 20px 40px rgba(0, 0, 0, 0.1),
    0 10px 20px rgba(0, 0, 0, 0.05),
    inset 0 1px 0 rgba(255, 255, 255, 0.1);
  border: 1px solid var(--color-border);
  backdrop-filter: blur(10px);
  overflow: hidden;
}

.auth-form-container::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg,
    var(--color-primary),
    rgba(var(--color-primary-rgb, 37, 99, 235), 0.7),
    var(--color-primary)
  );
}

/* 品牌头部 */
.brand-header {
  text-align: center;
  margin-bottom: 2.5rem;
}

.brand-logo {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
}

.brand-name {
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--color-heading);
  margin: 0;
  letter-spacing: -0.025em;
}

.welcome-message {
  margin-bottom: 1rem;
}

.form-title {
  font-size: 1.625rem;
  font-weight: 700;
  color: var(--color-heading);
  margin: 0 0 0.5rem 0;
  letter-spacing: -0.025em;
}

.form-subtitle {
  font-size: 1rem;
  color: var(--color-text-mute);
  margin: 0;
  line-height: 1.5;
}

/* 表单样式 */
.auth-form {
  display: flex;
  flex-direction: column;
  gap: 1.75rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 600;
  color: var(--color-heading);
  font-size: 0.875rem;
  margin-bottom: 0.25rem;
}

.form-label svg {
  color: var(--color-primary);
  flex-shrink: 0;
}

.input-wrapper {
  position: relative;
}

.form-input {
  width: 100%;
  padding: 1rem 1.25rem;
  border: 2px solid var(--color-border);
  border-radius: 12px;
  font-size: 1rem;
  background-color: var(--color-background-soft);
  color: var(--color-text);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-sizing: border-box;
}

.form-input:focus {
  outline: none;
  border-color: var(--color-primary);
  background-color: var(--color-background);
  transform: translateY(-1px);
  box-shadow:
    0 4px 12px rgba(var(--color-primary-rgb, 37, 99, 235), 0.15),
    0 0 0 4px rgba(var(--color-primary-rgb, 37, 99, 235), 0.1);
}

.form-input:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.form-input::placeholder {
  color: var(--color-text-mute);
}

.password-toggle {
  position: absolute;
  right: 1rem;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: var(--color-text-mute);
  cursor: pointer;
  padding: 0.25rem;
  border-radius: 6px;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.password-toggle:hover {
  color: var(--color-primary);
  background-color: var(--color-background-mute);
}

.input-border {
  position: absolute;
  bottom: 0;
  left: 50%;
  width: 0;
  height: 2px;
  background: linear-gradient(90deg, var(--color-primary), rgba(var(--color-primary-rgb, 37, 99, 235), 0.7));
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  transform: translateX(-50%);
}

.form-input:focus + .input-border {
  width: 100%;
}

/* 提交按钮 */
.submit-button {
  width: 100%;
  padding: 1rem 1.5rem;
  font-size: 1.1rem;
  font-weight: 600;
  border-radius: 12px;
  background: linear-gradient(135deg, var(--color-primary), rgba(var(--color-primary-rgb, 37, 99, 235), 0.9));
  border: none;
  color: white;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  margin-top: 0.5rem;
  box-shadow: 0 4px 12px rgba(var(--color-primary-rgb, 37, 99, 235), 0.3);
}

.submit-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(var(--color-primary-rgb, 37, 99, 235), 0.4);
}

.submit-button:active:not(:disabled) {
  transform: translateY(-1px);
}

.submit-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
  box-shadow: 0 4px 12px rgba(var(--color-primary-rgb, 37, 99, 235), 0.2);
}

/* 错误信息 */
.error-message {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem;
  background: linear-gradient(135deg, var(--color-danger), rgba(220, 53, 69, 0.9));
  color: white;
  border-radius: 12px;
  font-size: 0.9rem;
  box-shadow: 0 4px 12px rgba(220, 53, 69, 0.3);
  animation: slideIn 0.3s ease-out;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 切换按钮 */
.auth-toggle {
  text-align: center;
  margin-top: 1rem;
  padding-top: 1.5rem;
  border-top: 1px solid var(--color-border);
}

.auth-toggle p {
  margin: 0;
  font-size: 0.95rem;
  color: var(--color-text-mute);
}

.toggle-link {
  color: var(--color-primary);
  text-decoration: none;
  font-weight: 600;
  margin-left: 0.25rem;
  transition: all 0.2s;
  position: relative;
}

.toggle-link:hover {
  color: var(--color-primary-dark);
}

.toggle-link::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 0;
  height: 2px;
  background: var(--color-primary);
  transition: width 0.3s ease;
}

.toggle-link:hover::after {
  width: 100%;
}

/* 装饰元素 */
.form-decoration {
  position: absolute;
  bottom: 1rem;
  right: 1.5rem;
  display: flex;
  gap: 0.5rem;
}

.decoration-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--color-primary);
  opacity: 0.3;
  animation: pulse 2s ease-in-out infinite;
}

.decoration-dot:nth-child(2) {
  animation-delay: 0.5s;
}

.decoration-dot:nth-child(3) {
  animation-delay: 1s;
}

@keyframes pulse {
  0%, 100% {
    opacity: 0.3;
    transform: scale(1);
  }
  50% {
    opacity: 0.7;
    transform: scale(1.2);
  }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .auth-form-container {
    padding: 2rem 1.5rem;
    margin: 1rem;
    border-radius: 16px;
  }

  .brand-name {
    font-size: 1.5rem;
  }

  .form-title {
    font-size: 1.375rem;
  }

  .form-subtitle {
    font-size: 0.9rem;
  }

  .auth-form {
    gap: 1.5rem;
  }

  .form-input {
    padding: 0.875rem 1rem;
  }

  .submit-button {
    padding: 0.875rem 1.25rem;
    font-size: 1rem;
  }
}

@media (max-width: 480px) {
  .auth-form-container {
    padding: 1.5rem 1rem;
  }

  .brand-logo {
    flex-direction: column;
    gap: 0.5rem;
  }

  .form-decoration {
    display: none;
  }
}
</style>
