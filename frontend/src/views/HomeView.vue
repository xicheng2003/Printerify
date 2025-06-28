<script setup>
import { reactive } from 'vue';
import api from '@/services/apiService'; // 导入我们封装好的API服务
import PaymentUploader from '@/components/PaymentUploader.vue';
// 导入我们的新组件
import FileUploader from '@/components/FileUploader.vue';
import BaseButton from '@/components/BaseButton.vue';
// (您还可以按照这个思路创建PrintOptions.vue, PriceResult.vue等更多组件)

// 使用一个reactive对象来管理整个页面的状态
const state = reactive({
  step: 1, // 1: 选择文件, 2: 设置规格, 3: 显示价格, 4: 完成
  file: null,
  options: {
    paper_size: 'A4',
    color: '黑白',
    sided: '单面',
    copies: 1,
  },
  phoneNumber: '',
  priceQuote: null, // 存储报价结果 { pages, price }
   screenshotId: null, // 存储截图ID
  finalOrder: null, // 存储最终订单结果
  isLoading: false, // 控制加载状态
  errorMessage: '',
});

// 当FileUploader组件选择了文件后，此方法被调用
function onFileSelected(selectedFile) {
  state.file = selectedFile;
  state.step = 2; // 进入下一步
}

// 新增一个方法来处理截图上传成功事件
function onScreenshotUploaded(uploadedId) {
  state.screenshotId = uploadedId;
}

// 点击“计算价格”按钮
async function handlePriceQuote() {
  state.isLoading = true;
  state.errorMessage = '';
  try {
    const response = await api.getPriceQuote(state.file, state.options);
    state.priceQuote = response.data;
    state.step = 3; // 进入下一步
  } catch (error) {
    state.errorMessage = '计价失败，请稍后重试。';
    console.error(error);
  } finally {
    state.isLoading = false;
  }
}

// 点击“确认下单”按钮
async function handleCreateOrder() {
  // ... 检查手机号的逻辑 ...
  if (!state.screenshotId) { // <--- 新增检查
      state.errorMessage = '请先上传付款截图！';
      return;
  }

  state.isLoading = true;
  state.errorMessage = '';
  try {
    const fileUploadResponse = await api.uploadPrintFile(state.file, 'PRINT');
    const fileId = fileUploadResponse.data.id;

    const orderData = {
      phone_number: state.phoneNumber,
      specifications: state.options,
      file_ids: [fileId],
      payment_screenshot_id: state.screenshotId, // <--- 关键！传递截图ID
    };

    const response = await api.createOrder(orderData);
    state.finalOrder = response.data;
    state.step = 4;
  } catch (error) {
    state.errorMessage = '订单创建失败！';
    console.error(error);
  } finally {
    state.isLoading = false;
  }
}

// 重置流程，再来一单
function reset() {
  Object.assign(state, {
    step: 1, file: null, priceQuote: null, finalOrder: null, phoneNumber: '', errorMessage: ''
  });
}
</script>

<template>
  <div class="main-container">
    <div class="card">

      <section v-if="state.step >= 1">
        <h2>1. 上传您的文档</h2>
        <FileUploader @file-selected="onFileSelected" />
      </section>

      <section v-if="state.step >= 2">
        <h2>2. 设置打印选项</h2>
        <div class="options-grid">
          <div>
            <label>纸张大小:</label>
            <select v-model="state.options.paper_size">
              <option>A4</option><option>A3</option><option>B5</option>
            </select>
          </div>
          <div>
            <label>色彩:</label>
            <select v-model="state.options.color">
              <option>黑白</option><option>彩色</option>
            </select>
          </div>
          <div>
            <label>份数:</label>
            <input type="number" v-model="state.options.copies" min="1"/>
          </div>
        </div>
        <BaseButton @click="handlePriceQuote" :loading="state.isLoading">计算价格</BaseButton>
      </section>

      <section v-if="state.step >= 3">
        <h2>3. 确认价格并支付</h2>
        <div class="price-result" v-if="state.priceQuote">
          <p>预估页数: <strong>{{ state.priceQuote.estimated_pages }}</strong> 页</p>
          <p class="price">预估价格: <strong>¥ {{ state.priceQuote.estimated_price.toFixed(2) }}</strong></p>
        </div>

        <div class="payment-section">
            <p class="payment-instruction">请扫描下方二维码完成支付，并将支付成功页面截图后上传。</p>
            <img src="/qr-code.jpg" alt="收款二维码" class="qr-code">

            <PaymentUploader @upload-success="onScreenshotUploaded" />
        </div>
        <div class="form-group">
          <label>请输入手机号以完成下单：</label>
          <input type="tel" v-model="state.phoneNumber" placeholder="用于查询订单" />
        </div>

        <BaseButton
          @click="handleCreateOrder"
          :loading="state.isLoading"
          :disabled="!state.screenshotId"
        >
          我已支付，确认下单
        </BaseButton>
        </section>

      <section v-if="state.step === 4" class="completion-view">
        <h2>🎉 订单提交成功！</h2>
        <p>您的订单号为：<strong>{{ state.finalOrder.order_number }}</strong></p>
        <p>请妥善保管，用于查询订单状态。</p>
        <BaseButton @click="reset">再下一单</BaseButton>
      </section>

      <p v-if="state.errorMessage" class="error-message">{{ state.errorMessage }}</p>

    </div>
    </div>
</template>

<style scoped>
.main-container { max-width: 768px; margin: 0 auto; /* HomeView独有，所以保留 */ }
.card { background: #fff; border-radius: 12px; padding: 2rem; box-shadow: 0 8px 32px rgba(0,0,0,0.1); }
section { border-bottom: 1px solid #eee; padding-bottom: 2rem; margin-bottom: 2rem; }
section:last-child { border-bottom: none; }
h2 { margin-top: 0; }
.options-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-bottom: 1.5rem; }
.price-result { background: #f8f9fa; padding: 1rem; border-radius: 8px; margin-bottom: 1.5rem; }
.price { font-size: 1.5rem; color: #dc3545; }
.completion-view { text-align: center; }
.error-message { color: red; font-weight: bold; }

/* payment-section 和 qr-code 样式 */
.payment-section {
  border-top: 1px solid #eee;
  padding: 1.5rem 0;
  margin-top: 1.5rem;
  text-align: center;
}
.payment-instruction {
  margin-top: 0;
  color: #333;
}
.qr-code {
  max-width: 200px;
  margin: 1rem auto;
  display: block;
  border: 1px solid #ddd;
  padding: 5px;
  border-radius: 8px;
}
.form-group {
  margin-top: 1.5rem;
}
</style>
