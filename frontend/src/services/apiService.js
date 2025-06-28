// frontend/src/services/apiService.js
import axios from 'axios';

// 创建一个axios实例，可以进行统一的配置，如请求头、超时等
const apiClient = axios.create({
  baseURL: '/', // 因为我们使用Vite代理，所以这里写根路径即可
});

// 封装所有与后端交互的函数
export default {
  /**
   * 获取价格报价
   * @param {File} file - 用户上传的文件对象
   * @param {object} specifications - 打印规格对象
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
   * 上传打印文件（为后续创建订单做准备）
   * @param {File} file - 用户上传的文件对象
   * @param {string} purpose - 文件用途（如打印文件或付款凭证）
   * @returns {Promise}
   */
  uploadPrintFile(file, purpose) {
    // 创建一个FormData对象来封装文件和其他数据
    const formData = new FormData();
    // 将文件和用途添加到FormData中
    formData.append('file', file);
    formData.append('purpose', purpose);
    // 发送POST请求到后端的文件上传接口
    return apiClient.post('/api/files/', formData, {
      // 设置请求头为multipart/form-data，以便后端正确解析文件上传
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
   * @param {string} orderNumber - 订单号
   * @returns {Promise}
   */
  queryOrder(phoneNumber, orderNumber) {
    return apiClient.get('/api/orders/', {
      params: {
        phone_number: phoneNumber,
        order_number: orderNumber
      },
    });
  },
};
