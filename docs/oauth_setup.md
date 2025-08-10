# OAuth 第三方登录配置指南

本文档说明如何为 Printerify 项目配置 GitHub 和 Google OAuth 登录。

## 前置要求

1. **HTTPS 环境**：生产环境必须使用 HTTPS
2. **域名验证**：需要在 OAuth 提供商处验证你的域名
3. **回调 URL 配置**：设置正确的授权回调地址

## GitHub OAuth 配置

### 1. 创建 GitHub OAuth App

1. 访问 [GitHub Developer Settings](https://github.com/settings/developers)
2. 点击 "New OAuth App"
3. 填写应用信息：
   - **Application name**: Printerify
   - **Homepage URL**: `https://print.morlight.top`
   - **Authorization callback URL**: `https://print.morlight.top/social/github/login/callback/`

### 2. 获取凭据

创建完成后，你会获得：
- **Client ID**
- **Client Secret**

### 3. 环境变量配置

在 `.env` 文件中添加：

```bash
GITHUB_CLIENT_ID=your-github-client-id
GITHUB_CLIENT_SECRET=your-github-client-secret
```

## Google OAuth 配置

### 1. 创建 Google OAuth 2.0 客户端

1. 访问 [Google Cloud Console](https://console.cloud.google.com/)
2. 创建新项目或选择现有项目
3. 启用 Google+ API
4. 在 "凭据" 页面创建 "OAuth 2.0 客户端 ID"
5. 配置授权信息：
   - **应用类型**: Web 应用
   - **名称**: Printerify
   - **已获授权的 JavaScript 来源**: `https://print.morlight.top`
   - **已获授权的重定向 URI**: `https://print.morlight.top/social/google/login/callback/`

### 2. 获取凭据

创建完成后，你会获得：
- **客户端 ID**
- **客户端密钥**

### 3. 环境变量配置

在 `.env` 文件中添加：

```bash
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
```

## 本地开发配置

对于本地开发，回调 URL 应该是：

- GitHub: `http://localhost:8000/social/github/login/callback/`
- Google: `http://localhost:8000/social/google/login/callback/`

## 安全注意事项

1. **保密性**：OAuth 密钥必须保密，不要提交到代码仓库
2. **HTTPS**：生产环境必须使用 HTTPS
3. **域名验证**：确保在 OAuth 提供商处正确配置你的域名
4. **权限范围**：只请求必要的权限范围

## 测试 OAuth 登录

1. 启动后端服务：`python manage.py runserver`
2. 启动前端服务：`npm run dev`
3. 访问登录页面，点击 GitHub 或 Google 登录按钮
4. 完成 OAuth 授权流程
5. 验证用户是否成功创建和登录

## 故障排除

### 常见问题

1. **"OAuth未配置"错误**
   - 检查环境变量是否正确设置
   - 确认 `.env` 文件在正确位置

2. **回调 URL 不匹配**
   - 检查 OAuth 提供商处的回调 URL 配置
   - 确认域名和端口号完全匹配

3. **权限不足**
   - 检查 OAuth 应用的权限设置
   - 确认 API 已启用

### 调试技巧

1. 检查 Django 日志输出
2. 使用浏览器开发者工具查看网络请求
3. 验证 OAuth 提供商处的应用配置

## 生产环境部署

1. 设置 `DEBUG=False`
2. 配置 HTTPS
3. 更新 OAuth 提供商处的回调 URL
4. 设置正确的环境变量
5. 测试 OAuth 流程

## 相关文件

- `backend/settings.py` - OAuth 配置
- `api/views.py` - OAuth 视图
- `api/models.py` - 用户模型
- `frontend/src/components/OAuthLogin.vue` - OAuth 登录组件
- `frontend/src/components/AuthForm.vue` - 认证表单
