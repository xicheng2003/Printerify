<template>
  <div class="product-intro">
    <!-- Hero Section -->
    <section class="hero-section">
      <div class="container hero-content">
        <div class="hero-text">
          <h1 class="hero-title">
            让打印变得<br />
            <span class="highlight">简单、快速、可靠</span>
          </h1>
          <p class="hero-subtitle">
            告别繁琐的传统打印店。随时随地上传文件，自定义打印设置，扫码即取。
            专为现代校园生活打造。
          </p>
          <div class="hero-actions">
            <RouterLink to="/order">
              <BaseButton size="large" class="cta-button">立即开始打印</BaseButton>
            </RouterLink>
            <button class="secondary-button" @click="scrollToFeatures">
              了解更多
            </button>
          </div>
          <div class="hero-stats">
            <div class="stat-item">
              <span class="stat-value">10k+</span>
              <span class="stat-label">累计打印页数</span>
            </div>
            <div class="stat-item">
              <span class="stat-value">99%</span>
              <span class="stat-label">好评率</span>
            </div>
          </div>
        </div>
        <div class="hero-visual">
          <!-- Abstract Paper Animation Representation -->
          <div class="paper-stack">
            <div class="paper paper-1"></div>
            <div class="paper paper-2"></div>
            <div class="paper paper-3">
              <div class="paper-content">
                <div class="line title-line"></div>
                <div class="line"></div>
                <div class="line"></div>
                <div class="line short"></div>
                <div class="print-status">
                  <span class="status-icon">✓</span> 打印完成
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section id="features" class="features-section">
      <div class="container">
        <div class="section-header">
          <h2>为什么选择 Printerify？</h2>
          <p>我们重新定义了自助打印体验，每一个细节都为您考虑。</p>
        </div>
        <div class="features-grid">
          <div class="feature-card" v-for="feature in features" :key="feature.title">
            <div class="feature-icon-wrapper">
              <component :is="feature.icon" class="feature-icon" />
            </div>
            <h3>{{ feature.title }}</h3>
            <p>{{ feature.description }}</p>
            <div class="feature-tags">
              <span v-for="tag in feature.tags" :key="tag" class="feature-tag">{{ tag }}</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Workflow Section -->
    <section class="workflow-section">
      <div class="container">
        <div class="section-header">
          <h2>只需三步，轻松搞定</h2>
        </div>
        <div class="workflow-steps">
          <div class="step-item" v-for="(step, index) in steps" :key="index">
            <div class="step-header">
              <div class="step-number">0{{ index + 1 }}</div>
              <div class="step-subtitle">{{ step.subtitle }}</div>
            </div>
            <div class="step-icon-wrapper">
               <component :is="step.icon" />
            </div>
            <h3>{{ step.title }}</h3>
            <p>{{ step.description }}</p>
            <ul class="step-details">
              <li v-for="detail in step.details" :key="detail">{{ detail }}</li>
            </ul>
          </div>
        </div>
      </div>
    </section>

    <!-- FAQ Section -->
    <section class="faq-section">
      <div class="container">
        <div class="section-header">
          <h2>常见问题解答</h2>
          <p>您可能关心的问题，我们都整理好了。</p>
        </div>
        <div class="faq-container">
          <div
            v-for="(faq, index) in faqs"
            :key="index"
            class="faq-item"
            :class="{ 'is-open': activeFaqIndex === index }"
          >
            <button
              class="faq-question"
              @click="toggleFaq(index)"
              :aria-expanded="activeFaqIndex === index"
            >
              <span class="question-text">{{ faq.question }}</span>
              <span class="faq-icon">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <polyline points="6 9 12 15 18 9"></polyline>
                </svg>
              </span>
            </button>
            <div
              class="faq-answer"
              :style="{ maxHeight: activeFaqIndex === index ? '200px' : '0' }"
            >
              <div class="answer-content" v-html="faq.answer"></div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="cta-section">
      <div class="container">
        <div class="cta-card">
            <div class="cta-background">
              <div class="circle circle-1"></div>
              <div class="circle circle-2"></div>
              <div class="circle circle-3"></div>
              <div class="grid-pattern"></div>
            </div>          <div class="cta-content">
            <h2 class="cta-title">准备好体验更智能的打印了吗？</h2>
            <p class="cta-description">
              加入 Printerify，告别排队与繁琐。无论是论文、作业还是资料，我们都能为您提供完美的打印体验。
            </p>

            <div class="cta-actions">
              <RouterLink to="/order">
                <BaseButton variant="primary" class="cta-button-primary">
                  立即开始打印
                  <svg xmlns="http://www.w3.org/2000/svg" class="icon-arrow" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clip-rule="evenodd" />
                  </svg>
                </BaseButton>
              </RouterLink>
              <RouterLink to="/query" class="cta-link">
                查询已有订单
              </RouterLink>
            </div>

            <div class="cta-features">
              <div class="cta-feature-item">
                <span class="check-icon">✓</span> 无需注册
              </div>
              <div class="cta-feature-item">
                <span class="check-icon">✓</span> 极速出单
              </div>
              <div class="cta-feature-item">
                <span class="check-icon">✓</span> 隐私保护
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { RouterLink } from 'vue-router';
import BaseButton from '@/components/BaseButton.vue';

