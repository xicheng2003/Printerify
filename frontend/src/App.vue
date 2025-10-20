<template>
  <div id="app-container">
    <header class="app-header" :class="{ scrolled: isScrolled }">
      <div class="container">
        <!-- 【重要更新】将 logo 容器改为指向首页的链接 -->
        <RouterLink to="/" class="logo-container" @click="closeMobileMenu">
          <!-- Logo SVG is preserved -->
          <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M7 17H5C3.89543 17 3 16.1046 3 15V11C3 9.89543 3.89543 9 5 9H19C20.1046 9 21 9.89543 21 11V15C21 16.1046 20.1046 17 19 17H17" stroke="var(--color-primary)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M17 9V7C17 5.89543 16.1046 5 15 5H9C7.89543 5 7 5.89543 7 7V9" stroke="var(--color-primary)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <rect x="7" y="13" width="10" height="8" rx="1" stroke="var(--color-heading)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M17 13H19V11" stroke="var(--color-heading)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <h1>Printerify</h1>
        </RouterLink>

        <nav class="desktop-nav">
          <RouterLink to="/order" class="nav-link">
            <svg class="nav-icon" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
              <polyline points="14 2 14 8 20 8"></polyline>
              <line x1="16" y1="13" x2="8" y2="13"></line>
              <line x1="16" y1="17" x2="8" y2="17"></line>
              <polyline points="10 9 9 9 8 9"></polyline>
            </svg>
            <span class="nav-text">自助打印</span>
          </RouterLink>
          <RouterLink to="/query" class="nav-link">
            <svg class="nav-icon" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="8" y1="6" x2="21" y2="6"></line>
              <line x1="8" y1="12" x2="21" y2="12"></line>
              <line x1="8" y1="18" x2="21" y2="18"></line>
              <line x1="3" y1="6" x2="3.01" y2="6"></line>
              <line x1="3" y1="12" x2="3.01" y2="12"></line>
              <line x1="3" y1="18" x2="3.01" y2="18"></line>
            </svg>
            <span class="nav-text">订单查询</span>
          </RouterLink>
          <RouterLink to="/terms" class="nav-link">
            <svg class="nav-icon" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="10"></circle>
              <line x1="12" y1="16" x2="12" y2="12"></line>
              <line x1="12" y1="8" x2="12.01" y2="8"></line>
            </svg>
            <span class="nav-text">关于</span>
          </RouterLink>
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

      <Transition name="dropdown-fade">
        <div v-if="isMobileMenuOpen" class="mobile-menu-dropdown">
          <nav class="mobile-nav">
            <RouterLink to="/order" @click="closeMobileMenu">自助打印</RouterLink>
            <RouterLink to="/query" @click="closeMobileMenu">订单查询</RouterLink>
            <RouterLink to="/terms" @click="closeMobileMenu">关于</RouterLink>

            <!-- 移动端登录注册选项 -->
            <div class="mobile-auth-section">
              <div v-if="userStore.isAuthenticated" class="mobile-user-menu">
                <div class="mobile-user-info">
                  <div class="mobile-avatar">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                      <circle cx="12" cy="7" r="4"></circle>
                    </svg>
                  </div>
                  <span class="mobile-username">{{ userStore.user?.username }}</span>
                </div>
                <RouterLink to="/profile" @click="closeMobileMenu" class="mobile-menu-item">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                    <circle cx="12" cy="7" r="4"></circle>
                  </svg>
                  个人中心
                </RouterLink>
                <button @click="handleMobileLogout" class="mobile-menu-item mobile-logout">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
                    <polyline points="16 17 21 12 16 7"></polyline>
                    <line x1="21" y1="12" x2="9" y2="12"></line>
                  </svg>
                  退出登录
                </button>
              </div>
              <div v-else class="mobile-auth-buttons">
                <RouterLink to="/auth/login" @click="closeMobileMenu" class="mobile-auth-button mobile-login">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4m-5-4l-3-3 3-3m-3 3h9"></path>
                  </svg>
                  登录
                </RouterLink>
                <RouterLink to="/auth/register" @click="closeMobileMenu" class="mobile-auth-button mobile-register">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                    <circle cx="8.5" cy="7" r="4"></circle>
                    <path d="M20 8v6M23 11l-3 3-3-3"></path>
                  </svg>
                  注册
                </RouterLink>
              </div>
            </div>
          </nav>
        </div>
      </Transition>
    </header>

    <main class="app-main">
      <RouterView />
    </main>

    <footer class="app-footer">
      <div class="container">
        <p>&copy; 2025 Printerify. All Rights Reserved.</p>
      </div>
    </footer>

    <Teleport to="body">
      <LoadingSpinner v-if="orderStore.isLoading" />
    </Teleport>
    </div>
