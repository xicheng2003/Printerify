<template>
  <div class="auth-view">
    <div class="auth-container">
      <AuthForm 
        :is-login="isLoginView" 
        @update:isLogin="toggleAuthMode"
        @auth-success="handleAuthSuccess"
      />
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import AuthForm from '@/components/AuthForm.vue'

const router = useRouter()
const route = useRoute()

// 根据当前路由动态计算是登录还是注册视图
const isLoginView = computed(() => route.name === 'login')

function toggleAuthMode() {
  // 切换登录/注册模式
  if (route.name === 'login') {
    router.push('/auth/register')
  } else {
    router.push('/auth/login')
  }
}

function handleAuthSuccess() {
  // 认证成功后重定向到首页
  router.push('/')
}
</script>

<style scoped>
.auth-view {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: calc(100vh - 200px);
  padding: 2rem 1rem;
}

.auth-container {
  width: 100%;
  max-width: 500px;
}

@media (max-width: 768px) {
  .auth-view {
    padding: 1rem;
  }
}
</style>