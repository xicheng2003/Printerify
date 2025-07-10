# backend/debug_user_delete.py

import traceback
from django.contrib.auth import get_user_model
from django.db.models.query import QuerySet

print("DEBUG: User delete trap is being set...")

User = get_user_model()

# 保存原始的 delete 方法
original_delete = QuerySet.delete

# 定义我们新的、带有日志记录的 delete 方法
def verbose_delete(self):
    # 我们只关心针对 User 模型的删除操作
    if self.model == User:
        print("="*80)
        print("!!! ALERT: A process is attempting to delete User objects.")
        print("!!! 以下是代码调用堆栈追溯信息:")
        # 打印完整的堆栈信息，以便我们找到调用者
        traceback.print_stack()
        print("="*80)

    # 执行原始的删除操作
    return original_delete(self)

# 用我们新的方法替换掉原始的 delete 方法（这被称为"猴子补丁"）
QuerySet.delete = verbose_delete

print("DEBUG: User delete trap has been successfully set.")