# Printerify Copilot Instructions

This document provides context and guidelines for AI agents working on the Printerify codebase.

## 🧠 General Guidelines
- **Always respond in 中文**.
- **不要过度设计**，保证代码简洁易懂，简单实用。
- **写代码时，要注意圈复杂度**，代码尽可能复用。
- **写代码时，注意模块设计**，尽量使用设计模式。
- **改动时最小化修改**，尽量不修改到其他模块代码。

## 🏗 Project Architecture

Printerify is a document printing service platform built with a Django backend and Vue 3 frontend.

- **Backend**: Django 5.2+, Django REST Framework (DRF), Celery (Async Tasks), Redis (Broker/Cache).
- **Frontend**: Vue 3 (Composition API), Vite, Tailwind CSS, Pinia.
- **Database**: SQLite (Dev), PostgreSQL (Prod).
- **Admin UI**: Django Unfold theme with custom dashboard overrides.

### Key Directories
- `api/`: Core Django app (Models, Views, Serializers, Tasks).
- `backend/`: Project settings and configuration.
- `frontend/`: Vue 3 SPA source code.
- `templates/admin/`: Custom Admin UI templates (specifically `index.html` for Dashboard).
- `docs/`: Project documentation (Implementation guides, troubleshooting).
- `scripts/`: Utility and maintenance scripts.

## 🚀 Critical Workflows

### Development Server
- **Backend**: `python manage.py runserver` (Runs on port 8000).
- **Frontend**: `cd frontend && npm run dev` (Runs on port 5173).
- **Celery**: `celery -A backend worker -l info -P eventlet` (Windows) or `celery -A backend worker -l info` (Linux).

### Testing
- **Run All Tests**: Use the provided scripts in the root directory.
  - Windows: `.\run_tests.bat`
  - Linux/Mac: `./run_tests.sh`
- **Frontend Tests**: `cd frontend && npm run test` (Vitest).

### Database & Migrations
- **Migrations**: Standard Django commands (`makemigrations`, `migrate`).
- **Fixing Duplicates**: If `IntegrityError` occurs on pickup codes, check `scripts/` for cleanup scripts.

## 🧩 Project-Specific Conventions

### 1. Backend Logic (`api/`)
- **Pickup Codes**: Generated randomly (10-999) via `api.models.generate_pickup_code`. Do NOT use sequential logic. Includes retry mechanism for uniqueness.
- **File Storage**: Files are stored in `order_documents/YYYY-MM-DD/<pickup_code>/Group_<id>/<sequence>_<filename>`. See `get_order_document_path` in `api/models.py`.
- **Concurrency**: `Order.save()` includes a retry loop for optimistic locking when generating unique fields.

### 2. Admin Dashboard (`api/dashboard.py` & `templates/admin/`)
- **Data Source**: `api.dashboard.dashboard_callback` provides `kpi` and `charts` context.
- **Rendering**: `templates/admin/index.html` overrides the Unfold dashboard to render Chart.js charts manually.
- **Styling**: Uses Tailwind CSS classes directly in the template.

### 3. Frontend Components (`frontend/src/`)
- **Theming**: Uses CSS variables (e.g., `var(--color-primary)`) defined in `assets/main.css` for light/dark mode support.
- **Components**: Prefer using `BaseButton.vue` and other base components over raw HTML elements.
- **API Calls**: Centralized in `services/` (e.g., `api.js`).

## ⚠️ Common Pitfalls
- **Admin Dashboard Visibility**: If the dashboard is blank, ensure `templates/admin/index.html` is correctly extending `unfold/layouts/base_simple.html` and that `dashboard_callback` is registered in `backend/settings.py`.
- **Static Files**: When changing Admin UI, ensure `python manage.py collectstatic` is run if in production mode, or that `DEBUG=True` handles it in dev.
- **Celery Tasks**: PDF generation happens asynchronously. Ensure the Celery worker is running to process `api.tasks`.

## 🔍 Debugging
- **Logs**: Check `django.log` in the root directory for backend errors.
- **Frontend**: Use Vue DevTools and Console for frontend state issues.