</template>

<script setup>
import { ref, watchEffect, onMounted, onUnmounted } from 'vue'; // 1. 引入 watchEffect
import { RouterLink, RouterView, useRouter } from 'vue-router';
import ThemeSwitcher from '@/components/ThemeSwitcher.vue';
import UserAuthStatus from '@/components/UserAuthStatus.vue';
import LoadingSpinner from '@/components/LoadingSpinner.vue';
import { useOrderStore } from '@/stores/order';
import { useUserStore } from '@/stores/user';

const isMobileMenuOpen = ref(false);
const isScrolled = ref(false); // 新增：跟踪滚动状态
const forceExpanded = ref(false); // 新增：强制保持详细状态
const orderStore = useOrderStore();
const userStore = useUserStore();
const router = useRouter();

// 3. 新增一个副作用函数，用于动态修改网页"画布"的底色
watchEffect(() => {
  // a. 定义两种背景色
  const softBackground = 'var(--color-background-soft)';
  const mainBackground = 'var(--color-background)';

  // b. 根据当前主题，设置 <body> 的背景色
  // 这将改变刘海屏等安全区域的颜色
  document.body.style.backgroundColor = softBackground;

  // c. 确保应用容器的背景色是主背景色
  // 这样做可以避免在切换主题时，页面背景出现不必要的闪烁
  const appContainer = document.getElementById('app-container');
  if (appContainer) {
    appContainer.style.backgroundColor = mainBackground;
  }
});

// 全局认证事件监听器
function handleAuthUnauthorized() {
  console.log('检测到认证失效，清除用户状态');
  userStore.logout();
  // 如果当前页面需要认证，重定向到登录页
  if (router.currentRoute.value.meta.requiresAuth) {
    router.push({ name: 'login', query: { redirect: router.currentRoute.value.fullPath } });
  }
}

// 定期检查用户状态
let statusCheckInterval;

// 滚动事件处理
function handleScroll() {
  // 如果菜单已打开或强制保持展开状态，不触发缩略状态
  if (!isMobileMenuOpen.value && !forceExpanded.value) {
    isScrolled.value = window.scrollY > 80;
  }
}

onMounted(() => {
  // 监听认证失效事件
  window.addEventListener('auth:unauthorized', handleAuthUnauthorized);

  // 监听滚动事件
  window.addEventListener('scroll', handleScroll);

  // 每5分钟检查一次用户状态
  statusCheckInterval = setInterval(() => {
    if (userStore.isAuthenticated) {
      userStore.checkAndRefreshUserStatus();
    }
  }, 5 * 60 * 1000);
});

onUnmounted(() => {
  // 清理事件监听器和定时器
  window.removeEventListener('auth:unauthorized', handleAuthUnauthorized);
  window.removeEventListener('scroll', handleScroll);
  if (statusCheckInterval) {
    clearInterval(statusCheckInterval);
  }
});

function toggleMobileMenu() {
  if (!isMobileMenuOpen.value) {
    // 打开菜单：强制展开并保持详细状态
    forceExpanded.value = true;
    isScrolled.value = false;
    // 延迟打开菜单，让动画更流畅
    setTimeout(() => {
      isMobileMenuOpen.value = true;
    }, 100);
  } else {
    // 关闭菜单
    isMobileMenuOpen.value = false;
    forceExpanded.value = false;
    // 关闭后，根据滚动位置决定是否恢复缩略状态
    if (window.scrollY > 80) {
      isScrolled.value = true;
    }
  }
}

function closeMobileMenu() {
  isMobileMenuOpen.value = false;
  forceExpanded.value = false;
  // 关闭菜单后，根据滚动位置决定是否恢复缩略状态
  if (window.scrollY > 80) {
    isScrolled.value = true;
  }
}

