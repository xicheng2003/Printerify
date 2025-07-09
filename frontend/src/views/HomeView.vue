<template>
  <div class="home-view container">
    <!-- Section 1: Hero -->
    <section class="hero-section">
      <h2>简单三步，轻松完成打印</h2>
      <p>高效、便捷的自助打印服务，为您节省宝贵时间。</p>
    </section>

    <!-- Section 2: How it works -->
    <section class="how-it-works">
      <div class="step-card">
        <div class="step-icon">1</div>
        <h3>上传文件</h3>
        <p>点击下方区域，选择您需要打印的文档或PDF文件。</p>
      </div>
      <div class="step-card">
        <div class="step-icon">2</div>
        <h3>提交订单</h3>
        <p>设置打印选项，填写必要信息后提交您的打印订单。</p>
      </div>
      <div class="step-card">
        <div class="step-icon">3</div>
        <h3>上门取件</h3>
        <p>订单完成后，凭生成的取件码即可上门取件。</p>
      </div>
    </section>

    <!-- Section 3: Uploader and Form -->
    <section class="upload-section">
      <div class="upload-card">
        <FileUploader @file-uploaded="handleFileUploaded" />
        <OrderForm v-if="uploadedFileId" :file-id="uploadedFileId" />
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import FileUploader from '../components/FileUploader.vue';
import OrderForm from '../components/OrderForm.vue';

const uploadedFileId = ref(null);

function handleFileUploaded(fileId) {
  uploadedFileId.value = fileId;
}
</script>

<style scoped>
.container {
  width: 90%;
  max-width: 1200px;
  margin: 0 auto;
}

.hero-section {
  text-align: center;
  padding: 2rem 0;
  margin-bottom: 2rem;
}

.hero-section h2 {
  font-size: 2.5rem;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 0.5rem;
}

.hero-section p {
  font-size: 1.125rem;
  color: #64748b;
  max-width: 600px;
  margin: 0 auto;
}

.how-it-works {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
  margin-bottom: 3rem;
}

.step-card {
  background-color: #ffffff;
  border-radius: 12px;
  padding: 2rem;
  text-align: center;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  border: 1px solid #e2e8f0;
}

.step-icon {
  width: 50px;
  height: 50px;
  background-color: #e0e7ff;
  color: #3730a3;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  font-weight: 700;
  margin: 0 auto 1.5rem;
}

.step-card h3 {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #334155;
}

.step-card p {
  color: #64748b;
  line-height: 1.6;
}

.upload-section {
  padding-bottom: 2rem;
}

.upload-card {
  background-color: #ffffff;
  border-radius: 16px;
  padding: 2rem;
  max-width: 800px;
  margin: 0 auto;
  box-shadow: 0 10px 15px -3px rgba(0,0,0,.1), 0 4px 6px -4px rgba(0,0,0,.1);
  border: 1px solid #e2e8f0;
}
</style>
