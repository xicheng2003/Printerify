<template>
  <div class="home-view container">
    <Teleport to="body">
      <div v-if="isLoading" class="loading-overlay">
        <div class="spinner"></div>
        <p class="loading-text">处理中，请稍候...</p>
      </div>
    </Teleport>

    <!-- 订单人工处理时效提醒横幅（5秒后显示，固定顶部，内容下移） -->
    <Teleport to="body">
      <transition name="slide-down" appear>
        <div v-if="showTimingBanner" class="timing-banner" role="alert" aria-live="polite">
          <div class="timing-banner-content">
            <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="timing-banner-icon">
              <circle cx="12" cy="12" r="10"></circle>
              <line x1="12" y1="8" x2="12.01" y2="8"></line>
              <line x1="12" y1="12" x2="12" y2="16"></line>
            </svg>
            <div class="timing-banner-text">
              <strong>下单提示：</strong>
              <span>
                订单提交后需人工打印处理，请耐心等待完成。若您时间紧急，请先与客服沟通并确认预计完成时间后再下单，以免影响使用。感谢理解与支持！
              </span>
            </div>
          </div>
          <button class="timing-banner-close" @click="dismissTimingBanner" aria-label="关闭时效提醒">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>
      </transition>
    </Teleport>

    <!-- 登录引导横幅 - 仅对未登录用户显示 -->
    <transition name="slide-down" appear>
      <div v-if="!userStore.isAuthenticated && showLoginGuideBanner" class="login-guide-banner">
        <div class="banner-content">
          <div class="banner-left">
            <div class="banner-icon">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"></path>
                <polyline points="10,17 15,12 10,7"></polyline>
                <line x1="15" y1="12" x2="3" y2="12"></line>
              </svg>
            </div>
            <div class="banner-text">
              <h3 class="banner-title">登录体验更多功能</h3>
              <p class="banner-subtitle">保存订单历史 • 专属优惠券 • 快速下单</p>
            </div>
          </div>
          <div class="banner-actions">
            <button @click="goToLogin" class="banner-login-btn">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"></path>
                <polyline points="10,17 15,12 10,7"></polyline>
                <line x1="15" y1="12" x2="3" y2="12"></line>
              </svg>
              立即登录
            </button>
            <button @click="goToRegister" class="banner-register-btn">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                <circle cx="8.5" cy="7" r="4"></circle>
                <line x1="20" y1="8" x2="20" y2="14"></line>
                <line x1="23" y1="11" x2="17" y2="11"></line>
              </svg>
              免费注册
            </button>
            <button @click="remindLater" class="banner-remind-btn">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="10"></circle>
                <polyline points="12,6 12,12 16,14"></polyline>
              </svg>
              稍后提醒
            </button>
          </div>
          <button @click="dismissBanner" class="banner-close-btn" title="关闭提示">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>
      </div>
    </transition>

    <section class="hero-section">
      <h2 class="animated-hero-title">简单、快速、可靠</h2>
      <p>Printerify，为每一次打印赋能。</p>
    </section>

    <section class="process-section">
      <div class="process-card">
        <Stepper :current-step="currentStep" :steps="['配置订单', '支付', '完成']" />

        <div class="step-content">
          <Step1_Config
            v-if="currentStep === 1"
            ref="fileUploaderRef"
            :agreedToTerms="agreedToTerms"
            :agreedToPrivacy="agreedToPrivacy"
            @update:agreedToTerms="agreedToTerms = $event"
            @update:agreedToPrivacy="agreedToPrivacy = $event"
            @next="goToPaymentStep"
            @open-terms="openTermsModal"
            @open-privacy="openPrivacyModal"
            @show-billing="showBillingModal = true"
          />

          <Step2_Payment
            v-if="currentStep === 2"
            @screenshot-uploaded="onScreenshotUploaded"
            @create-order="handleCreateOrder"
            @back="currentStep = 1"
          />

          <Step3_Result v-if="currentStep === 3 && finalOrder" :finalOrder="finalOrder" @reset="resetForNewOrder" />
        </div>

        <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
      </div>
    </section>
  </div>

  <Teleport to="body">
    <Modal :show="showTermsModal" @close="showTermsModal = false">
        <template #header><h3>服务条款</h3></template>
        <template #body>
          <LegalDocument type="terms" mode="compact" />
        </template>
    </Modal>

    <Modal :show="showPrivacyModal" @close="showPrivacyModal = false">
        <template #header><h3>隐私协议</h3></template>
        <template #body>
          <LegalDocument type="privacy" mode="compact" />
        </template>
    </Modal>

    <Modal :show="showBillingModal" @close="showBillingModal = false">
      <template #header><h3>计费规则说明</h3></template>
      <template #body>
        <div class="billing-rules-content" v-if="orderStore.pricingConfig">
          <ul>
            <li>
              <strong>计价公式</strong>
              <p><span class="formula-highlight">总费用 = 基础服务费 + 打印费用 + 装订费用（可选）</span></p>
            </li>
            <li>
              <strong>基础服务费</strong>
              <p>每笔订单将统一收取 {{ orderStore.pricingConfig.base_service_fee }}元 的基础服务费。</p>
            </li>
            <li>
              <strong>打印费用</strong>
              <p>单面双面相同价格。</p>
              <table class="price-table">
                <thead>
                  <tr>
                    <th>规格</th>
                    <th>色彩</th>
                    <th>单价（每面）</th>
                  </tr>
                </thead>
                <tbody>
                  <template v-for="(specs, paperSize) in orderStore.pricingConfig.print" :key="paperSize">
                    <template v-for="(modes, colorMode) in specs" :key="colorMode">
                      <tr>
                        <td>{{ formatPaperSize(paperSize) }}</td>
                        <td>{{ formatColorMode(colorMode) }}</td>
                        <td>{{ modes.single }}元</td>
                      </tr>
                    </template>
                  </template>
                </tbody>
              </table>
            </li>
            <li>
              <strong>装订费用</strong>
              <table class="price-table">
                <thead>
                  <tr>
                    <th>装订方式</th>
                    <th>价格</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(price, type) in orderStore.pricingConfig.binding" :key="type">
                    <td>{{ formatBindingType(type) }}</td>
                    <td>{{ price }}元</td>
                  </tr>
                </tbody>
              </table>
            </li>
          </ul>
        </div>
        <div v-else class="loading-text">正在加载计费规则...</div>
      </template>
    </Modal>
  </Teleport>
