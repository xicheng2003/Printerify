# Printerify 脚本工具

本目录包含了Printerify项目的各种实用脚本和工具。

## 脚本列表

### 🔧 检查和调试脚本
- `check_migration_status.py` - 检查Django迁移状态
- `check_oauth_config.py` - 检查OAuth配置
- `setup_env.py` - 环境设置脚本

### 🧪 测试脚本
- `test_oauth.py` - OAuth功能测试
- `test_oauth_binding.py` - OAuth绑定测试
- `test_oauth_config.py` - OAuth配置测试
- `test_oauth_integration.py` - OAuth集成测试
- `test_oauth_binding_simple.py` - 简化OAuth绑定测试
- `test_oauth_fix.py` - OAuth修复测试
- `test_payment_upload_fix.py` - 支付上传修复测试
- `test_register_debug.py` - 注册调试测试

### 📊 其他工具
- `howmigrations` - 迁移相关工具

## 使用方法

1. **运行测试脚本**: `python scripts/test_*.py`
2. **运行检查脚本**: `python scripts/check_*.py`
3. **运行设置脚本**: `python scripts/setup_env.py`

## 注意事项

- 这些脚本主要用于开发和调试
- 在生产环境中使用前请仔细检查
- 建议在运行脚本前备份重要数据
- 新的脚本工具请放在此目录中，并在README中说明用途