function handleMobileLogout() {
  userStore.logout();
  closeMobileMenu();
  router.push('/');
}
</script>

<style scoped>
#app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  /* ▼▼▼ 第1处修改：将这里的背景色改回原来的值 ▼▼▼ */
  background-color: var(--color-background);
}

.app-header {
  position: sticky;
  top: 0;
  z-index: 1000;
  padding: 1rem 0;
  transition: all 0.3s ease;
}

/* 滚动后的样式 */
.app-header.scrolled {
  padding: 0.5rem 0;
}

.app-header .container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: var(--color-background-soft);
  border-radius: 20px;
  padding: 1rem 1.75rem;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  border: 1px solid var(--color-border);
  transition: all 0.3s ease;
  width: auto;
  max-width: 950px;
  margin: 0 auto;
}

/* 滚动后的岛屿样式 - 玻璃态效果 */
.app-header.scrolled .container {
  padding: 0.75rem 1.5rem;
  box-shadow: 0 6px 24px rgba(0, 0, 0, 0.15);
  border-radius: 16px;
  max-width: 500px;
  background-color: rgba(var(--color-background-soft-rgb), 0.8);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(var(--color-border-rgb), 0.6);
}

.app-header.scrolled .logo-container svg {
  width: 28px;
  height: 28px;
}

.app-header.scrolled .logo-container h1 {
  font-size: 1.25rem;
}

.logo-container {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex-shrink: 0;
}

.logo-container svg {
  transition: all 0.3s ease;
  flex-shrink: 0;
}

.logo-container h1 {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--color-heading);
  margin: 0;
  transition: all 0.3s ease;
  white-space: nowrap;
  overflow: hidden;
}

/* 滚动后隐藏品牌名 */
.app-header.scrolled .logo-container {
  gap: 0;
}

.app-header.scrolled .logo-container h1 {
  width: 0;
  opacity: 0;
}

.header-controls {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex-shrink: 0;
}

.desktop-nav {
  display: flex;
  gap: 0.5rem;
  margin-right: auto;
  margin-left: 1.5rem;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  text-decoration: none;
  color: var(--color-text-mute);
  font-weight: 500;
  transition: all 0.3s ease;
  padding: 0.5rem 0.875rem;
  border-radius: 12px;
  white-space: nowrap;
}

.nav-link:hover {
  color: var(--color-primary);
  background-color: var(--color-background-mute);
}

.nav-link.router-link-exact-active {
  color: var(--color-primary);
  background-color: var(--color-background-mute);
}

.nav-icon {
  flex-shrink: 0;
  transition: all 0.3s ease;
}

.nav-text {
  transition: all 0.3s ease;
  overflow: hidden;
}

/* 滚动后隐藏文字，只显示图标 */
.app-header.scrolled .nav-text {
  width: 0;
  opacity: 0;
}

.app-header.scrolled .nav-link {
  gap: 0;
  padding: 0.5rem;
}

.app-main {
  flex-grow: 1;
  padding: 2rem 0;
  /* ▼▼▼ 第2处修改：确保主要内容区域的背景色被明确指定 ▼▼▼ */
  /* 如果您之前没有加过这一行，请加上它 */
  background-color: var(--color-background);
}

.app-footer {
  background-color: var(--color-background-soft);
  color: var(--color-text-mute);
  padding: 1rem 0;
  text-align: center;
  font-size: 0.875rem;
  font-weight: 400;
  border-top: 1px solid var(--color-border);
}

.container {
  width: 90%;
  max-width: 1200px;
  margin: 0 auto;
}

/* 移动端菜单下拉框样式调整 */
.mobile-menu-dropdown {
  position: absolute;
  top: calc(100% + 0.5rem);
  left: 5%;
  right: 5%;
  background-color: var(--color-background-soft);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
  border: 1px solid var(--color-border);
  border-radius: 16px;
  overflow: hidden;
}

.mobile-menu-button {
  display: none;
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.5rem;
  color: var(--color-heading);
  z-index: 1010;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  align-items: center;
  justify-content: center;
  transition: background-color 0.2s;
}
.mobile-menu-button:hover {
    background-color: var(--color-background-mute);
}

