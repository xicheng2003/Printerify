# Printerify 项目整理说明

## 🗂️ 目录整理完成

项目根目录已经完成整理，所有临时文档和测试脚本都已归类到相应的目录中。

## 📁 新的目录结构

### docs/ - 项目文档
- **implementation-guides/** - 实施指南和部署文档
- **fix-summaries/** - 问题修复总结和解决方案
- **troubleshooting/** - 故障排除指南
- **debug-scripts/** - 调试脚本（预留）

### scripts/ - 实用脚本
- 测试脚本 (`test_*.py`)
- 检查脚本 (`check_*.py`)
- 工具脚本 (`setup_env.py`, `howmigrations`)

## 🔄 移动的文件列表

### 文档文件
- `OAUTH_PRODUCTION_DEPLOYMENT.md` → `docs/implementation-guides/`
- `OAUTH_FIX_SUMMARY.md` → `docs/fix-summaries/`
- `OAUTH_BINDING_SOLUTION.md` → `docs/fix-summaries/`
- `PAYMENT_UPLOAD_FIX_SUMMARY.md` → `docs/fix-summaries/`
- `USER_REGISTRATION_FIX_SUMMARY.md` → `docs/fix-summaries/`
- `LOGIN_GUIDE_IMPLEMENTATION.md` → `docs/implementation-guides/`
- `USER_ORDER_EMAIL_IMPLEMENTATION.md` → `docs/implementation-guides/`
- `GEMINI.md` → `docs/implementation-guides/`
- `IMPROVEMENTS_TODO.md` → `docs/implementation-guides/`
- `DJANGO_MIGRATION_TROUBLESHOOTING.md` → `docs/troubleshooting/`

### 脚本文件
- `test_*.py` → `scripts/`
- `check_*.py` → `scripts/`
- `setup_env.py` → `scripts/`
- `howmigrations` → `scripts/`

## 📋 保留在根目录的文件

- `README.md` - 项目主要说明文档
- `manage.py` - Django管理脚本
- `requirements.txt` - Python依赖
- `pyproject.toml` - 项目配置
- `run_tests.sh` / `run_tests.bat` - 测试运行脚本
- `env_example.txt` - 环境变量示例

## 🚫 已忽略的文件

- `temp_uploads/` - 临时上传目录
- `*.log` - 日志文件
- `db.sqlite3` - 开发数据库
- `.coverage` - 测试覆盖率文件
- `htmlcov/` - 测试覆盖率报告

## 💡 使用建议

1. **新文档**: 根据内容类型放入相应的 `docs/` 子目录
2. **新脚本**: 放入 `scripts/` 目录
3. **临时文件**: 使用 `temp_uploads/` 目录，该目录已被git忽略
4. **日志文件**: 定期清理，避免占用过多空间

## 🔍 快速查找

- **部署相关**: `docs/implementation-guides/`
- **问题解决**: `docs/fix-summaries/`
- **故障排除**: `docs/troubleshooting/`
- **测试工具**: `scripts/`

项目现在更加整洁有序，便于维护和查找相关文档！
