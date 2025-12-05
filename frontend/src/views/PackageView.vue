<template>
  <div class="package-view">
    <div class="package-container">
      <!-- 页面标题 -->
      <div class="page-header">
        <h1 class="page-title">打印套餐</h1>
        <p class="page-subtitle">预充值享折扣，套餐永久有效，让打印更省心</p>
      </div>

      <!-- 加载状态 -->
      <div v-if="loading" class="loading-state">
        <div class="spinner"></div>
        <span>加载套餐中...</span>
      </div>

      <!-- 套餐列表 -->
      <div v-else class="packages-grid">
        <div
          v-for="pkg in packages"
          :key="pkg.id"
          class="package-card"
          :class="{ 'featured': pkg.is_featured }"
        >
          <!-- 推荐标签 -->
          <div v-if="pkg.is_featured" class="featured-badge">
            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="currentColor">
              <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>
            </svg>
            推荐
          </div>

          <div class="package-content">
            <!-- 套餐名称 -->
            <h3 class="package-name">{{ pkg.name }}</h3>

            <!-- 套餐描述 -->
            <p v-if="pkg.description" class="package-desc">{{ pkg.description }}</p>

            <!-- 页数展示 -->
            <div class="package-pages">
              <span class="pages-value">{{ pkg.pages }}</span>
              <span class="pages-unit">页</span>
            </div>

            <!-- 价格区域 -->
            <div class="package-price">
              <div class="price-row">
                <span class="price-current">¥{{ pkg.price }}</span>
                <span v-if="pkg.original_price && pkg.original_price > pkg.price" class="price-original">
                  ¥{{ pkg.original_price }}
                </span>
              </div>
              <div class="price-per-page">
                约 ¥{{ pkg.price_per_page.toFixed(3) }}/页
              </div>
            </div>

            <!-- 折扣和节省 -->
            <div v-if="pkg.discount_rate < 100" class="package-discount">
              <span class="discount-badge">{{ pkg.discount_rate / 10 }}折</span>
              <span v-if="pkg.savings > 0" class="savings-text">省 ¥{{ pkg.savings.toFixed(2) }}</span>
            </div>

            <!-- 有效期 -->
            <div class="package-validity">
              <svg v-if="!pkg.validity_days" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
                <polyline points="22 4 12 14.01 9 11.01"/>
              </svg>
              <svg v-else xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"/>
                <polyline points="12 6 12 12 16 14"/>
              </svg>
              <span v-if="pkg.validity_days">有效期 {{ pkg.validity_days }} 天</span>
              <span v-else class="validity-forever">永久有效</span>
            </div>

            <!-- 购买按钮 -->
            <button @click="selectPackage(pkg)" class="purchase-btn" :class="{ 'featured-btn': pkg.is_featured }">
              立即购买
            </button>
          </div>
        </div>
      </div>

      <!-- 套餐说明 -->
      <div class="info-card">
        <h2 class="info-title">套餐说明</h2>
        <div class="info-grid">
          <div class="info-item">
            <div class="info-icon highlight">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>
              </svg>
            </div>
            <div class="info-text">
              <h3>极速下单</h3>
              <p>使用余额支付无需上传凭证，一键完成下单</p>
            </div>
          </div>
          <div class="info-item">
            <div class="info-icon">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
              </svg>
            </div>
            <div class="info-text">
              <h3>一次购买，长期使用</h3>
              <p>套餐余额永久有效，无需担心过期浪费</p>
            </div>
          </div>
          <div class="info-item">
            <div class="info-icon">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="12" y1="1" x2="12" y2="23"/>
                <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>
              </svg>
            </div>
            <div class="info-text">
              <h3>按实际页数扣费</h3>
              <p>打印多少页扣除多少页，计费透明</p>
            </div>
          </div>
          <div class="info-item">
            <div class="info-icon">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/>
                <polyline points="17 6 23 6 23 12"/>
              </svg>
            </div>
            <div class="info-text">
              <h3>折扣享不停</h3>
              <p>套餐页数越多，折扣越大，最高享8折优惠</p>
            </div>
          </div>
          <div class="info-item">
            <div class="info-icon">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
                <line x1="12" y1="8" x2="12" y2="16"/>
                <line x1="8" y1="12" x2="16" y2="12"/>
              </svg>
            </div>
            <div class="info-text">
              <h3>余额可累加</h3>
              <p>多次购买余额累计，不限使用次数</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 购买抽屉 -->
    <Teleport to="body">
      <Transition name="drawer-overlay">
        <div v-if="showPurchaseModal" class="drawer-overlay" @click.self="closePurchaseModal"></div>
      </Transition>
      <Transition name="drawer-slide">
        <div v-if="showPurchaseModal" class="drawer-container">
          <!-- 抽屉头部 -->
          <div class="drawer-header">
            <h2 class="drawer-title">购买套餐</h2>
            <button class="drawer-close" @click="closePurchaseModal">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="18" y1="6" x2="6" y2="18"/>
                <line x1="6" y1="6" x2="18" y2="18"/>
              </svg>
            </button>
          </div>

          <!-- 抽屉内容 -->
          <div class="drawer-body">
            <!-- 套餐摘要 -->
            <div class="selected-package-summary">
              <div class="summary-main">
                <span class="summary-name">{{ selectedPackage?.name }}</span>
                <span class="summary-pages">{{ selectedPackage?.pages }} 页</span>
              </div>
              <div class="summary-price">
                <span class="summary-label">支付金额</span>
                <span class="summary-value">¥{{ selectedPackage?.price }}</span>
              </div>
            </div>

            <!-- 支付方式 -->
            <div class="payment-section">
              <label class="section-label">选择支付方式</label>
              <div class="payment-method-selector">
                <label :class="{ 'active': purchaseForm.payment_method === 'WECHAT' }">
                  <input type="radio" v-model="purchaseForm.payment_method" value="WECHAT" name="package-payment-method"/>
                  <img src="/wechat-logo.png" alt="微信支付" class="payment-button-image" />
                </label>
                <label :class="{ 'active': purchaseForm.payment_method === 'ALIPAY' }">
                  <input type="radio" v-model="purchaseForm.payment_method" value="ALIPAY" name="package-payment-method"/>
                  <img src="/alipay-logo.png" alt="支付宝" class="payment-button-image" />
                </label>
              </div>
            </div>

            <!-- 二维码区域 -->
            <div class="qr-section">
              <div v-if="purchaseForm.payment_method === 'WECHAT'" class="qr-content">
                <p class="qr-instruction">请使用微信扫描下方二维码完成支付</p>
                <div class="qr-wrapper">
                  <img src="/wechat_qr.jpg" alt="微信收款二维码" class="qr-image">
                </div>
              </div>
              <div v-else-if="purchaseForm.payment_method === 'ALIPAY'" class="qr-content">
                <p class="qr-instruction">请使用支付宝扫描二维码，或点击下方链接</p>
                <div class="qr-wrapper">
                  <img src="/alipay_qr.jpg" alt="支付宝收款二维码" class="qr-image">
                </div>
                <a href="https://qr.alipay.com/2m611064ovvydd9jbdrnv22" target="_blank" class="alipay-link">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>
                    <polyline points="15 3 21 3 21 9"/>
                    <line x1="10" y1="14" x2="21" y2="3"/>
                  </svg>
                  点此跳转支付宝APP付款
                </a>
              </div>
            </div>

            <!-- 凭证上传 -->
            <div class="upload-section">
              <label class="section-label">上传支付凭证</label>
              <PaymentUploader @upload-success="handleScreenshotUploaded" />
            </div>

            <!-- 备注 -->
            <div class="remark-section">
              <label class="section-label">备注（选填）</label>
              <textarea
                v-model="purchaseForm.remark"
                rows="2"
                class="remark-input"
                placeholder="如有特殊说明，请在此填写..."
              ></textarea>
            </div>
          </div>

          <!-- 操作按钮 -->
          <div class="drawer-actions">
            <button class="action-btn cancel-btn" @click="closePurchaseModal">
              取消
            </button>
            <button
              class="action-btn confirm-btn"
              @click="submitPurchase"
              :disabled="purchasing || !purchaseForm.payment_screenshot_id"
            >
              <span v-if="purchasing" class="btn-loading">
                <span class="spinner-small"></span>
                提交中...
              </span>
              <span v-else>确认购买</span>
            </button>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import apiService from '@/services/apiService'
