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
      <p class="pages-info">共需打印 {{ totalPages }} 页</p>
    </div>

    <!-- 支付方式选择 -->
    <div class="payment-method-selector">
      <label :class="{ 'active': orderStore.paymentMethod === 'WECHAT' }">
        <input type="radio" v-model="orderStore.paymentMethod" value="WECHAT" name="payment-method"/>
        <img src="/wechat-logo.png" alt="微信支付" class="payment-button-image"/>
      </label>
      <label :class="{ 'active': orderStore.paymentMethod === 'ALIPAY' }">
        <input type="radio" v-model="orderStore.paymentMethod" value="ALIPAY" name="payment-method"/>
        <img src="/alipay-logo.png" alt="支付宝" class="payment-button-image"/>
      </label>
      <label
        v-if="userStore.isAuthenticated"
        :class="{ 'active': orderStore.paymentMethod === 'BALANCE', 'disabled': userBalance < totalPages }"
        class="balance-label"
      >
        <input
          type="radio"
          v-model="orderStore.paymentMethod"
          value="BALANCE"
          name="payment-method"
          :disabled="userBalance < totalPages"
        />
        <div class="balance-payment-content">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="balance-icon">
            <circle cx="12" cy="12" r="10"></circle>
            <path d="M16 8h-6a2 2 0 1 0 0 4h4a2 2 0 1 1 0 4H8"></path>
            <path d="M12 18V6"></path>
          </svg>
          <span class="balance-text">余额支付</span>
          <span class="balance-hint">({{ userBalance }}页)</span>
        </div>
      </label>
    </div>

    <!-- 余额支付详情 -->
    <div v-if="orderStore.paymentMethod === 'BALANCE'" class="balance-payment-detail">
      <div v-if="userBalance >= totalPages" class="balance-sufficient">
        <div class="balance-check-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
            <polyline points="22 4 12 14.01 9 11.01"></polyline>
          </svg>
        </div>
        <h4>余额充足，可以支付</h4>
        <div class="balance-calculation">
          <div class="calc-row">
            <span>当前余额：</span>
            <span class="calc-value">{{ userBalance }} 页</span>
          </div>
          <div class="calc-row">
            <span>本次消费：</span>
            <span class="calc-value deduct">- {{ totalPages }} 页</span>
          </div>
          <div class="calc-row total">
            <span>支付后余额：</span>
            <span class="calc-value">{{ userBalance - totalPages }} 页</span>
          </div>
        </div>
        <router-link to="/packages" class="recharge-link-inline">余额不够？去购买套餐</router-link>
      </div>
      <div v-else class="balance-insufficient">
        <div class="balance-warn-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"/>
            <line x1="12" y1="8" x2="12" y2="12"/>
            <line x1="12" y1="16" x2="12.01" y2="16"/>
          </svg>
        </div>
        <h4>余额不足</h4>
        <p>当前余额 {{ userBalance }} 页，需要 {{ totalPages }} 页，还差 {{ totalPages - userBalance }} 页</p>
        <router-link to="/packages" class="recharge-btn-large">立即购买套餐</router-link>
      </div>
    </div>

    <!-- 第三方支付：二维码和上传凭证 -->
    <div v-if="orderStore.paymentMethod === 'WECHAT' || orderStore.paymentMethod === 'ALIPAY'" class="third-party-payment">
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
    </div>

    <div class="form-group">
      <label>请输入手机号以完成下单：</label>
      <input type="tel" v-model="orderStore.phoneNumber" placeholder="用于查询订单" :disabled="isLoading" />
      <p v-if="isAutoFilled" class="auto-fill-hint">
        <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
        已自动填充您绑定的手机号
      </p>
    </div>

    <!-- 备注触发区域 (简洁版) -->
    <div class="remark-simple-trigger" @click="showRemarkModal = true" role="button" tabindex="0">
      <svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="remark-icon-simple">
        <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
        <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
      </svg>
      <span v-if="!orderStore.remark">添加备注（可选）</span>
      <span v-else class="remark-text-preview">
        <span class="label">备注：</span>{{ orderStore.remark }}
      </span>
    </div>

    <BaseButton @click="createOrder" :loading="isLoading" class="full-width-btn">我已支付，确认下单</BaseButton>
    <BaseButton variant="secondary" @click="$emit('back')" class="full-width-btn secondary-action-btn">上一步</BaseButton>

    <!-- 备注模态框 -->
    <Teleport to="body">
      <Modal :show="showRemarkModal" @close="showRemarkModal = false">
        <template #header><h3>订单备注</h3></template>
        <template #body>
          <div class="remark-input-wrapper">
            <textarea
              v-model="orderStore.remark"
              placeholder="如有特殊要求（如：配送时间、包装要求等），请在此说明..."
              rows="5"
              class="remark-textarea"
            ></textarea>
          </div>
        </template>
        <template #footer>
          <div class="modal-actions">
             <BaseButton @click="showRemarkModal = false" class="full-width-btn">保存备注</BaseButton>
          </div>
        </template>
      </Modal>
    </Teleport>
  </div>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue';
