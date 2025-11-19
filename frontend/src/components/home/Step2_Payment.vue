<template>
  <div>
    <h3 class="step-title">第二步：确认信息并支付</h3>

    <div v-if="anyEstimated" class="order-estimated-alert" role="alert" aria-live="polite">
      <div class="estimated-icon">
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>
      </div>
      <div class="estimated-text">
        <strong>价格提示：</strong>
        <span>当前页数为预估，计价可能不准确。建议上传 PDF 格式获得精确价格。若继续提交，系统将尝试在后台更新为精确价格。如有任何疑问，请联系我们。</span>
      </div>
    </div>

    <div class="price-result">
      <p>订单总计</p>
      <p class="price"><strong>¥ {{ totalCost }}</strong></p>
    </div>

    <div class="payment-method-selector">
      <label :class="{ 'active': orderStore.paymentMethod === 'WECHAT' }">
        <input type="radio" v-model="orderStore.paymentMethod" value="WECHAT" name="payment-method"/>
        <img src="/wechat-logo.png" alt="微信支付" class="payment-button-image"/>
      </label>
      <label :class="{ 'active': orderStore.paymentMethod === 'ALIPAY' }">
        <input type="radio" v-model="orderStore.paymentMethod" value="ALIPAY" name="payment-method"/>
        <img src="/alipay-logo.png" alt="支付宝" class="payment-button-image"/>
      </label>
    </div>

    <div class="payment-section">
      <div v-if="orderStore.paymentMethod === 'WECHAT'">
        <p class="payment-instruction">请使用微信扫描下方二维码完成支付</p>
        <img src="/wechat_qr.jpg" alt="微信收款二维码" class="qr-code">
      </div>
      <div v-if="orderStore.paymentMethod === 'ALIPAY'">
         <p class="payment-instruction">请使用支付宝扫描二维码，或点击下方链接</p>
         <img src="/alipay_qr.jpg" alt="支付宝收款二维码" class="qr-code">
         <a href="https://qr.alipay.com/2m611064ovvydd9jbdrnv22" target="_blank" class="payment-link">
           点此跳转支付宝APP付款
         </a>
      </div>
    </div>

    <div class="payment-section">
      <PaymentUploader @upload-success="onScreenshotUploaded" />
    </div>

    <div class="form-group">
      <label>请输入手机号以完成下单：</label>
      <input type="tel" v-model="orderStore.phoneNumber" placeholder="用于查询订单" :disabled="isLoading" />
    </div>

    <BaseButton @click="createOrder" :loading="isLoading" class="full-width-btn">我已支付，确认下单</BaseButton>
    <BaseButton variant="secondary" @click="$emit('back')" class="full-width-btn secondary-action-btn">上一步</BaseButton>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useOrderStore } from '@/stores/order';
import PaymentUploader from '@/components/PaymentUploader.vue';
import BaseButton from '@/components/BaseButton.vue';

const emits = defineEmits(['screenshot-uploaded','create-order','back']);
const orderStore = useOrderStore();

const isLoading = computed(() => orderStore.isSubmitting || false);
const anyEstimated = computed(() => orderStore.groups.some(g => g.documents.some(d => d.isEstimated)));
const totalCost = computed(() => orderStore.totalCost);

function onScreenshotUploaded(id) {
  emits('screenshot-uploaded', id);
}

function createOrder() {
  emits('create-order');
}
</script>

<style scoped>
.secondary-action-btn {
  margin-top: 1rem;
}
</style>
