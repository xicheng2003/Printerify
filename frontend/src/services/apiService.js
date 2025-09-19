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
  withCredentials: true, // 确保每个请求都携带凭据
  timeout: 10000, // 10秒超时
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
    if (error.response) {
      const { status, data } = error.response;

      switch (status) {
        case 400:
          // 处理验证错误，提供友好的中文提示
          const friendlyError = formatValidationErrors(data);
          error.friendlyMessage = friendlyError;
          console.warn('请求验证失败:', friendlyError);
          break;
        case 401:
          // 认证失败，清除本地token
          localStorage.removeItem('token');
          error.friendlyMessage = '登录已过期，请重新登录';
          window.dispatchEvent(new CustomEvent('auth:unauthorized'));
          break;
        case 403:
          error.friendlyMessage = '权限不足，无法执行此操作';
          console.warn('权限不足:', data);
          break;
        case 404:
          error.friendlyMessage = '请求的资源不存在';
          console.warn('请求的资源不存在:', data);
          break;
        case 500:
          error.friendlyMessage = '服务器内部错误，请稍后重试';
          console.error('服务器内部错误:', data);
          break;
        default:
          error.friendlyMessage = '请求失败，请稍后重试';
          console.error('请求失败:', data);
      }
    } else if (error.request) {
      // 请求已发出但没有收到响应
      error.friendlyMessage = '网络连接失败，请检查网络后重试';
      console.error('网络错误，请检查网络连接');
    } else {
      // 请求配置出错
      error.friendlyMessage = '请求配置错误，请检查输入';
      console.error('请求配置错误:', error.message);
    }
    return Promise.reject(error);
  }
);

// 格式化验证错误的函数
function formatValidationErrors(errorData) {
  if (typeof errorData === 'string') {
    return errorData;
  }

  if (typeof errorData === 'object' && errorData !== null) {
    const errorMessages = [];

    // 处理字段验证错误
    for (const [field, errors] of Object.entries(errorData)) {
      if (Array.isArray(errors)) {
        // 将字段名转换为中文
        const fieldName = getFieldDisplayName(field);
        errors.forEach(error => {
          errorMessages.push(`${fieldName}: ${error}`);
        });
      } else if (typeof errors === 'string') {
        errorMessages.push(errors);
      }
    }

    return errorMessages.length > 0 ? errorMessages.join('; ') : '输入数据验证失败';
  }

  return '请求数据格式错误';
}

// 字段名中英文映射
function getFieldDisplayName(field) {
  const fieldMap = {
    'username': '用户名',
    'email': '邮箱',
    'password': '密码',
    'password_confirm': '确认密码',
    'phone_number': '手机号',
    'first_name': '姓',
    'last_name': '名',
    'non_field_errors': '通用错误',
    'detail': '错误详情'
  };

  return fieldMap[field] || field;
}

// 初始化 CSRF token
async function initializeCSRF() {
  try {
    await apiClient.get('/api/csrf/');
  } catch (error) {
    console.warn('Failed to get CSRF token:', error);
  }
}

// 在模块加载时初始化 CSRF
initializeCSRF();

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
   * 上传打印文件
   * @param {File} file - 用户上传的文件对象
   * @param {function} onUploadProgress - Axios的进度回调函数
   * @returns {Promise}
   */
  uploadPrintFile(file, onUploadProgress) {
    const formData = new FormData();
    formData.append('file', file);

    return apiClient.post('/api/upload/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
      onUploadProgress, // 将回调函数传递给axios
    });
  },

  /**
   * 上传付款截图
   * @param {File} file - 用户上传的文件对象
   * @returns {Promise}
   */
  uploadPaymentScreenshot(file) {
    const formData = new FormData();
    formData.append('file', file);

    return apiClient.post('/api/upload-screenshot/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },

  /**
   * 获取价格估算
   * @param {File|null} file - 原始文件对象（可为null，如果使用file_path）
   * @param {object} specifications - 包含打印选项的对象
   * @returns {Promise}
   */
  getPriceQuote(file, specifications) {
    if (file) {
      // 如果提供了文件，使用FormData上传
      const formData = new FormData();
      formData.append('file', file);
      Object.keys(specifications).forEach(key => {
        formData.append(key, specifications[key]);
      });

      return apiClient.post('/api/estimate-price/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
    } else {
      // 如果没有文件，直接发送JSON数据（用于已上传的文件）
      return apiClient.post('/api/estimate-price/', specifications);
    }
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
    // 新端点要求同时提供手机号与取件码
    if (!phoneNumber || !pickupCode) {
      throw new Error('请同时提供手机号与取件码进行查询');
    }

    return apiClient.post('/api/orders/query/', {
      phone_number: phoneNumber,
      pickup_code: pickupCode,
    });
  },

  // 获取当前用户订单列表
  getUserOrders() {
    return apiClient.get('/api/orders/');
  },

  // OAuth绑定相关方法
  bindGitHubAccount() {
    return apiClient.post('/api/oauth/bindings/github/');
  },

  bindGoogleAccount() {
    return apiClient.post('/api/oauth/bindings/google/');
  },

  unbindOAuthAccount(provider) {
    return apiClient.delete(`/api/oauth/bindings/${provider}/`);
  },

  getOAuthUserInfo() {
    return apiClient.get('/api/oauth/userinfo/');
  },

  getOAuthBindings() {
    return apiClient.get('/api/oauth/bindings/');
  },

  getUserProfile() {
    return apiClient.get('/api/users/profile/');
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
  },

  // 检查token是否有效
  async validateToken() {
    try {
      const response = await this.getProfile();
      return response.status === 200;
    } catch {
      return false;
    }
  }
};
