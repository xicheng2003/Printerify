# Printerify

> 为每一次打印赋能。

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.x-green.svg)](https://www.djangoproject.com/)
[![Vue.js](https://img.shields.io/badge/Vue.js-3.x-brightgreen.svg)](https://vuejs.org/)
[![Vite](https://img.shields.io/badge/Vite-5.x-purple.svg)](https://vitejs.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

**Printerify** 是一个现代化的自助打印订单管理服务。它旨在通过一个简洁、高效的Web界面，将传统、繁琐的线下打印流程进行革新，为用户提供一个从文件上传、规格定制、在线计价、支付凭证上传到订单状态追踪的完整闭环体验。

对于服务管理员，Printerify提供了一个强大的后台，可以集中管理所有订单、查看打印文档，并一键批量下载文件，极大地提升了处理效率。

## ✨ 核心功能

- **多格式文件上传**: 支持PDF、Word等常见文档格式。
- **自定义打印规格**: 用户可自由选择纸张大小、色彩、份数等。
- **实时智能计价**: 根据文件页数（支持PDF/Word页数识别）和打印规格自动计算价格。
- **凭证上传系统**: 集成线下扫码支付流程，用户可上传支付截图作为凭证。
- **订单状态追踪**: 用户可通过手机号和订单号随时查询订单的最新状态（如：待处理、打印中、已完成）。
- **多视图前端**: 采用Vue Router实现下单和查询页面的分离，体验专业。
- **强大的管理后台**: 管理员可通过Django Admin查看所有订单、修改状态，并一键批量下载打印文件（打包为zip）。

## 🚀 技术栈

- **后端**:
    - **Python 3.11+**
    - **Django 5.x**: 核心Web框架。
    - **Django REST Framework**: 用于构建强大的RESTful API。
    - **Pillow, PyPDF2, python-docx**: 用于处理图片和文件内容。
- **前端**:
    - **Vue.js 3.x**: 采用组合式API (Composition API) 进行开发。
    - **Vite**: 提供极速的前端开发与构建体验。
    - **Vue Router**: 用于构建单页面应用（SPA）的路由。
    - **Axios**: 用于与后端API进行HTTP通信。

## 🛠️ 本地部署与运行指南

### 先决条件

- Python 3.8+
- Node.js 18.x+ 和 npm
- Git

### 1. 克隆仓库

```bash
git clone https://your-repository-url/Printerify.git
cd Printerify
```

### 2. 后端设置

```bash
# 进入项目根目录

# 1. 创建并激活Python虚拟环境
python -m venv venv
# Windows
.\venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

# 2. 安装后端依赖
pip install -r requirements.txt 
# (提示: 您可以通过 pip freeze > requirements.txt 命令生成此文件)

# 3. 应用数据库迁移
python manage.py migrate

# 4. 创建后台管理员账号
python manage.py createsuperuser

# 5. 运行后端开发服务器
python manage.py runserver
# 后端服务将运行在 [http://127.0.0.1:8000](http://127.0.0.1:8000)
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

## 📄 API 端点概览

- `POST /api/files/`: 上传文件（打印文档或付款截图）。
- `POST /api/price-quote/`: 获取价格报价。
- `GET, POST /api/orders/`: 获取订单列表或创建新订单。
- `GET /api/orders/?phone_number=<num>&order_number=<num>`: 查询特定订单。

---

希望您喜欢 **Printerify**！