</template>

<script setup>
import { ref, watch, onUnmounted, onMounted, nextTick } from 'vue'; //【修改】引入 watch, onUnmounted, onMounted, nextTick
import { useRouter } from 'vue-router'; // 导入路由
import { useOrderStore } from '@/stores/order';
import apiService from '@/services/apiService'; //【修改】使用apiService而不是直接使用axios
import { useUserStore } from '@/stores/user'; // 导入用户状态管理

// 导入组件
import Stepper from '@/components/Stepper.vue';
// FileUploader/PaymentUploader/BaseButton are now encapsulated in step components
import Modal from '@/components/Modal.vue';
// OrderConfiguration moved into Step1_Config
import LegalDocument from '@/components/legal/LegalDocument.vue';
import Step1_Config from '@/components/home/Step1_Config.vue';
import Step2_Payment from '@/components/home/Step2_Payment.vue';
import Step3_Result from '@/components/home/Step3_Result.vue';

// --- 使用 Pinia Store 和 Router ---
const orderStore = useOrderStore();
const userStore = useUserStore(); // 使用用户状态管理
const router = useRouter(); // 使用路由
const screenshotId = ref(null); // <-- 【新增】用于存储凭证ID的状态

// ▼▼▼ 订单时效提醒横幅状态（5秒后出现） ▼▼▼
const showTimingBanner = ref(false);
function dismissTimingBanner() {
  showTimingBanner.value = false;
}

// --- UI 控制相关的本地状态 ---
const currentStep = ref(1);
const isLoading = ref(false); // 用于控制加载状态
const errorMessage = ref('');
const agreedToTerms = ref(false);
const agreedToPrivacy = ref(false);
const showTermsModal = ref(false);
const showPrivacyModal = ref(false);
const showBillingModal = ref(false); // 用于显示计费规则说明的模态框
const fileUploaderRef = ref(null);
const finalOrder = ref(null); // 用于存储最终成功创建的订单信息

