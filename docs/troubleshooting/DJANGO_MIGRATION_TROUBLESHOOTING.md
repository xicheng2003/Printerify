# Django迁移故障排除指南

## 当前迁移状态分析

### 已存在的迁移文件
- `0001_initial.py` - 初始迁移（包含User、Order、BindingGroup、Document模型）
- `0002_user_avatar_url_user_github_id_user_google_id.py` - 添加OAuth相关字段

### 模型变更总结
1. **User模型扩展**:
   - 新增 `phone_number` 字段
   - 新增 `created_at`, `updated_at` 字段
   - 新增 `avatar_url`, `github_id`, `google_id` 字段（OAuth支持）

2. **Order模型**:
   - 新增 `user` 外键字段（关联用户）
   - 新增 `payment_method` 字段
   - 新增 `payment_screenshot` 字段

3. **新增模型**:
   - `BindingGroup` - 装订组管理
   - `Document` - 文档管理

## 迁移可能遇到的问题

### 1. 数据库连接问题
```bash
# 检查数据库连接
python manage.py dbshell

# 检查数据库配置
python manage.py check --database default
```

### 2. 字段冲突问题
- 如果生产环境已有数据，新增的必填字段可能导致冲突
- 解决方案：为新增字段设置默认值或允许为空

### 3. 外键约束问题
- `Order.user` 字段可能因为现有订单没有用户关联而失败
- 解决方案：先创建迁移，再处理数据

## 迁移失败后的解决方案

### 方案1: 强制迁移（推荐用于开发环境）
```bash
# 1. 重置迁移状态
python manage.py migrate api zero

# 2. 删除迁移文件（保留__init__.py）
rm api/migrations/0*.py

# 3. 重新创建迁移
python manage.py makemigrations api

# 4. 应用迁移
python manage.py migrate
```

### 方案2: 数据安全迁移（推荐用于生产环境）
```bash
# 1. 备份当前数据库
pg_dump your_database > backup_$(date +%Y%m%d_%H%M%S).sql

# 2. 检查迁移计划
python manage.py sqlmigrate api 0001

# 3. 应用迁移（如果失败，查看具体错误）
python manage.py migrate api 0001

# 4. 处理数据冲突
python manage.py shell
```

### 方案3: 手动修复迁移
```bash
# 1. 查看迁移状态
python manage.py showmigrations

# 2. 标记特定迁移为已应用
python manage.py migrate --fake api 0001

# 3. 继续后续迁移
python manage.py migrate
```

## 数据迁移脚本

### 处理现有订单数据
```python
# 在Django shell中运行
from api.models import Order, User

# 为现有订单创建默认用户（如果需要）
for order in Order.objects.filter(user__isnull=True):
    # 创建匿名用户或跳过
    print(f"Order {order.order_number} has no user")
```

### 处理字段默认值
```python
# 为新增字段设置默认值
from django.db import connection

with connection.cursor() as cursor:
    # 更新phone_number字段
    cursor.execute("""
        UPDATE api_user 
        SET phone_number = 'N/A' 
        WHERE phone_number IS NULL
    """)
```

## 生产环境部署检查清单

### 部署前检查
- [ ] 备份生产数据库
- [ ] 在测试环境验证迁移
- [ ] 检查所有环境变量配置
- [ ] 验证OAuth配置

### 部署步骤
```bash
# 1. 停止应用服务
sudo systemctl stop your-django-app

# 2. 备份数据库
pg_dump production_db > production_backup.sql

# 3. 拉取最新代码
git pull origin main

# 4. 安装依赖
pip install -r requirements.txt

# 5. 运行迁移
python manage.py migrate

# 6. 收集静态文件
python manage.py collectstatic --noinput

# 7. 重启服务
sudo systemctl start your-django-app

# 8. 检查服务状态
sudo systemctl status your-django-app
```

### 部署后验证
```bash
# 1. 检查应用状态
curl -I https://your-domain.com/health/

# 2. 检查数据库连接
python manage.py dbshell

# 3. 验证OAuth配置
python manage.py shell
# 在shell中测试OAuth服务
```

## 常见错误及解决方案

### 错误1: "django.db.utils.IntegrityError: NOT NULL constraint failed"
**原因**: 新增字段没有默认值，但现有数据需要该字段
**解决方案**:
```python
# 在迁移文件中添加默认值
migrations.AddField(
    model_name='user',
    name='phone_number',
    field=models.CharField(max_length=20, blank=True, null=True, default=''),
)
```

### 错误2: "django.db.utils.OperationalError: table already exists"
**原因**: 迁移状态不一致
**解决方案**:
```bash
# 重置迁移状态
python manage.py migrate --fake-initial
```

### 错误3: "django.db.utils.ProgrammingError: column does not exist"
**原因**: 数据库结构与模型不匹配
**解决方案**:
```bash
# 重新同步数据库
python manage.py migrate --run-syncdb
```

## 回滚策略

### 快速回滚
```bash
# 1. 回滚到特定迁移
python manage.py migrate api 0001

# 2. 恢复数据库备份
psql your_database < backup_file.sql

# 3. 回滚代码
git reset --hard HEAD~1
```

### 数据恢复
```bash
# 1. 停止应用
sudo systemctl stop your-django-app

# 2. 恢复数据库
pg_restore -d your_database backup_file.dump

# 3. 重启应用
sudo systemctl start your-django-app
```

## 预防措施

### 1. 迁移测试
- 在开发环境完整测试迁移流程
- 使用生产数据的副本进行测试
- 验证所有模型关系和数据完整性

### 2. 备份策略
- 自动数据库备份
- 代码版本控制
- 迁移文件版本管理

### 3. 监控和日志
- 监控迁移执行状态
- 记录详细的迁移日志
- 设置迁移失败告警

## 总结

迁移失败是常见问题，关键是要有完整的备份和回滚策略。建议：

1. **开发环境**: 使用方案1快速重置
2. **生产环境**: 使用方案2安全迁移
3. **紧急情况**: 使用回滚策略快速恢复
4. **预防为主**: 充分测试，做好备份

记住：**数据安全第一，功能第二**。在生产环境进行任何迁移前，都要确保有完整的备份和回滚方案。
