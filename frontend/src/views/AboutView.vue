<template>
  <div class="about-container">
    <section class="hero-section">
      <h2 class="animated-hero-title">关于 Printerify</h2>
      <p>Printerify，为每一次打印赋能。</p>
    </section>
    
    <div class="about-card">
      <div class="about-content">
        <p>Printerify 是一个为您提供简单、快速、可靠在线打印服务的平台。我们相信，用户的每一次打印都承载着独特的价值与期待。因此，Printerify 致力于通过现代化的技术与人性化的设计，简化繁琐的打印流程，让每位用户都能轻松、安心地将数字想法转化为高质量的实体文本，为您的学习、工作与生活提供坚实助力。</p>
        
        <h3>我们的愿景</h3>
        <p>让打印变得简单、快捷，让每个人都能享受到高效便利的打印服务。</p>

        <h3>核心优势</h3>
        <ul>
          <li><strong>简单易用</strong> - 直观的界面设计，几步即可完成打印订单</li>
          <li><strong>快速响应</strong> - 高效的处理流程，确保您的文件及时打印</li>
          <li><strong>安全可靠</strong> - 完善的数据保护机制，保障您的文件隐私</li>
          <li><strong>灵活配置</strong> - 支持多种打印选项，满足不同需求</li>
        </ul>

        <h3>项目信息</h3>
        <p>本项目是一个开源项目，我们欢迎所有感兴趣的开发者参与贡献或提出宝贵建议。您可以通过以下链接访问我们的项目仓库。</p>
        <p>
          <strong>项目地址:</strong> <a href="https://github.com/xicheng2003/printerify" target="_blank" rel="noopener noreferrer">github.com/xicheng2003/printerify</a><br>
          <strong>主要开发者:</strong> xicheng2003
        </p>

        <h3>联系我们</h3>
        <p>如果您有任何问题、建议或合作意向，欢迎通过以下方式与我们联系：</p>
        <p>
          <strong>邮箱:</strong> <a href="mailto:xicheng.lin@foxmail.com">xicheng.lin@foxmail.com</a>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
// No additional script needed
</script>

<style scoped>
.about-container {
  font-family: 'Noto Sans SC', sans-serif;
  padding: 1rem;
  max-width: 800px;
  margin: 1rem auto;
}

.hero-section {
  text-align: center;
  padding: 2rem 0;
  margin-bottom: 2rem;
}

.hero-section h2 {
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--color-heading);
  margin-bottom: 0.5rem;
}

.hero-section p {
  font-size: 1.125rem;
  color: var(--color-text-mute);
}

/* --- Animated Title --- */
.animated-hero-title {
  --scroll-width: 400px;
  /* 请确保项目中已引入 'Inter' 字体，否则将回退至 sans-serif */
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
  background-size: var(--scroll-width) 100%;
  animation: seamless-scroll 5s linear infinite;
  text-shadow:
    0px 1px 1px rgba(255, 255, 255, 0.1),
    0 0 10px rgba(192, 219, 255, 0.2),
    0 0 30px rgba(192, 219, 255, 0.1),
    0px -1px 1px rgba(0, 0, 0, 0.4);
}

/* 亮色模式下的专属样式 */
html:not(.dark) .animated-hero-title {
  --scroll-width: 300px;
  background: linear-gradient(
    100deg,
    #333333, #aeaeae, #232323, #aeaeae, #333333
  );
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  background-repeat: repeat-x;
  background-size: var(--scroll-width) 100%;
  text-shadow:
    0px 1px 1px rgba(255, 255, 255, 0.5),
    0px -1px 1px rgba(0, 0, 0, 0.1);
}

@keyframes seamless-scroll {
  from {
    background-position: 0 0;
  }
  to {
    background-position: calc(-1 * var(--scroll-width)) 0;
  }
}

/* --- 响应式调整 --- */
@media (max-width: 767px) {
  .hero-section h2 { font-size: 2rem; }
  .hero-section p { font-size: 1rem; }
  .animated-hero-title {
    font-size: 2.6rem;
    letter-spacing: -1px;
  }
}

.about-card {
  padding: 2rem 3rem;
  background-color: var(--color-background-soft);
  border-radius: 8px;
  box-shadow: var(--shadow-card);
  border: 1px solid var(--color-border);
}

.about-content {
  text-align: justify;
  line-height: 1.8;
  color: var(--color-text);
}

.about-content h3 {
  font-size: 1.25rem;
  color: var(--color-heading);
  margin-top: 2rem;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid var(--color-border);
}

.about-content p {
  margin-bottom: 1rem;
}

.about-content ul {
  margin: 1rem 0 1.5rem 1.5rem;
  line-height: 1.8;
}

.about-content li {
  margin-bottom: 0.75rem;
}

.about-content a {
  color: var(--color-primary);
  text-decoration: none;
  font-weight: 500;
}

.about-content a:hover {
  text-decoration: underline;
}

@media (max-width: 767px) {
  .about-card {
    padding: 1.5rem 1rem;
  }
  .about-content h3 {
    font-size: 1.1rem;
  }
  .about-content {
    line-height: 1.7;
    font-size: 0.9rem;
  }
}
</style>