// 法律文档更新提醒标识
const LEGAL_UPDATE_DATE = '2025-10-21'; // 法律文档最后更新日期
// legal update flag and binding help moved into step components

// 登录引导横幅相关状态
const showLoginGuideBanner = ref(true); // 默认显示

// 页面初始化时检查用户是否之前关闭过横幅
onMounted(() => {
  // 获取最新的计费规则
  orderStore.fetchPricingConfig();

  // 5 秒后显示订单人工处理时效提醒横幅
  setTimeout(() => {
    showTimingBanner.value = true;
  }, 5000);
});

// 根据横幅高度动态向下推内容，避免覆盖
watch(showTimingBanner, async (visible) => {
  if (typeof window === 'undefined') return;
  if (visible) {
    await nextTick();
    const el = document.querySelector('.timing-banner');
    if (el) {
      document.body.style.paddingTop = el.offsetHeight + 'px';
    }
  } else {
    document.body.style.paddingTop = '';
  }
});

// 监听步骤变化，自动滚动到顶部
watch(currentStep, () => {
  if (typeof window !== 'undefined') {
    window.scrollTo({ top: 400, behavior: 'smooth' });
  }
});

// 监听用户登录状态变化
const unwatchAuth = watch(() => userStore.isAuthenticated, (isAuth) => {
  if (isAuth) {
    // 用户登录成功后自动隐藏横幅
    showLoginGuideBanner.value = false;
  } else {
    // 用户登出后重新显示横幅
    showLoginGuideBanner.value = true;
  }
});

// 监听用户信息变化，自动填充手机号
watch(() => userStore.user, (newUser) => {
  if (newUser && newUser.phone_number && !orderStore.phoneNumber) {
    orderStore.phoneNumber = newUser.phone_number;
  }
}, { immediate: true });

// 组件卸载时清理监听器
onUnmounted(() => {
  unwatchAuth();
});

function dismissBanner() {
  showLoginGuideBanner.value = false;
}

function goToLogin() {
  router.push('/auth/login');
  dismissBanner();
}

function goToRegister() {
  router.push('/auth/register');
  dismissBanner();
}

function remindLater() {
  showLoginGuideBanner.value = false;
  setTimeout(() => {
    if (!userStore.isAuthenticated) {
      showLoginGuideBanner.value = true;
    }
  }, 5 * 60 * 1000);
}

function openTermsModal() {
  showTermsModal.value = true;
  localStorage.setItem('legalDocsLastViewed', LEGAL_UPDATE_DATE);
}

function openPrivacyModal() {
  showPrivacyModal.value = true;
  localStorage.setItem('legalDocsLastViewed', LEGAL_UPDATE_DATE);
}

// Step components manage ready/next text and file selection

function onScreenshotUploaded(uploadedId) {
  screenshotId.value = uploadedId;
}

function goToPaymentStep() {
  if (agreedToTerms.value && agreedToPrivacy.value && orderStore.isReadyToSubmit) {
    currentStep.value = 2;
  }
}

async function handleCreateOrder() {
  if (!screenshotId.value) {
    errorMessage.value = '请先上传付款截图！';
    return;
  }
  if (!orderStore.phoneNumber) {
    errorMessage.value = '请输入您的手机号码！';
    return;
  }

  isLoading.value = true;
  errorMessage.value = '';

  const payload = {
    payment_screenshot_id: screenshotId.value,
    payment_method: orderStore.paymentMethod,
    phone_number: orderStore.phoneNumber,
    remark: orderStore.remark, // 添加备注字段
    groups: orderStore.groups.map((group, groupIndex) => ({
      binding_type: group.bindingType,
      sequence_in_order: groupIndex + 1,
      documents: group.documents.map((doc, docIndex) => ({
        file_id: doc.serverId,
        original_filename: doc.fileName,
        paper_size: doc.settings.paperSize,
        color_mode: doc.settings.colorMode,
        print_sided: doc.settings.printSided,
        copies: doc.settings.copies,
        sequence_in_group: docIndex + 1,
      })),
    })),
  };

  try {
    const response = await apiService.createOrder(payload);
    finalOrder.value = response.data;
    currentStep.value = 3;
  } catch (error) {
    console.error('Order creation failed:', error.response?.data || error.message);
    errorMessage.value = '订单创建失败，请稍后重试或联系客服。';
  } finally {
    isLoading.value = false;
  }
}

