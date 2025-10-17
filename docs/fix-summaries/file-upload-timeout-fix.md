# 文件上传超时问题修复总结

## 问题描述
用户在上传大文件时遇到超时错误，导致上传失败。

## 根本原因分析

经过全面审查前后端代码，发现以下几个关键问题：

### 1. **前端 API 客户端超时设置过短** ⚠️ 主要问题
- **位置**: `frontend/src/services/apiService.js`
- **问题**: axios 实例的默认超时时间仅为 **10秒**
- **影响**: 大文件上传如果超过 10 秒会被强制中断

### 2. **Vite 开发服务器代理无超时配置**
- **位置**: `frontend/vite.config.js`
- **问题**: 代理配置未明确设置超时参数
- **影响**: 使用默认超时（通常 30 秒），对于大文件仍可能不够

### 3. **Django 后端缺少文件大小限制配置**
- **位置**: `backend/settings.py`
- **问题**: 未配置 `DATA_UPLOAD_MAX_MEMORY_SIZE` 和 `FILE_UPLOAD_MAX_MEMORY_SIZE`
- **影响**: 使用 Django 默认值（2.5MB），超过此大小会触发临时文件存储，可能影响性能

### 4. **错误提示不够友好**
- **位置**: 多处
- **问题**: 超时错误未被特殊处理，用户只看到通用错误信息
- **影响**: 用户不清楚问题原因，无法采取相应措施

## 修复方案

### ✅ 修复 1: 增加前端 API 超时时间

**文件**: `frontend/src/services/apiService.js`

```javascript
// 修改前
const apiClient = axios.create({
  baseURL: '/',
  withCredentials: true,
  timeout: 10000, // 10秒超时
});

// 修改后
const apiClient = axios.create({
  baseURL: '/',
  withCredentials: true,
  timeout: 120000, // 120秒（2分钟）超时 - 适合大文件上传
});
```

**说明**: 将全局超时从 10 秒增加到 2 分钟，为大文件上传提供足够时间。

---

### ✅ 修复 2: 为文件上传单独设置更长超时

**文件**: `frontend/src/services/apiService.js`

```javascript
uploadPrintFile(file, onUploadProgress) {
  const formData = new FormData();
  formData.append('file', file);

  return apiClient.post('/api/upload/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
    onUploadProgress,
    timeout: 300000, // 上传文件专用超时：5分钟
  });
},
```

**说明**: 为文件上传专门设置 5 分钟超时，覆盖全局配置。

---

### ✅ 修复 3: 配置 Vite 代理超时

**文件**: `frontend/vite.config.js`

```javascript
server: {
  port: 5173,
  proxy: {
    '/api': {
      target: 'http://127.0.0.1:8000',
      changeOrigin: true,
      secure: false,
      timeout: 300000, // 5分钟超时，适合大文件上传
      proxyTimeout: 300000
    }
  }
}
```

**说明**: 确保 Vite 开发服务器的代理不会提前终止长时间的上传请求。

---

### ✅ 修复 4: 配置 Django 文件上传大小限制

**文件**: `backend/settings.py`

```python
# File upload settings
# 允许上传最大100MB的文件（适合大文档）
DATA_UPLOAD_MAX_MEMORY_SIZE = 104857600  # 100 MB in bytes
FILE_UPLOAD_MAX_MEMORY_SIZE = 104857600  # 100 MB in bytes
```

**说明**: 
- 明确设置文件上传大小限制为 100MB
- 超过此限制会返回 413 错误，前端可以友好提示

---

### ✅ 修复 5: 改进超时错误处理

**文件**: `frontend/src/services/apiService.js`

在响应拦截器中添加超时错误检测：

```javascript
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    // 检查是否是超时错误
    if (error.code === 'ECONNABORTED' || error.message.includes('timeout')) {
      error.friendlyMessage = '上传超时，请检查文件大小或网络连接。建议：文件大小不超过50MB';
      console.error('请求超时:', error.message);
      return Promise.reject(error);
    }
    
    if (error.response) {
      const { status, data } = error.response;
      switch (status) {
        // ... 其他错误处理
        case 413:
          error.friendlyMessage = '文件过大，请上传小于100MB的文件';
          console.error('文件过大:', data);
          break;
        // ...
      }
    }
    // ...
  }
);
```

**说明**: 
- 特别处理 `ECONNABORTED` 和包含 "timeout" 的错误
- 为 413 状态码（文件过大）添加友好提示

---

### ✅ 修复 6: 改进 Store 层错误提示

**文件**: `frontend/src/stores/order.js`

```javascript
async function _uploadFile(docId) {
  const doc = findDocumentById(docId);
  if (!doc) return;

  try {
    const response = await apiService.uploadPrintFile(doc.fileObject, (progressEvent) => {
      if (progressEvent.total) {
        doc.uploadProgress = Math.round((progressEvent.loaded * 100) / progressEvent.total);
      }
    });
    doc.uploadProgress = 100;
    doc.serverId = response.data.file_id;
    await _fetchPriceForDocument(docId);
  } catch (error) {
    console.error('File upload error:', error);
    // 使用友好的错误提示
    if (error.friendlyMessage) {
      doc.error = error.friendlyMessage;
    } else if (error.code === 'ECONNABORTED' || error.message?.includes('timeout')) {
      doc.error = '上传超时，文件可能过大';
    } else {
      doc.error = '上传失败，请重试';
    }
  } finally {
    doc.isUploading = false;
  }
}
```

**说明**: 将 API Service 中的友好错误信息传递给文档对象，用户可在界面上看到具体原因。

---

### ✅ 修复 7: 添加用户提示

**文件**: `frontend/src/views/HomeView.vue`

