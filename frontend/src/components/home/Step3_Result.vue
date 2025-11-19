<template>
  <div v-if="finalOrder" class="completion-view">
    <svg xmlns="http://www.w3.org/2000/svg" width="60" height="60" viewBox="0 0 24 24" fill="none" stroke="var(--color-success)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <h3 class="step-title">订单提交成功！</h3>
    <p>取件时请出示取件码，请牢记或截图保存。</p>
    <p>凭手机号和取件码，可在订单查询页面查询订单状态</p>
    <strong> 取件地址：西四学生宿舍 425 </strong>
    <div class="pickup-code-wrapper">
      <span class="pickup-code-label">您的取件码</span>
      <strong class="pickup-code">{{ finalOrder.pickup_code }}</strong>
    </div>
    <p class="order-number-info">完整订单号: {{ finalOrder.order_number }}</p>
    <BaseButton @click="$emit('reset')" class="full-width-btn">再来一单</BaseButton>
  </div>
</template>

<script setup>
import BaseButton from '@/components/BaseButton.vue';
const props = defineProps({ finalOrder: { type: Object, required: true } });
// emits handled in template
</script>

<style scoped>
.completion-view {
  text-align: center;
  padding: 2rem 0;
}

.completion-view > p {
  color: var(--color-text-mute);
  margin-bottom: 1rem;
}

.step-title {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  color: var(--color-heading);
}

.pickup-code-wrapper {
  background-color: var(--color-background-mute);
  border: 1px dashed var(--color-primary);
  padding: 1rem;
  border-radius: 8px;
  margin: 1.5rem auto;
  max-width: 300px;
}

.pickup-code-label {
  font-size: 1rem;
  color: var(--color-text);
}

.pickup-code {
  display: block;
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--color-primary);
  letter-spacing: 4px;
  margin-top: 0.5rem;
}

.order-number-info {
  color: var(--color-text-mute);
  font-size: 0.875rem;
  margin-top: -0.5rem;
  margin-bottom: 2rem;
}

.full-width-btn {
  width: 100%;
  padding: 0.875rem;
  font-size: 1.1rem;
}
</style>
