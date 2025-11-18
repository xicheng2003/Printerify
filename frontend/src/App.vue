<template>
  <div id="app-container">
    <TheNavbar />
    <main class="app-main">
      <RouterView v-slot="{ Component }">
        <template v-if="Component">
          <Transition name="fade" mode="out-in">
            <KeepAlive>
              <component :is="Component"></component>
            </KeepAlive>
          </Transition>
        </template>
      </RouterView>
    </main>
    <TheFooter />
  </div>
</template>

<script setup>
import { RouterView } from 'vue-router';
import TheNavbar from './components/TheNavbar.vue';
import TheFooter from './components/TheFooter.vue';
import { useOrderStore } from '@/stores/order';
import LoadingSpinner from '@/components/LoadingSpinner.vue';

const orderStore = useOrderStore();
</script>

<style scoped>
.app-main {
  padding-top: 80px; /* Adjust this value based on the actual height of your header */
  min-height: calc(100vh - 80px); /* Adjust 80px if footer height changes */
  display: flex;
  flex-direction: column;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
