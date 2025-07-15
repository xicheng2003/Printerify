# backend/celery.py

import os
from celery import Celery

# 指向你的 Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

# 创建 Celery 应用
app = Celery("backend")

# 从 settings 加载配置
app.config_from_object("django.conf:settings", namespace="CELERY")

# 自动发现所有已注册 app 下的 tasks.py 文件
app.autodiscover_tasks()