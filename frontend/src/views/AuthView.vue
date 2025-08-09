<template>
  <div class="auth-view">
    <div class="auth-container">
      <AuthForm 
        :is-login="isLogin" 
        @update:isLogin="isLogin = $event"
        @auth-success="handleAuthSuccess"
      />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import AuthForm from '@/components/AuthForm.vue'

const router = useRouter()
const isLogin = ref(true)

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