import { useOrderStore } from '@/stores/order';
import { useUserStore } from '@/stores/user';
import PaymentUploader from '@/components/PaymentUploader.vue';
import BaseButton from '@/components/BaseButton.vue';
import Modal from '@/components/Modal.vue';
import apiService from '@/services/apiService';

const emits = defineEmits(['screenshot-uploaded','create-order','back']);
const orderStore = useOrderStore();
const userStore = useUserStore();

const showRemarkModal = ref(false);
const userBalance = ref(0);

const isLoading = computed(() => orderStore.isSubmitting || false);
const anyEstimated = computed(() => orderStore.groups.some(g => g.documents.some(d => d.isEstimated)));
const totalCost = computed(() => orderStore.totalCost);

// 计算订单总页数
const totalPages = computed(() => {
  let total = 0;
  orderStore.groups.forEach(group => {
    group.documents.forEach(doc => {
      total += (doc.pageCount || 0) * (doc.copies || 1);
    });
  });
  return total;
});

const isAutoFilled = computed(() => {
  return userStore.isAuthenticated &&
         userStore.user?.phone_number &&
         orderStore.phoneNumber === userStore.user.phone_number;
});

function onScreenshotUploaded(id) {
  emits('screenshot-uploaded', id);
}

// 加载用户余额
async function loadUserBalance() {
  if (!userStore.isAuthenticated) return;
  try {
    const response = await apiService.getUserBalance();
    userBalance.value = response.data.page_balance || 0;
  } catch (error) {
    console.error('获取余额失败:', error);
  }
}

function createOrder() {
  // 判断是否使用余额支付
  const useBalance = orderStore.paymentMethod === 'BALANCE';

  // 如果选择余额支付但余额不足，阻止提交
  if (useBalance && userBalance.value < totalPages.value) {
    alert('余额不足，无法下单');
    return;
  }

  // 将使用余额的选项传递给父组件
  emits('create-order', { useBalance });
}

onMounted(() => {
  loadUserBalance();
});

// 监听用户登录状态变化
if (userStore.isAuthenticated) {
  loadUserBalance();
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

/* 备注触发区域 (简洁版) */
.remark-simple-trigger {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  margin-top: 0.5rem;
  margin-bottom: 1.5rem;
  cursor: pointer;
  color: var(--color-text-mute);
  font-size: 0.9rem;
  transition: color 0.2s;
  user-select: none;
}

.remark-simple-trigger:hover {
  color: var(--color-primary);
}

.remark-icon-simple {
  flex-shrink: 0;
  opacity: 0.8;
}

.remark-text-preview {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 300px; /* 限制最大宽度，防止过长 */
}

.remark-text-preview .label {
  font-weight: 500;
}

/* 模态框内样式 */
.remark-input-wrapper {
  margin-bottom: 1rem;
}
.remark-textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid var(--color-border);
  border-radius: 8px;
  background-color: var(--color-background);
  color: var(--color-text);
  font-family: inherit;
  font-size: 0.95rem;
  resize: vertical;
  transition: border-color 0.2s;
}

.remark-textarea:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 2px rgba(var(--color-primary-rgb, 37, 99, 235), 0.1);
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
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

.pages-info {
  margin-top: 0.5rem;
  font-size: 0.9rem;
  color: var(--color-text-mute);
}

.payment-method-selector {
  display: flex;
  justify-content: center;
  gap: 1.5rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
}