在上传须知中添加文件大小提示：

```vue
<div class="upload-notice" v-if="orderStore.groups.length === 0">
  <p><strong>上传须知</strong></p>
  <ul>
    <li><strong>格式推荐</strong>: 为确保打印效果与排版格式一致，强烈建议您上传 <strong>PDF</strong> 格式的文档。</li>
    <li><strong>文件大小</strong>: 单个文件大小建议不超过 <strong>50MB</strong>，最大支持 100MB。大文件上传时间较长，请耐心等待。</li>
    <li><strong>隐私安全</strong>: 所有文件将通过加密通道上传，并存储在专用服务器上。打印完成后，您的文件将被<strong>立即销毁</strong>，绝不外泄。</li>
    <li><strong>合规声明</strong>: 请遵守相关法律法规，<strong>严禁上传</strong>任何涉密、涉政及其他违禁内容的文件。</li>
  </ul>
</div>
```

**说明**: 在上传前就告知用户文件大小限制和上传时间预期。

---

## 配置总结

| 配置项 | 修改前 | 修改后 | 说明 |
|--------|--------|--------|------|
| API 全局超时 | 10 秒 | 120 秒（2 分钟） | 适应普通 API 请求 |
| 文件上传超时 | 10 秒 | 300 秒（5 分钟） | 专门为上传设置 |
| Vite 代理超时 | 默认（~30 秒） | 300 秒（5 分钟） | 确保代理不中断 |
| Django 文件大小限制 | 2.5 MB（默认） | 100 MB | 支持大文档 |

---

## 测试建议

### 1. 小文件测试（< 5MB）
- 应该能在几秒内完成上传
- 不应触发任何超时

### 2. 中等文件测试（5-20MB）
- 应该能在 30 秒内完成
- 上传进度条应正常显示

### 3. 大文件测试（20-50MB）
- 应该能在 2 分钟内完成
- 上传进度条应平滑更新
- 不应出现超时错误

### 4. 超大文件测试（50-100MB）
- 应该能在 5 分钟内完成
- 如果网络较慢，应给出明确提示
- 接近 100MB 应能成功，超过 100MB 应返回友好错误

### 5. 网络中断测试
- 人为中断网络，验证错误提示是否友好
- 恢复网络后，应能重新上传

---

## 生产环境注意事项

### 1. Nginx 配置（如果使用）

生产环境如果使用 Nginx 作为反向代理，需要配置相应的超时和大小限制：

```nginx
server {
    # ... 其他配置 ...
    
    # 文件上传大小限制
    client_max_body_size 100M;
    
    # 上传超时时间
    client_body_timeout 300s;
    
    # 代理超时时间
    proxy_connect_timeout 300s;
    proxy_send_timeout 300s;
    proxy_read_timeout 300s;
    
    location /api/ {
        proxy_pass http://backend_server;
        # ... 其他代理配置 ...
    }
}
```

### 2. Gunicorn/uWSGI 配置

Django 应用服务器也需要配置超时：

**Gunicorn**:
```bash
gunicorn --timeout 300 backend.wsgi:application
```

**uWSGI**:
```ini
[uwsgi]
socket-timeout = 300
harakiri = 300
```

### 3. 数据库连接池

如果上传过程中需要写数据库，确保连接池配置合理：

```python
# settings.py
DATABASES = {
    'default': {
        # ... 其他配置 ...
        'CONN_MAX_AGE': 600,  # 连接保持 10 分钟
    }
}
```

---

## 后续优化建议

### 1. 实现断点续传
- 使用分片上传技术（Chunked Upload）
- 支持大文件分块上传，失败后从断点继续
- 可参考库：`django-chunked-upload`

### 2. 添加客户端文件验证
- 在上传前检查文件大小
- 显示预估上传时间
- 大文件给出警告提示

### 3. 优化上传体验
- 显示上传速度（MB/s）
- 显示剩余时间
- 支持取消上传

### 4. 后台异步处理
- 文件上传完成后，立即返回响应
- 使用 Celery 异步处理文件分析、页数计算等耗时操作
- 通过 WebSocket 或轮询通知前端处理进度

### 5. 使用云存储
- 考虑使用 AWS S3、阿里云 OSS 等云存储服务
- 客户端直传，减少服务器压力
- 支持 CDN 加速

---

## 修改文件清单

1. ✅ `frontend/src/services/apiService.js` - 增加超时配置和错误处理
2. ✅ `frontend/vite.config.js` - 配置代理超时
3. ✅ `backend/settings.py` - 配置文件上传大小限制
4. ✅ `frontend/src/stores/order.js` - 改进错误提示
5. ✅ `frontend/src/views/HomeView.vue` - 添加用户提示

---

## 验证步骤

### 重启开发服务器

修改完成后，需要重启前后端服务器以使配置生效：

```bash
# 前端
cd frontend
npm run dev

# 后端
python manage.py runserver
```

### 测试上传

1. 准备不同大小的测试文件
2. 逐个上传，观察控制台输出
3. 验证超时时间是否足够
4. 验证错误提示是否友好

---

## 总结

本次修复主要解决了**前端超时时间过短**的问题，这是导致大文件上传失败的根本原因。同时：

- ✅ 前端增加了超时配置（2-5 分钟）
- ✅ 后端配置了文件大小限制（100MB）
- ✅ 改进了错误提示的友好性
- ✅ 添加了用户操作指引

修复后，用户应该能够顺利上传最大 100MB 的文件，超时或过大文件会收到清晰的错误提示。

---

**修复日期**: 2025-10-17  
**修复人**: GitHub Copilot  
**问题来源**: 用户反馈大文件上传失败
