<template>
  <div class="order-form">
    <form @submit.prevent="createOrder" class="form-grid">

      <div class="form-group full-width">
        <label for="phone_number">手机号码 (用于查询订单)</label>
        <input type="text" id="phone_number" v-model="orderDetails.phone_number" placeholder="请输入您的手机号码" required>
      </div>

      <div class="form-group">
        <label for="copies">打印份数</label>
        <input type="number" id="copies" v-model.number="orderDetails.copies" min="1" required>
      </div>

      <div class="form-group">
        <label for="color">色彩</label>
        <select id="color" v-model="orderDetails.color" required>
          <option value="false">黑白打印</option>
          <option value="true">彩色打印</option>
        </select>
      </div>

      <div class="form-group">
        <label for="double_sided">单/双面</label>
        <select id="double_sided" v-model="orderDetails.double_sided" required>
          <option value="false">单面打印</option>
          <option value="true">双面打印</option>
        </select>
      </div>

      <div class="form-group full-width">
        <button type="submit" :disabled="isSubmitting" class="submit-button">
          {{ isSubmitting ? '正在创建订单...' : '提交订单并获取付款码' }}
        </button>
      </div>

    </form>
    <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import apiService from '../services/apiService';

const props = defineProps({
  fileId: {
    type: [String, Number],
    required: true
  }
});

const emit = defineEmits(['order-created']);

const orderDetails = ref({
  phone_number: '',
  copies: 1,
  color: 'false', // 默认为黑白
  double_sided: 'false' // 默认为单面
});
const isSubmitting = ref(false);
const errorMessage = ref('');

async function createOrder() {
  isSubmitting.value = true;
  errorMessage.value = '';
  try {
    const orderData = {
      ...orderDetails.value,
      // 将字符串 'true'/'false' 转换为布尔值以适配后端
      color: orderDetails.value.color === 'true',
      double_sided: orderDetails.value.double_sided === 'true',
      print_files: [props.fileId]
    };
    const response = await apiService.createOrder(orderData);

    emit('order-created', response.data);

  } catch (error) {
    errorMessage.value = '订单创建失败，请检查您的输入。';
    console.error('Order creation failed:', error);
  } finally {
    isSubmitting.value = false;
  }
}
</script>

<style scoped>
.order-form {
  margin-top: 2rem;
  border-top: 1px solid var(--border-color);
  padding-top: 2rem;
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group.full-width {
  grid-column: 1 / -1;
}

.form-group label {
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: var(--text-dark);
}

.submit-button {
  width: 100%;
  padding: 0.875rem;
  font-size: 1.1rem;
}

.error-message {
  margin-top: 1rem;
  color: #ef4444;
  text-align: center;
  background-color: rgba(239, 68, 68, 0.1);
  padding: 0.75rem;
  border-radius: 8px;
}
</style>
