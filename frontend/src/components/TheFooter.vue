<template>
  <footer class="app-footer">
    <div class="footer-container">
      <div class="footer-brand">
        <RouterLink to="/" class="logo-and-title-link">
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="footer-logo-svg">
            <path d="M7 17H5C3.89543 17 3 16.1046 3 15V11C3 9.89543 3.89543 9 5 9H19C20.1046 9 21 9.89543 21 11V15C21 16.1046 20.1046 17 19 17H17" stroke="var(--color-primary)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M17 9V7C17 5.89543 16.1046 5 15 5H9C7.89543 5 7 5.89543 7 7V9" stroke="var(--color-primary)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <rect x="7" y="13" width="10" height="8" rx="1" stroke="var(--color-heading)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M17 13H19V11" stroke="var(--color-heading)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <h3 class="footer-title">Printerify</h3>
        </RouterLink>
        <p class="footer-tagline">为每一次打印赋能。</p>
      </div>

      <div class="footer-links-group">
        <div class="footer-links-column">
          <h4 class="footer-links-title">导航</h4>
          <ul class="footer-links-list">
            <li><RouterLink to="/" class="footer-link">主页</RouterLink></li>
            <li><RouterLink to="/order" class="footer-link">开始打印</RouterLink></li>
            <li><RouterLink to="/query" class="footer-link">订单查询</RouterLink></li>
            <li><RouterLink to="/profile" class="footer-link">个人中心</RouterLink></li>
          </ul>
        </div>
        <div class="footer-links-column">
          <h4 class="footer-links-title">支持</h4>
          <ul class="footer-links-list">
            <li><RouterLink to="/about" class="footer-link">关于我们</RouterLink></li>
            <li><a href="mailto:xicheng.lin@foxmail.com" class="footer-link">联系我们</a></li>
            <li><a href="https://github.com/xicheng2003/printerify" target="_blank" rel="noopener noreferrer" class="footer-link">GitHub 仓库</a></li>
          </ul>
        </div>
        <div class="footer-links-column">
          <h4 class="footer-links-title">法律</h4>
          <ul class="footer-links-list">
            <li><RouterLink to="/privacy" class="footer-link">隐私政策</RouterLink></li>
            <li><RouterLink to="/terms" class="footer-link">服务条款</RouterLink></li>
          </ul>
        </div>
      </div>
    </div>

    <div class="footer-bottom-bar">
      <p>&copy; {{ new Date().getFullYear() }} Printerify. 保留所有权利。</p>
    </div>
  </footer>
</template>

<script setup>
import { RouterLink } from 'vue-router';
</script>

<style scoped>
.app-footer {
  background-color: var(--color-background);
  border-top: 1px solid var(--color-border);
  padding: 4rem 1.5rem 2rem;
  margin-top: 4rem;
}

.footer-container {
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 4rem;
  padding-bottom: 3rem;
  align-items: start;
}

.footer-brand {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  align-items: flex-start;
}

.logo-and-title-link {
  display: inline-flex;
  align-items: center;
  gap: 0.75rem;
  text-decoration: none;
  opacity: 0.9;
  transition: opacity 0.2s;
}

.logo-and-title-link:hover {
  opacity: 1;
}

.footer-logo-svg {
  flex-shrink: 0;
}

.footer-title {
  font-family: 'Inter', sans-serif;
  font-weight: 700;
  font-size: 1.5rem;
  color: var(--color-heading);
  margin: 0;
  letter-spacing: -0.5px;
}

.footer-tagline {
  font-size: 0.9rem;
  line-height: 1.6;
  color: var(--color-text-mute);
  max-width: 300px;
  margin: 0;
}

.footer-links-group {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
}

.footer-links-title {
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--color-heading);
  margin-bottom: 1.25rem;
  letter-spacing: 0.5px;
  text-transform: uppercase;
}

.footer-links-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
}

.footer-link {
  color: var(--color-text-mute);
  text-decoration: none;
  font-size: 0.9rem;
  transition: color 0.2s ease;
}

.footer-link:hover {
  color: var(--color-heading);
}

.footer-bottom-bar {
  max-width: 1200px;
  margin: 0 auto;
  border-top: 1px solid var(--color-border);
  padding-top: 2rem;
  text-align: center;
  font-size: 0.8rem;
  color: var(--color-text-mute);
  opacity: 0.8;
}

/* ▼▼▼【核心修改】响应式布局中的对齐修正 ▼▼▼ */
@media (max-width: 820px) {
  .footer-container {
    grid-template-columns: 1fr;
    gap: 3rem;
    text-align: center;
  }

  .footer-brand {
    align-items: center;
  }

  .footer-tagline {
    text-align: center;
    margin: 0 auto;
  }

  .footer-links-group {
    width: 100%;
    justify-items: center;
    gap: 3rem;
  }

  .footer-links-column {
    display: flex;
    flex-direction: column;
    align-items: center;
  }
}

@media (max-width: 540px) {
  .app-footer {
    padding: 3rem 1rem 1.5rem;
  }

  .footer-links-group {
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
  }
}
</style>
