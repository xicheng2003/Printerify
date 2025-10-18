# 文件预览/下载功能部署指南

## 📋 功能说明

通过URL参数控制文件在浏览器中的行为：
- **在线预览**：`/media/file.pdf` → 浏览器内显示
- **下载文件**：`/media/file.pdf?download=1` → 触发下载

---

## 🚀 部署步骤

### 1. 前端部署（已完成）

**文件：** `frontend/src/views/QueryView.vue`

**修改内容：**
```vue
<!-- 文件操作链接 -->
<div class="file-actions">
  <a :href="doc.file_path" target="_blank" class="file-link">在线预览</a>
  <a :href="doc.file_path + '?download=1'" class="file-link download">下载文件</a>
</div>
```

**样式更新：**
- 简洁的两个链接按钮
- 预览：带边框的轮廓按钮
- 下载：实心主题色按钮

---

### 2. Nginx配置（需要在服务器上操作）

#### 步骤 2.1：备份现有配置

```bash
# SSH登录到服务器
ssh xicheng2003@your-server

# 备份配置文件
sudo cp /etc/nginx/sites-available/printerify /etc/nginx/sites-available/printerify.backup.$(date +%Y%m%d)
```

#### 步骤 2.2：编辑Nginx配置

```bash
sudo nano /etc/nginx/sites-available/printerify
```

找到 `location ^~ /media/` 部分，修改为：

```nginx
location ^~ /media/ {
    alias /home/xicheng2003/Printerify/media/;
    
    # 处理中文文件名
    charset utf-8;
    
    # 【关键】根据URL参数动态设置Content-Disposition
    set $disposition "inline";
    if ($arg_download = "1") {
        set $disposition "attachment";
    }
    
    # 动态设置响应头，支持中文文件名
    add_header Content-Disposition "$disposition; filename*=UTF-8''$uri" always;
    
    # MIME类型
    types {
        application/pdf pdf;
        image/jpeg jpg jpeg;
        image/png png;
    }
    
    # 缓存设置
    expires 7d;
    add_header Cache-Control "public";
    
    # 安全设置
    autoindex off;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    
    try_files $uri =404;
}
```

#### 步骤 2.3：测试配置

```bash
# 测试Nginx配置语法
sudo nginx -t
```

**预期输出：**
```
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
```

#### 步骤 2.4：重载Nginx

```bash
# 重载Nginx配置（不中断服务）
sudo systemctl reload nginx

# 或者重启Nginx
sudo systemctl restart nginx
```

#### 步骤 2.5：检查Nginx状态

```bash
# 查看Nginx状态
sudo systemctl status nginx

# 查看错误日志（如果有问题）
sudo tail -50 /var/log/nginx/error.log
```

---

### 3. 前端构建和部署

```bash
# 本地构建前端
cd frontend
npm run build

# 将构建产物上传到服务器
scp -r dist/* xicheng2003@your-server:/home/xicheng2003/Printerify/frontend/dist/
```

或者在服务器上构建：

```bash
# SSH到服务器
ssh xicheng2003@your-server

# 进入项目目录
cd /home/xicheng2003/Printerify

# 拉取最新代码
git pull origin main

# 构建前端
cd frontend
npm install
npm run build
```

---

## 🧪 测试验证

### 测试1：在线预览

1. 访问订单查询页面
2. 输入手机号和取件码查询订单
3. 点击"在线预览"按钮
4. **预期结果：**
   - 新标签页打开
   - 浏览器内置PDF查看器显示文件
   - 可以在浏览器中阅读、缩放

### 测试2：下载文件

1. 在同一订单页面
2. 点击"下载文件"按钮
3. **预期结果：**
   - 浏览器触发下载
   - 文件保存到下载文件夹
   - 文件名正确（包括中文）

### 测试3：中文文件名

1. 上传一个中文文件名的PDF（如"肖秀荣背诵赠品.pdf"）
2. 创建订单并查询
3. 测试预览和下载
4. **预期结果：**
   - 预览正常
   - 下载后文件名正确显示中文

### 测试4：URL直接访问

