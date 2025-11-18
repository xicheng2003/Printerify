<template>
  <header class="app-header" :class="{ scrolled: isScrolled }">
    <div class="container">
      <RouterLink to="/" class="logo-container" @click="closeMobileMenu">
        <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M7 17H5C3.89543 17 3 16.1046 3 15V11C3 9.89543 3.89543 9 5 9H19C20.1046 9 21 9.89543 21 11V15C21 16.1046 20.1046 17 19 17H17" stroke="var(--color-primary)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M17 9V7C17 5.89543 16.1046 5 15 5H9C7.89543 5 7 5.89543 7 7V9" stroke="var(--color-primary)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          <rect x="7" y="13" width="10" height="8" rx="1" stroke="var(--color-heading)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M17 13H19V11" stroke="var(--color-heading)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <h1>Printerify</h1>
      </RouterLink>

      <nav class="desktop-nav">
        <RouterLink to="/order" class="nav-link">自助打印</RouterLink>
        <RouterLink to="/query" class="nav-link">订单查询</RouterLink>
        <RouterLink to="/about" class="nav-link">关于</RouterLink>
      </nav>

      <div class="header-controls">
        <UserAuthStatus class="desktop-user-info" />
        <ThemeSwitcher />
        <button @click="toggleMobileMenu" class="mobile-menu-button">
          <svg v-if="isMobileMenuOpen" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
          <svg v-else xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="3" y1="12" x2="21" y2="12"></line><line x1="3" y1="6" x2="21" y2="6"></line><line x1="3" y1="18" x2="21" y2="18"></line>
          </svg>
        </button>
      </div>
    </div>

    <Transition name="mobile-menu-fade">
      <div v-if="isMobileMenuOpen" class="mobile-menu-overlay" @click="closeMobileMenu">
        <div class="mobile-menu-content" @click.stop>
          <nav class="mobile-nav">
            <RouterLink to="/order" @click="closeMobileMenu">自助打印</RouterLink>
            <RouterLink to="/query" @click="closeMobileMenu">订单查询</RouterLink>
            <RouterLink to="/about" @click="closeMobileMenu">关于</RouterLink>
          </nav>
          <div class="mobile-auth-section">
            <div v-if="userStore.isAuthenticated" class="mobile-user-menu">
              <div class="mobile-user-info">
                <img :src="userStore.user?.avatar_url" alt="avatar" class="mobile-avatar" v-if="userStore.user?.avatar_url" />
                <div class="mobile-avatar" v-else>
                  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="currentColor" d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4s-4 1.79-4 4s1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/></svg>
                </div>
                <span class="mobile-username">{{ userStore.user?.username }}</span>
              </div>
              <RouterLink to="/profile" @click="closeMobileMenu" class="mobile-menu-item">个人中心</RouterLink>
              <button @click="handleMobileLogout" class="mobile-menu-item mobile-logout">退出登录</button>
            </div>
            <div v-else class="mobile-auth-buttons">
              <RouterLink to="/auth/login" @click="closeMobileMenu" class="mobile-auth-button">登录</RouterLink>
              <RouterLink to="/auth/register" @click="closeMobileMenu" class="mobile-auth-button primary">注册</RouterLink>
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </header>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';
import { RouterLink, useRouter } from 'vue-router';
import { useUserStore } from '@/stores/user';
import ThemeSwitcher from './ThemeSwitcher.vue';
import UserAuthStatus from './UserAuthStatus.vue';

const userStore = useUserStore();
const router = useRouter();

const isScrolled = ref(false);
const isMobileMenuOpen = ref(false);

const handleScroll = () => {
  isScrolled.value = window.scrollY > 10;
};

const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value;
};

const closeMobileMenu = () => {
  isMobileMenuOpen.value = false;
};

const handleMobileLogout = () => {
  userStore.logout();
  closeMobileMenu();
  router.push('/');
};

