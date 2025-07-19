<template>
  <div class="page-container">
    <section class="hero-section">
      <div class="content-wrapper">
        <h1 class="hero-title">简单、快速、可靠的打印服务</h1>
        <p class="hero-subtitle">
          从上传文件到取件，我们为您提供一站式无忧打印解决方案。Printerify，为每一次打印赋能。
        </p>
        <router-link to="/order">
          <BaseButton>立即打印</BaseButton>
        </router-link>
      </div>
    </section>

    <section class="features-section">
      <div class="content-wrapper">
        <h2 class="section-title">核心功能</h2>
        <div class="features-grid">
          <div class="feature-card">
            <div class="icon-wrapper">
              <svg xmlns="http://www.w3.org/2000/svg" class="icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
              </svg>
            </div>
            <h3 class="feature-title">极简流程</h3>
            <p class="feature-description">通过我们精心设计的步骤引导，只需几分钟即可完成您的打印配置和下单。</p>
          </div>
          <div class="feature-card">
            <div class="icon-wrapper">
              <svg xmlns="http://www.w3.org/2000/svg" class="icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <h3 class="feature-title">状态实时</h3>
            <p class="feature-description">提交订单后，您可以随时通过订单号查询打印状态和订单信息，全程透明。</p>
          </div>
          <div class="feature-card">
            <div class="icon-wrapper">
              <svg xmlns="http://www.w3.org/2000/svg" class="icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
  <!-- 盾牌形状 -->
  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3l7 4v5c0 5.25-3.5 9.75-7 11-3.5-1.25-7-5.75-7-11V7l7-4z" />
  <!-- 十字图形 -->
  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v6m-3-3h6" />
</svg>

            </div>
            <h3 class="feature-title">品质保证</h3>
            <p class="feature-description">我们采用高质量的打印设备和材料，确保每一份文件都呈现出最佳的效果。</p>
          </div>
        </div>
      </div>
    </section>

    <section class="stats-section" ref="statsSection">
      <div class="content-wrapper stats-grid">
        <div class="stat-item">
          <span class="stat-number">{{ pageCountDisplay.toLocaleString() }}</span>
          <p class="stat-label">累计打印页数</p>
        </div>
        <div class="stat-item">
          <span class="stat-number">{{ userCountDisplay.toLocaleString() }}</span>
          <p class="stat-label">服务用户数</p>
        </div>
        <div class="stat-item">
          <span class="stat-number">{{ satisfactionRateDisplay }}%</span>
          <p class="stat-label">用户好评率</p>
        </div>
      </div>
    </section>

    <section class="how-it-works-section" ref="howItWorksSection">
      <div class="sticky-wrapper">
        <div class="content-wrapper">
          <h2 class="section-title">只需三步，轻松搞定</h2>
          <div class="stepper-container">
            <Stepper :currentStep="currentStep" :steps="steps" />
          </div>
          <div class="step-content">
            <transition name="fade" mode="out-in">
              <div v-if="currentStep === 1" class="step-pane" key="step1">
                <h3>第一步：上传您的文件</h3>
                <p>点击下方区域或直接拖拽文件至此，即可开始您的打印之旅。</p>
                <div class="mock-uploader">
                  <svg xmlns="http://www.w3.org/2000/svg" class="upload-icon" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M12 16.5V9.75m0 0l-3.75 3.75M12 9.75l3.75 3.75M3 17.25V6.75a2.25 2.25 0 012.25-2.25h13.5A2.25 2.25 0 0121 6.75v10.5a2.25 2.25 0 01-2.25 2.25H5.25A2.25 2.25 0 013 17.25z" /></svg>
                  <p><strong>点击或拖拽文件到这里</strong></p>
                  <span class="upload-hint">支持 PDF, DOC, PPT 等多种格式</span>
                </div>
              </div>
              <div v-else-if="currentStep === 2" class="step-pane" key="step2">
                <h3>第二步：设定打印选项</h3>
                <p>为文件分组、调整打印设置，一切尽在掌握。</p>
                <BindingGroup :group="sampleGroup" :group-index="0" is-demo-mode />
              </div>
