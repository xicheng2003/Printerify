<template>
  <div class="privacy-page">
    <h1>隐私政策</h1>
    <div class="privacy-content">
      <LegalDocument type="privacy" mode="full" />
    </div>
  </div>
</template>

<script setup>
import LegalDocument from '@/components/legal/LegalDocument.vue'
</script>

<style scoped>
.privacy-page {
  padding: 2rem 3rem;
  max-width: 800px;
  margin: 2rem auto;
  background-color: var(--color-background-soft);
  border-radius: 8px;
  box-shadow: var(--shadow-card);
  border: 1px solid var(--color-border);
}

.privacy-content {
  text-align: justify;
  line-height: 1.8;
  color: var(--color-text);
}

h1 {
  text-align: center;
  color: var(--color-heading);
  font-size: 2rem;
  margin-bottom: 1.5rem;
}

@media (max-width: 767px) {
  .privacy-page {
    padding: 1.5rem 1rem;
    margin: 1rem auto;
  }
  h1 {
    font-size: 1.5rem;
  }
  .privacy-content {
    line-height: 1.7;
    font-size: 0.9rem;
  }
}
</style>
