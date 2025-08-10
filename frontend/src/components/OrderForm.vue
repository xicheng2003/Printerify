<template>
  <div class="order-form">
    <!-- 用户认证状态提示 -->
    <div v-if="userStore.isAuthenticated" class="user-info">
      <div class="user-badge">
        <span class="user-icon">👤</span>
        <span>已登录: {{ userStore.userProfile?.username || userStore.userProfile?.phone_number }}</span>
        <span class="order-note">订单将自动关联到您的账户</span>
      </div>
    </div>

    <div v-else class="guest-info">
      <div class="guest-badge">
        <span class="guest-icon">👥</span>
        <span>游客模式</span>
        <span class="order-note">建议登录以获得更好的订单管理体验</span>
        <button @click="showLoginModal = true" class="login-btn">立即登录</button>
      </div>
    </div>

    <!-- 订单配置表单 -->
    <div class="order-config-section">
      <h3 class="section-title">订单配置</h3>

      <!-- 文件列表显示 -->
      <div v-if="orderStore.groups.length > 0" class="files-section">
        <h4 class="subsection-title">已选择的文件</h4>
        <div class="files-list">
          <div v-for="group in orderStore.groups" :key="group.id" class="file-group">
            <div class="group-header">
              <span class="group-label">装订组 {{ group.id.slice(-4) }}</span>
              <select
                v-model="group.bindingType"
                @change="orderStore.updateGroupBinding(group.id, group.bindingType)"
                class="binding-select"
              >
                <option value="none">不装订</option>
                <option value="staple_top_left">订书钉 (左上角)</option>
                <option value="staple_left_side">订书钉 (左侧)</option>
                <option value="staple">骑马钉</option>
                <option value="ring_bound">胶圈装</option>
              </select>
            </div>

            <div class="documents-list">
              <div v-for="doc in group.documents" :key="doc.id" class="document-item">
                <div class="doc-info">
                  <span class="doc-name">{{ doc.fileName }}</span>
                  <span v-if="doc.error" class="doc-error">{{ doc.error }}</span>
                  <span v-else-if="doc.isUploading" class="doc-status">上传中... {{ doc.uploadProgress }}%</span>
                  <span v-else-if="doc.isRecalculating" class="doc-status">计算价格中...</span>
                  <span v-else class="doc-status">已就绪</span>
                </div>

                <div class="doc-settings">
                  <select
                    v-model="doc.settings.colorMode"
                    @change="orderStore.updateDocumentSettings(doc.id, { colorMode: doc.settings.colorMode })"
                    class="setting-select"
                  >
                    <option value="black_white">黑白</option>
                    <option value="color">彩色</option>
                  </select>

                  <select
                    v-model="doc.settings.printSided"
                    @change="orderStore.updateDocumentSettings(doc.id, { printSided: doc.settings.printSided })"
                    class="setting-select"
                  >
                    <option value="single">单面</option>
                    <option value="double">双面</option>
                    <option value="single_double">封面单面</option>
                  </select>

                  <select
                    v-model="doc.settings.paperSize"
                    @change="orderStore.updateDocumentSettings(doc.id, { paperSize: doc.settings.paperSize })"
                    class="setting-select"
                  >
                    <option value="a4">A4</option>
                    <option value="b5">B5</option>
                  </select>

                  <input
                    type="number"
                    v-model.number="doc.settings.copies"
                    @change="orderStore.updateDocumentSettings(doc.id, { copies: doc.settings.copies })"
                    min="1"
                    class="copies-input"
                  >

                  <button
                    @click="orderStore.removeDocument(doc.id)"
                    class="remove-btn"
                    title="删除文件"
                  >
                    🗑️
                  </button>
                </div>

                <div v-if="doc.pageCount > 0" class="doc-details">
                  <span class="page-count">{{ doc.pageCount }} 页</span>
                  <span class="print-cost">¥{{ doc.printCost }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 订单信息表单 -->
      <form @submit.prevent="submitOrder" class="form-grid">
        <!-- 手机号码输入 -->
        <div class="form-group full-width">
          <label for="phone_number">
            手机号码
            <span v-if="!userStore.isAuthenticated" class="required">*</span>
            <span v-else class="optional">(可选，用于订单查询)</span>
          </label>
          <input
            type="text"
            id="phone_number"
            v-model="orderDetails.phone_number"
            :placeholder="userStore.isAuthenticated ? '可选，留空将使用账户手机号' : '请输入您的手机号码'"
            :required="!userStore.isAuthenticated"
          >
          <!-- 如果用户已登录且没有手机号，显示提示 -->
          <div v-if="userStore.isAuthenticated && !userStore.userProfile?.phone_number" class="phone-hint">
            💡 建议在个人资料中添加手机号，方便订单查询
          </div>
        </div>

        <!-- 支付方式选择 -->
        <div class="form-group full-width">
          <label for="payment_method">支付方式</label>
          <select id="payment_method" v-model="orderDetails.payment_method" required>
            <option value="ALIPAY">支付宝</option>
            <option value="WECHAT">微信支付</option>
          </select>
        </div>

        <!-- 付款凭证上传 -->
        <div class="form-group full-width">
          <label for="payment_screenshot">付款凭证 (可选)</label>
          <input
            type="file"
            id="payment_screenshot"
            @change="handlePaymentScreenshot"
            accept="image/*"
            class="file-input"
          >
          <div class="file-hint">支持 JPG、PNG 格式，用于确认付款</div>
        </div>

        <!-- 订单总价显示 -->
        <div class="form-group full-width">
          <div class="total-price-display">
            <span class="total-label">订单总价:</span>
            <span class="total-amount">¥{{ orderStore.totalCost }}</span>
          </div>
        </div>

        <div class="form-group full-width">
          <button
            type="submit"
            :disabled="!orderStore.isReadyToSubmit || orderStore.isLoading"
            class="submit-button"
          >
            {{ orderStore.isLoading ? '正在创建订单...' : '提交订单' }}
          </button>
        </div>
      </form>
    </div>

    <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>

    <!-- 登录模态框 -->
    <Modal v-if="showLoginModal" @close="showLoginModal = false">
      <template #header>
        <h3>登录账户</h3>
      </template>
      <template #body>
        <AuthForm @login-success="onLoginSuccess" />
      </template>
    </Modal>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useUserStore } from '../stores/user';