<div v-else-if="currentStep === 3" class="step-pane" key="step3">
  <h3>第三步：获取取件码</h3>
  <p>订单已成功提交！请凭以下取件码在服务点开放时间前往取件。</p>
  <div class="order-summary-container">
    <div class="summary-header">取件信息</div>
    <div class="summary-body">
      <div class="pickup-code-wrapper">
        <span class="pickup-code-label">您的取件码</span>
        <div class="pickup-code">P-168</div>
      </div>
      <div class="summary-item total">
        <span>订单总计</span>
        <span class="total-price">¥{{ sampleTotalCost }}</span>
      </div>
      <div class="pickup-info">
        <p><strong>服务时间:</strong> 工作日 09:00 - 18:00</p>
      </div>
    </div>
    <BaseButton class="confirm-button">我已保存取件码</BaseButton>
  </div>
</div>
            </transition>
          </div>
        </div>
      </div>
    </section>

    <section class="testimonials-section">
      <div class="content-wrapper">
        <h2 class="section-title">听听我们的用户怎么说</h2>
        <div class="testimonials-grid">
          <div class="testimonial-card">
           <p class="testimonial-quote">"这彻底改变了我们的打印流程。以往需要花费大量精力处理订单，并与用户沟通和确认打印稿件，现在在后台点击就能搞定，效率非常棒！"</p>
           <div class="testimonial-author">
             <span class="author-name">- Xicheng2003, 开发者</span>
           </div>
         </div>
         <div class="testimonial-card">
           <p class="testimonial-quote">"作为一名学生，我经常需要打印大量的论文和资料。这里的价格公道，而且订单追踪功能让我非常安心，总能准时拿到我的文件。"</p>
           <div class="testimonial-author">
             <span class="author-name">- 王同学, 大学生</span>
           </div>
         </div>
         <div class="testimonial-card">
           <p class="testimonial-quote">"传统用微信（即时通讯工具）去沟通调整打印参数，费时费力，沟通繁琐，现在自助下单一键解决。这里的服务非常可靠，从未出过差错，是我们可以信赖的合作伙伴。"</p>
           <div class="testimonial-author">
             <span class="author-name">- 张同学, 大学生</span>
           </div>
         </div>
        </div>
      </div>
    </section>

    <section class="cta-section">
        <div class="content-wrapper cta-content">
          <h2 class="cta-title">准备好体验便捷的打印服务了吗？</h2>
          <p class="cta-description">只需几步，即可上传文件、设置选项并轻松下单。</p>
          <p class="cta-description">立即开始，享受高质量的打印体验！</p>
          <router-link to="/order">
             <BaseButton class="cta-button">立即打印</BaseButton>
          </router-link>
        </div>
      </section>

  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue';
import Stepper from '@/components/Stepper.vue';
import BaseButton from '@/components/BaseButton.vue';
import BindingGroup from '@/components/BindingGroup.vue';

// --- 【重要逻辑更新】粘性滚动处理 ---
const steps = ref(['上传文件', '设置选项', '确认下单']);
const currentStep = ref(1);
const howItWorksSection = ref(null);

const handleStepperScroll = () => {
  const section = howItWorksSection.value;
  if (!section) return;

  const rect = section.getBoundingClientRect();
  const viewportHeight = window.innerHeight;

  // 当区域顶部滚动到视口顶部之上时，才开始计算进度
  // rect.top <= 0 表示粘性定位已生效或即将生效
  // rect.bottom >= viewportHeight 表示区域底部仍在视口之下，确保我们在"轨道"内
  if (rect.top <= 0 && rect.bottom >= viewportHeight) {
    // 计算在粘性区域内滚动的距离
    const scrollDistance = -rect.top;
    // 计算总的滚动行程 (区域总高度 - 一个视口的高度)
    const totalScrollRange = section.offsetHeight - viewportHeight;
    // 计算滚动进度
    const progress = Math.min(1, scrollDistance / totalScrollRange);

    // 根据进度切换步骤
    if (progress < 0.4) { // 为步骤1分配40%的行程
      currentStep.value = 1;
    } else if (progress < 0.8) { // 为步骤2分配40%的行程
      currentStep.value = 2;
    } else { // 剩余行程为步骤3
      currentStep.value = 3;
    }
  } else if (rect.top > 0) {
    // 如果区域滚回视口下方，重置到步骤1
    currentStep.value = 1;
  } else {
    // 如果完全滚过区域，确保停留在步骤3
    currentStep.value = 3;
  }
};

