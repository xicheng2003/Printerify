<script setup>
import { reactive, ref } from 'vue';
import api from '@/services/apiService';

// 导入所有需要的子组件
import FileUploader from '@/components/FileUploader.vue';
import PaymentUploader from '@/components/PaymentUploader.vue';
import BaseButton from '@/components/BaseButton.vue';

// --- 为FileUploader创建一个引用 ---
const fileUploaderRef = ref(null);

// 使用一个统一的reactive对象来管理整个页面的状态
const state = reactive({
  step: 1, // 1: 选择文件, 2: 设置规格, 3: 显示价格, 4: 完成
  file: null, // 存储文件对象
  fileId: null, // 存储上传成功后返回的文件ID
  options: {
    paper_size: 'A4',
    color: '黑白',
    sided: '单面',
    copies: 1,
    binding_method: '无装订',
    binding_detail: '',
  },
  phoneNumber: '',
  priceQuote: null,
  screenshotId: null,
  finalOrder: null,
  isLoading: false,
  errorMessage: '',
});

/**
 * 当文件上传成功后，由FileUploader组件触发此方法
 * @param {object} payload - 包含 { id, file } 的对象
 */
function onFileUploadSuccess(payload) {
  state.file = payload.file;
  state.fileId = payload.id;
  state.step = 2;
}

/**
 * 当付款截图上传成功后，由PaymentUploader组件触发
 * @param {number} uploadedId - 截图文件的ID
 */
function onScreenshotUploaded(uploadedId) {
  state.screenshotId = uploadedId;
}

/**
 * 点击“计算价格”按钮
 */
async function handlePriceQuote() {
  if (state.options.binding_method === '订书钉装订' && !state.options.binding_detail) {
    state.options.binding_detail = '左上角装订';
  }
  if (state.options.binding_method === '无装订') {
    state.options.binding_detail = '';
  }

  state.isLoading = true;
  state.errorMessage = '';
  try {
    const response = await api.getPriceQuote(state.file, state.options);
    state.priceQuote = response.data;
    state.step = 3;
  } catch (error) {
    state.errorMessage = '计价失败，请稍后重试。';
    console.error(error);
  } finally {
    state.isLoading = false;
  }
}

/**
 * 点击“确认下单”按钮
 */
async function handleCreateOrder() {
  if (!state.phoneNumber) {
    state.errorMessage = '请输入手机号！';
    return;
  }
  if (!state.screenshotId) {
    state.errorMessage = '请先上传付款截图！';
    return;
  }

  state.isLoading = true;
  state.errorMessage = '';
  try {
    const orderData = {
      phone_number: state.phoneNumber,
      specifications: state.options,
      file_ids: [state.fileId],
      payment_screenshot_id: state.screenshotId,
    };

    const response = await api.createOrder(orderData);

    // --- 调试步骤：在控制台打印出后端返回的完整数据 ---
    console.log("订单创建成功，后端返回的数据:", response.data);

    state.finalOrder = response.data;
    state.step = 4;
  } catch (error) {
    state.errorMessage = '订单创建失败！';
    console.error(error);
  } finally {
    state.isLoading = false;
  }
}

/**
 * 重置流程，再来一单
 */
function reset() {
  Object.assign(state, {
    step: 1,
    file: null,
    fileId: null,
    priceQuote: null,
    finalOrder: null,
    phoneNumber: '',
    screenshotId: null,
    errorMessage: '',
    options: {
        paper_size: 'A4',
        color: '黑白',
        sided: '单面',
        copies: 1,
        binding_method: '无装订',
        binding_detail: '',
    }
  });
  if (fileUploaderRef.value) {
    fileUploaderRef.value.reset();
  }
}
</script>

