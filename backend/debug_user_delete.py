# backend/debug_user_delete.py

import os
import django
import traceback

# --- 关键修复：在访问模型前，确保 Django 设置已配置 ---
# 这使得脚本可以在任何时间点被安全地导入。
print("DEBUG: 正在为调试陷阱配置 Django...")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
try:
    django.setup()
    print("DEBUG: Django 配置成功。")
except Exception as e:
    print(f"DEBUG: Django 配置时出错: {e}")
# -------------------------------------------------------------

from django.contrib.auth import get_user_model
from django.db.models.query import QuerySet

print("DEBUG: 正在设置用户删除陷阱...")

User = get_user_model()

# 保存原始的 delete 方法
original_delete = QuerySet.delete

# 定义我们新的、带有日志记录的 delete 方法
def verbose_delete(self):
    # 我们只关心针对 User 模型的删除操作
    if self.model == User:
        print("="*80)
        print("!!! 警报：有进程正在尝试删除用户对象。")
        print("!!! 以下是代码调用堆栈追溯信息:")
        # 打印完整的堆栈信息，以便我们找到调用者
        traceback.print_stack()
        print("="*80)
    
    # 执行原始的删除操作
    return original_delete(self)

# 用我们新的方法替换掉原始的 delete 方法（这被称为“猴子补丁”）
QuerySet.delete = verbose_delete

print("DEBUG: 用户删除陷阱已成功设置。")