function resetForNewOrder() {
  orderStore.resetStore();
  currentStep.value = 1;
  finalOrder.value = null;
  agreedToTerms.value = false;
  agreedToPrivacy.value = false;
  errorMessage.value = '';
  screenshotId.value = null;
  if (fileUploaderRef.value && fileUploaderRef.value.reset) {
    fileUploaderRef.value.reset();
  }
}

// anyEstimated handled inside Step2_Payment

function formatPaperSize(key) {
  const map = {
    'a4_70g': 'A4 (70g)',
    'a4_80g': 'A4 (80g)',
    'b5_70g': 'B5 (70g)'
  };
  return map[key] || key;
}

function formatColorMode(key) {
  const map = {
    'black_white': '黑白',
    'color': '彩色'
  };
  return map[key] || key;
}

function formatBindingType(key) {
  const map = {
    'none': '不装订',
    'staple_top_left': '左上角订书钉',
    'staple_left_side': '左侧订书钉',
    'staple': '骑马钉',
    'ring_bound': '胶圈装订'
  };
  return map[key] || key;
}

</script>

<style>

/* ===================================================================
  样式已更新，使用 CSS 变量以支持主题切换。
  所有布局、尺寸和响应式逻辑均已完整保留。
  ===================================================================
*/
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

.hero-section {
  text-align: center;
  padding: 2rem 0;
  margin-bottom: 2rem;
}

.hero-section h2 {
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--color-heading); /* 已修改 */
  margin-bottom: 0.5rem;
}

.hero-section p {
  font-size: 1.125rem;
  color: var(--color-text-mute); /* 已修改 */
}

.process-section {
  padding-bottom: 2rem;
}

/* 统一风格：订单层级的预估提示样式（与帮助提示风格一致） */
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

.process-card {
  background-color: var(--color-background-soft); /* 已修改 */
  border-radius: 16px;
  padding: 1.5rem 2.5rem;
  max-width: 800px;
  margin: 0 auto;
  box-shadow: var(--shadow-card); /* 已修改 */
  border: 1px solid var(--color-border); /* 已修改 */
  transition: background-color 0.3s, border-color 0.3s;
}



.error-message {
  color: var(--color-text-on-danger); /* 已修改 */
  font-weight: 500;
  margin-top: 1.5rem;
  text-align: center;
  background-color: var(--color-danger); /* 已修改 */
  padding: 0.75rem;
  border-radius: 8px;
}



.billing-rules-content ul {
  list-style-type: none;
  padding-left: 0;
  margin: 0;
}

.billing-rules-content li {
  margin-bottom: 1.25rem;
}

.billing-rules-content li:last-child {
  margin-bottom: 0;
}

.billing-rules-content strong {
  display: block;
  font-size: 1.1em;
  color: var(--color-heading); /* 已修改 */
  margin-bottom: 0.25rem;
}

.billing-rules-content p {
  margin: 0;
  color: var(--color-text-mute); /* 已修改 */
  line-height: 1.6;
}

.formula-highlight {
  display: block;
  text-align: center;
  margin: 1.2em auto 1.2em auto;
  background: var(--color-background-mute);
  color: var(--color-text);
  font-weight: 350;
  padding: 0.8em 1.2em;
  border-radius: 6px;
  font-size: 1.12em;
  letter-spacing: 0.5px;
}
/* 响应式优化 formula-highlight */
.formula-highlight {
  display: block;
  text-align: center;
  margin: 1.2em auto;
  background: var(--color-background-mute);
  color: var(--color-text);
  font-weight: 350;
  padding: 0.8em 1.2em;
  border-radius: 6px;
  font-size: 1.12em;
  letter-spacing: 0.5px;
  word-break: break-word;
  max-width: 100%;
  box-sizing: border-box;
}