// 【新增】在 sampleGroup 定义之后，添加这个计算属性
const sampleTotalCost = computed(() => {
  return sampleGroup.value.documents
    .reduce((total, doc) => total + parseFloat(doc.printCost), 0)
    .toFixed(2);
});

// --- 【重要更新】创建符合 BindingGroup 和 DocumentItem 期望的模拟数据 ---
const sampleGroup = ref({
  id: 'sample-group-1',
  index: '1',
  bindingType: 'staple_top_left',
  documents: [
    {
      id: 'sample-doc-1',
      fileName: '项目开题报告.pdf',
      isUploading: false,
      isRecalculating: false,
      uploadProgress: 100,
      pageCount: 25,
      printCost: '3.75',
      error: null,
      settings: {
        copies: 1,
        colorMode: 'black_white',
        printSided: 'double',
        paperSize: 'a4',
      }
    },
    {
      id: 'sample-doc-2',
      fileName: '答辩演示文稿_v3.pptx',
      pageCount: 42,
      printCost: '21.00',
      isUploading: false,
      isRecalculating: false,
      uploadProgress: 100,
      error: null,
      settings: {
        copies: 1,
        colorMode: 'black_white',
        printSided: 'single',
        paperSize: 'a4',
      }
    }
  ]
});


// --- Stats Counter Logic ---
const statsSection = ref(null);
const startAnimation = ref(false);
const pageCountDisplay = ref(0);
const userCountDisplay = ref(0);
const satisfactionRateDisplay = ref(0);
const pageCountTarget = 1089;
const userCountTarget = 46;
const satisfactionRateTarget = 99;

function animateValue(from, to, duration, onUpdate) {
  const startTimestamp = performance.now();
  const update = () => {
    const elapsed = performance.now() - startTimestamp;
    const progress = Math.min(1, elapsed / duration);
    const easedProgress = 1 - Math.pow(1 - progress, 3);
    const currentValue = Math.floor(from + (to - from) * easedProgress);
    onUpdate(currentValue);
    if (progress < 1) {
      requestAnimationFrame(update);
    } else {
      onUpdate(to);
    }
  };
  requestAnimationFrame(update);
}

watch(startAnimation, (isTriggered) => {
  if (isTriggered) {
    animateValue(0, pageCountTarget, 2500, (val) => pageCountDisplay.value = val);
    animateValue(0, userCountTarget, 2500, (val) => userCountDisplay.value = val);
    animateValue(0, satisfactionRateTarget, 3000, (val) => satisfactionRateDisplay.value = val);
  }
});

const handleStatsScroll = (entries, observer) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      startAnimation.value = true;
      observer.unobserve(statsSection.value);
    }
  });
};

// --- Lifecycle Hooks ---
let statsObserver = null;
let scrollListener = null;

onMounted(() => {
  scrollListener = () => handleStepperScroll();
  window.addEventListener('scroll', scrollListener, { passive: true });

  statsObserver = new IntersectionObserver(handleStatsScroll, { threshold: 0.5 });
  if (statsSection.value) {
    statsObserver.observe(statsSection.value);
  }
});

onUnmounted(() => {
  if (scrollListener) {
    window.removeEventListener('scroll', scrollListener);
  }
  if (statsObserver) {
    statsObserver.disconnect();
  }
});
</script>

<style scoped>
/* Scoped styles using CSS variables from main.css */
.page-container {
  color: var(--color-text);
  background-color: var(--color-background);
}

.content-wrapper {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}

