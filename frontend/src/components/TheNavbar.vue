<template>
  <header class="app-header" :class="{ scrolled: isScrolled }">
    <div class="container">
      <RouterLink to="/" class="logo-container" @click="closeMobileMenu">
        <div class="logo-icon">
          <svg width="36" height="36" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M7 17H5C3.89543 17 3 16.1046 3 15V11C3 9.89543 3.89543 9 5 9H19C20.1046 9 21 9.89543 21 11V15C21 16.1046 20.1046 17 19 17H17" stroke="var(--color-primary)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M17 9V7C17 5.89543 16.1046 5 15 5H9C7.89543 5 7 5.89543 7 7V9" stroke="var(--color-primary)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <rect x="7" y="13" width="10" height="8" rx="1" stroke="var(--color-heading)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M17 13H19V11" stroke="var(--color-heading)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </div>
        <h1>Printerify</h1>
      </RouterLink>

      <nav class="desktop-nav">
        <RouterLink to="/order" class="nav-link">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="6 9 6 2 18 2 18 9"></polyline>
            <path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"></path>
            <rect x="6" y="14" width="12" height="8"></rect>
          </svg>
          <span>自助打印</span>
        </RouterLink>
        <RouterLink to="/query" class="nav-link">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="11" cy="11" r="8"></circle>
            <path d="m21 21-4.35-4.35"></path>
          </svg>
          <span>订单查询</span>
        </RouterLink>
        <RouterLink to="/about" class="nav-link">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
            <polyline points="14 2 14 8 20 8"></polyline>
            <line x1="16" y1="13" x2="8" y2="13"></line>
            <line x1="16" y1="17" x2="8" y2="17"></line>
            <polyline points="10 9 9 9 8 9"></polyline>
          </svg>
          <span>关于</span>
        </RouterLink>
      </nav>

      <div class="header-controls">
        <UserAuthStatus class="desktop-user-info" />
        <ThemeSwitcher />
        <button @click="toggleMobileMenu" class="mobile-menu-button" :class="{ active: isMobileMenuOpen }">
          <span class="hamburger-line"></span>
          <span class="hamburger-line"></span>
          <span class="hamburger-line"></span>
        </button>
      </div>
    </div>
  </header>

  <Teleport to="body">
    <Transition name="mobile-menu-slide">
      <div v-if="isMobileMenuOpen" class="mobile-menu-overlay" @click="closeMobileMenu">
        <div class="mobile-menu-content" @click.stop>
          <nav class="mobile-nav">
            <RouterLink to="/order" @click="closeMobileMenu" class="mobile-nav-item">
              <div class="nav-icon-wrapper">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <polyline points="6 9 6 2 18 2 18 9"></polyline>
                  <path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"></path>
                  <rect x="6" y="14" width="12" height="8"></rect>
                </svg>
              </div>
              <span>自助打印</span>
            </RouterLink>
            <RouterLink to="/query" @click="closeMobileMenu" class="mobile-nav-item">
              <div class="nav-icon-wrapper">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="11" cy="11" r="8"></circle>
                  <path d="m21 21-4.35-4.35"></path>
                </svg>
              </div>
              <span>订单查询</span>
            </RouterLink>
            <RouterLink to="/about" @click="closeMobileMenu" class="mobile-nav-item">
              <div class="nav-icon-wrapper">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                  <polyline points="14 2 14 8 20 8"></polyline>
                  <line x1="16" y1="13" x2="8" y2="13"></line>
                  <line x1="16" y1="17" x2="8" y2="17"></line>
                  <polyline points="10 9 9 9 8 9"></polyline>
                </svg>
              </div>
              <span>关于</span>
            </RouterLink>
          </nav>

          <div class="mobile-auth-section">
            <div v-if="userStore.isAuthenticated" class="mobile-user-menu">
              <div class="mobile-user-card">
                <img :src="userStore.user?.avatar_url" alt="avatar" class="mobile-avatar" v-if="userStore.user?.avatar_url" />
                <div class="mobile-avatar placeholder" v-else>
                  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="currentColor" d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4s-4 1.79-4 4s1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/></svg>
                </div>
                <div class="mobile-user-details">
                  <span class="mobile-username">{{ userStore.user?.username }}</span>
                  <span class="mobile-user-role">普通用户</span>
                </div>
              </div>

              <div class="mobile-menu-group">
                <RouterLink to="/profile" @click="closeMobileMenu" class="mobile-nav-item">
                  <div class="nav-icon-wrapper">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                      <circle cx="12" cy="7" r="4"></circle>
                    </svg>
                  </div>
                  <span>个人中心</span>
                </RouterLink>
                <button @click="handleMobileLogout" class="mobile-nav-item mobile-logout">
                  <div class="nav-icon-wrapper danger">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
                      <polyline points="16 17 21 12 16 7"></polyline>
                      <line x1="21" y1="12" x2="9" y2="12"></line>
                    </svg>
                  </div>
                  <span>退出登录</span>
                </button>
              </div>
            </div>
            <div v-else class="mobile-auth-buttons">
              <RouterLink to="/auth/login" @click="closeMobileMenu" class="mobile-auth-button">登录</RouterLink>
              <RouterLink to="/auth/register" @click="closeMobileMenu" class="mobile-auth-button primary">注册</RouterLink>
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, watch } from 'vue';
import { RouterLink, useRouter } from 'vue-router';
import { useUserStore } from '@/stores/user';
import ThemeSwitcher from './ThemeSwitcher.vue';
import UserAuthStatus from './UserAuthStatus.vue';

