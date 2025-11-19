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
  background-color: var(--color-background-soft);
  color: var(--color-text-mute);
  border-top: 1px solid var(--color-border);
  padding: 3rem 1rem 1.5rem;
  margin-top: 4rem;
  transition: background-color 0.3s, border-color 0.3s;
}

.footer-container {
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 3rem;
  padding-bottom: 2.5rem;
  align-items: start;
}

.footer-brand {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  align-items: flex-start; /* 默认在桌面端左对齐 */
}

.logo-and-title-link {
  display: inline-flex;
  align-items: center;
  gap: 0.75rem;
  text-decoration: none;
}

.footer-logo-svg {
  flex-shrink: 0;
}

.footer-title {
  font-family: 'Inter', sans-serif;
  font-weight: 800;
  font-size: 1.75rem;
  color: var(--color-heading);
  margin: 0;
  transition: color 0.2s;
}

.logo-and-title-link:hover .footer-title {
  color: var(--color-primary);
}

.footer-tagline {
  font-size: 0.9rem;
  line-height: 1.6;
  max-width: 320px;
  margin: 0;
  text-align: left; /* 默认在桌面端左对齐 */
}

.footer-links-group {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
}

.footer-links-title {
  font-size: 1rem;
  font-weight: 600;
  color: var(--color-heading);
  margin-bottom: 1rem;
  letter-spacing: 0.5px;
}

.footer-links-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.footer-link {
  color: var(--color-text-mute);
  text-decoration: none;
  font-size: 0.9rem;
  transition: color 0.2s;
}

.footer-link:hover {
  color: var(--color-primary);
  text-decoration: underline;
  text-underline-offset: 4px;
}

.footer-bottom-bar {
  max-width: 1200px;
  margin: 0 auto;
  border-top: 1px solid var(--color-border);
  padding-top: 1.5rem;
  text-align: center;
  font-size: 0.85rem;
}

/* ▼▼▼【核心修改】响应式布局中的对齐修正 ▼▼▼ */
@media (max-width: 820px) {
  .footer-container {
    grid-template-columns: 1fr; /* 在移动端，布局变为单列 */
    gap: 3rem;
  }

  /* 当布局变为单列时，让品牌区内容水平居中 */
  .footer-brand {
    align-items: center;
  }

  /* Slogan 文本也需要居中 */
  .footer-tagline {
    text-align: center;
  }

  /* 优化移动端三列布局的对齐 */
  .footer-links-group {
    width: 100%;
    justify-items: center;
  }

  .footer-links-column {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
  }

  .footer-links-title {
    text-align: center;
    width: 100%;
  }

  .footer-links-list {
    align-items: center;
    width: 100%;
  }
}

@media (max-width: 540px) {
  .app-footer {
    padding-top: 2rem;
  }
  .footer-links-group {
    grid-template-columns: repeat(3, 1fr);

    gap: 2.5rem 1.5rem;
  }
}
</style>
