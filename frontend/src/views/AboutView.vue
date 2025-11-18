<template>
  <div class="about-page">
    <h1>关于 Printerify</h1>
    <div class="about-content">
      <p><strong>Printerify，为每一次打印赋能</strong>。</p>
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
</template>

<script setup>
// No additional script needed
</script>

<style scoped>
.about-page {
  padding: 2rem 3rem;
  max-width: 800px;
  margin: 2rem auto;
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

h1 {
  text-align: center;
  color: var(--color-heading);
  font-size: 2rem;
  margin-bottom: 1.5rem;
}

@media (max-width: 767px) {
  .about-page {
    padding: 1.5rem 1rem;
    margin: 1rem auto;
  }
  h1 {
    font-size: 1.5rem;
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