// Icons (Simple SVG components for demo)
const IconUpload = {
  template: `<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" /></svg>`
};
const IconSettings = {
  template: `<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" /><path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /></svg>`
};
const IconSecure = {
  template: `<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" /></svg>`
};
const IconDevice = {
  template: `<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z" /></svg>`
};
const IconCheck = {
  template: `<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>`
};

const features = [
  {
    title: '极速上传',
    description: '支持拖拽上传，秒级解析。无论是 PDF、Word 还是 PPT，都能完美兼容。',
    icon: IconUpload,
    tags: ['拖拽上传', '秒级解析', '多格式兼容']
  },
  {
    title: '实时计价',
    description: '调整参数实时显示价格，所见即所得。拒绝隐形消费，每一分钱都花得明白。',
    icon: IconSettings,
    tags: ['透明价格', '无隐形消费', '自动计算']
  },
  {
    title: '安全隐私',
    description: '文件加密传输，打印完成后自动销毁。您的数据安全是我们最看重的承诺。',
    icon: IconSecure,
    tags: ['加密传输', '自动销毁', '隐私保护']
  },
  {
    title: '多端同步',
    description: '手机、电脑、平板，随时随地访问。订单状态实时同步，一手掌握。',
    icon: IconDevice,
    tags: ['全平台支持', '实时状态', '随时访问']
  }
];

const steps = [
  {
    title: '上传文件',
    subtitle: 'Upload',
    description: '将您的文档拖入上传区域，系统自动解析页数与格式。',
    details: ['支持 PDF, Word, PPT', '智能解析页数', '自动检测格式'],
    icon: IconUpload
  },
  {
    title: '个性设置',
    subtitle: 'Settings',
    description: '选择纸张大小、单双面、黑白彩印及装订方式。',
    details: ['A4 / A3 纸张', '黑白 / 彩色打印', '单面 / 双面打印'],
    icon: IconSettings
  },
  {
    title: '支付取件',
    subtitle: 'Print',
    description: '扫码支付，获取取件码。前往打印点输入取件码即可拿走文件。',
    details: ['微信 / 支付宝', '凭码自助取件', '24小时随时取'],
    icon: IconCheck
  }
];

const scrollToFeatures = () => {
  document.getElementById('features')?.scrollIntoView({ behavior: 'smooth' });
};

