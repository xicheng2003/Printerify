<template>
  <div class="auth-view">
    <div class="auth-background">
      <!-- 装饰性几何图形 -->
      <div class="geometric-shape shape-1"></div>
      <div class="geometric-shape shape-2"></div>
      <div class="geometric-shape shape-3"></div>
    </div>

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
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  padding: 2rem 1rem;
  background: linear-gradient(135deg,
    var(--color-background) 0%,
    var(--color-background-soft) 50%,
    var(--color-background-mute) 100%
  );
  overflow: hidden;
}

.auth-background {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
  overflow: hidden;
}

.geometric-shape {
  position: absolute;
  border-radius: 50%;
  background: linear-gradient(45deg,
    rgba(var(--color-primary-rgb, 37, 99, 235), 0.1),
    rgba(var(--color-primary-rgb, 37, 99, 235), 0.05)
  );
  animation: float 6s ease-in-out infinite;
}

.shape-1 {
  width: 200px;
  height: 200px;
  top: 10%;
  left: 10%;
  animation-delay: 0s;
}

.shape-2 {
  width: 150px;
  height: 150px;
  top: 60%;
  right: 15%;
  animation-delay: 2s;
}

.shape-3 {
  width: 100px;
  height: 100px;
  bottom: 20%;
  left: 70%;
  animation-delay: 4s;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0px) rotate(0deg);
  }
  33% {
    transform: translateY(-20px) rotate(120deg);
  }
  66% {
    transform: translateY(10px) rotate(240deg);
  }
}

.auth-container {
  position: relative;
  z-index: 1;
  width: 100%;
  max-width: 450px;
}

@media (max-width: 768px) {
  .auth-view {
    padding: 1rem;
  }

  .auth-container {
    max-width: 100%;
  }

  .geometric-shape {
    opacity: 0.3;
  }
}

@media (max-width: 480px) {
  .geometric-shape {
    display: none;
  }
}
</style>
