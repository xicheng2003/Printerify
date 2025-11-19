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
      <p v-if="isAutoFilled" class="auto-fill-hint">
        <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
        已自动填充您绑定的手机号
      </p>
    </div>

    <BaseButton @click="createOrder" :loading="isLoading" class="full-width-btn">我已支付，确认下单</BaseButton>
    <BaseButton variant="secondary" @click="$emit('back')" class="full-width-btn secondary-action-btn">上一步</BaseButton>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useOrderStore } from '@/stores/order';
import { useUserStore } from '@/stores/user';
import PaymentUploader from '@/components/PaymentUploader.vue';
import BaseButton from '@/components/BaseButton.vue';

const emits = defineEmits(['screenshot-uploaded','create-order','back']);
const orderStore = useOrderStore();
const userStore = useUserStore();

const isLoading = computed(() => orderStore.isSubmitting || false);
const anyEstimated = computed(() => orderStore.groups.some(g => g.documents.some(d => d.isEstimated)));
const totalCost = computed(() => orderStore.totalCost);

const isAutoFilled = computed(() => {
  return userStore.isAuthenticated &&
         userStore.user?.phone_number &&
         orderStore.phoneNumber === userStore.user.phone_number;
});

function onScreenshotUploaded(id) {
  emits('screenshot-uploaded', id);
}

function createOrder() {
  emits('create-order');
}
</script>

<style scoped>
.step-title {
  font-size: 1.5rem;
  font-weight: 600;
  text-align: center;
  margin-bottom: 2rem;
  color: var(--color-heading);
}

.order-estimated-alert {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  background-color: rgba(var(--color-primary-rgb, 37, 99, 235), 0.08);
  border: 1px solid rgba(var(--color-primary-rgb, 37, 99, 235), 0.2);
  border-radius: 12px;
  margin: 0.5rem 0 1rem;
}

.auto-fill-hint {
  margin-top: 0.5rem;
  font-size: 0.85rem;
  color: var(--color-primary);
  display: flex;
  align-items: center;
  gap: 0.35rem;
}

.order-estimated-alert .estimated-icon {
  color: var(--color-primary);
  flex-shrink: 0;
  margin-top: 2px;
}

.order-estimated-alert .estimated-text strong {
  display: block;
  font-weight: 600;
  color: var(--color-heading);
  margin-bottom: 0.25rem;
}

.order-estimated-alert .estimated-text span {
  color: var(--color-text);
  font-size: 0.95rem;
  line-height: 1.6;
}

.price-result {
  background-color: var(--color-background-mute);
  border: 1px solid var(--color-primary);
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 1.5rem;
  text-align: center;
}

.price-result p {
    color: var(--color-text);
}

.price {
  font-size: 1.75rem;
  color: var(--color-primary);
  font-weight: 700;
}

.payment-method-selector {
  display: flex;
  justify-content: center;
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.payment-method-selector label {
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  border: 1px solid var(--color-border);
  border-radius: 10px;
  padding: 4px;
  transition: all 0.2s ease-in-out;
  width: 160px;
  height: 56px;
  box-sizing: border-box;
  background-color: var(--color-background);
}

.payment-method-selector label:hover {
  border-color: var(--color-border-hover);
}

.payment-method-selector label.active {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 2px var(--color-primary);
}

.payment-method-selector input[type="radio"] {
  display: none;
}

.payment-button-image {
  display: block;
  max-height: 100%;
  max-width: 100%;
  object-fit: contain;
  transition: filter 0.3s;
}

html.dark .payment-button-image {
  filter: invert(1) grayscale(1) brightness(1.5);
}

.payment-section {
  border-top: 1px solid var(--color-border);
  padding: 1.5rem 0;
  margin-top: 1.5rem;
  text-align: center;
}

.payment-instruction {
  margin-top: 0;
  color: var(--color-text);
}

.qr-code {
  max-width: 180px;
  margin: 1rem auto;
  display: block;
  border-radius: 8px;
  background-color: white;
  padding: 5px;
}

.payment-link {
  display: inline-block;
  margin-top: 1rem;
  padding: 0.6rem 1.2rem;
  background-color: #1677ff;
  color: white;
  text-decoration: none;
  border-radius: 5px;
  font-weight: 500;
  transition: background-color 0.2s;
}

.payment-link:hover {
  background-color: #4096ff;
}

.form-group {
  margin-top: 1.5rem;
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.75rem;
  font-weight: 500;
  color: var(--color-heading);
}

.form-group input[type="tel"] {
  width: 100%;
  padding: 0.75rem 1rem;
  font-size: 1rem;
  border-radius: 8px;
  border: 1px solid var(--color-border);
  background-color: var(--color-background);
  color: var(--color-text);
  transition: border-color 0.2s, box-shadow 0.2s;
}

.form-group input[type="tel"]:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(var(--color-primary-rgb, 37, 99, 235), 0.2);
}

.form-group input[type="tel"]::placeholder {
  color: var(--color-text-mute);
  opacity: 0.7;
}

.full-width-btn {
  width: 100%;
  padding: 0.875rem;
  font-size: 1.1rem;
}

.secondary-action-btn {
  margin-top: 1rem;
}

@media (max-width: 767px) {
  .step-title { font-size: 1.25rem; }
  .payment-method-selector { gap: 1rem; }
  .payment-method-selector label { width: 140px; height: 48px; }
}
</style>