// FAQ Data
const activeFaqIndex = ref(0);
const faqs = ref([
  {
    question: 'Printerify 支持哪些文件格式？',
    answer: '<p>Printerify 支持主流的文档格式，包括 PDF, DOC, DOCX, PPT, PPTX, JPG, PNG 等。为了获得最佳打印效果，我们强烈推荐您上传 PDF 文件。</p>'
  },
  {
    question: '使用 Printerify 如何收取费用？',
    answer: '<p>Printerify 的收费标准主要根据订单的页数、纸张类型和其他附加服务来计算。具体计费规则说明可在自助打印下单页面点击查看。在下单过程中，您也可以在确认订单前查看详细的费用明细。</p>'
  },
  {
    question: '在 Printerify 打印需要多长时间？',
    answer: '<p>生产时间取决于您的订单复杂程度和当前排队情况，通常在 6 小时内完成。具体订单状态可在订单查询页面查看。</p>'
  },
  {
    question: 'Printerify 有哪些打印规格可供选择？',
    answer: '<p>Printerify 提供多种打印规格选项，包括纸张大小（如 A4、B5）、单/双面（单面打印或双面打印）等，请以实际下单页面提供的选项为准。您可以在下单时根据需要选择合适的打印规格。</p>'
  },
  {
    question: '如果我对打印质量不满意怎么办？',
    answer: '<p>Printerify 对打印质量有严格的把控。如果您收到的成品有任何质量问题（如错印、装订错误等），请立即联系我们的客服，我们将为您免费重印或进行退款处理。</p>'
  },
  {
    question: '如何获取 Printerify 的服务支持？',
    answer: `<p>如果您在使用 Printerify 的过程中遇到任何问题或需要帮助，请随时联系我们的客服团队。</p>
             <p>您可以通过以下方式获取支持：</p>
             <ul>
               <li>访问我们的产品页面，查阅常见问题解答和使用指南。</li>
               <li>通过在线聊天工具（微信群或QQ群）与我们的客服代表实时沟通。</li>
               <li>用户群的加入方式可以发送邮件至 xicheng.lin@foxmail.com，我们会尽快邀请您加入。</li>
               <li>其他事宜也可发送电子邮件至 xicheng.lin@foxmail.com，我们会尽快回复您。</li>
             </ul>`
  }
]);

const toggleFaq = (index) => {
  activeFaqIndex.value = activeFaqIndex.value === index ? -1 : index;
};
</script>

<style scoped>
.product-intro {
  width: 100%;
  overflow-x: hidden;
  background-color: var(--color-background);
  background-image:
    radial-gradient(at 0% 0%, rgba(var(--color-primary-rgb), 0.03) 0px, transparent 50%),
    radial-gradient(at 100% 0%, rgba(var(--color-primary-rgb), 0.03) 0px, transparent 50%);
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1.5rem;
}

