<template>
  <div class="profile-view">
    <div class="container">
      <h1 class="page-title">个人资料</h1>
      <UserProfile />
    </div>
  </div>
</template>

<script setup>
import UserProfile from '@/components/UserProfile.vue'
</script>

<style scoped>
.profile-view {
  padding: 2rem 1rem;
  min-height: calc(100vh - 200px);
}

.container {
  max-width: 800px;
  margin: 0 auto;
}

.page-title {
  text-align: center;
  margin-bottom: 2rem;
  color: var(--color-heading);
  font-size: 2rem;
  font-weight: 700;
}

@media (max-width: 768px) {
  .profile-view {
    padding: 1rem;
  }
  
  .page-title {
    font-size: 1.5rem;
    margin-bottom: 1.5rem;
  }
}
</style>