import { useOrderStore } from '../stores/order';
import Modal from './Modal.vue';
import AuthForm from './AuthForm.vue';

const emit = defineEmits(['order-created']);

const userStore = useUserStore();
const orderStore = useOrderStore();

const orderDetails = ref({
  phone_number: '',
  payment_method: 'ALIPAY'
});

const errorMessage = ref('');
const showLoginModal = ref(false);

// 如果用户已登录且有手机号，自动填充
onMounted(() => {
  if (userStore.isAuthenticated && userStore.userProfile?.phone_number) {
    orderDetails.value.phone_number = userStore.userProfile.phone_number;
  }
});

// 登录成功后关闭模态框并填充用户信息
function onLoginSuccess() {
  showLoginModal.value = false;
  if (userStore.userProfile?.phone_number) {
    orderDetails.value.phone_number = userStore.userProfile.phone_number;
  }
}

// 处理付款凭证上传
function handlePaymentScreenshot(event) {
  const file = event.target.files[0];
  if (file) {
    orderStore.paymentScreenshotFile = file;
  }
}

async function submitOrder() {
  errorMessage.value = '';

  try {
    // 使用订单store的createOrder方法
    const orderData = {
      phone_number: orderDetails.value.phone_number || userStore.userProfile?.phone_number,
      payment_method: orderDetails.value.payment_method
    };

    const result = await orderStore.createOrder(orderData);
    emit('order-created', result);

  } catch (error) {
    errorMessage.value = '订单创建失败，请检查您的输入。';
    console.error('Order creation failed:', error);
  }
}
</script>

<style scoped>
.order-form {
  margin-top: 2rem;
  border-top: 1px solid var(--border-color);
  padding-top: 2rem;
}

.user-info, .guest-info {
  margin-bottom: 1.5rem;
  padding: 1rem;
  border-radius: 8px;
  border: 1px solid var(--border-color);
}

.user-info {
  background-color: #f0f9ff;
  border-color: #0ea5e9;
}