import PaymentUploader from '@/components/PaymentUploader.vue'

const router = useRouter()

const packages = ref([])
const loading = ref(true)
const showPurchaseModal = ref(false)
const selectedPackage = ref(null)
const purchasing = ref(false)

const purchaseForm = ref({
  package: null,
  payment_method: 'WECHAT',
  payment_screenshot_id: '',
  remark: ''
})

// 加载套餐列表
const loadPackages = async () => {
  try {
    loading.value = true
    const response = await apiService.getPackages()
    packages.value = response.data
  } catch (error) {
    console.error('加载套餐失败:', error)
    alert('加载套餐失败，请刷新重试')
  } finally {
    loading.value = false
  }
}

// 选择套餐
const selectPackage = (pkg) => {
  selectedPackage.value = pkg
  purchaseForm.value.package = pkg.id
  showPurchaseModal.value = true
}

// 关闭购买弹窗
const closePurchaseModal = () => {
  showPurchaseModal.value = false
  selectedPackage.value = null
  purchaseForm.value = {
    package: null,
    payment_method: 'WECHAT',
    payment_screenshot_id: '',
    remark: ''
  }
}

// 处理支付凭证上传成功
const handleScreenshotUploaded = (fileId) => {
  purchaseForm.value.payment_screenshot_id = fileId
}

