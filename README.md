<p align="center">
  <img src="docs/assets/printerify-logo.svg" alt="Printerify logo" width="128" height="128">
</p>

# Printerify-为每一次打印赋能

[![zh-CN](https://img.shields.io/badge/language-中文-blue.svg)](README.md)

**Printerify** 是一个现代化的在线文档打印服务平台，旨在为用户提供流畅、便捷、高度可定制的打印体验。从上传文件到最终下单，每一步都经过精心设计，确保操作直观、响应迅速。

[**线上访问地址 (Live Demo)**](https://print.morlight.top)

---

## ✨ 主要特性 (Features)

-   **🚀 异步处理**: 集成 Celery 和 Redis，实现订单处理、PDF 生成等耗时任务的异步化，极大提升了用户体验和系统响应速度。
-   **📚 多文件与装订组**: 支持用户上传多个文档，并将其分组进行不同的装订设置，满足复杂的打印需求。
-   **🎨 高度可定制化**: 提供丰富的打印选项，包括多种纸张尺寸 (A3, A4, B5)、单双面打印、彩色/黑白打印等。
-   **📱 响应式设计**: 完美适配桌面和移动设备，无论在任何终端上都能获得一致的优质体验。
-   **🌗 明暗主题**: 内置优雅的深色模式，并可根据系统设置自动切换，呵护您的双眼。
-   **💰 实时价格计算**: 所有打印选项的更改都会实时反馈在价格上，清晰透明。
-   **🔔 邮件通知**: 通过精心设计的邮件模板，及时向用户和管理员发送订单状态通知。
-   **🔐 OAuth 认证**: 支持多种第三方登录方式，提供安全便捷的用户认证体验。
-   **📄 多格式支持**: 支持 PDF、Word、图片等多种文档格式的上传和处理。
-   **🧩 现代前端**: 采用 Vue 3 + Tailwind CSS 构建，拥有动态加载、全局 Loading 指示器、交互式提示等现代化的 UI/UX。

## 🛠️ 技术栈 (Tech Stack)

-   **后端 (Backend)**: Django 5.2+, Django REST Framework 3.16+
-   **前端 (Frontend)**: Vue 3.5+, Tailwind CSS 3.4+, Vite 7.0+
-   **状态管理**: Pinia 3.0+
-   **异步任务队列 (Task Queue)**: Celery 5.5+
-   **消息代理 & 缓存 (Broker & Cache)**: Redis 5.2+
-   **数据库 (Database)**: PostgreSQL / MySQL / SQLite
-   **部署 (Deployment)**: Docker, Gunicorn, Nginx
-   **测试框架**: pytest, vitest
-   **代码质量**: ESLint, Prettier, Black

## 📁 项目目录结构

```
printerify/
├── api/                  # Django App - 核心API逻辑
│   ├── migrations/       # 数据库迁移文件
│   ├── services/         # 服务层 (例如, 定价)
│   ├── static/           # 静态文件
│   ├── templates/        # 邮件模板
│   ├── admin.py          # Django Admin 配置
│   ├── models.py         # 数据库模型
│   ├── pdf_generator.py  # PDF生成逻辑
│   ├── serializers.py    # DRF 序列化器
│   ├── tasks.py          # Celery 异步任务
│   ├── urls.py           # API URL 配置
│   └── views.py          # API 视图
├── backend/              # Django 项目 - 核心配置
│   ├── settings.py       # Django 设置
│   ├── urls.py           # 项目根 URL 配置
│   └── celery.py         # Celery 配置
├── frontend/             # Vue 3 前端应用
│   ├── public/           # 公共静态资源
│   ├── src/              # 源代码
│   │   ├── assets/       # CSS, 字体等资源
│   │   ├── components/   # 可复用 Vue 组件
│   │   ├── router/       # 路由配置
│   │   ├── services/     # API 服务调用
│   │   ├── stores/       # Pinia 状态管理
│   │   ├── views/        # 页面级组件
│   │   ├── App.vue       # 根组件
│   │   └── main.js       # 入口文件
│   ├── index.html        # HTML 入口
│   ├── package.json      # npm 依赖
│   ├── vite.config.js    # Vite 配置
│   ├── tailwind.config.js # Tailwind CSS 配置
│   └── postcss.config.js # PostCSS 配置
├── docs/                 # 项目文档
│   ├── implementation-guides/  # 实施指南和部署文档
│   ├── fix-summaries/          # 问题修复总结和解决方案
│   ├── troubleshooting/        # 故障排除指南
│   ├── debug-scripts/          # 调试脚本
│   ├── oauth_setup.md          # OAuth 设置指南
│   ├── frontend_testing.md     # 前端测试指南
│   ├── backend_testing.md      # 后端测试指南
│   ├── Privacy Policy.md       # 隐私政策
│   └── Terms of Service.md     # 服务条款
├── scripts/              # 实用脚本和工具
│   ├── test_*.py         # 测试脚本
│   ├── check_*.py        # 检查脚本
│   └── setup_env.py      # 环境设置脚本
├── media/                # 用户上传的媒体文件
├── temp_uploads/         # 临时上传目录
├── .gitignore
├── manage.py             # Django 管理脚本
├── README.md             # 项目说明
├── PROJECT_ORGANIZATION.md # 项目组织说明
├── requirements.txt      # Python 依赖
├── pyproject.toml        # 项目配置
├── run_tests.sh          # Linux/Mac 测试脚本
└── run_tests.bat         # Windows 测试脚本
```

## 🚀 快速开始 (Getting Started)

请按照以下步骤在本地运行本项目。

### 依赖环境 (Prerequisites)

-   Python 3.8+
-   Node.js 18+
-   Redis 5.0+
-   PostgreSQL 12+ (或其他你选择的数据库)

### 1. 克隆仓库

```bash
git clone https://github.com/xicheng2003/printerify.git
cd printerify
```

### 2. 后端设置 (Backend Setup)

```bash
# 创建并激活虚拟环境
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# 安装依赖
pip install -r requirements.txt

# 创建 .env 文件并配置环境变量 (参考 env_example.txt)
cp env_example.txt .env
# 使用编辑器修改 .env 文件
# nano .env

# 数据库迁移
python manage.py migrate

# 创建超级用户 (可选)
python manage.py createsuperuser

# 运行开发服务器
python manage.py runserver
```

### 3. 前端设置 (Frontend Setup)

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 运行开发服务器
npm run dev

# 构建生产版本
npm run build

# 代码格式化和检查
npm run format
npm run lint
```

### 4. 启动 Celery Worker

确保你的 Redis 服务正在运行，然后在项目根目录下打开一个新的终端：

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动 Celery worker
celery -A backend worker -l info

# 启动 Celery beat (如果需要定时任务)
celery -A backend beat -l info
```

### 5. 运行测试 (Running Tests)

```bash
# 运行所有后端测试
python manage.py test api.tests

# 运行特定测试
python -m pytest api/tests/ -v

# 运行前端测试
cd frontend
npm run test

# 运行测试并生成覆盖率报告
npm run test:run

# 或使用测试脚本
./run_tests.sh          # Linux/Mac
run_tests.bat           # Windows
```

## ⚙️ 环境变量 (Environment Variables)

项目依赖于环境变量进行配置。请在后端根目录下创建一个 `.env` 文件，并至少包含以下内容：

```env
# Django
SECRET_KEY='your-secret-key'
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

# Database
DATABASE_URL='postgres://user:password@host:port/dbname'
# 或者使用 SQLite (开发环境)
# DATABASE_URL='sqlite:///db.sqlite3'

# Redis (注意：Broker 和 Backend 建议使用不同的 DB)
REDIS_PASSWORD='your-redis-password'
CELERY_BROKER_URL='redis://:your-redis-password@127.0.0.1:6379/1'
CELERY_RESULT_BACKEND='redis://:your-redis-password@127.0.0.1:6379/2'

# Email
EMAIL_HOST='smtp.example.com'
EMAIL_PORT=587
EMAIL_HOST_USER='your-email@example.com'
EMAIL_HOST_PASSWORD='your-email-password'
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL='Printerify <noreply@example.com>'

# OAuth 设置 (如果使用第三方登录)
GOOGLE_CLIENT_ID='your-google-client-id'
GOOGLE_CLIENT_SECRET='your-google-client-secret'
GITHUB_CLIENT_ID='your-github-client-id'
GITHUB_CLIENT_SECRET='your-github-client-secret'
```

## 📚 文档导航

项目文档已按功能分类组织，便于查找：

- **📖 实施指南**: `docs/implementation-guides/` - 部署和功能实施指南
- **🔧 修复总结**: `docs/fix-summaries/` - 问题修复和解决方案
- **🚨 故障排除**: `docs/troubleshooting/` - 常见问题解决方法
- **🧪 测试指南**: `docs/frontend_testing.md`, `docs/backend_testing.md`
- **🔐 OAuth 设置**: `docs/oauth_setup.md` - 第三方登录配置

## 🧪 开发工具

### 代码质量
- **ESLint**: JavaScript/TypeScript 代码检查
- **Prettier**: 代码格式化
- **Black**: Python 代码格式化
- **pytest**: Python 测试框架
- **vitest**: Vue 组件测试

### 调试工具
- **Vue DevTools**: Vue 应用调试
- **Django Debug Toolbar**: Django 调试
- **Celery Flower**: 异步任务监控

## 🤝 贡献 (Contributing)

欢迎任何形式的贡献！你可以通过以下方式参与：

1.  Fork 本仓库
2.  创建你的特性分支 (`git checkout -b feature/AmazingFeature`)
3.  提交你的更改 (`git commit -m 'feat: Add some AmazingFeature'`)
4.  推送到分支 (`git push origin feature/AmazingFeature`)
5.  发起一个 Pull Request

### 贡献指南
- 遵循项目的代码规范
- 为新功能添加相应的测试
- 更新相关文档
- 确保所有测试通过

## 🐛 问题反馈

如果你遇到问题或有改进建议，请：

1. 查看 `docs/troubleshooting/` 目录中的故障排除指南
2. 检查 `docs/fix-summaries/` 目录中是否有类似问题的解决方案
3. 在 GitHub Issues 中搜索相关问题
4. 创建新的 Issue 并详细描述问题

## 📄 许可证 (License)

本项目采用 MIT 许可证。

## 🔗 相关链接

- [项目主页](https://print.morlight.top)
- [API 文档](https://print.morlight.top/api/docs/)
- [问题反馈](https://github.com/xicheng2003/printerify/issues)
- [项目组织说明](PROJECT_ORGANIZATION.md)