.section-title {
  text-align: center;
  font-size: 2.25rem;
  font-weight: 700;
  color: var(--color-heading);
  margin-bottom: 3rem;
}

/* Hero Section Styles */
.hero-section {
  background-color: var(--color-background-soft);
  text-align: center;
  padding: 6rem 2rem;
  border-bottom: 1px solid var(--color-border);
}

.hero-title {
  font-size: 2.5rem;
  font-weight: 600;
  color: var(--color-heading);
  line-height: 1.2;
}

.hero-subtitle {
  font-size: 1.25rem;
  color: var(--color-text);
  margin-top: 1rem;
  margin-bottom: 2rem;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

/* Features Section Styles */
.features-section {
  padding: 5rem 2rem;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(1, 1fr);
  gap: 2rem;
  max-width: 1100px;
  margin: 0 auto;
}

@media (min-width: 768px) {
  .features-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

.feature-card {
  text-align: center;
  padding: 2rem;
  background-color: var(--color-background-soft);
  border: 1px solid var(--color-border);
  border-radius: 12px;
  transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: var(--shadow-card);
}

.icon-wrapper {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 4rem;
  height: 4rem;
  border-radius: 50%;
  background-color: var(--color-primary-soft, #ebf4ff); /* Using a fallback */
  color: var(--color-primary);
  margin-bottom: 1.5rem;
}

.icon-wrapper .icon {
  width: 2rem;
  height: 2rem;
}

.feature-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--color-heading);
  margin-bottom: 0.5rem;
}

.feature-description {
  color: var(--color-text);
  line-height: 1.6;
}

/* Stats Section Styles */
.stats-section {
  background-color: var(--color-background);
  padding: 4rem 2rem;
  border-top: 1px solid var(--color-border);
  border-bottom: 1px solid var(--color-border);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(1, 1fr);
  gap: 2rem;
  text-align: center;
}

@media (min-width: 768px) {
  .stats-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

.stat-item {
  padding: 1rem;
}

.stat-number {
  font-size: 3rem;
  font-weight: 800;
  color: var(--color-primary);
  line-height: 1;
}

.stat-label {
  margin-top: 0.5rem;
  font-size: 1rem;
  color: var(--color-text);
  letter-spacing: 0.05em;
  text-transform: uppercase;
}

/* 【重要样式更新】粘性滚动相关样式 */
.how-it-works-section {
  background-color: var(--color-background-soft);
  /* 设置一个足够大的高度来创建滚动“轨道” */
  height: 300vh;
  padding: 5rem 2rem 0; /* 调整内边距以适应粘性布局 */
}

/* 新增的粘性包裹层样式 */
.sticky-wrapper {
  position: -webkit-sticky; /* 兼容 Safari */
  position: sticky;
  top: 0;
  height: 100vh; /* 占据整个视口高度 */
  display: flex;
  align-items: center;
  justify-content: center;
}

.sticky-wrapper > .content-wrapper {
  max-width: 1200px;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.section-title {
  padding-top: 3rem; /* 增加一些顶部空间 */
}

.stepper-container {
  max-width: 800px;
  margin: 0 auto 2.5rem auto;
  width: 100%;
}

.step-content {
  background-color: var(--color-background);
  border: 1px solid var(--color-border);
  border-radius: 12px;
  padding: 2rem;
  /* 高度由内容和父容器决定，不再设置min-height */
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  max-width: 800px;
  width: 100%;
  margin: 0 auto;
  position: relative;
  overflow: hidden;
  box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05), 0 2px 4px -1px rgba(0,0,0,0.03);
}

/* 【重要样式更新】为步骤面板增加内部滚动能力 */
.step-pane {
  width: 100%;
  max-width: 720px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start; /* 从顶部开始对齐 */

  /* 设置一个最大高度，内容超出时可滚动 */
  max-height: 75vh;
  overflow-y: auto; /* Y轴超出时自动显示滚动条 */

  /* 为滚动条留出空间，防止内容紧贴边缘 */
  padding: 1.5rem;
}


.step-content h3 {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--color-heading);
  margin-bottom: 1rem;
}

.step-content p {
  max-width: 500px;
  color: var(--color-text);
  margin-bottom: 1.5rem;
}

.step-image {
  max-width: 100%;
  height: auto;
  border-radius: 4px;
  margin-top: 1rem;
  border: 1px solid var(--color-border);
}

.mock-uploader {
  border: 2px dashed var(--color-border);
  border-radius: 8px;
  padding: 2rem;
  width: 100%;
  max-width: 400px;
  transition: border-color 0.2s;
  cursor: pointer;
}
.mock-uploader:hover {
  border-color: var(--color-primary);
}

.upload-icon {
  width: 3rem;
  height: 3rem;
  margin: 0 auto 1rem auto;
  color: var(--color-text);
}

.upload-hint {
  font-size: 0.875rem;
  color: var(--color-text);
  margin-top: 0.5rem;
}

/* Testimonials Section */
.testimonials-section {
  padding: 5rem 2rem;
  background-color: var(--color-background);
}

.testimonials-grid {
  display: grid;
  grid-template-columns: repeat(1, 1fr);
  gap: 2rem;
  max-width: 1100px;
  margin: 0 auto;
}

@media (min-width: 992px) {
  .testimonials-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

.testimonial-card {
  background-color: var(--color-background-soft);
  padding: 2rem;
  border: 1px solid var(--color-border);
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  position: relative;
}

.testimonial-quote {
  font-style: italic;
  color: var(--color-text);
  margin-bottom: 1.5rem;
  flex-grow: 1;
  z-index: 1;
}

.testimonial-card::before {
  content: '“';
  font-size: 5rem;
  font-weight: bold;
  color: var(--color-border);
  position: absolute;
  left: 1rem;
  top: 0.5rem;
  z-index: 0;
  line-height: 1;
}

.testimonial-author {
  text-align: right;
  font-weight: 600;
  color: var(--color-heading);
}

/* FAQ Section Styles */
.faq-section {
  padding: 5rem 2rem;
  background-color: var(--color-background-soft);
}

.faq-container {
  max-width: 800px;
  margin: 0 auto;
}

.faq-item {
  border-bottom: 1px solid var(--color-border);
}
.faq-item:first-of-type {
  border-top: 1px solid var(--color-border);
}

.faq-question {
  font-size: 1.125rem;
  font-weight: 500;
  color: var(--color-heading);
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  list-style: none; /* remove default marker */
  padding: 1.5rem 0;
}

.faq-question::-webkit-details-marker {
  display: none; /* remove default marker for webkit browsers */
}

.faq-question::after {
  content: '+';
  font-size: 1.5rem;
  font-weight: 300;
  transition: transform 0.2s ease-in-out;
}

details[open] > summary.faq-question::after {
  content: '−';
}

.faq-answer {
  color: var(--color-text);
  padding: 0 0 1.5rem 0;
  line-height: 1.7;
}

/* CTA Section Styles */
.cta-section {
  background-color: var(--color-background);
  padding: 5rem 2rem;
  text-align: center;
}

.cta-content {
  max-width: 800px;
  margin: 0 auto;
}

.cta-title {
  font-size: 2rem;
  font-weight: 700;
  color: var(--color-heading);
  margin-bottom: 1rem;
}

.cta-description {
  font-size: 1.125rem;
  color: var(--color-text);
  margin-bottom: 2rem;
}

.cta-button {
    font-size: 1.2rem;
    padding: 1rem 2rem;
}

/* Transition Styles */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.4s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
/* 新增：为步骤二和步骤三添加的补充样式 */
.binding-group-container,
.order-summary-container {
  width: 100%;
  max-width: 450px; /* 限制内容最大宽度，使其更美观 */
  margin-top: 1.5rem;
  border: 1px solid var(--color-border);
  border-radius: 8px;
  padding: 1.5rem;
  background-color: var(--color-background-soft);
}

.order-summary-container {
  text-align: left;
}

.summary-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 0;
  border-bottom: 1px solid var(--color-border);
}

.summary-item:last-child {
  border-bottom: none;
}

.summary-label {
  color: var(--color-text);
}

.summary-value {
  font-weight: 600;
  color: var(--color-heading);
}

.summary-total {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid var(--color-heading);
}

.summary-price {
  color: var(--color-primary);
  font-size: 1.5rem;
}
/* 【重要更新】确保以下样式存在或得到更新 */
.how-it-works-section {
  background-color: var(--color-background-soft);
  padding: 5rem 2rem;
}

.stepper-container {
  max-width: 800px;
  margin: 0 auto 2.5rem auto;
}

.step-content {
  background-color: var(--color-background);
  border: 1px solid var(--color-border);
  border-radius: 12px;
  padding: 2rem;
  min-height: 480px; /* 增加最小高度以容纳组件 */
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  max-width: 800px;
  margin: 0 auto;
  position: relative;
  overflow: hidden;
  box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05), 0 2px 4px -1px rgba(0,0,0,0.03);
}


