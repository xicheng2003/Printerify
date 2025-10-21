<template>
  <div class="terms-page">

    <!-- ========== UPDATED SECTION START ========== -->
    <h1>关于 Printerify</h1>
    <div class="about-section">
      <p><strong>Printerify，为每一次打印赋能</strong>。</p>
      <p>Printerify 是一个为您提供简单、快速、可靠在线打印服务的平台。我们相信，用户的每一次打印都承载着独特的价值与期待。因此，Printerify 致力于通过现代化的技术与人性化的设计，简化繁琐的打印流程，让每位用户都能轻松、安心地将数字想法转化为高质量的实体文本，为您的学习、工作与生活提供坚实助力。</p>
      <h3>项目信息</h3>
      <p>本项目是一个开源项目，我们欢迎所有感兴趣的开发者参与贡献或提出宝贵建议。您可以通过以下链接访问我们的项目仓库。</p>
      <p>
        <strong>项目地址:</strong> <a href="https://github.com/xicheng2003/printerify" target="_blank" rel="noopener noreferrer">github.com/xicheng2003/printerify</a><br>
        <strong>主要开发者:</strong> xicheng2003
      </p>
    </div>
    <!-- ========== UPDATED SECTION END ========== -->

    <hr />

    <h2>服务条款 (Terms of Service)</h2>
      <LegalDocument type="terms" mode="full" />

    <hr />

    <h2>隐私协议 (Privacy Policy)</h2>
      <LegalDocument type="privacy" mode="full" />
  </div>
</template>

<script setup>
import LegalDocument from '@/components/legal/LegalDocument.vue'
</script>
<style scoped>
/*
  TermsView.vue 的样式已更新，使用 CSS 变量以支持主题切换。
  所有布局、尺寸和响应式逻辑均已完整保留。
*/
.terms-page {
  padding: 2rem 3rem;
  max-width: 800px;
  margin: 2rem auto;
  background-color: var(--color-background-soft); /* 已修改 */
  border-radius: 8px;
  box-shadow: var(--shadow-card); /* 已修改 */
  border: 1px solid var(--color-border); /* 已修改 */
}

.about-section,
.terms-content {
  text-align: justify;
  line-height: 1.8;
  color: var(--color-text); /* 已修改 */
}

.about-section h3,
.terms-content h3 {
  font-size: 1.25rem;
  color: var(--color-heading); /* 已修改 */
  margin-top: 2rem;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid var(--color-border); /* 已修改 */
}

.about-section p,
.terms-content p {
  margin-bottom: 1rem;
}

.about-section a {
  color: var(--color-primary); /* 已修改 */
  text-decoration: none;
  font-weight: 500;
}

.about-section a:hover {
  text-decoration: underline;
}

h1,
h2 {
  text-align: center;
  color: var(--color-heading); /* 已修改 */
}

h1 {
  font-size: 2rem;
  margin-bottom: 1.5rem;
}

h2 {
  font-size: 1.5rem;
  margin-top: 2.5rem;
}

hr {
  margin: 2.5rem 0;
  border: 0;
  border-top: 1px solid var(--color-border); /* 已修改 */
}

@media (max-width: 767px) {
  .terms-page {
    padding: 1.5rem 1rem;
    margin: 1rem auto;
  }
  h1 {
    font-size: 1.5rem;
  }
  h2 {
    font-size: 1.25rem;
  }
  .about-section h3,
  .terms-content h3 {
    font-size: 1.1rem;
  }
  .about-section,
  .terms-content {
    line-height: 1.7;
    font-size: 0.9rem;
  }
}
</style>
