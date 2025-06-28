<script setup>
import { ref } from 'vue';
import axios from 'axios';

// --- 定义组件所需的状态变量 ---

// 存储用户选择的文件
const selectedFile = ref(null);
// 存储用户输入的手机号
const phoneNumber = ref('');
// --- 用这些独立的ref替换掉specificationsText ---
const paperSize = ref('A4');
const color = ref('黑白');
const sided = ref('单面');
const copies = ref(1);

// 控制是否显示加载提示
const isLoading = ref(false);
// 向用户显示操作结果的消息
const userMessage = ref('');

// --- 定义组件需要的方法 ---

// 当用户选择了文件后，这个方法会被调用
function handleFileChange(event) {
  selectedFile.value = event.target.files[0];
  userMessage.value = ''; // 清空之前的消息
}

// 点击“提交订单”按钮后，执行此核心方法
async function submitOrder() {
  // 1. 检查用户是否已选择文件
  if (!selectedFile.value) {
    userMessage.value = '错误：请先选择一个要打印的文件。';
    return;
  }
  if (!phoneNumber.value) {
    userMessage.value = '错误：请输入您的手机号。';
    return;
  }

  isLoading.value = true;
  userMessage.value = '正在上传文件，请稍候...';

  try {
    // 2. 第一步：上传文件
    const formData = new FormData();
    formData.append('file', selectedFile.value);

    const fileUploadResponse = await axios.post('/api/files/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    const fileId = fileUploadResponse.data.id;
    userMessage.value = `文件上传成功 (ID: ${fileId})！正在创建订单...`;

     // 用新的方式组装打印规格对象
    const specifications = {
        paper_size: paperSize.value,
        color: color.value,
        sided: sided.value,
        copies: copies.value
    };

    const orderData = {
        phone_number: phoneNumber.value,
        specifications: specifications, // 使用我们刚刚组装的对象
        file_ids: [fileId],
    };

    const orderCreateResponse = await axios.post('/api/orders/', orderData);

    // 4. 显示成功结果
    const newOrderNumber = orderCreateResponse.data.order_number;
    userMessage.value = `订单创建成功！您的订单号是：${newOrderNumber}，请妥善保存以便查询。`;

  } catch (error) {
    console.error('订单提交失败:', error);
    userMessage.value = '订单提交失败，请检查网络或联系管理员。';
  } finally {
    isLoading.value = false; // 无论成功失败，都结束加载状态
  }
}
</script>

<template>
  <div class="order-form-container">
    <h1>自助打印下单</h1>

    <div class="form-group">
      <label for="file-upload">第一步：上传打印文档</label>
      <input id="file-upload" type="file" @change="handleFileChange" />
    </div>

    <div class="form-group">
      <label for="phone-number">第二步：输入您的手机号</label>
      <input id="phone-number" type="tel" v-model="phoneNumber" placeholder="用于查询订单" />
    </div>

    <div class="form-group">
      <label>第三步：设置打印规格</label>
      <div class="spec-grid">
        <div>
          <label for="paper-size">纸张大小:</label>
          <select id="paper-size" v-model="paperSize">
            <option value="A4">A4</option>
            <option value="A3">A3</option>
            <option value="B5">B5</option>
          </select>
        </div>
        <div>
          <label for="color">色彩:</label>
          <select id="color" v-model="color">
            <option value="黑白">黑白</option>
            <option value="彩色">彩色</option>
          </select>
        </div>
        <div>
          <label>单/双面:</label>
          <input type="radio" id="single-sided" value="单面" v-model="sided">
          <label for="single-sided">单面</label>
          <input type="radio" id="double-sided" value="双面" v-model="sided">
          <label for="double-sided">双面</label>
        </div>
        <div>
          <label for="copies">打印份数:</label>
          <input id="copies" type="number" v-model="copies" min="1" />
        </div>
      </div>
    </div>

    <button @click="submitOrder" :disabled="isLoading">
      {{ isLoading ? '正在处理中...' : '提交订单' }}
    </button>

    <div v-if="userMessage" class="message">
      <p>{{ userMessage }}</p>
    </div>
  </div>
</template>

<style scoped>
.order-form-container {
  max-width: 600px;
  margin: 2rem auto;
  padding: 2rem;
  border: 1px solid #ccc;
  border-radius: 8px;
}
.form-group {
  margin-bottom: 1.5rem;
}
label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: bold;
}
input, textarea {
  width: 100%;
  padding: 0.5rem;
  font-size: 1rem;
  box-sizing: border-box;
}
button {
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
  cursor: pointer;
}
button:disabled {
  cursor: not-allowed;
  opacity: 0.6;
}
.message {
  margin-top: 1.5rem;
  padding: 1rem;
  border: 1px solid #ddd;
  background-color: #f4f4f4;
}
</style>
