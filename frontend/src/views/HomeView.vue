<template>
  <div class="home-view container">
    <Teleport to="body">
      <div v-if="isLoading" class="loading-overlay">
        <div class="spinner"></div>
        <p class="loading-text">处理中，请稍候...</p>
      </div>
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
          <div v-if="currentStep === 1">
            <h3 class="step-title">第一步：上传文档并设置规格</h3>

            <div class="billing-info-trigger" @click="showBillingModal = true">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg>
              <span>计费规则说明</span>
            </div>

            <div class="upload-notice" v-if="orderStore.groups.length === 0">
              <p><strong>上传须知</strong></p>
              <ul>
                <li><strong>格式推荐</strong>: 为确保打印效果与排版格式一致，强烈建议您上传 <strong>PDF</strong> 格式的文档。</li>
                <li><strong>文件大小</strong>: 单个文件大小建议不超过 <strong>100MB</strong>，最大支持 200MB。大文件上传时间较长，请耐心等待。</li>
                <li><strong>隐私安全</strong>: 所有文件将通过加密通道上传，并存储在专用服务器上。打印完成后，您的文件将被<strong>立即销毁</strong>，绝不外泄。</li>
                <li><strong>合规声明</strong>: 请遵守相关法律法规，<strong>严禁上传</strong>任何涉密、涉政及其他违禁内容的文件。</li>
              </ul>
            </div>

            <FileUploader
              ref="fileUploaderRef"
              @files-selected="handleFilesSelected"
              :disabled="!agreedToTerms || !agreedToPrivacy"
            />

            <transition name="fade">
              <div v-if="orderStore.groups.length > 0 && isBindingHelpVisible" class="binding-help-alert">
                <div class="help-alert-content">
                  <div class="help-alert-icon">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg>
                  </div>
                  <div class="help-alert-text">
                    <strong>装订组使用技巧：</strong>
                    <ul>
                      <li>
                        <strong>合并装订：</strong>新上传时，每个文件都是独立的"装订组"。如需将多个文件装订在一起，请按住组标题旁的 <span>⠿</span> 拖拽，并覆盖到另一组上即可合并。
                      </li>
                      <li>
                        <strong>调整顺序：</strong>当您为合并后的组选择了任意一项装订服务后，组内文件的从上到下顺序即为最终的打印和装订顺序。您可以按住单个文件左侧的 <span>⠿</span> 上下拖拽，自由调整它们的打印顺序。
                      </li>
                    </ul>
                  </div>
                </div>
                <button @click="dismissBindingHelp" class="help-alert-close-btn" title="关闭提示">
                  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
                </button>
              </div>
            </transition>
            <OrderConfiguration v-if="orderStore.groups.length > 0" />

            <div class="terms-agreement">
              <div class="terms-item">
                <input type="checkbox" id="terms" v-model="agreedToTerms" />
                <label for="terms">
                  我已阅读并同意
                  <a href="#" @click.prevent="openTermsModal" class="terms-link">
                    《服务条款》
                    <span v-if="hasLegalUpdate" class="update-dot" title="条款已于2025年10月21日更新"></span>
                  </a>
                </label>
              </div>
              <div class="terms-item">
                <input type="checkbox" id="privacy" v-model="agreedToPrivacy" />
                <label for="privacy">
                  我已阅读并同意
                  <a href="#" @click.prevent="openPrivacyModal" class="terms-link">
                    《隐私协议》
                    <span v-if="hasLegalUpdate" class="update-dot" title="协议已于2025年10月21日更新"></span>
                  </a>
                </label>
              </div>
            </div>

            <BaseButton
              v-if="orderStore.groups.length > 0"
              @click="goToPaymentStep"
              :disabled="!isReadyToGoNext"
              :loading="!orderStore.isReadyToSubmit"
              class="full-width-btn"
              style="margin-top: 2rem;"
            >
              <span>{{ nextStepButtonText }}</span>
            </BaseButton>
          </div>

          <div v-if="currentStep === 2">
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
            <BaseButton @click="handleCreateOrder" :loading="isLoading" class="full-width-btn">
              我已支付，确认下单
            </BaseButton>
          </div>

          <div v-if="currentStep === 3 && finalOrder" class="completion-view">
            <!-- 【修改】这里的 SVG stroke 颜色使用了 CSS 变量 -->
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
            <BaseButton @click="resetForNewOrder" class="full-width-btn">再来一单</BaseButton>
          </div>
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
        <div class="billing-rules-content">
          <li>
            <strong>计价公式</strong>
          <p><span class="formula-highlight">总费用 = 基础服务费 + 打印费用 + 装订费用（可选）</span></p>
          </li>
          <ul>
            <li>
              <strong>基础服务费</strong>
              <p>每笔订单将统一收取 0.50元 的基础服务费，用于覆盖设备维护和系统运营成本。</p>
            </li>
            <li>
              <strong>打印费用</strong>
              <p>单面双面相同价格。</p>
              <p>根据您选择的规格（纸张规格、色彩、单双面）按页计费，具体单价以页面实时显示为准。</p>
              <table class="price-table">
                <thead>
                  <tr>
                    <th>规格</th>
                    <th>克重</th>
                    <th>色彩</th>
                    <th>单价（每面）</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td>A4</td>
                    <td>70g</td>
                    <td>黑白</td>
                    <td>0.15元</td>
                  </tr>
                  <tr>
                    <td>A4</td>
                    <td>80g</td>
                    <td>黑白</td>
                    <td>0.15元</td>
                  </tr>
                  <tr>
                    <td>B5</td>
                    <td>70g</td>
                    <td>黑白</td>
                    <td>0.12元</td>
                  </tr>
                </tbody>
              </table>
              </li>

            <li>
              <strong>装订费用</strong>
              <p>若您选择装订服务，将根据不同的装订方式额外收取固定费用。</p>
            </li>
          </ul>
        </div>
      </template>
    </Modal>
  </Teleport>
