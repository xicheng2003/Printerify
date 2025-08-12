# Printerify 项目上下文

## 项目概述

Printerify 是一个现代化的在线文档打印服务平台，旨在为用户提供流畅、便捷、高度可定制的打印体验。用户可以上传文档，设置打印选项（如纸张尺寸、单双面、颜色模式、装订方式等），然后下单并支付。

### 核心特性
- **异步处理**：使用 Celery 和 Redis 处理订单处理、PDF 生成等耗时任务
- **多文件与装订组**：支持用户上传多个文档并分组进行不同的装订设置
- **高度可定制化**：提供丰富的打印选项（A4/B5纸张、单双面打印、彩色/黑白打印等）
- **响应式设计**：适配桌面和移动设备
- **明暗主题**：支持深色模式
- **实时价格计算**：所有选项更改都会实时反馈在价格上
- **邮件通知**：向用户和管理员发送订单状态通知
- **现代前端**：采用 Vue.js 构建

### 技术栈
- **后端**：Django 5.2, Django REST Framework, Celery, Redis
- **前端**：Vue.js 3, Vite, Pinia, Vue Router
- **数据库**：SQLite（开发）/ PostgreSQL（生产）
- **部署**：Docker, Gunicorn, Nginx（计划中）

## 项目结构

```
printerify/
├── api/                  # Django App - 核心API逻辑
│   ├── migrations/       # 数据库迁移文件
│   ├── services/         # 服务层 (例如, 定价)
│   ├── static/           # 静态文件
│   ├── templates/        # 邮件模板
│   ├── tests/            # 测试文件
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
├── frontend/             # Vue.js 前端应用
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
│   └── vite.config.js    # Vite 配置
├── docs/                 # 项目文档
├── media/                # 用户上传的媒体文件
├── .gitignore
├── manage.py             # Django 管理脚本
├── README.md             # 项目说明
└── requirements.txt      # Python 依赖
```

## 核心数据模型

### Order (订单)
- `order_number`：唯一订单号（时间戳+随机数）
- `pickup_code`：循环取件码（P-XXX格式）
- `phone_number`：用户手机号
- `total_price`：订单总价
- `status`：订单状态（待处理、处理中、已完成、已取消）
- `payment_method`：支付方式
- `payment_screenshot`：支付凭证截图
- `order_summary_pdf`：订单摘要PDF

### BindingGroup (装订组)
- `order`：所属订单（外键）
- `binding_type`：装订方式（不装订、订书钉等）
- `binding_cost`：装订费用
- `sequence_in_order`：组在订单中的顺序

### Document (文档)
- `group`：所属装订组（外键）
- `original_filename`：原始文件名
- `file_path`：文件存储路径
- `color_mode`：色彩模式（黑白、彩色）
- `print_sided`：单双面（单面、双面、封面单面）
- `paper_size`：纸张尺寸（A4、B5）
- `copies`：打印份数
- `page_count`：文件页数
- `print_cost`：打印费用
- `sequence_in_group`：文件在组内的顺序

## 构建和运行

### 后端设置
```bash
# 创建并激活虚拟环境
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# 安装依赖
pip install -r requirements.txt

# 数据库迁移
python manage.py migrate

# 运行开发服务器
python manage.py runserver
```

### 前端设置
```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 运行开发服务器
npm run dev
```

### 启动 Celery Worker
```bash
# 激活虚拟环境
source venv/bin/activate

# 启动 Celery worker
celery -A backend worker -l info
```

### 运行测试
```bash
# 运行所有后端测试
python manage.py test api.tests

# 或使用测试脚本 (Linux/Mac)
./run_tests.sh

# 或使用测试脚本 (Windows)
run_tests.bat
```

## 开发约定

### 后端开发
- 使用 Django 5.2 和 Django REST Framework
- 遵循 Django 最佳实践
- 模型设计遵循数据库规范化原则
- API 设计遵循 RESTful 原则
- 使用 Celery 处理异步任务
- 价格计算逻辑集中管理在 services/pricing.py

### 前端开发
- 使用 Vue 3 Composition API
- 使用 Pinia 进行状态管理
- 使用 Vue Router 进行路由管理
- 遵循组件化开发模式
- 使用 Tailwind CSS 进行样式设计（但禁用了 Preflight）

### 测试
- 单元测试、集成测试和功能测试并重
- 测试文件组织在 `api/tests/` 目录下
- 使用 Django TestCase 和 pytest
- 包含覆盖率报告生成

### 代码质量
- 后端使用 Python，遵循 PEP 8 规范
- 前端使用 JavaScript/TypeScript，遵循 ESLint 规则
- 代码注释使用中文，便于团队理解