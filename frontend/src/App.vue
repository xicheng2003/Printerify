<template>
  <div id="app-container">
    <header class="app-header">
      <div class="container">
        <div class="logo-container">
          <!-- Printerify SVG Logo -->
          <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M7 17H5C3.89543 17 3 16.1046 3 15V11C3 9.89543 3.89543 9 5 9H19C20.1046 9 21 9.89543 21 11V15C21 16.1046 20.1046 17 19 17H17" stroke="#2563eb" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M17 9V7C17 5.89543 16.1046 5 15 5H9C7.89543 5 7 5.89543 7 7V9" stroke="#2563eb" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <rect x="7" y="13" width="10" height="8" rx="1" stroke="#34495e" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M17 13H19V11" stroke="#34495e" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <h1>Printerify</h1>
        </div>
        <nav>
          <RouterLink to="/">自助打印</RouterLink>
          <RouterLink to="/query">订单查询</RouterLink>
          <RouterLink to="/terms">关于</RouterLink>
        </nav>
      </div>
    </header>

    <main class="app-main">
      <RouterView />
    </main>

    <footer class="app-footer">
      <div class="container">
        <p>&copy; 2025 Printerify. All Rights Reserved.</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<style scoped>
/* Scoped styles for App.vue layout */
#app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: #f8f9fa; /* Light grey background */
}

.app-header {
  background-color: #ffffff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  padding: 1rem 0;
  position: sticky;
  top: 0;
  z-index: 1000;
}

.app-header .container {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo-container {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.logo-container h1 {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0;
}

nav {
  display: flex;
  gap: 1.5rem;
}

nav a {
  text-decoration: none;
  color: #475569;
  font-weight: 500;
  transition: color 0.3s ease;
}

nav a:hover,
nav a.router-link-exact-active {
  color: #2563eb; /* Blue color for active/hover link */
}

.app-main {
  flex-grow: 1;
  padding: 2rem 0;
}

.app-footer {
  background-color: #e9ecef;
  color: #6c757d;
  padding: 1rem 0;
  text-align: center;
  font-size: 0.875rem;
}

/* General container class to center content */
.container {
  width: 90%;
  max-width: 1200px;
  margin: 0 auto;
}
</style>
