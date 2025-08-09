<template>
  <div class="auth-form-container">
    <h2 class="form-title">{{ isLogin ? '用户登录' : '用户注册' }}</h2>
    
    <form @submit.prevent="handleSubmit" class="auth-form">
      <div class="form-group">
        <label for="username">用户名</label>
        <input
          id="username"
          v-model="formData.username"
          type="text"
          required
          :disabled="loading"
          class="form-input"
        />
      </div>

      <div v-if="!isLogin" class="form-group">
        <label for="email">电子邮件</label>
        <input
          id="email"
          v-model="formData.email"
          type="email"
          required
          :disabled="loading"
          class="form-input"
        />
      </div>

      <div v-if="!isLogin" class="form-group">
        <label for="phone">手机号</label>
        <input
          id="phone"
          v-model="formData.phone_number"
          type="tel"
          :disabled="loading"
          class="form-input"
        />
      </div>

      <div class="form-group">
        <label for="password">密码</label>
        <input
          id="password"
          v-model="formData.password"
          type="password"
          required
          :disabled="loading"
          class="form-input"
        />
      </div>

      <div v-if="!isLogin" class="form-group">
        <label for="password_confirm">确认密码</label>
        <input
          id="password_confirm"
          v-model="formData.password_confirm"
          type="password"
          required
          :disabled="loading"
          class="form-input"
        />
      </div>

      <BaseButton
        type="submit"
        :loading="loading"
        :disabled="!isFormValid"
        class="submit-button"
      >
        {{ isLogin ? '登录' : '注册' }}
      </BaseButton>

      <div v-if="error" class="error-message">
        {{ error }}
      </div>

      <div class="auth-toggle">
        <p>
          {{ isLogin ? '还没有账户？' : '已有账户？' }}
          <a href="#" @click.prevent="toggleAuthMode">
            {{ isLogin ? '立即注册' : '立即登录' }}
          </a>
        </p>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, computed, reactive } from 'vue'
import { useUserStore } from '@/stores/user'
import BaseButton from '@/components/BaseButton.vue'

const props = defineProps({
  isLogin: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['auth-success'])

const userStore = useUserStore()
const loading = ref(false)
const error = ref('')

const formData = reactive({
  username: '',
  email: '',
  phone_number: '',
  password: '',
  password_confirm: ''
})

const isFormValid = computed(() => {
  if (props.isLogin) {
    return formData.username && formData.password
  } else {
    return (
      formData.username &&
      formData.email &&
      formData.password &&
      formData.password === formData.password_confirm
    )
  }
})

function toggleAuthMode() {
  emit('update:isLogin', !props.isLogin)
  error.value = ''
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
  max-width: 400px;
  margin: 0 auto;
  padding: 2rem;
  background-color: var(--color-background-soft);
  border-radius: 12px;
  box-shadow: var(--shadow-card);
  border: 1px solid var(--color-border);
}

.form-title {
  text-align: center;
  margin-bottom: 2rem;
  color: var(--color-heading);
  font-size: 1.5rem;
  font-weight: 600;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-weight: 500;
  color: var(--color-heading);
  font-size: 0.9rem;
}

.form-input {
  padding: 0.75rem 1rem;
  border: 1px solid var(--color-border);
  border-radius: 8px;
  font-size: 1rem;
  background-color: var(--color-background);
  color: var(--color-text);
  transition: border-color 0.2s, box-shadow 0.2s;
}

.form-input:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(var(--color-primary-rgb, 37, 99, 235), 0.2);
}

.form-input:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.submit-button {
  width: 100%;
  padding: 0.875rem;
  font-size: 1.1rem;
  font-weight: 600;
}

.error-message {
  padding: 0.75rem;
  background-color: var(--color-danger);
  color: var(--color-text-on-danger);
  border-radius: 8px;
  font-size: 0.9rem;
  text-align: center;
}

.auth-toggle {
  text-align: center;
  font-size: 0.9rem;
  color: var(--color-text-mute);
}

.auth-toggle a {
  color: var(--color-primary);
  text-decoration: none;
  font-weight: 500;
}

.auth-toggle a:hover {
  text-decoration: underline;
}
</style>