const userStore = useUserStore();
const router = useRouter();

const isScrolled = ref(false);
const isMobileMenuOpen = ref(false);

// 监听菜单打开状态，锁定/解锁 body 滚动
watch(isMobileMenuOpen, (isOpen) => {
  if (isOpen) {
    document.body.style.overflow = 'hidden';
  } else {
    document.body.style.overflow = '';
  }
});

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
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  padding: 0.75rem 0;
  background: transparent;
  border-bottom: 1px solid transparent;
}

.app-header.scrolled {
  background: var(--color-background-mute-alpha);
  backdrop-filter: saturate(180%) blur(20px);
  -webkit-backdrop-filter: saturate(180%) blur(20px);
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.06),
              0 0 1px rgba(0, 0, 0, 0.04);
  padding: 0.5rem 0;
  border-bottom: 1px solid var(--color-border);
}

.container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* Logo Styles */
.logo-container {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  text-decoration: none;
  color: var(--color-heading);
  transition: opacity 0.3s ease;
}

.logo-container:hover {
  opacity: 0.8;
}

/* 禁用logo的router-link-active样式 */
.logo-container.router-link-exact-active {
  color: var(--color-heading);
  background: none;
  box-shadow: none;
  transform: none;
}

.logo-container.router-link-exact-active::before {
  display: none;
}

.logo-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  color: var(--color-primary);
}

.logo-container h1 {
  font-size: 1.25rem;
  font-weight: 700;
  margin: 0;
  line-height: 1.2;
  letter-spacing: -0.02em;
  color: var(--color-heading);
}

/* Desktop Navigation */
.desktop-nav {
  display: none;
}

@media (min-width: 768px) {
  .desktop-nav {
    display: flex;
    gap: 2rem;
    align-items: center;
  }

  .nav-link {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    text-decoration: none;
    color: var(--color-text-mute);
    font-weight: 500;
    font-size: 0.9375rem;
    padding: 0.5rem 0;
    position: relative;
    transition: color 0.3s ease;
  }

  .nav-link::before {
    display: none;
  }

  .nav-link svg {
    display: none;
  }

  .nav-link:hover {
    color: var(--color-heading);
    transform: none;
  }

  .router-link-exact-active {
    color: var(--color-primary);
    background: none;
    box-shadow: none;
  }
}