// 提交购买
const submitPurchase = async () => {
  if (!purchaseForm.value.payment_screenshot_id) {
    alert('请先上传支付凭证')
    return
  }

  try {
    purchasing.value = true
    await apiService.purchasePackage(purchaseForm.value)

    alert('套餐购买成功！等待管理员审核后将自动充值到您的账户')
    closePurchaseModal()
    router.push('/profile')
  } catch (error) {
    console.error('购买套餐失败:', error)
    const errorMsg = error.response?.data?.error || error.response?.data?.detail || '购买失败，请重试'
    alert(errorMsg)
  } finally {
    purchasing.value = false
  }
}

onMounted(() => {
  loadPackages()
})
</script>

<style scoped>
/* ===== 页面布局 ===== */
.package-view {
  background-color: var(--color-background-soft);
  min-height: 100vh;
  padding: 2rem;
}

.package-container {
  max-width: 1200px;
  margin: 0 auto;
}

/* ===== 页面标题 ===== */
.page-header {
  text-align: center;
  margin-bottom: 3rem;
}

.page-title {
  font-size: 2.5rem;
  font-weight: 800;
  color: var(--color-heading);
  margin: 0 0 0.75rem;
}

.page-subtitle {
  font-size: 1.1rem;
  color: var(--color-text-mute);
  margin: 0;
}

/* ===== 加载状态 ===== */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 5rem 2rem;
  gap: 1rem;
  color: var(--color-text-mute);
}

.spinner {
  width: 48px;
  height: 48px;
  border: 4px solid var(--color-border);
  border-top-color: var(--color-primary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* ===== 套餐网格 ===== */
.packages-grid {
  display: grid;
  grid-template-columns: repeat(1, 1fr);
  gap: 1.5rem;
  margin-bottom: 3rem;
}

@media (min-width: 640px) {
  .packages-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1024px) {
  .packages-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}

/* ===== 套餐卡片 ===== */
.package-card {
  position: relative;
  background-color: var(--color-background);
  border: 1px solid var(--color-border);
  border-radius: 16px;
  overflow: hidden;
  transition: all 0.3s ease;
  box-shadow: var(--shadow-card);
}

.package-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.1);
  border-color: var(--color-primary);
}

.package-card.featured {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 2px rgba(var(--color-primary-rgb), 0.2);
}

.featured-badge {
  position: absolute;
  top: 12px;
  right: 12px;
  background-color: var(--color-primary);
  color: white;
  padding: 0.35rem 0.75rem;
  border-radius: 6px;
  font-size: 0.75rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.3rem;
  letter-spacing: 0.02em;
}

.package-content {
  padding: 1.5rem;
}

.package-name {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--color-heading);
  margin: 0 0 0.5rem;
}

.package-desc {
  font-size: 0.875rem;
  color: var(--color-text-mute);
  margin: 0 0 1rem;
  line-height: 1.5;
}

.package-pages {
  margin-bottom: 1rem;
}

.pages-value {
  font-size: 3rem;
  font-weight: 800;
  color: var(--color-heading);
  letter-spacing: -0.02em;
}

.pages-unit {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--color-text-mute);
  margin-left: 0.25rem;
}

.package-price {
  margin-bottom: 1rem;
}

.price-row {
  display: flex;
  align-items: baseline;
  gap: 0.5rem;
}

.price-current {
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--color-heading);
}

.price-original {
  font-size: 1rem;
  color: var(--color-text-mute);
  text-decoration: line-through;
}

.price-per-page {
  font-size: 0.8rem;
  color: var(--color-text-mute);
  margin-top: 0.25rem;
}

