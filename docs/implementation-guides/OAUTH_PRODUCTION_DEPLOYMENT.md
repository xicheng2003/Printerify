# OAuth生产环境部署指南

## 🎯 问题总结

你的OAuth认证在生产环境中回调到 `127.0.0.1` 的问题已经修复。主要原因是：

1. **硬编码的回调URL**：`api/views.py` 中硬编码了 `http://127.0.0.1:5173/oauth/callback`
2. **缺少环境变量配置**：没有配置生产环境的前端域名
3. **Django设置中的域名配置**：虽然配置了生产域名，但OAuth视图没有使用这些配置

## ✅ 已修复的问题

- [x] 在 `backend/settings.py` 中添加了 `FRONTEND_URL` 配置
- [x] 修复了 `api/views.py` 中所有硬编码的回调URL
- [x] 使用 `settings.FRONTEND_URL` 动态构建回调URL
- [x] 创建了配置检查脚本 `check_oauth_config.py`

## 🚀 生产环境部署步骤

### 1. 环境变量配置

在生产服务器上创建 `.env` 文件：

```bash
# Django 核心配置
SECRET_KEY=your-production-secret-key-here
DEBUG=False

# 数据库配置
USE_POSTGRES=True
POSTGRES_DB=printerify
POSTGRES_USER=your_db_user
POSTGRES_PASSWORD=your_db_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# 前端域名配置（重要！）
FRONTEND_URL=https://print.morlight.top

# OAuth配置
GITHUB_CLIENT_ID=你的GitHub客户端ID
GITHUB_CLIENT_SECRET=你的GitHub客户端密钥
GOOGLE_CLIENT_ID=你的Google客户端ID
GOOGLE_CLIENT_SECRET=你的Google客户端密钥
```

### 2. GitHub OAuth应用配置

1. 登录 [GitHub Developer Settings](https://github.com/settings/developers)
2. 创建新的 OAuth App 或编辑现有的
3. 设置以下参数：
   - **Application name**: Printerify
   - **Homepage URL**: `https://print.morlight.top`
   - **Authorization callback URL**: `https://print.morlight.top/api/oauth/github/callback/`

### 3. Google OAuth应用配置

1. 登录 [Google Cloud Console](https://console.cloud.google.com/)
2. 选择你的项目或创建新项目
3. 在 "APIs & Services" > "Credentials" 中创建 OAuth 2.0 客户端ID
4. 设置以下参数：
   - **Application type**: Web application
   - **Name**: Printerify
   - **Authorized redirect URIs**: `https://print.morlight.top/api/oauth/google/callback/`

### 4. 前端部署配置

确保前端部署到正确的域名：

```bash
# 构建生产版本
npm run build

# 部署到 print.morlight.top 域名
# 确保 /oauth/callback 路由正确配置
```

### 5. 后端部署配置

1. 设置环境变量：
```bash
export DEBUG=False
export FRONTEND_URL=https://print.morlight.top
```

2. 重启Django服务：
```bash
# 如果使用systemd
sudo systemctl restart your-django-service

# 如果使用supervisor
sudo supervisorctl restart your-django-app

# 如果使用gunicorn
pkill gunicorn
gunicorn backend.wsgi:application --bind 0.0.0.0:8000
```

## 🔍 部署后验证

### 1. 运行配置检查

```bash
python check_oauth_config.py
```

应该看到：
- ✅ 生产环境配置正确
- ✅ OAuth回调URL指向正确的域名

### 2. 测试OAuth流程

1. 访问 `https://print.morlight.top`
2. 点击GitHub或Google登录
3. 完成OAuth授权
4. 检查是否重定向到正确的回调页面

### 3. 检查浏览器网络请求

在浏览器开发者工具中：
1. 查看Network标签页
2. 观察OAuth回调请求
3. 确认重定向URL是 `https://print.morlight.top/oauth/callback`

## 🚨 常见问题排查

### 问题1：仍然回调到127.0.0.1

**原因**：环境变量没有正确加载或Django服务没有重启

**解决方案**：
```bash
# 检查环境变量
echo $FRONTEND_URL

# 重启Django服务
sudo systemctl restart your-django-service

# 检查Django日志
tail -f /var/log/django.log
```

### 问题2：OAuth提供商报错"redirect_uri_mismatch"

**原因**：OAuth应用的回调URL配置不正确

**解决方案**：
1. 检查GitHub/Google OAuth应用的回调URL设置
2. 确保完全匹配：`https://print.morlight.top/api/oauth/github/callback/`
3. 注意末尾的斜杠

### 问题3：前端路由404错误

**原因**：前端没有正确部署或路由配置错误

**解决方案**：
1. 检查前端构建是否成功
2. 确认 `/oauth/callback` 路由存在
3. 检查nginx/apache配置

## 📋 检查清单

部署前检查：
- [ ] 环境变量 `FRONTEND_URL=https://print.morlight.top` 已设置
- [ ] `DEBUG=False` 已设置
- [ ] GitHub OAuth应用回调URL已更新
- [ ] Google OAuth应用回调URL已更新
- [ ] 前端已部署到正确域名
- [ ] 后端服务已重启

部署后检查：
- [ ] 运行 `python check_oauth_config.py` 通过
- [ ] OAuth登录流程正常
- [ ] 回调URL正确
- [ ] 用户认证成功

## 🆘 获取帮助

如果仍然遇到问题：

1. 检查Django日志：`tail -f django.log`
2. 运行配置检查：`python check_oauth_config.py`
3. 检查浏览器开发者工具的网络请求
4. 确认所有环境变量都已正确设置

## 📝 总结

通过这次修复，你的OAuth系统现在可以：

- ✅ 根据环境自动选择正确的前端域名
- ✅ 开发环境使用 `http://127.0.0.1:5173`
- ✅ 生产环境使用 `https://print.morlight.top`
- ✅ 动态构建OAuth回调URL
- ✅ 避免硬编码的本地地址

现在你可以安全地部署到生产环境，OAuth认证将正确回调到你的生产域名！