.step-content h3 {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--color-heading);
  margin-bottom: 0.75rem;
}

.step-content p {
  max-width: 500px;
  color: var(--color-text);
  margin-bottom: 2rem;
}

.step-image {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
  margin-top: 1rem;
  border: 1px solid var(--color-border);
}

.mock-uploader {
  border: 2px dashed var(--color-border);
  border-radius: 8px;
  padding: 2.5rem;
  width: 100%;
  max-width: 450px;
  transition: border-color 0.2s, background-color 0.2s;
  cursor: pointer;
}
.mock-uploader:hover {
  border-color: var(--color-primary);
  background-color: var(--color-background-soft);
}

.upload-icon {
  width: 3rem;
  height: 3rem;
  margin: 0 auto 1rem auto;
  color: var(--color-text-light);
}

.upload-hint {
  font-size: 0.875rem;
  color: var(--color-text);
  margin-top: 0.5rem;
}

/* Transition Styles */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.4s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

/* 【重要样式更新】为步骤三的取件信息摘要添加样式 */
.order-summary-container {
  width: 100%;
  max-width: 400px; /* 调整宽度以适应新内容 */
  text-align: left;
  border: 1px solid var(--color-border);
  border-radius: 8px;
  background-color: var(--color-background-soft);
  overflow: hidden; /* 确保子元素的圆角生效 */
}
.summary-header {
  padding: 1rem 1.5rem;
  font-weight: 600;
  color: var(--color-heading);
  background-color: var(--color-background);
  border-bottom: 1px solid var(--color-border);
}
.summary-body {
  padding: 1.5rem;
}
.pickup-code-wrapper {
  text-align: center;
  margin-bottom: 1.5rem;
}
.pickup-code-label {
  font-size: 0.9rem;
  color: var(--color-text);
}
.pickup-code {
  font-size: 2.5rem;
  font-weight: 700;
  letter-spacing: 0.2rem;
  color: var(--color-primary);
  background-color: var(--color-background);
  padding: 0.75rem 1.5rem;
  border-radius: 6px;
  margin-top: 0.5rem;
  border: 1px dashed var(--color-primary);
}
.summary-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 0;
}
.summary-item.total {
  font-weight: bold;
  font-size: 1.1rem;
  color: var(--color-heading);
  padding-top: 1rem;
  border-top: 1px solid var(--color-border);
}
.total-price {
  color: var(--color-primary);
  font-size: 1.25rem;
}
/* 【重要样式更新】调整取件信息区域的样式 */
.pickup-info {
  text-align: center; /* 居中显示服务时间 */
  margin-top: 1.5rem;
  padding-top: 1rem;
  border-top: 1px solid var(--color-border);
  font-size: 0.9rem;
  color: var(--color-text);
}

.pickup-info p {
  margin: 0; /* 移除默认的段落间距 */
}
.confirm-button {
  width: 100%;
  padding: 0.9rem;
  font-size: 1rem;
  border-radius: 0 0 7px 7px; /* 只保留底部圆角 */
  border-top: 1px solid var(--color-border-hover);
}
</style>
