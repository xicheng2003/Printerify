<template>
  <div class="home-view container">
    <section class="hero-section">
      <h2>简单，快速，可靠</h2>
      <p>Printerify，为每一次打印赋能。</p>
    </section>

    <section class="process-section">
      <div class="process-card">
        <Stepper :current-step="state.step" />

        <div class="step-content">
          <div v-if="state.step === 1">
            <h3 class="step-title">第一步：上传您的文档</h3>

            <!-- *** THE FIX IS HERE: Added upload notice section *** -->
            <div class="upload-notice">
              <p><strong>上传须知</strong></p>
              <ul>
                <li><strong>格式推荐</strong>: 为确保打印效果与排版格式一致，强烈建议您上传 <strong>PDF</strong> 格式的文档。</li>
                <li><strong>隐私安全</strong>: 我们非常重视您的隐私。所有文件将通过加密通道上传，并存储在专用服务器上。打印完成后，您的文件将被<strong>立即销毁</strong>，绝不外泄。</li>
                <li><strong>合规声明</strong>: 请遵守相关法律法规，<strong>严禁上传</strong>任何涉密、涉政及其他违禁内容的文件。</li>
              </ul>
            </div>

            <FileUploader ref="fileUploaderRef" @upload-success="onFileUploadSuccess" />
          </div>

          <div v-if="state.step === 2">
            <h3 class="step-title">第二步：设置打印选项</h3>
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
                  <option>单双（即首页封面为单面打印，其余内容双面打印）</option>
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

            <div class="pricing-rules">
              <p><strong>计费规则说明</strong></p>
              <ul>
                <li>打印费用: 单面打印 0.15元/页，双面打印 0.30元/页 (即每面0.15元)。</li>
                <li>装订服务: 若选择装订，将额外收取 0.10元/本。</li>
                <li>基础服务费: 每笔订单将收取 0.50元 的基础服务费。</li>
              </ul>
            </div>

            <BaseButton @click="handlePriceQuote" :loading="state.isLoading" class="full-width-btn">计算价格</BaseButton>
          </div>

          <div v-if="state.step === 3">
            <h3 class="step-title">第三步：确认价格并支付</h3>
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
            <BaseButton @click="handleCreateOrder" :loading="state.isLoading" :disabled="!state.screenshotId" class="full-width-btn">
              我已支付，确认下单
            </BaseButton>
          </div>

          <div v-if="state.step === 4" class="completion-view">
            <svg xmlns="http://www.w3.org/2000/svg" width="60" height="60" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
            <h3 class="step-title">订单提交成功！</h3>
            <p>取件时请出示取件码，请牢记或截图保存。</p>
            <p>凭手机号和取件码，可在订单查询页面查询订单状态</p>
            <div class="pickup-code-wrapper">
              <span class="pickup-code-label">您的取件码</span>
              <strong class="pickup-code">{{ state.finalOrder.pickup_code }}</strong>
            </div>
            <p class="order-number-info">完整订单号: {{ state.finalOrder.order_number }}</p>
            <BaseButton @click="reset" class="full-width-btn">再来一单</BaseButton>
          </div>
        </div>

        <p v-if="state.errorMessage" class="error-message">{{ state.errorMessage }}</p>
      </div>
    </section>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue';
import api from '@/services/apiService';

// 导入所有需要的子组件
import Stepper from '@/components/Stepper.vue';
import FileUploader from '@/components/FileUploader.vue';
import PaymentUploader from '@/components/PaymentUploader.vue';
import BaseButton from '@/components/BaseButton.vue';

const fileUploaderRef = ref(null);

const state = reactive({
  step: 1,
  file: null,
  fileId: null,
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

function onFileUploadSuccess(payload) {
  state.file = payload.file;
  state.fileId = payload.id;
  state.step = 2;
}

function onScreenshotUploaded(uploadedId) {
  state.screenshotId = uploadedId;
}

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
    state.finalOrder = response.data;
    state.step = 4;
  } catch (error) {
    state.errorMessage = '订单创建失败！';
    console.error(error);
  } finally {
    state.isLoading = false;
  }
}

function reset() {
  Object.assign(state, {
    step: 1, file: null, fileId: null, priceQuote: null, finalOrder: null,
    phoneNumber: '', screenshotId: null, errorMessage: '',
    options: { paper_size: 'A4', color: '黑白', sided: '单面', copies: 1, binding_method: '无装订', binding_detail: '' }
  });
  if (fileUploaderRef.value) {
    fileUploaderRef.value.reset();
  }
}
</script>