/* Hero Section */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeInRight {
  from {
    opacity: 0;
    transform: translateX(30px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.hero-section {
  padding: 6rem 0;
  background: linear-gradient(135deg, var(--color-background-soft) 0%, var(--color-background) 100%);
  position: relative;
  overflow: hidden;
}

.hero-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4rem;
  align-items: center;
}

.hero-title {
  font-size: 3.5rem;
  font-weight: 800;
  line-height: 1.2;
  margin-bottom: 1.5rem;
  color: var(--color-heading);
  opacity: 0;
  animation: fadeInUp 0.8s ease-out forwards;
}

.hero-title .highlight {
  color: var(--color-primary);
  background: linear-gradient(120deg, rgba(var(--color-primary-rgb), 0.1) 0%, rgba(var(--color-primary-rgb), 0.05) 100%);
  padding: 0 0.5rem;
  border-radius: 8px;
}

.hero-subtitle {
  font-size: 1.25rem;
  color: var(--color-text-mute);
  margin-bottom: 2.5rem;
  line-height: 1.6;
  max-width: 540px;
  opacity: 0;
  animation: fadeInUp 0.8s ease-out 0.2s forwards;
}

.hero-actions {
  display: flex;
  gap: 1rem;
  margin-bottom: 3rem;
  opacity: 0;
  animation: fadeInUp 0.8s ease-out 0.4s forwards;
}

.secondary-button {
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 600;
  font-size: 1rem;
  color: var(--color-text);
  background: transparent;
  border: 1px solid var(--color-border);
  cursor: pointer;
  transition: all 0.2s;
}

.secondary-button:hover {
  border-color: var(--color-primary);
  color: var(--color-primary);
  background-color: rgba(var(--color-primary-rgb), 0.05);
}

.hero-stats {
  display: flex;
  gap: 3rem;
  padding-top: 2rem;
  border-top: 1px solid var(--color-border);
  opacity: 0;
  animation: fadeInUp 0.8s ease-out 0.6s forwards;
}

.stat-item {
  display: flex;
  flex-direction: column;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--color-heading);
}

.stat-label {
  font-size: 0.875rem;
  color: var(--color-text-mute);
}

/* Hero Visual - Paper Animation */
.hero-visual {
  position: relative;
  height: 400px;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  animation: fadeInRight 1s ease-out 0.4s forwards;
}

.paper-stack {
  position: relative;
  width: 240px;
  height: 320px;
}

.paper {
  position: absolute;
  width: 100%;
  height: 100%;
  background: var(--color-background);
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  border: 1px solid var(--color-border);
  transition: transform 0.5s ease;
}

.paper-1 {
  transform: rotate(-6deg) translate(-10px, 10px);
  z-index: 1;
  background-color: var(--color-background-soft);
}

.paper-2 {
  transform: rotate(3deg) translate(10px, -5px);
  z-index: 2;
  background-color: var(--color-background-mute);
}

.paper-3 {
  transform: rotate(-2deg);
  z-index: 3;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--color-background);
}

.hero-visual:hover .paper-1 {
  transform: rotate(-12deg) translate(-20px, 20px);
}

.hero-visual:hover .paper-2 {
  transform: rotate(6deg) translate(20px, -10px);
}

.hero-visual:hover .paper-3 {
  transform: rotate(0deg) scale(1.05);
  box-shadow: 0 20px 40px rgba(var(--color-primary-rgb), 0.15);
}

.paper-content {
  width: 80%;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.line {
  height: 8px;
  background-color: var(--color-border);
  border-radius: 4px;
  width: 100%;
}

.title-line {
  height: 12px;
  width: 60%;
  background-color: var(--color-primary);
  opacity: 0.2;
  margin-bottom: 0.5rem;
}

.short {
  width: 40%;
}

.print-status {
  margin-top: 2rem;
  align-self: center;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--color-success);
  font-weight: 600;
  font-size: 0.875rem;
  background: rgba(40, 167, 69, 0.1);
  padding: 0.5rem 1rem;
  border-radius: 20px;
}

/* Features Section */
.features-section {
  padding: 6rem 0;
  background-color: var(--color-background);
}

.section-header {
  text-align: center;
  max-width: 700px;
  margin: 0 auto 4rem;
}

.section-header h2 {
  font-size: 2.25rem;
  font-weight: 700;
  color: var(--color-heading);
  margin-bottom: 1rem;
}

.section-header p {
  font-size: 1.125rem;
  color: var(--color-text-mute);
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
}

.feature-card {
  padding: 2rem;
  border-radius: 16px;
  background: var(--color-background-soft);
  transition: transform 0.3s, box-shadow 0.3s;
  border: 1px solid transparent;
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: var(--shadow-card);
  border-color: var(--color-border);
  background: var(--color-background);
}

.feature-icon-wrapper {
  width: 48px;
  height: 48px;
  background: rgba(var(--color-primary-rgb), 0.1);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1.5rem;
  color: var(--color-primary);
}

.feature-icon {
  width: 24px;
  height: 24px;
}

.feature-card h3 {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 0.75rem;
  color: var(--color-heading);
}

.feature-card p {
  color: var(--color-text-mute);
  line-height: 1.6;
}

.feature-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: 1rem;
}

.feature-tag {
  font-size: 0.75rem;
  padding: 0.25rem 0.75rem;
  background-color: var(--color-background-mute);
  color: var(--color-text-mute);
  border-radius: 12px;
  border: 1px solid var(--color-border);
  transition: all 0.2s ease;
}