**测试预览：**
```bash
# 使用curl测试（应返回 inline）
curl -I "https://print.morlight.top/media/order_documents/2025-10-17/P-092/Group_37/01_file.pdf"

# 检查响应头
Content-Disposition: inline; filename*=UTF-8''...
```

**测试下载：**
```bash
# 使用curl测试（应返回 attachment）
curl -I "https://print.morlight.top/media/order_documents/2025-10-17/P-092/Group_37/01_file.pdf?download=1"

# 检查响应头
Content-Disposition: attachment; filename*=UTF-8''...
```

---

## 🔍 故障排查

### 问题1：点击"下载"仍然预览

**可能原因：**
- Nginx配置未生效
- 浏览器缓存

**解决方案：**
```bash
# 检查Nginx配置是否正确加载
sudo nginx -T | grep -A 20 "location.*media"

# 清除浏览器缓存或使用隐私模式测试

# 查看实际响应头
curl -I "https://print.morlight.top/media/path/file.pdf?download=1"
```

### 问题2：下载的文件名乱码

**可能原因：**
- 未设置 `charset utf-8`
- `filename*=UTF-8''` 格式不正确

**解决方案：**
```nginx
# 确保配置中包含
charset utf-8;
add_header Content-Disposition "$disposition; filename*=UTF-8''$uri" always;
```

### 问题3：Nginx配置测试失败

**可能原因：**
- 语法错误
- `if` 语句位置不对

**解决方案：**
```bash
# 查看详细错误
sudo nginx -t

# 检查配置文件语法
# 确保 if 语句在 add_header 之前
```

### 问题4：前端显示旧版本

**可能原因：**
- 前端未重新构建
- 浏览器缓存

**解决方案：**
```bash
# 重新构建前端
cd frontend
npm run build

# 硬刷新浏览器：Ctrl+Shift+R（Windows）或 Cmd+Shift+R（Mac）
```

---

## 📊 工作原理

### URL参数控制流程

```
用户点击"在线预览"
  ↓
前端生成URL: /media/file.pdf
  ↓
Nginx检测: $arg_download = ""
  ↓
设置: $disposition = "inline"
  ↓
响应头: Content-Disposition: inline
  ↓
浏览器: 在线显示 ✅

---

用户点击"下载文件"
  ↓
前端生成URL: /media/file.pdf?download=1
  ↓
Nginx检测: $arg_download = "1"
  ↓
设置: $disposition = "attachment"
  ↓
响应头: Content-Disposition: attachment
  ↓
浏览器: 触发下载 ✅
```

### Content-Disposition 响应头说明

```http
# 预览模式
Content-Disposition: inline; filename*=UTF-8''/media/order_documents/.../file.pdf

# 下载模式
Content-Disposition: attachment; filename*=UTF-8''/media/order_documents/.../file.pdf
```

**参数说明：**
- `inline`：浏览器尝试内联显示
- `attachment`：浏览器强制下载
- `filename*=UTF-8''`：RFC 5987格式，支持中文文件名

---

## 🎯 验收标准

- ✅ 点击"在线预览"在新标签页打开PDF
- ✅ 点击"下载文件"触发浏览器下载
- ✅ 中文文件名正确显示
- ✅ 移动端正常工作
- ✅ 响应头正确设置
- ✅ 不影响其他功能

---

## 📚 相关文档

- Nginx配置示例：`docs/nginx-production-config.conf`
- 快速修复指南：`docs/nginx-location-priority-404-fix.md`
- 功能详细说明：`docs/file-view-download-options.md`

---

## 📝 回滚方案

如果部署后出现问题，可以快速回滚：

```bash
# 恢复Nginx配置
sudo cp /etc/nginx/sites-available/printerify.backup.YYYYMMDD /etc/nginx/sites-available/printerify

# 测试配置
sudo nginx -t

# 重载Nginx
sudo systemctl reload nginx

# 前端回滚到上一个版本
cd /home/xicheng2003/Printerify
git checkout <previous-commit>
cd frontend
npm run build
```

---

**部署日期：** 2025-10-18  
**部署状态：** ⏳ 待部署  
**预计影响：** 低（仅增强功能，不影响现有流程）
