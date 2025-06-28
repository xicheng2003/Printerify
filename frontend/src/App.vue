<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <div id="app-container">
    <header class="app-header">
      <div class="container header-content">
        <h1>自助打印服务</h1>
        <nav class="main-nav">
          <RouterLink to="/">自助下单</RouterLink>
          <RouterLink to="/query">订单查询</RouterLink>
        </nav>
      </div>
    </header>

    <main class="app-main">
      <div class="container">
        <RouterView />
      </div>
    </main>

    <footer class="app-footer">
      <div class="container">
        <p>&copy; 2025 您的打印服务. All Rights Reserved.</p>
      </div>
    </footer>
  </div>
</template>

<style>
/* ... 您之前已有的全局样式保持不变 ... */
:root {
  --primary-color: #007bff;
  --light-gray: #f4f7f6;
  --text-color: #333;
  --border-color: #e9ecef;
}
body { margin: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; background-color: var(--light-gray); color: var(--text-color); line-height: 1.6; }
#app-container { display: flex; flex-direction: column; min-height: 100vh; }
.container { width: 100%; max-width: 960px; margin: 0 auto; padding: 0 1rem; }
.app-header { background-color: #fff; box-shadow: 0 2px 4px rgba(0,0,0,0.05); padding: 1rem 0; border-bottom: 1px solid var(--border-color); }
.app-main { flex-grow: 1; padding: 2rem 0; }
.app-footer { background-color: #343a40; color: #fff; padding: 1.5rem 0; text-align: center; font-size: 0.9rem; }
.app-footer p { margin: 0; }

/* --- 新增的导航样式 --- */
.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.app-header h1 {
  margin: 0;
  font-size: 1.5rem;
  color: var(--primary-color);
}

.main-nav a {
  margin-left: 1.5rem;
  text-decoration: none;
  color: #555;
  font-weight: 500;
  padding-bottom: 5px;
  border-bottom: 2px solid transparent;
  transition: color 0.3s, border-color 0.3s;
}

.main-nav a:hover {
  color: var(--primary-color);
}

/* Vue Router会自动为当前激活的链接添加这个类名 */
.main-nav a.router-link-exact-active {
  color: var(--primary-color);
  border-bottom-color: var(--primary-color);
}
</style>
