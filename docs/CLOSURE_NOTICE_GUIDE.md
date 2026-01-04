# 暂停营业提示功能使用指南

## 功能概述

这是一个完整的、生产级的暂停营业提示系统，允许你在需要时快速切换营业状态。当营业状态关闭时，用户将被重定向到一个温馨的关闭提示页面。

## 架构设计

### 后端（Django）
1. **SystemConfig 模型**（`api/models.py`）
   - 单例模式，只维护一条配置记录
   - 包含营业状态、关闭原因、重新开业日期等信息
   - 支持灵活的通知内容

2. **API 端点**（`api/views.py`）
   - `GET /api/system-config/` - 获取系统配置（公开接口）

3. **Admin 后台**（`api/admin.py`）
   - 管理员可以轻松修改营业状态
   - 一键进入配置编辑页面

### 前端（Vue 3）
1. **ClosureNoticeView 组件**（`frontend/src/views/ClosureNoticeView.vue`）
   - 美观的关闭提示页面
   - 支持显示重新开业日期和额外通知
   - 响应式设计，支持所有设备

2. **路由守卫**（`frontend/src/router/index.js`）
   - 自动检查营业状态
   - 智能重定向逻辑
   - 配置缓存机制（5分钟）

## 使用步骤

### 1. 关闭营业

访问Django Admin：
```
http://localhost:8000/admin/
```

1. 找到 "系统配置" 模块
2. 点击编辑系统配置
3. **取消勾选** "is_open"（营业状态）
4. 编辑以下信息：
   - **closure_reason**: 关闭原因（例：放假暂停营业，感谢您的理解！）
   - **reopening_date**: 预计重新营业日期（可选）
   - **notice_content**: 额外提示内容（可选，支持多行）
   - **allow_viewing_history**: 是否允许已登录用户查看历史订单

5. 点击 "保存"

### 2. 验证关闭状态

打开前端应用，用户将被自动重定向到关闭提示页面：
```
http://localhost:5173/closure-notice
```

页面将显示：
- ✗ 暂停营业中
- 关闭原因
- 预计重新开业时间（如果设置了）
- 额外通知信息（如果有）
- 可用的操作按钮（查看历史订单、返回首页、登出等）

### 3. 恢复营业

1. 访问 Django Admin 系统配置页面
2. **勾选** "is_open"
3. 点击 "保存"

用户将立即可以访问所有功能。

## 配置详解

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `is_open` | Boolean | 营业状态。勾选=营业，取消勾选=关闭 |
| `closure_reason` | String (max 500) | 显示给用户的关闭原因，例如"放假暂停营业" |
| `reopening_date` | Date | 预计重新营业日期。留空则不显示 |
| `notice_content` | Text | 额外通知内容，支持多行。例如客服电话、邮箱等 |
| `allow_viewing_history` | Boolean | 关闭期间是否允许已登录用户查看历史订单 |

## 用户体验流程

### 当营业状态为关闭时：

```
用户访问任何页面
    ↓
路由守卫检查系统配置
    ↓
is_open = False
    ↓
重定向到 /closure-notice
    ↓
显示温馨的关闭页面，包括：
  ✓ 营业状态提示
  ✓ 关闭原因
  ✓ 重新开业时间（如果有）
  ✓ 额外通知
  ✓ 可选操作按钮
```

### 允许的操作：

1. **查看历史订单**（如果 `allow_viewing_history=True` 且用户已登录）
2. **返回首页**（重定向到 `/` 仍会回到关闭页面）
3. **登出账号**（仅对已登录用户）

## 最佳实践

### 1. 设置完整的关闭信息

```
closure_reason: "放假暂停营业，感谢您的理解！"
reopening_date: "2026-02-01"  # 清晰的重新开业日期
notice_content: """
我们将在2月1日恢复营业。
如有紧急需求，请通过以下方式联系我们：
📧 邮箱：support@printerify.com
📱 电话：400-XXX-XXXX
感谢您的耐心等待！"""
```

### 2. 给已登录用户提供查看历史的权限

在大多数情况下，建议保持 `allow_viewing_history=True`，这样：
- 已登录用户可以查看和跟踪已提交的订单
- 增强用户体验和信任度

### 3. 预留足够的关闭通知期

如果可能，在关闭营业前给用户发送邮件/通知，告知关闭时间和重新开业日期。

### 4. 定期检查系统配置

建议在以下情况检查系统配置：
- 营业即将恢复时
- 突发情况导致需要临时关闭时

## 故障排除

### 问题1：关闭后前端仍显示营业界面

**原因**：前端配置缓存未过期（5分钟）

**解决**：
1. 硬刷新前端页面（Ctrl+Shift+R）
2. 或者等待5分钟让缓存自动更新

### 问题2：Admin后台看不到系统配置

**原因**：未运行最新的迁移

**解决**：
```bash
python manage.py migrate api
```

### 问题3：已登录用户无法查看历史订单

**原因**：`allow_viewing_history` 设置为 False

**解决**：在 Admin 中将该选项改为 True

## 代码层面的扩展

### 添加邮件通知（高级）

当营业状态改变时，自动发送邮件给所有用户：

```python
# api/models.py
class SystemConfig(models.Model):
    # ... 现有字段 ...
    
    def save(self, *args, **kwargs):
        # 检查是否状态改变
        if self.pk:
            old_instance = SystemConfig.objects.get(pk=self.pk)
            if old_instance.is_open != self.is_open:
                # 发送邮件通知
                from .tasks import notify_users_of_status_change
                notify_users_of_status_change.delay(self.is_open)
        
        super().save(*args, **kwargs)
```

### 添加维护公告（高级）

在已关闭的情况下显示倒计时：

修改 `ClosureNoticeView.vue`：
```vue
<div v-if="reopeningDate" class="countdown">
  距重新开业还有：{{ daysUntilReopening }} 天
</div>
```

## 文件清单

本功能新增/修改的文件：

1. **新增**：`api/models.py` - SystemConfig 模型
2. **修改**：`api/models.py` - 数据库迁移
3. **新增**：`api/views.py` - get_system_config() 视图
4. **修改**：`api/urls.py` - 添加 system-config 路由
5. **修改**：`api/admin.py` - SystemConfigAdmin 后台管理
6. **新增**：`frontend/src/views/ClosureNoticeView.vue` - 关闭提示页面
7. **修改**：`frontend/src/router/index.js` - 路由守卫和缓存逻辑

## 总结

这个暂停营业系统采用了以下最佳实践：

✅ **单一配置源** - 后端统一管理营业状态  
✅ **智能缓存** - 减少API调用，提升性能  
✅ **优雅降级** - 如果API请求失败，默认显示营业  
✅ **用户友好** - 美观的UI和清晰的提示信息  
✅ **灵活控制** - 易于从Admin后台管理  
✅ **响应式设计** - 支持所有设备和屏幕尺寸  
✅ **权限隔离** - 已登录用户可有条件访问某些功能  

祝你放假愉快！🎉
