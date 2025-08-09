// frontend/src/services/apiService.js
import axios from 'axios';

// --- 新增的配置 ---
// 这两行代码会告诉axios自动处理Django的CSRF令牌
axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.withCredentials = true; // 允许跨域请求携带cookie

// 创建一个axios实例，可以进行统一的配置
const apiClient = axios.create({
  baseURL: '/', // 因为我们使用Vite代理，所以这里写根路径即可
});

// 添加请求拦截器来自动添加认证token
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Token ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 添加响应拦截器来处理认证错误
apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response && error.response.status === 401) {
      // 认证失败，清除本地token
      localStorage.removeItem('token');
    }
    return Promise.reject(error);
  }
);

// 封装所有与后端交互的函数
export default {
  // 认证相关API
  register(userData) {
    return apiClient.post('/api/register/', userData);
  },

  login(credentials) {
    return apiClient.post('/api/login/', credentials);
  },

  logout() {
    return apiClient.post('/api/logout/');
  },

  getProfile() {
    return apiClient.get('/api/profile/');
  },

  updateProfile(updateData) {
    return apiClient.put('/api/profile/update/', updateData);
  },

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
  
  // 设置认证token
  setAuthToken(token) {
    apiClient.defaults.headers.common['Authorization'] = `Token ${token}`;
  },
  
  // 移除认证token
  removeAuthToken() {
    delete apiClient.defaults.headers.common['Authorization'];
  },
  
  // 获取当前token
  getToken() {
    return localStorage.getItem('token');
  }
};