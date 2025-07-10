// frontend/src/services/apiService.js
import axios from 'axios';

// 创建一个axios实例，可以进行统一的配置
const apiClient = axios.create({
  baseURL: '/', // 因为我们使用Vite代理，所以这里写根路径即可
});

// 封装所有与后端交互的函数
export default {
  /**
   * 上传文件（包括打印文档和付款截图），并支持进度回调
   * @param {File} file - 用户上传的文件对象
   * @param {string} purpose - 文件用途, 'PRINT' 或 'PAYMENT'
   * @param {function} onUploadProgress - Axios的进度回调函数
   * @returns {Promise}
   */
  uploadPrintFile(file, purpose, onUploadProgress) {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('purpose', purpose);

    return apiClient.post('/api/files/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
      onUploadProgress, // 将回调函数传递给axios
    });
  },

  /**
   * 获取价格估算
   * @param {File} file - 原始文件对象
   * @param {object} specifications - 包含打印选项的对象
   * @returns {Promise}
   */
  getPriceQuote(file, specifications) {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('specifications', JSON.stringify(specifications));

    return apiClient.post('/api/price-quote/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },

  /**
   * 创建最终订单
   * @param {object} orderData - 包含手机号、规格、文件ID等的订单数据
   * @returns {Promise}
   */
  createOrder(orderData) {
    return apiClient.post('/api/orders/', orderData);
  },

  /**
   * 查询订单状态
   * @param {string} phoneNumber - 手机号
   * @param {string} pickupCode - 取件码
   * @returns {Promise}
   */
  queryOrder(phoneNumber, pickupCode) {
    if (!phoneNumber && !pickupCode) {
      throw new Error('至少提供手机号或取件码进行查询');
    }

    return apiClient.get('/api/orders/', {
      params: {
        phone_number: phoneNumber,
        pickup_code: pickupCode,
      },
    });
  },
};