.payment-method-selector label {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  border: 2px solid var(--color-border);
  border-radius: 12px;
  padding: 1rem;
  transition: all 0.2s ease-in-out;
  min-width: 140px;
  box-sizing: border-box;
  background-color: var(--color-background);
  position: relative;
}

.payment-method-selector label:hover:not(.disabled) {
  border-color: var(--color-border-hover);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.payment-method-selector label.active {
  border-color: var(--color-primary);
  background-color: rgba(var(--color-primary-rgb, 37, 99, 235), 0.05);
}

.payment-method-selector label.disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.payment-method-selector input[type="radio"] {
  display: none;
}

.payment-button-image {
  display: block;
  height: 40px;
  width: auto;
  object-fit: contain;
  transition: filter 0.3s;
}

/* 余额支付选项样式 */
.balance-label {
  flex-direction: row !important;
  padding: 0.75rem 1rem !important;
}

.balance-payment-content {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.balance-icon {
  color: var(--color-primary);
  flex-shrink: 0;
  transition: filter 0.3s;
}

html.dark .balance-icon {
  filter: grayscale(1) brightness(1.5);
}

.balance-text {
  font-size: 0.9rem;
  font-weight: 500;
  color: var(--color-heading);
}

.balance-hint {
  font-size: 0.8rem;
  color: var(--color-text-mute);
}

.payment-method-name {
  font-size: 0.9rem;
  font-weight: 500;
  color: var(--color-heading);
  text-align: center;
}

/* 余额支付详情 */
.balance-payment-detail {
  background-color: var(--color-background-soft);
  border: 1px solid var(--color-border);
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
  text-align: center;
}

.balance-sufficient h4,
.balance-insufficient h4 {
  margin-top: 0.5rem;
  margin-bottom: 1rem;
  font-size: 1.2rem;
  color: var(--color-heading);
}

.balance-check-icon,
.balance-warn-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 64px;
  height: 64px;
  border-radius: 50%;
  margin-bottom: 0.5rem;
}

.balance-check-icon {
  background-color: rgba(16, 185, 129, 0.1);
  color: #10b981;
}

.balance-warn-icon {
  background-color: rgba(239, 68, 68, 0.1);
  color: #ef4444;
}

.balance-calculation {
  background-color: var(--color-background);
  border-radius: 8px;
  padding: 1rem;
  margin: 1rem 0;
  text-align: left;
}

.calc-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 0;
  font-size: 0.95rem;
  color: var(--color-text);
}

.calc-row.total {
  border-top: 2px solid var(--color-border);
  margin-top: 0.5rem;
  padding-top: 1rem;
  font-weight: 600;
  font-size: 1.05rem;
}

.calc-value {
  font-weight: 600;
  color: var(--color-primary);
}

.calc-value.deduct {
  color: #ef4444;
}

.recharge-link-inline {
  display: inline-block;
  margin-top: 1rem;
  font-size: 0.9rem;
  color: var(--color-primary);
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  background-color: rgba(59, 130, 246, 0.1);
  transition: all 0.2s;
}

.recharge-link-inline:hover {
  background-color: rgba(59, 130, 246, 0.2);
}

.balance-insufficient p {
  color: var(--color-text);
  margin-bottom: 1.5rem;
}

.recharge-btn-large {
  display: inline-block;
  padding: 0.75rem 2rem;
  background-color: var(--color-primary);
  color: white;
  text-decoration: none;
  border-radius: 8px;
  font-weight: 600;
  transition: all 0.2s;
  box-shadow: 0 2px 8px rgba(var(--color-primary-rgb, 37, 99, 235), 0.3);
}

.recharge-btn-large:hover {
  background-color: var(--color-primary-dark);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(var(--color-primary-rgb, 37, 99, 235), 0.4);
}

/* 第三方支付区域 */
.third-party-payment {
  border-top: 1px solid var(--color-border);
  margin-top: 1.5rem;
  padding-top: 1.5rem;
}

html.dark .payment-button-image {
  filter: invert(1) grayscale(1) brightness(1.5);
}

.payment-section {
  text-align: center;
  margin-top: 1.5rem;
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
  .payment-method-selector label { min-width: 120px; padding: 0.75rem; }
}
</style>
