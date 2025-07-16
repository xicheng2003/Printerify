<template>
  <div class="order-configuration">
    <BindingGroup
      v-for="(group, index) in orderStore.groups"
      :key="group.id"
      :group="group"
      :index="index"
    />
    <div v-if="orderStore.groups.length === 0" class="empty-state">
      <p>请点击上方按钮上传文件以开始配置。</p>
    </div>
  </div>
</template>

<script setup>
import { useOrderStore } from '@/stores/order';
import BindingGroup from './BindingGroup.vue'; // 导入装订组组件

const orderStore = useOrderStore();
</script>

<style scoped>
.order-configuration {
  margin-top: 2rem;
  /* 延续您 process-card 的风格 */
  padding: 0;
  border: none;
  background-color: transparent;
}
.empty-state {
  text-align: center;
  color: #64748b; /* 延续您 hero-section p 的颜色 */
  padding: 2rem;
  background-color: #f8f9fa; /* 延续您 terms-agreement 的背景色 */
  border: 1px dashed #e2e8f0;
  border-radius: 12px;
}
</style>