/* Header Controls */
.header-controls {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.desktop-user-info {
  display: none;
}

@media (min-width: 768px) {
  .desktop-user-info {
    display: block;
  }
}

/* Mobile Menu Button */
.mobile-menu-button {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.5rem;
  color: var(--color-heading);
  display: flex;
  flex-direction: column;
  gap: 5px;
  width: 40px;
  height: 40px;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: background-color 0.2s, color 0.2s;
  position: relative;
  overflow: hidden;
}

.mobile-menu-button:hover {
  background-color: var(--color-background-mute);
}

.hamburger-line {
  width: 18px;
  height: 2px;
  background: currentColor;
  border-radius: 2px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  z-index: 1;
}

.mobile-menu-button.active .hamburger-line:nth-child(1) {
  transform: translateY(7px) rotate(45deg);
}

.mobile-menu-button.active .hamburger-line:nth-child(2) {
  opacity: 0;
  transform: scaleX(0);
}

.mobile-menu-button.active .hamburger-line:nth-child(3) {
  transform: translateY(-7px) rotate(-45deg);
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
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  z-index: 1001;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 1.5rem;
}

.mobile-menu-content {
  background: var(--color-background-soft);
  width: 100%;
  max-width: 420px;
  max-height: 85vh;
  border-radius: 20px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

/* Mobile Navigation */
.mobile-nav {
  display: flex;
  flex-direction: column;
  padding: 1.5rem;
  gap: 0.5rem;
  overflow-y: auto;
  flex: 1;
}

.mobile-nav-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  text-decoration: none;
  color: var(--color-text);
  font-size: 1rem;
  font-weight: 500;
  padding: 0.5rem;
  border-radius: 12px;
  transition: all 0.2s ease;
  background: transparent;
  border: none;
  width: 100%;
  text-align: left;
  cursor: pointer;
}

.mobile-nav-item:hover,
.mobile-nav-item:active {
  background: var(--color-background-mute);
}

.mobile-nav-item.router-link-exact-active {
  background: var(--color-background-mute);
  color: var(--color-heading);
}

.nav-icon-wrapper {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: var(--color-background-mute);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-text-mute);
  transition: all 0.2s ease;
}

.mobile-nav-item:hover .nav-icon-wrapper,
.mobile-nav-item.router-link-exact-active .nav-icon-wrapper {
  background: var(--color-primary);
  color: white;
}

.nav-icon-wrapper.danger {
  color: var(--color-danger);
  background: rgba(220, 53, 69, 0.1);
}

.mobile-nav-item:hover .nav-icon-wrapper.danger {
  background: var(--color-danger);
  color: white;
}

.mobile-logout {
  color: var(--color-danger);
}

/* Mobile Auth Section */
.mobile-auth-section {
  margin-top: auto;
  padding: 1.5rem;
  border-top: 1px solid var(--color-border);
  background: var(--color-background-soft);
}

.mobile-user-menu {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.mobile-user-card {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding-bottom: 0.5rem;
}

.mobile-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: var(--color-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  color: white;
  flex-shrink: 0;
}

.mobile-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.mobile-user-details {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.mobile-username {
  font-weight: 600;
  font-size: 1.1rem;
  color: var(--color-heading);
}

.mobile-user-role {
  font-size: 0.8rem;
  color: var(--color-text-mute);
  background: var(--color-background-mute);
  padding: 0.1rem 0.5rem;
  border-radius: 4px;
  align-self: flex-start;
}

.mobile-menu-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.mobile-auth-buttons {
  display: flex;
  gap: 0.75rem;
}

.mobile-auth-button {
  flex: 1;
  text-align: center;
  padding: 0.875rem;
  border-radius: 12px;
  text-decoration: none;
  background: var(--color-background-mute);
  color: var(--color-text);
  font-weight: 600;
  font-size: 0.9375rem;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.mobile-auth-button:active {
  transform: scale(0.98);
}

.mobile-auth-button.primary {
  background: var(--color-primary);
  color: #fff;
  box-shadow: 0 4px 12px rgba(var(--color-primary-rgb), 0.3);
}

.mobile-auth-button.primary:hover {
  box-shadow: 0 6px 16px rgba(var(--color-primary-rgb), 0.4);
  transform: translateY(-2px);
}

/* Transitions */
.mobile-menu-slide-enter-active,
.mobile-menu-slide-leave-active {
  transition: opacity 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}

.mobile-menu-slide-enter-from,
.mobile-menu-slide-leave-to {
  opacity: 0;
}

.mobile-menu-slide-enter-active .mobile-menu-content,
.mobile-menu-slide-leave-active .mobile-menu-content {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.mobile-menu-slide-enter-from .mobile-menu-content {
  transform: scale(0.9);
  opacity: 0;
}

.mobile-menu-slide-leave-to .mobile-menu-content {
  transform: scale(0.95);
  opacity: 0;
}
</style>

<style>
/* 暗色模式下的品牌名渐变效果 - 放在非 scoped 样式中以避免编译问题 */
html.dark .logo-container h1 {
  background: linear-gradient(135deg, var(--color-heading) 0%, var(--color-primary) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
</style>
