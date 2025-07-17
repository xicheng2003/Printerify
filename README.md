# Printerify - 现代化的自助打印解决方案

> 为每一次打印赋能。

[![Django](https://img.shields.io/badge/Django-4.2-092E20?style=for-the-badge&logo=django)](https://www.djangoproject.com/)
[![Vue.js](https://img.shields.io/badge/Vue.js-3-4FC08D?style=for-the-badge&logo=vue.js)](https://vuejs.org/)
[![Celery](https://img.shields.io/badge/Celery-5.2-3776AB?style=for-the-badge&logo=celery)](https://docs.celeryq.dev/en/stable/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

**Printerify** 是一个功能完善的全栈Web应用，旨在提供一个无缝、高效的在线自助打印体验。用户可以轻松上传文件，自定义详细的打印规格，实时查看价格，并通过一个清晰的多步骤流程完成下单。

---

### ✨ 核心功能

* **多文件上传与管理**: 支持一次性上传多个文档（PDF, Word, PPT等）。

* **实时计价**: 根据份数、色彩、单双面和装订方式，动态计算订单总价。

* **灵活的打印配置**:
    * 对每个文件进行独立的打印设置。
    * 通过拖拽轻松调整文件在组内的打印顺序。
    * 通过拖拽合并不同的装订组。

* **响应式与移动端优先设计**:
    * 界面在桌面和移动设备上均有良好表现。
    * 配置项支持**折叠/展开**，极大优化了小屏幕上的操作空间和拖拽体验。

* **清晰的下单流程**: 通过步骤条（Stepper）引导用户完成从配置、支付到获取取件码的全过程。

* **异步任务处理**: 使用 Celery 在后台处理耗时的任务（如生成PDF订单摘要、发送邮件通知），确保前端操作流畅，无卡顿。

* **增强的交互反馈**:
    * **全局加载指示器**：在下单等耗时操作期间提供明确的“处理中”反馈。
    * **总价更新动画**：价格变动时，总价会高亮或跳动，给用户即时确认。

* **订单状态查询**: 用户可通过手机号和取件码随时查询订单的最新状态。

---

### 🛠️ 技术栈

* **后端**:
    * **框架**: Django & Django REST Framework
    * **数据库**: PostgreSQL (生产环境), SQLite (开发环境)
    * **异步任务**: Celery & Redis
    * **PDF处理**: WeasyPrint

* **前端**:
    * **框架**: Vue.js 3 (组合式 API)
    * **构建工具**: Vite
    * **状态管理**: Pinia
    * **路由**: Vue Router
    * **拖拽**: vuedraggable

---

### 🚀 本地部署与运行指南

#### 1. 后端 (Django)

**环境准备:**
* Python 3.10+
* Redis

**安装与启动:**

```bash
# 1. 克隆项目到本地
git clone [https://github.com/your-username/Printerify.git](https://github.com/your-username/Printerify.git)
cd Printerify

# 2. 创建并激活 Python 虚拟环境
python -m venv venv
source venv/bin/activate  # on Windows, use `venv\Scripts\activate`

# 3. 安装后端依赖
pip install -r requirements.txt

# 4. 执行数据库迁移
python manage.py migrate

# 5. 启动 Django 开发服务器 (一个终端)
python manage.py runserver

# 6. 启动 Redis 服务器 (请确保已安装并运行)

# 7. 启动 Celery Worker (需要新开一个终端)
#    确保虚拟环境已激活
celery -A backend worker -l info


```

### 3. 前端设置

```bash
# 新开一个命令行终端，进入frontend目录
cd frontend

# 1. 安装前端依赖
npm install

# 2. 运行前端开发服务器
npm run dev
# 前端应用将运行在 http://localhost:5173 (或其他可用端口)
```

现在，您可以打开浏览器访问 `http://localhost:5173` 开始使用Printerify了！

## 📁 项目结构概览

```bash
Printerify/
├── backend/         # Django 项目配置 (settings.py, urls.py)
├── api/             # Django 应用，处理核心业务逻辑
│   ├── models.py      # 数据库模型 (Order, Document等)
│   ├── serializers.py # 数据序列化
│   ├── views.py       # API 视图
│   ├── tasks.py       # Celery 异步任务
│   └── urls.py        # API 路由
├── frontend/        # Vue.js 前端项目
│   ├── src/
│   │   ├── components/  # 可复用组件 (Stepper, DocumentItem等)
│   │   ├── views/       # 页面级组件 (HomeView, QueryView)
│   │   ├── stores/      # Pinia 全局状态管理
│   │   ├── router/      # Vue Router 路由配置
│   │   └── App.vue      # 应用主入口
│   └── vite.config.js # Vite 配置
├── media/           # 用户上传的文件存储目录
└── manage.py        # Django 管理脚本
```

---

本项目采用 MIT License 授权。