<template>
  <div class="main-container">
    <div class="card">

      <!-- 步骤一：文件上传 -->
      <section v-if="state.step >= 1">
        <h2>1. 上传您的文档</h2>
        <FileUploader ref="fileUploaderRef" @upload-success="onFileUploadSuccess" />
      </section>

      <!-- 步骤二：打印规格 -->
      <section v-if="state.step >= 2">
        <h2>2. 设置打印选项</h2>
        <div class="options-grid">
          <div>
            <label>纸张大小:</label>
            <input type="text" :value="state.options.paper_size" disabled />
          </div>
          <div>
            <label>色彩:</label>
            <input type="text" :value="state.options.color" disabled />
          </div>
          <div>
            <label>打印模式:</label>
            <select v-model="state.options.sided" :disabled="state.isLoading">
              <option>单面</option>
              <option>双面</option>
              <option>单双</option>
            </select>
          </div>
          <div>
            <label>份数:</label>
            <input type="number" v-model="state.options.copies" min="1" :disabled="state.isLoading"/>
          </div>
          <div>
            <label>装订方式:</label>
            <select v-model="state.options.binding_method" :disabled="state.isLoading">
              <option>无装订</option>
              <option>订书钉装订</option>
            </select>
          </div>
          <div v-if="state.options.binding_method === '订书钉装订'">
            <label>装订位置:</label>
            <select v-model="state.options.binding_detail" :disabled="state.isLoading">
              <option>左上角装订</option>
              <option>左侧装订</option>
            </select>
          </div>
        </div>
        <BaseButton @click="handlePriceQuote" :loading="state.isLoading">计算价格</BaseButton>
      </section>

      <!-- 步骤三：确认价格并支付 -->
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
          <input type="tel" v-model="state.phoneNumber" placeholder="用于查询订单" :disabled="state.isLoading" />
        </div>
        <BaseButton @click="handleCreateOrder" :loading="state.isLoading" :disabled="!state.screenshotId">
          我已支付，确认下单
        </BaseButton>
      </section>

      <!-- 步骤四：完成 (已修改) -->
      <section v-if="state.step === 4" class="completion-view">
        <h2>🎉 订单提交成功！</h2>
        <p class="pickup-code-label">请牢记您的取件码</p>
        <div class="pickup-code-display">
          {{ state.finalOrder.pickup_code }}
        </div>
        <p class="sub-info">您可使用“手机号”+“取件码”随时查询订单状态。</p>
        <p class="order-number-info">完整订单号为：{{ state.finalOrder.order_number }}</p>
        <BaseButton @click="reset">再下一单</BaseButton>
      </section>

      <p v-if="state.errorMessage" class="error-message">{{ state.errorMessage }}</p>

    </div>
  </div>
</template>

<style scoped>
/* 样式保持不变 */
.main-container { max-width: 768px; margin: 0 auto; }
.card { background: #fff; border-radius: 12px; padding: 2rem; box-shadow: 0 8px 32px rgba(0,0,0,0.1); }
section { border-bottom: 1px solid #eee; padding-bottom: 2rem; margin-bottom: 2rem; }
section:last-child { border-bottom: none; }
h2 { margin-top: 0; }
.options-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}
.options-grid div { display: flex; flex-direction: column; }
.options-grid label { margin-bottom: 0.5rem; font-weight: 500; color: #555; }
.options-grid input[type="text"], .options-grid input[type="number"], .options-grid select { padding: 0.75rem; border: 1px solid #ccc; border-radius: 6px; font-size: 1rem; }
.options-grid input[disabled] { background-color: #f8f9fa; cursor: not-allowed; }
.price-result { background: #f8f9fa; padding: 1rem; border-radius: 8px; margin-bottom: 1.5rem; }
.price { font-size: 1.5rem; color: #dc3545; }
.completion-view { text-align: center; }
.error-message { color: red; font-weight: bold; margin-top: 1rem; text-align: center; }
.payment-section { border-top: 1px solid #eee; padding: 1.5rem 0; margin-top: 1.5rem; text-align: center; }
.payment-instruction { margin-top: 0; color: #333; }
.qr-code { max-width: 200px; margin: 1rem auto; display: block; border: 1px solid #ddd; padding: 5px; border-radius: 8px; }
.form-group { margin-top: 1.5rem; }

/* --- 新增：完成页面的取件码样式 --- */
.pickup-code-label {
  font-size: 1.1rem;
  color: #555;
  margin-bottom: 0.5rem;
}
.pickup-code-display {
  font-size: 2.5rem;
  font-weight: 700;
  color: #fff;
  background-color: #007bff;
  padding: 1rem 2rem;
  border-radius: 8px;
  display: inline-block;
  margin-bottom: 1rem;
  letter-spacing: 2px;
}
.sub-info {
  color: #6c757d;
  font-size: 0.9rem;
}
.order-number-info {
  color: #aaa;
  font-size: 0.8rem;
  margin-bottom: 2rem;
}
</style>