.guest-info {
  background-color: #fef3c7;
  border-color: #f59e0b;
}

.user-badge, .guest-badge {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
}

.user-icon, .guest-icon {
  font-size: 1.2rem;
}

.order-note {
  color: #6b7280;
  font-size: 0.8rem;
  margin-left: auto;
}

.login-btn {
  background-color: #3b82f6;
  color: white;
  border: none;
  padding: 0.25rem 0.75rem;
  border-radius: 4px;
  font-size: 0.8rem;
  cursor: pointer;
  margin-left: auto;
}

.login-btn:hover {
  background-color: #2563eb;
}

.order-config-section {
  margin-top: 2rem;
}

.section-title {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 1rem;
  color: var(--text-color);
}

.subsection-title {
  font-size: 1rem;
  font-weight: 500;
  margin-bottom: 0.75rem;
  color: var(--text-color);
}

.files-section {
  margin-bottom: 2rem;
  padding: 1rem;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  background-color: var(--bg-color);
}

.file-group {
  margin-bottom: 1rem;
  padding: 1rem;
  border: 1px solid var(--border-color);
  border-radius: 6px;
  background-color: var(--bg-color);
}

.group-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.group-label {
  font-weight: 500;
  color: var(--text-color);
}

.binding-select {
  padding: 0.25rem 0.5rem;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  font-size: 0.9rem;
}

.documents-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.document-item {
  padding: 0.75rem;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  background-color: var(--bg-color);
}

.doc-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.doc-name {
  font-weight: 500;
  color: var(--text-color);
}

.doc-status {
  font-size: 0.8rem;
  color: #6b7280;
}

.doc-error {
  font-size: 0.8rem;
  color: #ef4444;
}

.doc-settings {
  display: flex;
  gap: 0.5rem;
  align-items: center;
  margin-bottom: 0.5rem;
  flex-wrap: wrap;
}

.setting-select, .copies-input {
  padding: 0.25rem 0.5rem;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  font-size: 0.8rem;
  min-width: 80px;
}

.copies-input {
  width: 60px;
}

.remove-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1rem;
  padding: 0.25rem;
  border-radius: 4px;
}

.remove-btn:hover {
  background-color: #f3f4f6;
}

.doc-details {
  display: flex;
  justify-content: space-between;
  font-size: 0.8rem;
  color: #6b7280;
}

.page-count {
  color: var(--text-color);
}

.print-cost {
  color: #10b981;
  font-weight: 500;
}

.required {
  color: #ef4444;
}

.optional {
  color: #6b7280;
  font-size: 0.8rem;
}

.phone-hint {
  font-size: 0.8rem;
  color: #6b7280;
  margin-top: 0.25rem;
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
}

.full-width {
  grid-column: 1 / -1;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: var(--text-color);
}

.form-group input,
.form-group select {
  padding: 0.75rem;
  border: 1px solid var(--border-color);
  border-radius: 6px;
  font-size: 1rem;
  background-color: var(--bg-color);
  color: var(--text-color);
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.file-input {
  padding: 0.5rem;
  border: 2px dashed var(--border-color);
  border-radius: 6px;
  background-color: var(--bg-color);
  cursor: pointer;
}

.file-hint {
  font-size: 0.8rem;
  color: #6b7280;
  margin-top: 0.25rem;
}

.total-price-display {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background-color: #f0f9ff;
  border: 1px solid #0ea5e9;
  border-radius: 8px;
}

.total-label {
  font-size: 1.1rem;
  font-weight: 500;
  color: var(--text-color);
}

.total-amount {
  font-size: 1.5rem;
  font-weight: 700;
  color: #10b981;
}

.submit-button {
  background-color: #10b981;
  color: white;
  border: none;
  padding: 1rem 2rem;
  border-radius: 8px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s;
}

.submit-button:hover:not(:disabled) {
  background-color: #059669;
}

.submit-button:disabled {
  background-color: #9ca3af;
  cursor: not-allowed;
}

.error-message {
  margin-top: 1rem;
  padding: 1rem;
  background-color: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 6px;
  color: #dc2626;
  text-align: center;
}
</style>