.feature-tag:hover {
  background-color: rgba(var(--color-primary-rgb), 0.1);
  color: var(--color-primary);
  border-color: rgba(var(--color-primary-rgb), 0.2);
}

/* Workflow Section */
.workflow-section {
  padding: 6rem 0;
  background-color: var(--color-background-soft);
}

.workflow-steps {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
  margin-top: 3rem;
}

.step-item {
  position: relative;
  background: var(--color-background);
  padding: 2.5rem 2rem;
  border-radius: 24px;
  border: 1px solid transparent;
  display: flex;
  flex-direction: column;
  transition: all 0.3s ease;
}

.step-item:hover {
  transform: translateY(-5px);
  box-shadow: var(--shadow-card);
  border-color: var(--color-border);
}

.step-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 2rem;
}

.step-number {
  font-family: 'Arial', sans-serif;
  font-size: 3rem;
  font-weight: 900;
  line-height: 1;
  color: var(--color-primary);
  opacity: 0.1;
}

.step-subtitle {
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 2px;
  font-weight: 700;
  color: var(--color-primary);
  opacity: 0.6;
  writing-mode: vertical-rl;
  transform: rotate(180deg);
}

.step-icon-wrapper {
  width: 64px;
  height: 64px;
  background: linear-gradient(135deg, var(--color-background-soft) 0%, var(--color-background) 100%);
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1.5rem;
  color: var(--color-primary);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.05);
}

.step-icon-wrapper svg {
  width: 32px;
  height: 32px;
}

.step-item h3 {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 1rem;
  color: var(--color-heading);
}

.step-item p {
  color: var(--color-text-mute);
  font-size: 1rem;
  line-height: 1.6;
  margin-bottom: 2rem;
}

.step-details {
  list-style: none;
  padding: 0;
  margin: 0;
  margin-top: auto;
  border-top: 1px solid var(--color-border);
  padding-top: 1.5rem;
}

.step-details li {
  position: relative;
  padding-left: 1.25rem;
  margin-bottom: 0.5rem;
  font-size: 0.875rem;
  color: var(--color-text-mute);
}

.step-details li::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0.6em;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background-color: var(--color-primary);
  opacity: 0.4;
}

.step-details li:last-child {
  margin-bottom: 0;
}

/* CTA Section */
.cta-section {
  padding: 8rem 0;
  background-color: var(--color-background);
}

.cta-card {
  position: relative;
  background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
  border-radius: 32px;
  padding: 6rem 2rem;
  text-align: center;
  color: white;
  overflow: hidden;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
  border: 1px solid rgba(255, 255, 255, 0.05);
  isolation: isolate;
}

.cta-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
  z-index: -1;
}

.circle {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.6;
}

.circle-1 {
  width: 400px;
  height: 400px;
  top: -100px;
  left: -100px;
  background: #3b82f6;
  animation: float 10s ease-in-out infinite;
}

.circle-2 {
  width: 500px;
  height: 500px;
  bottom: -150px;
  right: -150px;
  background: #6366f1;
  animation: float 12s ease-in-out infinite reverse;
}

.circle-3 {
  width: 300px;
  height: 300px;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: #0ea5e9;
  opacity: 0.2;
  animation: pulse 8s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translate(0, 0); }
  50% { transform: translate(30px, 20px); }
}

@keyframes pulse {
  0%, 100% { transform: translate(-50%, -50%) scale(1); opacity: 0.2; }
  50% { transform: translate(-50%, -50%) scale(1.5); opacity: 0.1; }
}

.grid-pattern {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image:
    linear-gradient(rgba(255, 255, 255, 0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.03) 1px, transparent 1px);
  background-size: 40px 40px;
  opacity: 0.5;
  mask-image: radial-gradient(circle at center, black 40%, transparent 100%);
}