<style scoped>
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem; /* Add horizontal padding for mobile */
}
.hero-section { text-align: center; padding: 2rem 0; margin-bottom: 2rem; }
.hero-section h2 { font-size: 2.5rem; font-weight: 700; color: #1e293b; }
.hero-section p { font-size: 1.125rem; color: #64748b; }
.process-section { padding-bottom: 2rem; }
.process-card {
  background-color: #ffffff;
  border-radius: 16px;
  padding: 1.5rem 2.5rem;
  max-width: 800px;
  margin: 0 auto;
  box-shadow: 0 10px 15px -3px rgba(0,0,0,.1), 0 4px 6px -4px rgba(0,0,0,.1);
  border: 1px solid #e2e8f0;
}
.step-title { font-size: 1.5rem; font-weight: 600; text-align: center; margin-bottom: 2rem; color: var(--text-dark); }
.options-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}
.options-grid div { display: flex; flex-direction: column; }
.options-grid label { margin-bottom: 0.5rem; font-weight: 500; color: var(--text-dark); }
.price-result { background: #f0f4ff; border: 1px solid #c7d2fe; padding: 1rem; border-radius: 8px; margin-bottom: 1.5rem; text-align: center; }
.price { font-size: 1.75rem; color: var(--primary-color); font-weight: 700; }
.payment-section { border-top: 1px solid var(--border-color); padding: 1.5rem 0; margin-top: 1.5rem; text-align: center; }
.payment-instruction { margin-top: 0; color: #334155; }
.qr-code { max-width: 180px; margin: 1rem auto; display: block; border-radius: 8px; }
.form-group {
  margin-top: 1.5rem;
  margin-bottom: 1.5rem;
}
.form-group label { margin-bottom: 0.5rem; font-weight: 500; }
.full-width-btn { width: 100%; padding: 0.875rem; font-size: 1.1rem; }
.completion-view { text-align: center; padding: 2rem 0; }
.completion-view > p {
  color: #64748b;
  margin-bottom: 1rem;
}
.pickup-code-wrapper { background-color: #f0f4ff; border: 1px dashed var(--primary-color); padding: 1rem; border-radius: 8px; margin: 1.5rem auto; max-width: 300px; }
.pickup-code-label { font-size: 1rem; color: #475569; }
.pickup-code { display: block; font-size: 2.5rem; font-weight: 700; color: var(--primary-color); letter-spacing: 4px; margin-top: 0.5rem; }
.error-message { color: #ef4444; font-weight: 500; margin-top: 1.5rem; text-align: center; background-color: rgba(239, 68, 68, 0.1); padding: 0.75rem; border-radius: 8px;}
.order-number-info {
  color: #94a3b8;
  font-size: 0.875rem;
  margin-top: -0.5rem;
  margin-bottom: 2rem;
}
.pricing-rules, .upload-notice {
  background-color: #f8f9fa;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  padding: 1rem 1.5rem;
  margin-bottom: 2rem;
  font-size: 0.9rem;
  color: #495057;
}
.pricing-rules p, .upload-notice p {
  margin: 0 0 0.75rem 0;
  font-weight: 600;
  color: var(--text-dark);
}
.pricing-rules ul, .upload-notice ul {
  list-style-type: none;
  padding-left: 0;
}
.pricing-rules li, .upload-notice li {
  margin-bottom: 0.5rem;
  position: relative;
  padding-left: 1.25rem;
}
.pricing-rules li::before, .upload-notice li::before {
  content: '•';
  color: var(--primary-color);
  font-weight: bold;
  display: inline-block;
  position: absolute;
  left: 0;
  top: 0;
}
.pricing-rules li:last-child, .upload-notice li:last-child {
  margin-bottom: 0;
}
.upload-notice li strong {
  color: #c2410c; /* A warm orange color for emphasis */
}

@media (max-width: 767px) {
  .hero-section h2 {
    font-size: 2rem;
  }
  .hero-section p {
    font-size: 1rem;
  }
  .step-title {
    font-size: 1.25rem;
  }
  .process-card {
    padding: 1.5rem 1rem;
  }
  .options-grid {
    grid-template-columns: 1fr;
  }
  .pickup-code {
    font-size: 2rem;
  }
}
</style>