onMounted(() => {
  window.addEventListener('scroll', handleScroll);
});

onBeforeUnmount(() => {
  window.removeEventListener('scroll', handleScroll);
});
</script>

<style scoped>
.app-header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  transition: background-color 0.3s ease, box-shadow 0.3s ease, backdrop-filter 0.3s ease;
  padding: 1rem 0;
}

.app-header.scrolled {
  background-color: var(--color-background-mute-alpha);
  backdrop-filter: saturate(180%) blur(10px);
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo-container {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  text-decoration: none;
  color: var(--color-heading);
}

.logo-container h1 {
  font-size: 1.5rem;
  font-weight: 700;
  margin: 0;
}

.desktop-nav {
  display: none;
}

@media (min-width: 768px) {
  .desktop-nav {
    display: flex;
    gap: 2rem;
  }
  .nav-link {
    text-decoration: none;
    color: var(--color-text);
    font-weight: 500;
    position: relative;
    transition: color 0.3s ease;
  }
  .nav-link::after {
    content: '';
    position: absolute;
    bottom: -5px;
    left: 0;
    width: 0;
    height: 2px;
    background-color: var(--color-primary);
    transition: width 0.3s ease;
  }
  .nav-link:hover,
  .router-link-exact-active {
    color: var(--color-primary);
  }
  .nav-link:hover::after,
  .router-link-exact-active::after {
    width: 100%;
  }
}

.header-controls {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.desktop-user-info {
  display: none;
}
@media (min-width: 768px) {
  .desktop-user-info {
    display: block;
  }
}

.mobile-menu-button {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.5rem;
  color: var(--color-heading);
}
@media (min-width: 768px) {
  .mobile-menu-button {
    display: none;
  }
}

/* Mobile Menu Overlay */
.mobile-menu-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 1001;
  display: flex;
  justify-content: center;
  align-items: center;
}

.mobile-menu-content {
  background-color: var(--color-background-soft);
  border-radius: 1rem;
  padding: 2rem;
  width: 90%;
  max-width: 400px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.1);
}

.mobile-nav {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  border-bottom: 1px solid var(--color-border);
  padding-bottom: 1.5rem;
  margin-bottom: 1.5rem;
}

.mobile-nav a {
  text-decoration: none;
  color: var(--color-text);
  font-size: 1.1rem;
  font-weight: 500;
}

.mobile-auth-section .mobile-user-menu {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.mobile-user-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-weight: 500;
}

.mobile-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background-color: var(--color-background-mute);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}
.mobile-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.mobile-menu-item {
  background: none;
  border: none;
  color: var(--color-text);
  text-decoration: none;
  font-size: 1rem;
  text-align: left;
  padding: 0.5rem 0;
  cursor: pointer;
}

.mobile-logout {
  color: var(--color-danger);
}

.mobile-auth-buttons {
  display: flex;
  gap: 1rem;
}

.mobile-auth-button {
  flex: 1;
  text-align: center;
  padding: 0.75rem;
  border-radius: 0.5rem;
  text-decoration: none;
  background-color: var(--color-background-mute);
  color: var(--color-text);
  font-weight: 500;
}

.mobile-auth-button.primary {
  background-color: var(--color-primary);
  color: #fff;
}


/* Transition */
.mobile-menu-fade-enter-active,
.mobile-menu-fade-leave-active {
  transition: opacity 0.3s ease;
}
.mobile-menu-fade-enter-from,
.mobile-menu-fade-leave-to {
  opacity: 0;
}
.mobile-menu-fade-enter-active .mobile-menu-content,
.mobile-menu-fade-leave-active .mobile-menu-content {
  transition: transform 0.3s ease;
}
.mobile-menu-fade-enter-from .mobile-menu-content {
  transform: scale(0.95) translateY(-10px);
}
.mobile-menu-fade-leave-to .mobile-menu-content {
  transform: scale(0.95) translateY(-10px);
}
</style>