.package-discount {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.discount-badge {
  display: inline-block;
  background-color: #fef2f2;
  color: #dc2626;
  padding: 0.25rem 0.6rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 500;
  font-weight: 600;
}

.savings-text {
  font-size: 0.875rem;
  color: #10b981;
  font-weight: 600;
}

.package-validity {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: var(--color-text-mute);
  margin-bottom: 1.5rem;
}

.validity-forever {
  color: #10b981;
  font-weight: 600;
}

.purchase-btn {
  width: 100%;
  padding: 0.875rem;
  border: none;
  border-radius: 10px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  background-color: var(--color-background-mute);
  color: var(--color-heading);
  border: 1px solid var(--color-border);
}

.purchase-btn:hover {
  background-color: var(--color-primary);
  color: white;
  border-color: var(--color-primary);
}

.purchase-btn.featured-btn {
  background-color: var(--color-primary);
  color: white;
  border: none;
}

.purchase-btn.featured-btn:hover {
  background-color: var(--color-primary-hover);
}

/* ===== 说明卡片 ===== */
.info-card {
  background-color: var(--color-background);
  border: 1px solid var(--color-border);
  border-radius: 16px;
  padding: 2rem;
  box-shadow: var(--shadow-card);
}

.info-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--color-heading);
  margin: 0 0 1.5rem;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(1, 1fr);
  gap: 1.5rem;
}

@media (min-width: 768px) {
  .info-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

.info-item {
  display: flex;
  gap: 1rem;
  align-items: flex-start;
}

.info-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background-color: var(--color-background-mute);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-text-mute);
  flex-shrink: 0;
}

.info-icon.highlight {
  background-color: var(--color-primary);
  color: white;
}

.info-text h3 {
  font-size: 1rem;
  font-weight: 600;
  color: var(--color-heading);
  margin: 0 0 0.35rem;
}

.info-text p {
  font-size: 0.875rem;
  color: var(--color-text-mute);
  margin: 0;
  line-height: 1.5;
}

/* ===== 抽屉组件 ===== */
.drawer-overlay {
  position: fixed;
  inset: 0;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 1000;
  backdrop-filter: blur(2px);
}

.drawer-container {
  position: fixed;
  background-color: var(--color-background);
  z-index: 1001;
  overflow-y: auto;
  box-shadow: -4px 0 24px rgba(0, 0, 0, 0.15);
  display: flex;
  flex-direction: column;

  /* 桌面端: 右侧抽屉 */
  top: 0;
  right: 0;
  bottom: 0;
  width: 460px;
  max-width: 100%;
}

.drawer-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid var(--color-border);
  flex-shrink: 0;
  background-color: var(--color-background);
}

.drawer-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--color-heading);
  margin: 0;
}

.drawer-close {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  border: none;
  background-color: var(--color-background-mute);
  color: var(--color-text-mute);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.drawer-close:hover {
  background-color: var(--color-danger);
  color: white;
}

.drawer-body {
  flex: 1;
  overflow-y: auto;
  padding-bottom: 1rem;
}

/* ===== 套餐摘要 ===== */
.selected-package-summary {
  margin: 1.5rem;
  padding: 1.25rem;
  background-color: var(--color-background-soft);
  border: 1px solid var(--color-border);
  border-radius: 12px;
}

.summary-main {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.summary-name {
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--color-heading);
}

.summary-pages {
  font-size: 1rem;
  font-weight: 600;
  color: var(--color-primary);
}

.summary-price {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 0.75rem;
  border-top: 1px solid rgba(var(--color-primary-rgb), 0.15);
}

.summary-label {
  font-size: 0.875rem;
  color: var(--color-text-mute);
}

.summary-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--color-primary);
}

/* ===== 支付方式 ===== */
.payment-section,
.upload-section,
.remark-section {
  padding: 0 1.5rem;
  margin-bottom: 1.25rem;
}

.section-label {
  display: block;
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--color-heading);
  margin-bottom: 0.75rem;
}

.payment-method-selector {
  display: flex;
  justify-content: center;
  gap: 1.5rem;
}

.payment-method-selector label {
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  border: 2px solid var(--color-border);
  border-radius: 12px;
  padding: 1rem;
  transition: all 0.2s ease-in-out;
  min-width: 100px;
  background-color: var(--color-background);
}

