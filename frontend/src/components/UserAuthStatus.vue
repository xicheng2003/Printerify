<template>
  <div class="user-auth-status">
    <div v-if="isAuthenticated" class="user-menu">
      <div class="user-info" @click="toggleMenu">
        <div class="avatar">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
            <circle cx="12" cy="7" r="4"></circle>
          </svg>
        </div>
        <span class="username">{{ user.username }}</span>
        <svg 
          xmlns="http://www.w3.org/2000/svg" 
          width="16" 
          height="16" 
          viewBox="0 0 24 24" 
          fill="none" 
          stroke="currentColor" 
          stroke-width="2" 
          stroke-linecap="round" 
          stroke-linejoin="round"
          :class="{ 'rotate': isMenuOpen }"
        >
          <polyline points="6 9 12 15 18 9"></polyline>
        </svg>
      </div>
      
      <Transition name="slide-fade">
        <div v-if="isMenuOpen" class="dropdown-menu">
          <router-link to="/profile" class="menu-item" @click="closeMenu">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
              <circle cx="12" cy="7" r="4"></circle>
            </svg>
            个人资料
          </router-link>
          <router-link to="/orders" class="menu-item" @click="closeMenu">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="10" cy="20.5" r="1"/>
              <circle cx="18" cy="20.5" r="1"/>
              <path d="M2.5 2.5h3l2.7 12.4a2 2 0 0 0 2 1.6h7.7a2 2 0 0 0 2-1.6l1.6-8.4H7.1"/>
            </svg>
            我的订单
          </router-link>
          <div class="menu-divider"></div>
          <button @click="handleLogout" class="menu-item logout-item">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
              <polyline points="16 17 21 12 16 7"></polyline>
              <line x1="21" y1="12" x2="9" y2="12"></line>
            </svg>
            退出登录
          </button>
        </div>
      </Transition>
    </div>
    
    <div v-else class="auth-buttons">
      <router-link to="/auth/login" class="auth-button login-button">
        登录
      </router-link>
      <router-link to="/auth/register" class="auth-button register-button">
        注册
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useUserStore } from '@/stores/user'
import { useRouter } from 'vue-router'

const userStore = useUserStore()
const router = useRouter()
const isMenuOpen = ref(false)

const isAuthenticated = computed(() => userStore.isAuthenticated)
const user = computed(() => userStore.user)

function toggleMenu() {
  isMenuOpen.value = !isMenuOpen.value
}

function closeMenu() {
  isMenuOpen.value = false
}

function handleLogout() {
  userStore.logout()
  closeMenu()
  router.push('/')
}
</script>

<style scoped>
.user-auth-status {
  position: relative;
}

.user-menu {
  position: relative;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 0.75rem;
  background-color: var(--color-background-mute);
  border-radius: 50px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.user-info:hover {
  background-color: var(--color-background-soft);
}

.avatar {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background-color: var(--color-primary);
  color: white;
}

.username {
  font-weight: 500;
  color: var(--color-text);
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  right: 0;
  background-color: var(--color-background-soft);
  border: 1px solid var(--color-border);
  border-radius: 8px;
  box-shadow: var(--shadow-card);
  min-width: 200px;
  z-index: 1000;
  margin-top: 0.5rem;
}

.menu-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  width: 100%;
  padding: 0.75rem 1rem;
  text-decoration: none;
  color: var(--color-text);
  background: none;
  border: none;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.2s;
}

.menu-item:hover {
  background-color: var(--color-background-mute);
  color: var(--color-primary);
}

.menu-divider {
  height: 1px;
  background-color: var(--color-border);
  margin: 0.25rem 0;
}

.logout-item {
  color: var(--color-danger);
}

.logout-item:hover {
  background-color: var(--color-background-mute);
  color: var(--color-danger-hover);
}

.auth-buttons {
  display: flex;
  gap: 0.5rem;
}

.auth-button {
  padding: 0.5rem 1rem;
  border-radius: 50px;
  text-decoration: none;
  font-weight: 500;
  font-size: 0.9rem;
  transition: all 0.2s;
}

.login-button {
  background-color: transparent;
  color: var(--color-text);
  border: 1px solid var(--color-border);
}

.login-button:hover {
  background-color: var(--color-background-mute);
}

.register-button {
  background-color: var(--color-primary);
  color: var(--color-text-on-primary);
  border: 1px solid var(--color-primary);
}

.register-button:hover {
  background-color: var(--color-primary-hover);
}

.rotate {
  transform: rotate(180deg);
}

.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: all 0.3s ease;
}

.slide-fade-enter-from,
.slide-fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

@media (max-width: 768px) {
  .auth-buttons {
    gap: 0.25rem;
  }
  
  .auth-button {
    padding: 0.5rem 0.75rem;
    font-size: 0.8rem;
  }
}
</style>