</template>

<script setup>
import { ref, computed, watch, onUnmounted, onMounted } from 'vue'; //【修改】引入computed, watch, onUnmounted
import { useRouter } from 'vue-router'; // 导入路由
import { useOrderStore } from '@/stores/order';
import apiService from '@/services/apiService'; //【修改】使用apiService而不是直接使用axios
import { useUserStore } from '@/stores/user'; // 导入用户状态管理

// 导入组件
import Stepper from '@/components/Stepper.vue';
import FileUploader from '@/components/FileUploader.vue';
import PaymentUploader from '@/components/PaymentUploader.vue';
import BaseButton from '@/components/BaseButton.vue';
import Modal from '@/components/Modal.vue';
import OrderConfiguration from '@/components/OrderConfiguration.vue';
import LegalDocument from '@/components/legal/LegalDocument.vue';

// --- 使用 Pinia Store 和 Router ---
const orderStore = useOrderStore();
const userStore = useUserStore(); // 使用用户状态管理
const router = useRouter(); // 使用路由
const screenshotId = ref(null); // <-- 【新增】用于存储凭证ID的状态

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
const hasLegalUpdate = computed(() => {
  const lastViewedDate = localStorage.getItem('legalDocsLastViewed');
  return !lastViewedDate || lastViewedDate < LEGAL_UPDATE_DATE;
});

// ▼▼▼ 在这里新增控制逻辑 ▼▼▼
const isBindingHelpVisible = ref(true); // 默认显示

function dismissBindingHelp() {
  isBindingHelpVisible.value = false;
}

// 登录引导横幅相关状态
const showLoginGuideBanner = ref(true); // 默认显示