.payment-method-selector label:hover {
  border-color: var(--color-border-hover);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.payment-method-selector label.active {
  border-color: var(--color-primary);
  background-color: rgba(var(--color-primary-rgb), 0.05);
}

.payment-method-selector input[type="radio"] {
  display: none;
}

.payment-button-image {
  display: block;
  height: 40px;
  width: auto;
  object-fit: contain;
}

html.dark .payment-button-image {
  filter: invert(1) grayscale(1) brightness(1.5);
}

/* ===== 二维码区域 ===== */
.qr-section {
  padding: 0 1.5rem;
  margin-bottom: 1.25rem;
}

.qr-content {
  background-color: var(--color-background-soft);
  border-radius: 12px;
  padding: 1.25rem;
  text-align: center;
}

.qr-instruction {
  font-size: 0.875rem;
  color: var(--color-text-mute);
  margin: 0 0 1rem;
}

.qr-wrapper {
  display: inline-block;
  padding: 0.5rem;
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.qr-image {
  max-width: 180px;
  width: 100%;
  height: auto;
  border-radius: 8px;
  display: block;
}

.alipay-link {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: 1rem;
  padding: 0.6rem 1.25rem;
  background-color: #1677ff;
  color: white;
  text-decoration: none;
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 500;
  transition: all 0.2s;
}

.alipay-link:hover {
  background-color: #4096ff;
  transform: translateY(-1px);
}

/* ===== 备注输入 ===== */
.remark-input {
  width: 100%;
  padding: 0.875rem;
  border: 1px solid var(--color-border);
  border-radius: 10px;
  background-color: var(--color-background);
  color: var(--color-text);
  font-size: 0.9rem;
  font-family: inherit;
  resize: vertical;
  transition: border-color 0.2s;
}

.remark-input:focus {
  outline: none;
  border-color: var(--color-primary);
}

.remark-input::placeholder {
  color: var(--color-text-mute);
}

/* ===== 操作按钮 ===== */
.drawer-actions {
  display: flex;
  gap: 0.75rem;
  padding: 1.25rem 1.5rem;
  border-top: 1px solid var(--color-border);
  background-color: var(--color-background);
  flex-shrink: 0;
}

.action-btn {
  flex: 1;
  padding: 0.875rem;
  border-radius: 10px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
}

.cancel-btn {
  background-color: var(--color-background-mute);
  color: var(--color-text);
  border: 1px solid var(--color-border);
}

.cancel-btn:hover {
  background-color: var(--color-background-soft);
}

.confirm-btn {
  background-color: var(--color-primary);
  color: white;
}

.confirm-btn:hover:not(:disabled) {
  background-color: var(--color-primary-hover);
}

.confirm-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-loading {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.spinner-small {
  width: 18px;
  height: 18px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

/* ===== 抽屉动画 ===== */
.drawer-overlay-enter-active,
.drawer-overlay-leave-active {
  transition: opacity 0.3s ease;
}

.drawer-overlay-enter-from,
.drawer-overlay-leave-to {
  opacity: 0;
}

/* 桌面端: 从右侧滑入 */
.drawer-slide-enter-active,
.drawer-slide-leave-active {
  transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

.drawer-slide-enter-from,
.drawer-slide-leave-to {
  transform: translateX(100%);
}

/* ===== 响应式调整 ===== */
@media (max-width: 640px) {
  .package-view {
    padding: 1rem;
  }

  .page-title {
    font-size: 1.75rem;
  }

  .page-subtitle {
    font-size: 0.95rem;
  }

  .package-content {
    padding: 1.25rem;
  }

  .pages-value {
    font-size: 2.5rem;
  }

  .info-card {
    padding: 1.5rem;
  }

  /* 移动端: 底部抽屉 */
  .drawer-container {
    top: auto;
    left: 0;
    right: 0;
    bottom: 0;
    width: 100%;
    max-height: 92vh;
    border-radius: 20px 20px 0 0;
    box-shadow: 0 -4px 24px rgba(0, 0, 0, 0.15);
  }

  .drawer-header {
    padding: 1rem 1.25rem;
    position: relative;
  }

  /* 移动端拖拽指示条 */
  .drawer-header::before {
    content: '';
    position: absolute;
    top: 8px;
    left: 50%;
    transform: translateX(-50%);
    width: 36px;
    height: 4px;
    background-color: var(--color-border);
    border-radius: 2px;
  }

  .drawer-title {
    font-size: 1.1rem;
    padding-top: 0.5rem;
  }

  .drawer-body {
    padding-bottom: 0.5rem;
  }

  .selected-package-summary {
    margin: 1rem;
  }

  .payment-section,
  .upload-section,
  .remark-section,
  .qr-section {
    padding: 0 1rem;
  }

  .drawer-actions {
    padding: 1rem;
    /* iOS 安全区域 */
    padding-bottom: max(1rem, env(safe-area-inset-bottom));
  }

  .qr-image {
    width: 140px;
    height: 140px;
  }

  /* 移动端动画: 从底部滑入 */
  .drawer-slide-enter-from,
  .drawer-slide-leave-to {
    transform: translateY(100%);
  }
}
</style>