@media (max-width: 600px) {
  .formula-highlight {
    font-size: 1em;
    padding: 0.7em 0.5em;
    margin: 1em 0.2em;
  }
}

/* 响应式优化 price-table */
.price-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 0.5em;
  font-size: 0.95em;
  overflow-x: auto;
  display: block;
}

.price-table th, .price-table td {
  border: 1px solid var(--color-border);
  padding: 0.5em 1em;
  text-align: center;
  min-width: 80px;
}

@media (max-width: 600px) {
  .price-table {
    font-size: 0.85em;
    margin-top: 0.5em;
    /* 让表格横向滚动，防止内容溢出 */
    overflow-x: auto;
    display: block;
  }
  .price-table th, .price-table td {
    padding: 0.4em 0.5em;
    min-width: 70px;
    font-size: 0.95em;
  }
}

.price-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 0.5em;
  font-size: 0.95em;
}
.price-table th, .price-table td {
  border: 1px solid var(--color-border);
  padding: 0.5em 1em;
  text-align: center;
}
.price-table th {
  background: var(--color-background-mute);
  font-weight: 600;
  color: var(--color-text);
}
.price-table tr:nth-child(even) {
  background: var(--color-background);
}

html.dark .price-table th {
  background: var(--color-background-mute);
  color: var(--color-text);
}
html.dark .price-table td {
  border-color: var(--color-border);
  color: var(--color-text);
}
html.dark .price-table tr:nth-child(even) {
  background: var(--color-background);
}

@media (max-width: 767px) {
  .hero-section h2 { font-size: 2rem; }
  .hero-section p { font-size: 1rem; }
  .process-card { padding: 1.5rem 1rem; }
}

.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(var(--color-background-rgb, 255, 255, 255), 0.8); /* 已修改，支持主题 */
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  z-index: 9999;
  backdrop-filter: blur(4px);
}

.spinner {
  width: 50px;
  height: 50px;
  border: 5px solid rgba(var(--color-primary-rgb, 37, 99, 235), 0.2); /* 已修改，支持主题 */
  border-top-color: var(--color-primary); /* 已修改 */
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.loading-text {
  margin-top: 1.5rem;
  font-size: 1rem;
  font-weight: 500;
  color: var(--color-text); /* 已修改 */
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}


/* ===================================================================
   登录引导横幅样式
   =================================================================== */
.login-guide-banner {
  background: linear-gradient(135deg,
    rgba(248, 250, 252, 0.95) 0%,
    rgba(241, 245, 249, 0.9) 100%);
  border-radius: 16px;
  margin-bottom: 2rem;
  box-shadow:
    0 4px 6px -1px rgba(0, 0, 0, 0.1),
    0 2px 4px -1px rgba(0, 0, 0, 0.06);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(148, 163, 184, 0.2);
  overflow: hidden;
  position: relative;
  max-width: 950px;
  margin-left: auto;
  margin-right: auto;
}

.banner-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.5rem 2rem;
  gap: 1.5rem;
  position: relative;
}

.banner-left {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex: 1;
}

.banner-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  background: rgba(59, 130, 246, 0.1);
  border-radius: 12px;
  color: var(--color-primary);
  flex-shrink: 0;
}

.banner-text {
  color: var(--color-heading);
}

.banner-title {
  font-size: 1.25rem;
  font-weight: 700;
  margin: 0 0 0.25rem 0;
  line-height: 1.2;
}

.banner-subtitle {
  font-size: 0.9rem;
  margin: 0;
  color: var(--color-text-mute);
  line-height: 1.4;
}

.banner-actions {
  display: flex;
  gap: 0.75rem;
  flex-shrink: 0;
}

.banner-login-btn,
.banner-register-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.25rem;
  border: none;
  border-radius: 10px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  text-decoration: none;
}

.banner-login-btn {
  background: rgba(59, 130, 246, 0.1);
  color: var(--color-primary);
  border: 1px solid rgba(59, 130, 246, 0.2);
}

.banner-login-btn:hover {
  background: rgba(59, 130, 246, 0.15);
  border-color: rgba(59, 130, 246, 0.3);
  transform: translateY(-1px);
}

.banner-register-btn {
  background: var(--color-primary);
  color: white;
}

