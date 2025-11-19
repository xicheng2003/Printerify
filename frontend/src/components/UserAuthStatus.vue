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
        <span class="username">{{ user?.username || '用户' }}</span>
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

      <Transition name="fade-scale">
        <div v-if="isMenuOpen" class="dropdown-menu">
          <div class="menu-header">
            <span class="menu-label">账号</span>
          </div>
          <router-link to="/profile" class="menu-item" @click="closeMenu">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="menu-icon">
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
              <circle cx="12" cy="7" r="4"></circle>
            </svg>
            个人中心
          </router-link>
          <div class="menu-divider"></div>
          <button @click="handleLogout" class="menu-item logout-item">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="menu-icon">
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
  gap: 0.75rem;
  cursor: pointer;
  padding: 0.5rem 0.75rem;
  border-radius: 9999px;
  transition: background-color 0.2s;
  border: 1px solid transparent;
}

.user-info:hover {
  background-color: var(--color-background-mute);
  border-color: var(--color-border);
}

.avatar {
  width: 32px;
  height: 32px;
  background-color: rgba(var(--color-primary-rgb), 0.1);
  color: var(--color-primary);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.username {
  font-weight: 500;
  color: var(--color-heading);
  font-size: 0.95rem;
}

.rotate {
  transform: rotate(180deg);
  transition: transform 0.3s ease;
}

.dropdown-menu {
  position: absolute;
  top: 120%;
  right: 0;
  width: 200px;
  background-color: var(--color-background);
  border: 1px solid var(--color-border);
  border-radius: 12px;
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1);
  padding: 0.5rem;
  z-index: 100;
  transform-origin: top right;
}

.menu-header {
  padding: 0.5rem 0.75rem;
}

.menu-label {
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--color-text-mute);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.menu-item {
  display: flex;
  align-items: center;
  width: 100%;
  padding: 0.625rem 0.75rem;
  border: none;
  background: none;
  color: var(--color-text);
  font-size: 0.875rem;
  cursor: pointer;
  border-radius: 8px;
  transition: background-color 0.2s;
  text-decoration: none;
  text-align: left;
}

.menu-item:hover {
  background-color: var(--color-background-mute);
  color: var(--color-heading);
}

.menu-icon {
  margin-right: 0.75rem;
  opacity: 0.8;
}

.menu-divider {
  height: 1px;
  background-color: var(--color-border);
  margin: 0.5rem 0;
}

.logout-item {
  color: var(--color-danger);
}

.logout-item:hover {
  background-color: rgba(220, 53, 69, 0.05);
  color: var(--color-danger-hover);
}

/* Animation */
.fade-scale-enter-active,
.fade-scale-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}

.fade-scale-enter-from,
.fade-scale-leave-to {
  opacity: 0;
  transform: scale(0.95);
}

.auth-buttons {
  display: flex;
  gap: 1rem;
}

.auth-button {
  padding: 0.5rem 1.25rem;
  border-radius: 9999px;
  font-size: 0.9rem;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.2s;
}

.login-button {
  color: var(--color-text);
}

.login-button:hover {
  color: var(--color-primary);
}

.register-button {
  background-color: var(--color-primary);
  color: white;
}

.register-button:hover {
  background-color: var(--color-primary-hover);
  transform: translateY(-1px);
  box-shadow: 0 4px 6px rgba(var(--color-primary-rgb), 0.2);
}

@media (max-width: 767px) {
  .auth-buttons {
    display: none;
  }
  .user-menu {
    display: block;
  }
}
</style>
