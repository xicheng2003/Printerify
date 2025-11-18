<template>
  <div id="app-container">
    <TheNavbar />
    <main class="app-main">
      <RouterView />
    </main>
    <TheFooter />
  </div>
</template>

<script setup>
import { RouterView } from 'vue-router';
import TheNavbar from './components/TheNavbar.vue';
import TheFooter from './components/TheFooter.vue';
</script>

<style scoped>
.app-main {
  padding-top: 80px;
  min-height: calc(100vh - 80px);
  width: 100%;
}
</style>