.banner-register-btn:hover {
  background: rgba(59, 130, 246, 0.9);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

.banner-remind-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.25rem;
  border: none;
  border-radius: 10px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  text-decoration: none;
  background: rgba(148, 163, 184, 0.1);
  color: var(--color-text-mute);
  border: 1px solid rgba(148, 163, 184, 0.2);
}

.banner-remind-btn:hover {
  background: rgba(148, 163, 184, 0.15);
  border-color: rgba(148, 163, 184, 0.3);
  transform: translateY(-1px);
}

.banner-close-btn {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: rgba(148, 163, 184, 0.1);
  border: none;
  border-radius: 50%;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: var(--color-text-mute);
  transition: all 0.2s ease;
  opacity: 0.7;
}

.banner-close-btn:hover {
  background: rgba(148, 163, 184, 0.2);
  opacity: 1;
  transform: scale(1.1);
}

/* 横幅动画 */
.slide-down-enter-active,
.slide-down-leave-active {
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.slide-down-enter-from {
  opacity: 0;
  transform: translateY(-20px) scale(0.95);
}

.slide-down-leave-to {
  opacity: 0;
  transform: translateY(-20px) scale(0.95);
}

/* ===================== 顶部订单时效提醒横幅 ===================== */
.timing-banner {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  padding: 0.75rem 1.25rem;
  box-sizing: border-box;
  border-bottom: 1px solid rgba(var(--color-primary-rgb,37,99,235),0.25);
  background: var(--color-background-soft); /* 设为完全不透明的主题背景 */
  box-shadow: 0 2px 4px rgba(0,0,0,0.08), 0 4px 12px rgba(0,0,0,0.06);
  color: var(--color-heading);
  animation: timing-banner-drop 0.45s ease;
  z-index: 10000;
}

@keyframes timing-banner-drop {
  0% { transform: translateY(-100%); opacity: 0; }
  100% { transform: translateY(0); opacity: 1; }
}

.timing-banner-content {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  flex: 1;
  line-height: 1.5;
}

.timing-banner-icon {
  color: var(--color-primary);
  flex-shrink: 0;
  margin-top: 2px;
}

.timing-banner-text strong {
  display: inline-block;
  margin-right: 0.25rem;
  font-weight: 600;
}
.timing-banner-text span {
  color: var(--color-text);
  font-size: 0.85rem;
}

.timing-banner-close {
  background: rgba(var(--color-primary-rgb,37,99,235),0.1);
  border: 1px solid rgba(var(--color-primary-rgb,37,99,235),0.25);
  color: var(--color-text-mute);
  width: 32px;
  height: 32px;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.timing-banner-close:hover {
  background: rgba(var(--color-primary-rgb,37,99,235),0.2);
  color: var(--color-text);
}

/* 暗色模式适配 */
html.dark .timing-banner {
  background: var(--color-background-soft); /* 暗色模式同样不透明 */
  border-bottom-color: rgba(var(--color-primary-rgb,37,99,235),0.35);
}
html.dark .timing-banner-close {
  background: rgba(var(--color-primary-rgb,37,99,235),0.15);
  border-color: rgba(var(--color-primary-rgb,37,99,235),0.35);
}
html.dark .timing-banner-close:hover {
  background: rgba(var(--color-primary-rgb,37,99,235),0.3);
}

@media (max-width: 640px) {
  .timing-banner { padding: 0.6rem 0.9rem; }
  .timing-banner-text span { font-size: 0.78rem; }
  .timing-banner-close { width: 28px; height: 28px; }
}
/* ===================== 顶部订单时效提醒横幅结束 ===================== */

/* 响应式设计 */
@media (max-width: 1024px) {
  .banner-content {
    padding: 1.25rem 1.5rem;
    gap: 1rem;
  }

  .banner-title {
    font-size: 1.125rem;
  }

  .banner-subtitle {
    font-size: 0.85rem;
  }
}

@media (max-width: 768px) {
  .banner-content {
    flex-direction: column;
    align-items: stretch;
    padding: 1.25rem 1.25rem 1rem;
    gap: 1.25rem;
  }

  .banner-left {
    justify-content: center;
    text-align: center;
  }

  .banner-actions {
    justify-content: center;
    flex-wrap: wrap;
    gap: 0.75rem;
  }

  .banner-close-btn {
    top: 0.75rem;
    right: 0.75rem;
  }

  .banner-title {
    font-size: 1.1rem;
  }

  .banner-subtitle {
    font-size: 0.8rem;
  }
}

@media (max-width: 480px) {
  .login-guide-banner {
    margin-bottom: 1.5rem;
    border-radius: 12px;
  }

  .banner-content {
    padding: 1rem 1rem 0.75rem;
  }

  .banner-actions {
    flex-direction: column;
    gap: 0.5rem;
    width: 100%;
  }

  .banner-login-btn,
  .banner-register-btn,
  .banner-remind-btn {
    width: 100%;
    justify-content: center;
    padding: 0.875rem 1rem;
  }

  .banner-left {
    gap: 0.75rem;
  }

  .banner-icon {
    width: 40px;
    height: 40px;
  }

  .banner-title {
    font-size: 1rem;
  }

  .banner-subtitle {
    font-size: 0.75rem;
  }
}

/* 暗色模式适配 */
html.dark .login-guide-banner {
  background: linear-gradient(135deg,
    rgba(30, 41, 59, 0.95) 0%,
    rgba(51, 65, 85, 0.9) 100%);
  border-color: rgba(148, 163, 184, 0.3);
}

/* ===================================================================
   登录引导横幅样式结束
   =================================================================== */

/* ---【优化方案】基于 CSS 变量的真正无缝循环动画 --- */

/* 1. 基础/暗色模式样式 */
.animated-hero-title {
  /* ▼▼▼【核心修改 ①】定义一个 CSS 变量，用于控制背景宽度 ▼▼▼ */
  --scroll-width: 400px;

  font-family: 'Inter', sans-serif;
  font-weight: 800;
  font-size: 3.2rem;
  text-align: center;
  letter-spacing: -1.5px;

  background: linear-gradient(
    100deg,
    #666666, #b2b2b2, #ffffff, #b2b2b2, #666666
  );
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;

  background-repeat: repeat-x;

  /* ▼▼▼【核心修改 ②】使用变量设定背景尺寸 ▼▼▼ */
  background-size: var(--scroll-width) 100%;

  /* 应用下方经过优化的、动态的滚动动画 */
  animation: seamless-scroll 5s linear infinite;

  text-shadow:
    0px 1px 1px rgba(255, 255, 255, 0.1),
    0 0 10px rgba(192, 219, 255, 0.2),
    0 0 30px rgba(192, 219, 255, 0.1),
    0px -1px 1px rgba(0, 0, 0, 0.4);
}

/* 2. 亮色模式专属样式 */
html:not(.dark) .animated-hero-title {
  /* ▼▼▼【核心修改 ③】仅需重写变量的值，即可改变背景尺寸 ▼▼▼ */
  --scroll-width: 300px; /* 可根据需要调整此值 */

  /* ▼▼▼【核心修改 ④】调整渐变色，使其首尾颜色相同，实现真正的无缝 ▼▼▼ */
  background: linear-gradient(
    100deg,
    #333333, #aeaeae, #232323, #aeaeae, #333333
  );
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;

  /* 其他属性会自动继承或复用，无需重复声明 */
  background-repeat: repeat-x;
  background-size: var(--scroll-width) 100%;

  text-shadow:
    0px 1px 1px rgba(255, 255, 255, 0.5),
    0px -1px 1px rgba(0, 0, 0, 0.1);
}


/* 3. 动画定义 */
@keyframes seamless-scroll {
  from {
    background-position: 0 0;
  }
  to {
    /* ▼▼▼【核心修改 ⑤】使用变量设定动画位移，确保其与背景尺寸始终一致 ▼▼▼ */
    background-position: calc(-1 * var(--scroll-width)) 0;
  }
}

/* 4. 响应式调整 (保持不变) */
@media (max-width: 767px) {
  .animated-hero-title {
    font-size: 2.6rem;
    letter-spacing: -1px;
  }
}
/* --- 优化方案结束 --- */
</style>