.cta-content {
  position: relative;
  z-index: 1;
  max-width: 700px;
  margin: 0 auto;
}

.cta-title {
  font-size: 3rem;
  font-weight: 800;
  margin-bottom: 1.5rem;
  color: white;
  line-height: 1.1;
  letter-spacing: -0.02em;
  background: linear-gradient(to bottom right, #ffffff, #cbd5e1);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.cta-description {
  font-size: 1.25rem;
  margin-bottom: 3.5rem;
  color: #cbd5e1;
  line-height: 1.6;
}

.cta-actions {
  display: flex;
  gap: 1.5rem;
  justify-content: center;
  align-items: center;
  margin-bottom: 4rem;
  flex-wrap: wrap;
}

.cta-button-primary {
  background: white !important;
  color: #0f172a !important;
  font-size: 1.125rem !important;
  padding: 1rem 2.5rem !important;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  border: none;
  border-radius: 9999px !important;
  font-weight: 600 !important;
  transition: all 0.3s ease !important;
  box-shadow: 0 0 20px rgba(255, 255, 255, 0.1);
}

.cta-button-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 0 30px rgba(255, 255, 255, 0.3);
  background: #f8fafc !important;
}

.icon-arrow {
  width: 20px;
  height: 20px;
  transition: transform 0.2s;
}

.cta-button-primary:hover .icon-arrow {
  transform: translateX(4px);
}

.cta-link {
  color: #94a3b8;
  font-weight: 600;
  text-decoration: none;
  padding: 0.75rem 1.5rem;
  border-radius: 9999px;
  transition: all 0.2s;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.cta-link:hover {
  color: white;
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.2);
}

.cta-features {
  display: flex;
  justify-content: center;
  gap: 3rem;
  flex-wrap: wrap;
  padding-top: 2rem;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
}

.cta-feature-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  color: #e2e8f0;
  font-size: 1rem;
  font-weight: 500;
}

.check-icon {
  background: rgba(59, 130, 246, 0.2);
  color: #60a5fa;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.875rem;
  font-weight: bold;
}

@media (max-width: 640px) {
  .cta-title {
    font-size: 2.25rem;
  }

  .cta-actions {
    flex-direction: column;
    gap: 1rem;
    width: 100%;
  }

  .cta-button-primary, .cta-link {
    width: 100%;
    justify-content: center;
  }

  .cta-features {
    gap: 1.5rem;
    flex-direction: column;
    align-items: center;
  }
}

/* FAQ Section */
.faq-section {
  padding: 6rem 0;
  background-color: var(--color-background);
}

.faq-container {
  max-width: 800px;
  margin: 0 auto;
}

.faq-item {
  border-bottom: 1px solid var(--color-border);
}

.faq-item:last-child {
  border-bottom: none;
}

.faq-question {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 0;
  background: none;
  border: none;
  cursor: pointer;
  text-align: left;
  color: var(--color-heading);
  font-weight: 600;
  font-size: 1.125rem;
  transition: color 0.2s;
}

.faq-question:hover {
  color: var(--color-primary);
}

.faq-icon {
  color: var(--color-text-mute);
  transition: transform 0.3s ease;
}

.faq-item.is-open .faq-icon {
  transform: rotate(180deg);
  color: var(--color-primary);
}

.faq-answer {
  overflow: hidden;
  transition: max-height 0.3s ease-in-out;
}

.answer-content {
  padding-bottom: 1.5rem;
  color: var(--color-text-mute);
  line-height: 1.6;
}

/* Responsive Design */
@media (max-width: 960px) {
  .hero-content {
    grid-template-columns: 1fr;
    text-align: center;
    gap: 3rem;
  }

  .hero-actions {
    justify-content: center;
  }

  .hero-stats {
    justify-content: center;
  }

  .hero-visual {
    height: 300px;
  }

  .workflow-steps {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 640px) {
  .hero-title {
    font-size: 2.5rem;
  }

  .section-header h2 {
    font-size: 1.75rem;
  }
}
</style>