// 页面初始化时检查用户是否之前关闭过横幅
onMounted(() => {
  // 移除本地存储检查，让横幅每次都能显示
  // const hideBanner = localStorage.getItem('hideLoginGuideBanner');
  // if (hideBanner === 'true') {
  //   showLoginGuideBanner.value = false;
  // }
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

// 组件卸载时清理监听器
onUnmounted(() => {
  unwatchAuth();
});

function dismissBanner() {
  showLoginGuideBanner.value = false;
  // 不再保存到本地存储，让横幅在下次访问时重新显示
  // localStorage.setItem('hideLoginGuideBanner', 'true');
}

function goToLogin() {
  // 跳转到登录页面
  router.push('/auth/login');
  dismissBanner();
}

function goToRegister() {
  // 跳转到注册页面
  router.push('/auth/register');
  dismissBanner();
}

function remindLater() {
  // 稍后提醒逻辑，隐藏横幅一段时间后重新显示
  showLoginGuideBanner.value = false;
  // 设置一个较短的延迟时间，比如5分钟后重新显示
  setTimeout(() => {
    if (!userStore.isAuthenticated) {
      showLoginGuideBanner.value = true;
    }
  }, 5 * 60 * 1000); // 5分钟
}
// ▲▲▲ 新增代码结束 ▲▲▲

// 法律文档模态框打开函数（打开时标记为已查看）
function openTermsModal() {
  showTermsModal.value = true;
  // 用户打开查看后，标记已查看最新版本
  localStorage.setItem('legalDocsLastViewed', LEGAL_UPDATE_DATE);
}

function openPrivacyModal() {
  showPrivacyModal.value = true;
  // 用户打开查看后，标记已查看最新版本
  localStorage.setItem('legalDocsLastViewed', LEGAL_UPDATE_DATE);
}

const isReadyToGoNext = computed(() => {
  return orderStore.isReadyToSubmit && agreedToTerms.value && agreedToPrivacy.value;
});

// 【新增】这个计算属性根据不同状态显示不同的按钮文本
const nextStepButtonText = computed(() => {
  if (!agreedToTerms.value || !agreedToPrivacy.value) {
    return '请先同意服务条款和隐私协议';
  }
  if (!orderStore.isReadyToSubmit) {
    return '处理文件中...';
  }
  return `下一步，确认订单 (总计 ¥${totalCost.value})`;
});

const totalCost = computed(() => orderStore.totalCost);

// --- 方法 ---
function handleFilesSelected(files) {
  orderStore.addFiles(files);
}

// 【新增】处理截图上传成功的事件函数
function onScreenshotUploaded(uploadedId) {
  screenshotId.value = uploadedId;
}

function goToPaymentStep() {
  if (isReadyToGoNext.value) { // <--- 将 isReadyToSubmit 修改为 isReadyToGoNext
    currentStep.value = 2;
  }
}

// 【关键】最终的订单创建函数
async function handleCreateOrder() {
  // 基础校验
  if (!screenshotId.value) { // <-- 【修改】校验逻辑
    errorMessage.value = '请先上传付款截图！';
    return;
  }
  if (!orderStore.phoneNumber) {
    errorMessage.value = '请输入您的手机号码！';
    return;
  }

  isLoading.value = true;
  errorMessage.value = '';

  // 1. 从 Store 中构建后端需要的JSON数据结构
  const payload = {
    // 【修改】将 screenshotId 添加到 payload 中
    payment_screenshot_id: screenshotId.value,
    payment_method: orderStore.paymentMethod, // <-- 【新增】确保这一行存在
    phone_number: orderStore.phoneNumber,
    groups: orderStore.groups.map((group, groupIndex) => ({
      binding_type: group.bindingType,
      sequence_in_order: groupIndex + 1,
      documents: group.documents.map((doc, docIndex) => ({
        file_id: doc.serverId, // 使用预上传后服务器返回的ID
        original_filename: doc.fileName,
        paper_size: doc.settings.paperSize, // <--- 【核心修正】在这里补上 paper_size 字段
        color_mode: doc.settings.colorMode,
        print_sided: doc.settings.printSided,
        copies: doc.settings.copies,
        sequence_in_group: docIndex + 1,
      })),
    })),
    // payment_method: orderStore.paymentMethod,
    // 【待办】支付凭证也需要预上传并获取ID
  };

  try {
    // 2. 发送创建订单的POST请求
    const response = await apiService.createOrder(payload);

    // 3. 处理成功响应
    finalOrder.value = response.data; // 保存成功返回的订单数据
    currentStep.value = 3; // 跳转到成功页面

  } catch (error) {
    console.error('Order creation failed:', error.response?.data || error.message);
    errorMessage.value = '订单创建失败，请稍后重试或联系客服。';
  } finally {
    isLoading.value = false;
  }
}

function resetForNewOrder() { // <--- 1. 将函数名从 reset 修改为 resetForNewOrder
  orderStore.resetStore();
  currentStep.value = 1;
  finalOrder.value = null; // <--- 2. 增加这一行，清空上一单的结果
  agreedToTerms.value = false;
  agreedToPrivacy.value = false;
  errorMessage.value = '';
  screenshotId.value = null; // <--- 3. 增加这一行，重置截图ID
  if (fileUploaderRef.value) {
    fileUploaderRef.value.reset();
  }
}

// 订单层面的“是否预估”判断（任一文档为预估即为预估）
const anyEstimated = computed(() => orderStore.groups.some(g => g.documents.some(d => d.isEstimated)));

</script>

<style scoped>

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

.step-title {
  font-size: 1.5rem;
  font-weight: 600;
  text-align: center;
  margin-bottom: 2rem;
  color: var(--color-heading); /* 已修改 */
}

.options-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.options-grid div {
  display: flex;
  flex-direction: column;
}

.options-grid label {
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: var(--color-heading); /* 已修改 */
}

.price-result {
  background-color: var(--color-background-mute); /* 已修改 */
  border: 1px solid var(--color-primary); /* 已修改 */
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
  color: var(--color-primary); /* 已修改 */
  font-weight: 700;
}

.payment-section {
  border-top: 1px solid var(--color-border); /* 已修改 */
  padding: 1.5rem 0;
  margin-top: 1.5rem;
  text-align: center;
}

.payment-instruction {
  margin-top: 0;
  color: var(--color-text); /* 已修改 */
}

.qr-code {
  max-width: 180px;
  margin: 1rem auto;
  display: block;
  border-radius: 8px;
  background-color: white; /* 为确保二维码可扫，背景强制为白色 */
  padding: 5px; /* 增加内边距，确保扫描效果 */
}

.form-group {
  margin-top: 1.5rem;
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block; /* 【修复】让标签独占一行，从而与输入框产生间距 */
  margin-bottom: 0.75rem; /* 【修复】增加明确的下边距 */
  font-weight: 500;
  color: var(--color-heading);
}

.full-width-btn {
  width: 100%;
  padding: 0.875rem;
  font-size: 1.1rem;
}

.completion-view {
  text-align: center;
  padding: 2rem 0;
}

.completion-view > p {
  color: var(--color-text-mute); /* 已修改 */
  margin-bottom: 1rem;
}

.pickup-code-wrapper {
  background-color: var(--color-background-mute); /* 已修改 */
  border: 1px dashed var(--color-primary); /* 已修改 */
  padding: 1rem;
  border-radius: 8px;
  margin: 1.5rem auto;
  max-width: 300px;
}

.pickup-code-label {
  font-size: 1rem;
  color: var(--color-text); /* 已修改 */
}

.pickup-code {
  display: block;
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--color-primary); /* 已修改 */
  letter-spacing: 4px;
  margin-top: 0.5rem;
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

.order-number-info {
  color: var(--color-text-mute); /* 已修改 */
  font-size: 0.875rem;
  margin-top: -0.5rem;
  margin-bottom: 2rem;
}

.upload-notice {
  background-color: var(--color-background-mute);
  border: 1px solid var(--color-border);
  border-radius: 8px;
  padding: 1rem 1.5rem;
  margin-bottom: 2rem;
  font-size: 0.9rem;
  color: var(--color-text);
}

.upload-notice p {
  margin: 0 0 0.75rem 0;
  font-weight: 500;
  color: var(--color-heading);
}
/* --- 【新增】请在这里添加以下新规则 --- */
.upload-notice p strong {
  font-weight: 700; /* 或者 bold, 800, 900，具体取决于字体支持 */
}

.upload-notice ul {
  list-style-type: none;
  padding-left: 0;
}

.upload-notice li {
  margin-bottom: 0.75rem; /* 稍微增加行间距 */
  position: relative;
  padding-left: 1.25rem;
  font-weight: 500; /* 【修复】恢复字体粗细 */
  line-height: 1.6; /* 增加行高，提升可读性 */
}

.upload-notice li::before {
  content: '•';
  color: var(--color-primary);
  font-weight: bold;
  display: inline-block;
  position: absolute;
  left: 0;
  top: 0;
}

.upload-notice li:last-child {
  margin-bottom: 0;
}

.upload-notice li strong {
  color: var(--color-primary); /* 【修复】将关键词颜色修正为主题蓝 */
  font-weight: 600; /* 【修复】恢复关键词粗细 */
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
  transition: filter 0.3s; /* 【新增】为滤镜添加平滑过渡 */
}

/* --- 【核心修改】暗色模式下，为图片应用滤镜 --- */
html.dark .payment-button-image {
  filter: invert(1) grayscale(1) brightness(1.5);
}

.payment-link {
  display: inline-block;
  margin-top: 1rem;
  padding: 0.6rem 1.2rem;
  background-color: #1677ff; /* 支付宝品牌色，保持不变 */
  color: white;
  text-decoration: none;
  border-radius: 5px;
  font-weight: 500;
  transition: background-color 0.2s;
}

.payment-link:hover {
  background-color: #4096ff;
}

.terms-agreement {
  font-size: 0.9rem;
  color: var(--color-text-mute); /* 已修改 */
  margin-top: 2rem;
  margin-bottom: 0;
  padding: 1rem;
  background-color: var(--color-background-mute); /* 已修改 */
  border: 1px solid var(--color-border); /* 已修改 */
  border-radius: 8px;
}

.terms-agreement .terms-item {
  margin-bottom: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.terms-agreement .terms-item:last-child {
  margin-bottom: 0;
}

.terms-agreement input[type="checkbox"] {
  margin-right: 0.5rem;
  width: auto;
  flex-shrink: 0;
}

.terms-agreement label {
  margin-bottom: 0;
  font-weight: normal;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.terms-agreement .terms-link {
  position: relative;
  display: inline-block;
  color: var(--color-primary);
  text-decoration: underline;
  cursor: pointer;
}

/* 小红点更新标识 */
.update-dot {
  position: absolute;
  top: 1px;
  right: 2px;
  width: 8px;
  height: 8px;
  background: rgb(239, 68, 68);
  border-radius: 50%;
  border: 1.5px solid var(--color-background-mute);

  /* 动画选择 - 取消注释你喜欢的一个 */

  /* 选项1: 脉动+扩散波（当前使用，微信/QQ风格） */
  /* animation: pulse-ripple 2s ease-in-out infinite; */

  /* 选项2: 简单闪烁 */
  animation: blink 1.5s ease-in-out infinite;

  /* 选项3: 轻微跳动 */
  /* animation: bounce 1s ease-in-out infinite; */

  /* 选项4: 呼吸灯效果 */
  /* animation: breathe 2s ease-in-out infinite; */

  /* 选项5: 旋转闪烁 */
  /* animation: spin-fade 2s linear infinite; */

  /* 选项6: 无动画（静态红点） */
  /* animation: none; */
}

html.dark .update-dot {
  background: rgb(248, 113, 113);
  border-color: var(--color-background-mute);
}

/* 动画1: 脉动+扩散波 - 微信/QQ消息提示风格 */
@keyframes pulse-ripple {
  0%, 100% {
    transform: scale(1);
    box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7);
  }
  50% {
    transform: scale(1.1);
    box-shadow: 0 0 0 4px rgba(239, 68, 68, 0);
  }
}

/* 动画2: 简单闪烁 */
@keyframes blink {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.3;
  }
}

/* 动画3: 轻微跳动 */
@keyframes bounce {
  0%, 100% {
    transform: translateY(0) scale(1);
  }
  25% {
    transform: translateY(-2px) scale(1.05);
  }
  75% {
    transform: translateY(1px) scale(0.98);
  }
}

/* 动画4: 呼吸灯效果 */
@keyframes breathe {
  0%, 100% {
    opacity: 1;
    transform: scale(1);
  }
  50% {
    opacity: 0.5;
    transform: scale(0.9);
  }
}

/* 动画5: 旋转闪烁 */
@keyframes spin-fade {
  0%, 100% {
    opacity: 1;
    transform: rotate(0deg) scale(1);
  }
  50% {
    opacity: 0.6;
    transform: rotate(180deg) scale(1.1);
  }
}

.terms-text {
  font-family: inherit;
  font-size: 0.9rem;
  line-height: 1.7;
  text-align: left;
  color: var(--color-text); /* 已修改 */
}

.terms-text h4 {
  font-size: 1.1rem;
  font-weight: 600;
  margin-top: 1.5em;
  margin-bottom: 0.5em;
  color: var(--color-heading); /* 已修改 */
}

.terms-text p {
  margin-bottom: 1em;
}

.terms-text p:first-child {
    margin-top: 0;
}

.billing-info-trigger {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  color: var(--color-text-mute); /* 已修改 */
  font-size: 0.9rem;
  margin-bottom: 2rem;
  cursor: pointer;
  transition: color 0.2s;
}

.billing-info-trigger:hover {
  color: var(--color-primary); /* 已修改 */
}

.billing-info-trigger svg {
  margin-top: -2px;
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
  .step-title { font-size: 1.25rem; }
  .process-card { padding: 1.5rem 1rem; }
  .pickup-code { font-size: 2rem; }
  .payment-method-selector { gap: 1rem; }
  .payment-method-selector label { width: 140px; height: 48px; }
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
/* --- 【修复】为手机号输入框添加样式 --- */
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
/* ▼▼▼ 在这里新增全局帮助信息框的样式 ▼▼▼ */
.binding-help-alert {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  /* 定义一个更柔和的信息提示背景色 */
  background-color: rgba(var(--color-primary-rgb, 37, 99, 235), 0.08);
  border: 1px solid rgba(var(--color-primary-rgb, 37, 99, 235), 0.2);
  border-radius: 12px;
  padding: 1rem;
  margin-top: 2rem; /* 与上方的 FileUploader 保持间距 */
  margin-bottom: 1.5rem; /* 与下方的 OrderConfiguration 保持间距 */
}

.help-alert-content {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
}

.help-alert-icon {
  color: var(--color-primary);
  flex-shrink: 0;
  margin-top: 2px;
}


.help-alert-close-btn {
  background: none;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  padding: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-text-mute);
  transition: background-color 0.2s, color 0.2s;
  flex-shrink: 0;
}

.help-alert-close-btn:hover {
  background-color: var(--color-background-mute);
  color: var(--color-text);
}
/* 更新帮助文本的样式 */
.help-alert-text strong {
  font-weight: 600;
  color: var(--color-heading);
  display: block; /* 让标题独占一行 */
  margin-bottom: 0.5rem;
}

.help-alert-text p,
.help-alert-text ul { /* 同时为 p 和 ul 设置样式 */
  font-size: 0.9rem;
  color: var(--color-text);
  margin: 0;
  line-height: 1.6;
  padding-left: 0.1em; /* 为 ul 添加左边距 */
}

.help-alert-text li {
  margin-bottom: 0.5rem;
}
.help-alert-text li:last-child {
  margin-bottom: 0;
  padding-left: 0; /* 最后一项不需要左边距 */
}

.help-alert-text li::marker {
  color: var(--color-primary); /* 美化列表的项目符号 */
}

.help-alert-text li strong {
  display: inline; /* 修正 li 内 strong 的显示方式 */
  margin-bottom: 0;
}

/* 这个是新增的，用于高亮显示拖拽图标 */
.help-alert-text span {
  font-family: monospace;
  background-color: var(--color-border);
  padding: 0 4px;
  border-radius: 3px;
  font-weight: 600;
  display: inline-block;
  line-height: 1;
}
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.4s ease, transform 0.4s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
/* ▲▲▲ 新增样式结束 ▲▲▲ */

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