/* 原有的移动端菜单下拉框样式已移到 .container 后面 */

.mobile-nav {
  display: flex;
  flex-direction: column;
  padding: 0.5rem 0;
}

.mobile-nav a {
  text-decoration: none;
  color: var(--color-text);
  font-weight: 500;
  font-size: 1rem;
  padding: 0.75rem 1.5rem;
  transition: color 0.3s ease, background-color 0.3s ease;
  text-align: left;
}

.mobile-nav a:hover {
  background-color: var(--color-background-mute);
}

.mobile-nav a.router-link-exact-active {
  color: var(--color-primary);
  font-weight: 600;
}

/* 移动端认证区域样式 */
.mobile-auth-section {
  border-top: 1px solid var(--color-border);
  margin-top: 0.5rem;
  padding-top: 0.5rem;
}

.mobile-user-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1.5rem;
  background-color: var(--color-background-mute);
  margin: 0 1rem 0.5rem 1rem;
  border-radius: 12px;
}

.mobile-avatar {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background-color: var(--color-primary);
  color: white;
  flex-shrink: 0;
}

.mobile-username {
  font-weight: 600;
  color: var(--color-heading);
  font-size: 1rem;
}

.mobile-menu-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  width: 100%;
  padding: 0.75rem 1.5rem;
  text-decoration: none;
  color: var(--color-text);
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 500;
  transition: background-color 0.3s ease, color 0.3s ease;
  text-align: left;
}

.mobile-menu-item:hover {
  background-color: var(--color-background-mute);
  color: var(--color-primary);
}

.mobile-logout {
  color: var(--color-danger);
}

.mobile-logout:hover {
  background-color: var(--color-background-mute);
  color: var(--color-danger-hover);
}

.mobile-auth-buttons {
  padding: 0.5rem 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.mobile-auth-button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.875rem 1.25rem;
  border-radius: 12px;
  text-decoration: none;
  font-weight: 600;
  font-size: 1rem;
  transition: all 0.3s ease;
  text-align: center;
}

.mobile-login {
  background-color: transparent;
  color: var(--color-text);
  border: 2px solid var(--color-border);
}

.mobile-login:hover {
  background-color: var(--color-background-mute);
  border-color: var(--color-primary);
  color: var(--color-primary);
}

.mobile-register {
  background-color: var(--color-primary);
  color: var(--color-text-on-primary);
  border: 2px solid var(--color-primary);
  box-shadow: 0 4px 12px rgba(var(--color-primary-rgb, 37, 99, 235), 0.3);
}

.mobile-register:hover {
  background-color: var(--color-primary-hover);
  border-color: var(--color-primary-hover);
  transform: translateY(-1px);
  box-shadow: 0 6px 16px rgba(var(--color-primary-rgb, 37, 99, 235), 0.4);
}

.dropdown-fade-enter-active,
.dropdown-fade-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}
.dropdown-fade-enter-from,
.dropdown-fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

@media (max-width: 767px) {
  .desktop-nav {
    display: none;
  }
  .mobile-menu-button {
    display: flex;
  }

  /* 隐藏桌面端用户信息组件 */
  .desktop-user-info {
    display: none;
  }

  /* --- 移动端导航栏优化 --- */
  .app-header {
    padding: 0.75rem 0; /* 减小垂直内边距 */
  }

  .app-header .container {
    max-width: calc(100% - 2rem);
    padding: 0.875rem 1.25rem;
  }

  /* 移动端滚动后更紧凑 - 卡片变短 */
  .app-header.scrolled .container {
    max-width: 200px; /* 移动端缩略时卡片变短 */
    padding: 0.625rem 1rem;
    justify-content: space-between; /* 均匀分布三个元素 */
  }

  /* 移动端滚动后 Logo 容器不占用额外空间 */
  .app-header.scrolled .logo-container {
    margin: 0;
  }

  /* 移动端滚动后右侧控制区均匀分布 */
  .app-header.scrolled .header-controls {
    gap: 0.75rem;
  }

  .logo-container svg {
    width: 28px; /* 缩小 Logo */
    height: 28px;
  }

  .logo-container h1 {
    font-size: 1.25rem; /* 缩小标题 */
  }
}
</style>
