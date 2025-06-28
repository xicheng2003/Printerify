<script setup>
defineProps({
  loading: Boolean,
  disabled: Boolean,
});
</script>

<template>
  <button class="base-button" :disabled="loading || disabled">
    <div v-if="loading" class="spinner"></div>
    <slot v-else></slot> </button>
</template>

<style scoped>
/* ... (可以从OrderQuery.vue中复制并调整按钮和spinner的样式) ... */
.base-button {
  position: relative;
  padding: 0.8rem 2rem;
  /* ... 其他样式 ... */
}
.spinner {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  /* ... spinner样式 ... */
}
</style>
